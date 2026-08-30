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
    "gemini-3.1-flash-image",  # Nano Banana 2 (default, fast, 4K, 14 ref images)
    "gemini-3.1-flash-lite-image",  # Nano Banana 2 Lite (fastest, cheapest)
    "gemini-3-pro-image",  # Nano Banana Pro (premium, complex reasoning, 4K)
    "gemini-2.5-flash-image",  # Nano Banana (legacy)
]

ASPECT_RATIOS = [
    "1:1",
    "1:4",
    "1:8",
    "2:3",
    "3:2",
    "3:4",
    "4:1",
    "4:3",
    "4:5",
    "5:4",
    "8:1",
    "9:16",
    "16:9",
    "21:9",
]

IMAGE_SIZES = [
    "512px",
    "0.5K",
    "1K",
    "2K",
    "4K",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate and edit images using Gemini Nano Banana image generation models via Gemini Interactions API."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default="",
        help="Prompt text for image generation or editing (ignored if --stdin or --file is used).",
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
        default="gemini-3.1-flash-image",
        choices=SUPPORTED_MODELS,
        help="Model ID (default: gemini-3.1-flash-image).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.jpg",
        help="Output image file path (default: output.jpg).",
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
        help="Aspect ratio for generated image (e.g., '1:1', '16:9', '9:16', '4:3', '3:2', etc.).",
    )
    parser.add_argument(
        "-s",
        "--size",
        "--image-size",
        dest="image_size",
        choices=IMAGE_SIZES,
        default=None,
        help="Image resolution size: '512px' (0.5K), '1K' (default), '2K', '4K'. Must be uppercase 'K'.",
    )
    parser.add_argument(
        "-i",
        "--image",
        action="append",
        dest="images",
        default=[],
        help="Input reference/source image path(s) for image editing or composition (can be specified multiple times, up to 14 images).",
    )
    parser.add_argument(
        "--video",
        dest="video",
        default=None,
        help="Video URL (e.g. YouTube) or local video file path for video-to-image generation (supported by Gemini 3.1 Flash Image).",
    )
    parser.add_argument(
        "--previous-id",
        "--previous-interaction-id",
        dest="previous_interaction_id",
        default=None,
        help="Previous interaction ID for multi-turn sequential image editing.",
    )
    parser.add_argument(
        "--search",
        "--grounding",
        action="store_true",
        help="Enable Grounding with Google Search for real-time web knowledge.",
    )
    parser.add_argument(
        "--image-search",
        action="store_true",
        help="Enable Google Image Search grounding alongside Web Search (Gemini 3.1 Flash Image only).",
    )
    parser.add_argument(
        "--thinking-level",
        dest="thinking_level",
        choices=["minimal", "high"],
        default=None,
        help="Control thinking level for Gemini 3.1 Flash Image: 'minimal' (default) or 'high'.",
    )
    parser.add_argument(
        "--save-thoughts",
        action="store_true",
        help="Save intermediate thought process text and images to disk.",
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
            mime_type = "image/png"

    with open(path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    return {
        "type": "image",
        "mime_type": mime_type,
        "data": image_b64,
    }


def load_video_payload(video_input: str) -> dict:
    # Check if it's a web URL (like YouTube)
    if video_input.startswith(("http://", "https://")):
        return {
            "type": "video",
            "uri": video_input,
            "mime_type": "video/mp4",
        }

    # Otherwise treat as local video file
    path = Path(video_input)
    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_input}")

    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type or not mime_type.startswith("video/"):
        mime_type = "video/mp4"

    with open(path, "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode("utf-8")

    return {
        "type": "video",
        "mime_type": mime_type,
        "data": video_b64,
    }


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

    # 2. Build input payload
    if args.images or args.video:
        input_payload = []
        if prompt_text:
            input_payload.append({"type": "text", "text": prompt_text})

        # Process video input
        if args.video:
            try:
                input_payload.append(load_video_payload(args.video))
            except Exception as e:  # noqa: BLE001
                print(f"Error loading video '{args.video}': {e}", file=sys.stderr)
                sys.exit(1)

        # Process image inputs (up to 14 reference images for Gemini 3)
        if args.images:
            if len(args.images) > 14:
                print(
                    "Warning: Gemini 3 image models support up to 14 reference images. Truncating to the first 14 images.",
                    file=sys.stderr,
                )
                args.images = args.images[:14]

            for img_path in args.images:
                try:
                    input_payload.append(load_image_payload(img_path))
                except Exception as e:  # noqa: BLE001
                    print(f"Error loading image '{img_path}': {e}", file=sys.stderr)
                    sys.exit(1)
    else:
        input_payload = prompt_text

    # 3. Build response_format
    out_ext = Path(args.output).suffix.lower()
    if out_ext == ".png":
        out_mime = "image/png"
    elif out_ext == ".webp":
        out_mime = "image/webp"
    else:
        out_mime = "image/jpeg"

    response_format = {
        "type": "image",
        "mime_type": out_mime,
    }
    if args.aspect_ratio:
        response_format["aspect_ratio"] = args.aspect_ratio
    if args.image_size:
        # Standardize 0.5K if user passes 512px
        size_val = "512px" if args.image_size in ["512px", "0.5K"] else args.image_size
        response_format["image_size"] = size_val

    # 4. Build create parameters
    create_kwargs = {
        "model": args.model,
        "input": input_payload,
        "response_format": response_format,
    }

    if args.previous_interaction_id:
        create_kwargs["previous_interaction_id"] = args.previous_interaction_id

    # Grounding tools
    if args.search or args.image_search:
        search_types = ["web_search"]
        if args.image_search:
            search_types.append("image_search")
        create_kwargs["tools"] = [
            {
                "type": "google_search",
                "search_types": search_types,
            }
        ]

    # Generation config
    generation_config = {}
    if args.thinking_level:
        generation_config["thinking_level"] = args.thinking_level
    if generation_config:
        create_kwargs["generation_config"] = generation_config

    client = genai.Client(api_key=GEMINI_API_KEY)
    print(f"Generating image with model '{args.model}'...")

    # 5. Call API with retries
    interaction = None
    retries = max(1, args.retry + 1)
    for attempt in range(1, retries + 1):
        try:
            interaction = client.interactions.create(**create_kwargs)
            break
        except Exception as e:  # noqa: BLE001
            if attempt < retries:
                wait_time = 2 ** (attempt - 1)
                print(
                    f"Warning: Image generation attempt {attempt} failed ({e}). Retrying in {wait_time}s...",
                    file=sys.stderr,
                )
                time.sleep(wait_time)
            else:
                print(f"Failed to generate image: {e}", file=sys.stderr)
                sys.exit(1)

    # Display interaction ID for follow-up turns
    if getattr(interaction, "id", None):
        print(f"Interaction ID: {interaction.id}")

    # 6. Extract images, text, and thoughts
    images_data = []
    text_list = []
    thought_texts = []
    thought_images = []

    # Convenience properties
    if getattr(interaction, "output_image", None) and getattr(
        interaction.output_image, "data", None
    ):
        images_data.append(base64.b64decode(interaction.output_image.data))

    if getattr(interaction, "output_text", None):
        text_list.append(interaction.output_text)

    # Detailed inspection of steps
    if getattr(interaction, "steps", None):
        for step in interaction.steps:
            step_type = getattr(step, "type", None)

            if step_type == "model_output":
                for content_block in getattr(step, "content", []):
                    c_type = getattr(content_block, "type", None)
                    if c_type == "image" and getattr(content_block, "data", None):
                        img_bytes = base64.b64decode(content_block.data)
                        if img_bytes not in images_data:
                            images_data.append(img_bytes)
                    elif c_type == "text" and getattr(content_block, "text", None):
                        txt = content_block.text
                        if txt not in text_list:
                            text_list.append(txt)

            elif step_type == "thought" and args.save_thoughts:
                for content_block in getattr(step, "summary", []):
                    c_type = getattr(content_block, "type", None)
                    if c_type == "text" and getattr(content_block, "text", None):
                        thought_texts.append(content_block.text)
                    elif c_type == "image" and getattr(content_block, "data", None):
                        thought_images.append(base64.b64decode(content_block.data))

    # 7. Save generated image(s)
    if images_data:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if len(images_data) == 1:
            with open(out_path, "wb") as f:
                f.write(images_data[0])
            print(f"Image saved successfully to: {out_path.resolve()}")
        else:
            stem = out_path.stem
            suffix = out_path.suffix or ".jpg"
            for idx, img_bytes in enumerate(images_data, start=1):
                cur_out = out_path.parent / f"{stem}_{idx}{suffix}"
                with open(cur_out, "wb") as f:
                    f.write(img_bytes)
                print(f"Image {idx} saved successfully to: {cur_out.resolve()}")
    else:
        print("Warning: No image data returned by the model.", file=sys.stderr)

    # 8. Save or display thoughts if requested
    if args.save_thoughts:
        out_dir = Path(args.output).parent
        stem = Path(args.output).stem
        if thought_texts:
            thought_txt_path = out_dir / f"{stem}_thoughts.txt"
            with open(thought_txt_path, "w", encoding="utf-8") as f:
                f.write("\n".join(thought_texts) + "\n")
            print(f"Thoughts log saved to: {thought_txt_path.resolve()}")

        for idx, t_img in enumerate(thought_images, start=1):
            thought_img_path = out_dir / f"{stem}_thought_image_{idx}.png"
            with open(thought_img_path, "wb") as f:
                f.write(t_img)
            print(f"Thought image {idx} saved to: {thought_img_path.resolve()}")

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
