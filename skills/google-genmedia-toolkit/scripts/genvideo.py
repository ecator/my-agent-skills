# /// script
# dependencies = [
#   "google-genai",
#   "python-dotenv",
#   "httpx[socks]"
# ]
# ///

import argparse
import base64
import mimetypes
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

SUPPORTED_MODELS = [
    "gemini-omni-1.1-flash",  # Gemini Omni Flash (video generation, editing, extension)
]

ASPECT_RATIOS = [
    "16:9",
    "9:16",
]

RESOLUTIONS = [
    "360p",
    "720p",
    "1080p",
    "4k",
]

TASKS = [
    "text_to_video",
    "image_to_video",
    "reference_to_video",
    "edit",
    "extend",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate, edit, and extend videos using Gemini Omni Flash (gemini-omni-1.1-flash) via Gemini Interactions API."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default="",
        help="Prompt text for video generation, editing, or extension (ignored if --stdin or --file is used).",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="input_file",
        default=None,
        help="Read the prompt from a text file.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read the prompt from standard input (stdin) for multi-line or complex prompts.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gemini-omni-1.1-flash",
        choices=SUPPORTED_MODELS,
        help="Model ID (default: gemini-omni-1.1-flash).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.mp4",
        help="Output video file path (default: output.mp4).",
    )
    parser.add_argument(
        "-t",
        "--text-output",
        dest="text_output",
        default=None,
        help="Save conversational text / description response to a file instead of printing to stdout.",
    )
    parser.add_argument(
        "-a",
        "--aspect-ratio",
        dest="aspect_ratio",
        choices=ASPECT_RATIOS,
        default=None,
        help="Aspect ratio for generated video ('16:9' landscape [default], '9:16' portrait).",
    )
    parser.add_argument(
        "-r",
        "--resolution",
        dest="resolution",
        choices=RESOLUTIONS,
        default=None,
        help="Output video resolution: '360p', '720p' (default), '1080p', '4k'.",
    )
    parser.add_argument(
        "-i",
        "--image",
        action="append",
        dest="images",
        default=[],
        help="Input reference/source image path(s) for image-to-video, first/last frame interpolation, or subject reference (can be specified multiple times).",
    )
    parser.add_argument(
        "-v",
        "--video",
        dest="video",
        default=None,
        help="Input source video file path or URI for video editing or extension.",
    )
    parser.add_argument(
        "--task",
        dest="task",
        choices=TASKS,
        default=None,
        help="Explicitly specify intended behavior in video_config ('text_to_video', 'image_to_video', 'reference_to_video', 'edit', 'extend').",
    )
    parser.add_argument(
        "--delivery",
        dest="delivery",
        choices=["inline", "uri"],
        default=None,
        help="Delivery mode in response_format: 'inline' (default base64) or 'uri' (Google-hosted URI polling & download for videos >4MB or high-res).",
    )
    parser.add_argument(
        "--previous-id",
        "--previous-interaction-id",
        dest="previous_interaction_id",
        default=None,
        help="Previous interaction ID for multi-turn sequential video editing or multi-turn extension.",
    )
    parser.add_argument(
        "--save-thoughts",
        action="store_true",
        help="Save intermediate thought process text to disk.",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="Number of automatic retries on transient server errors (default: 3).",
    )
    return parser.parse_args()


def load_image_payload(image_path: str) -> dict:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type or not mime_type.startswith("image/"):
        ext = path.suffix.lower()
        if ext in [".jpg", ".jpeg"]:
            mime_type = "image/jpeg"
        elif ext == ".png":
            mime_type = "image/png"
        elif ext == ".webp":
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"

    with open(path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    return {
        "type": "image",
        "mime_type": mime_type,
        "data": image_b64,
    }


def upload_media_file(
    client: genai.Client, file_path: str, media_type: str = "video"
) -> dict:
    # If already a Google-hosted URI (e.g. gs:// or files/...)
    if file_path.startswith(("gs://", "https://", "files/")):
        return {
            "type": "document",
            "uri": file_path,
        }

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"{media_type.capitalize()} file not found: {file_path}"
        )

    print(f"Uploading {media_type} '{file_path}' via Files API...")
    uploaded_file = client.files.upload(file=str(path))

    while True:
        state = getattr(uploaded_file.state, "name", str(uploaded_file.state))
        if state == "ACTIVE":
            break
        elif state == "PROCESSING":
            print(f"Waiting for {media_type} to be processed...")
            time.sleep(5)
            uploaded_file = client.files.get(name=uploaded_file.name)
        elif state == "FAILED":
            raise RuntimeError(
                f"{media_type.capitalize()} processing failed on server."
            )
        else:
            # Other state or already ready
            break

    print(f"{media_type.capitalize()} processing complete: {uploaded_file.uri}")
    return {
        "type": "document",
        "uri": uploaded_file.uri,
    }


def download_uri_video(client: genai.Client, video_uri: str, out_path: Path):
    file_id = video_uri.split("/")[-1].split("?")[0].split(":")[0]
    name = (
        f"files/{file_id}"
        if not video_uri.startswith("files/")
        else video_uri.split("?")[0].split(":")[0]
    )

    print(f"Waiting for generated video processing ({name})...")
    while True:
        f_info = client.files.get(name=name)
        state = getattr(f_info.state, "name", str(f_info.state))
        if state == "ACTIVE":
            break
        elif state == "FAILED":
            raise RuntimeError("Video generation failed on server.")
        time.sleep(5)

    print(f"Downloading video from {video_uri} to {out_path}...")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    video_bytes = client.files.download(file=video_uri)
    with open(out_path, "wb") as f:
        f.write(video_bytes)


def main():
    args = parse_args()

    # 1. Resolve prompt
    if args.input_file:
        file_path = Path(args.input_file)
        if not file_path.exists():
            print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
    elif args.stdin:
        sys.stdin.reconfigure(encoding="utf-8")
        prompt_text = sys.stdin.read().strip()
    else:
        prompt_text = args.prompt.strip()

    if not prompt_text and not args.images and not args.video:
        print(
            "Error: Prompt or at least one image/video is required. Provide prompt as argument, pass --file, pipe via --stdin, or pass --image / --video.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # 2. Build input payload
    if args.images or args.video:
        input_payload = []

        # Upload video if provided (recommended via Files API)
        if args.video:
            try:
                input_payload.append(upload_media_file(client, args.video, "video"))
            except Exception as e:  # noqa: BLE001
                print(
                    f"Error preparing video input '{args.video}': {e}", file=sys.stderr
                )
                sys.exit(1)

        # Process image inputs
        if args.images:
            for img_path in args.images:
                try:
                    input_payload.append(load_image_payload(img_path))
                except Exception as e:  # noqa: BLE001
                    print(f"Error loading image '{img_path}': {e}", file=sys.stderr)
                    sys.exit(1)

        if prompt_text:
            input_payload.append({"type": "text", "text": prompt_text})
    else:
        input_payload = prompt_text

    # 3. Build response_format
    response_format = {
        "type": "video",
    }
    if args.aspect_ratio:
        response_format["aspect_ratio"] = args.aspect_ratio
    if args.resolution:
        response_format["resolution"] = args.resolution
    if args.delivery:
        response_format["delivery"] = args.delivery

    # 4. Build create parameters
    create_kwargs = {
        "model": args.model,
        "input": input_payload,
        "response_format": response_format,
    }

    if args.previous_interaction_id:
        create_kwargs["previous_interaction_id"] = args.previous_interaction_id

    # Generation config (video_config task)
    if args.task:
        create_kwargs["generation_config"] = {
            "video_config": {
                "task": args.task,
            }
        }

    print(f"Generating video with model '{args.model}'...")

    # 5. Call API with retries
    interaction = None
    total_attempts = max(1, args.retry + 1)
    for attempt in range(1, total_attempts + 1):
        try:
            interaction = client.interactions.create(**create_kwargs)
            break
        except Exception as e:  # noqa: BLE001
            if attempt < total_attempts:
                wait_time = 2 ** (attempt - 1)
                print(
                    f"Warning: Video generation attempt {attempt} failed ({e}). Retrying in {wait_time}s...",
                    file=sys.stderr,
                )
                time.sleep(wait_time)
            else:
                print(f"Failed to generate video: {e}", file=sys.stderr)
                sys.exit(1)

    # Display interaction ID for follow-up turns
    if getattr(interaction, "id", None):
        print(f"Interaction ID: {interaction.id}")

    # 6. Extract video, text, and thoughts
    video_bytes = None
    video_uri = None
    text_list = []
    thought_texts = []

    # Convenience properties
    if getattr(interaction, "output_video", None):
        out_vid = interaction.output_video
        if getattr(out_vid, "data", None):
            video_bytes = base64.b64decode(out_vid.data)
        elif getattr(out_vid, "uri", None):
            video_uri = out_vid.uri

    if getattr(interaction, "output_text", None):
        text_list.append(interaction.output_text)

    # Detailed inspection of steps
    if getattr(interaction, "steps", None):
        for step in interaction.steps:
            step_type = getattr(step, "type", None)

            if step_type == "model_output":
                for content_block in getattr(step, "content", []):
                    c_type = getattr(content_block, "type", None)
                    if c_type == "video":
                        if not video_bytes and getattr(content_block, "data", None):
                            video_bytes = base64.b64decode(content_block.data)
                        elif not video_uri and getattr(content_block, "uri", None):
                            video_uri = content_block.uri
                    elif c_type == "text" and getattr(content_block, "text", None):
                        txt = content_block.text
                        if txt not in text_list:
                            text_list.append(txt)

            elif step_type == "thought" and args.save_thoughts:
                blocks = getattr(step, "content", None) or getattr(step, "summary", [])
                for content_block in blocks:
                    txt = getattr(content_block, "text", None)
                    if txt and txt not in thought_texts:
                        thought_texts.append(txt)

    # 7. Save generated video
    out_path = Path(args.output)
    if video_bytes:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(video_bytes)
        print(f"Video saved successfully to: {out_path.resolve()}")
    elif video_uri:
        try:
            download_uri_video(client, video_uri, out_path)
            print(f"Video downloaded and saved successfully to: {out_path.resolve()}")
        except Exception as e:  # noqa: BLE001
            print(
                f"Error downloading video from URI '{video_uri}': {e}", file=sys.stderr
            )
            sys.exit(1)
    else:
        print("Warning: No video data or URI returned by the model.", file=sys.stderr)

    # 8. Save thoughts if requested
    if args.save_thoughts and thought_texts:
        out_dir = out_path.parent
        stem = out_path.stem
        thought_txt_path = out_dir / f"{stem}_thoughts.txt"
        with open(thought_txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(thought_texts) + "\n")
        print(f"Thoughts log saved to: {thought_txt_path.resolve()}")

    # 9. Save or print text output
    all_text = "\n".join(text_list).strip()
    if all_text:
        if args.text_output:
            txt_path = Path(args.text_output)
            txt_path.parent.mkdir(parents=True, exist_ok=True)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(all_text + "\n")
            print(f"Text output saved successfully to: {txt_path.resolve()}")
        else:
            print("\n--- Model Response Text ---")
            print(all_text)
            print("---------------------------\n")


if __name__ == "__main__":
    main()
