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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate music using Google Lyria 3 models (Lyria 3 Clip / Pro) via Gemini Interactions API."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default="",
        help="Prompt text for music generation (ignored if --stdin or --file is used).",
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
        default="lyria-3-clip-preview",
        choices=["lyria-3-clip-preview", "lyria-3-pro-preview"],
        help="Model ID: 'lyria-3-clip-preview' (default, 30s clips) or 'lyria-3-pro-preview' (full songs).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.mp3",
        help="Output audio file path (default: output.mp3).",
    )
    parser.add_argument(
        "-l",
        "--lyrics-output",
        "--lyrics",
        dest="lyrics_output",
        default=None,
        help="Save generated lyrics / song structure to a file instead of printing to stdout.",
    )
    parser.add_argument(
        "-i",
        "--image",
        action="append",
        dest="images",
        default=[],
        help="Input image file path(s) for image-to-music generation (can be specified multiple times, up to 10 images).",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="Number of automatic retries on transient server/token errors (default: 3).",
    )
    return parser.parse_args()


def load_image_payload(image_path: str) -> dict:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "image/jpeg"

    with open(path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    return {
        "type": "image",
        "mime_type": mime_type,
        "data": image_b64,
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

    if not prompt_text and not args.images:
        print(
            "Error: Prompt or at least one image is required. Provide prompt as argument, pass --file, pipe via --stdin, or pass --image.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2. Build input payload
    if args.images:
        if len(args.images) > 10:
            print(
                "Warning: Lyria 3 supports up to 10 images. Truncating to the first 10 images.",
                file=sys.stderr,
            )
            args.images = args.images[:10]

        input_payload = []
        if prompt_text:
            input_payload.append({"type": "text", "text": prompt_text})
        for img_path in args.images:
            try:
                input_payload.append(load_image_payload(img_path))
            except Exception as e:  # noqa: BLE001
                print(f"Error loading image '{img_path}': {e}", file=sys.stderr)
                sys.exit(1)
    else:
        input_payload = prompt_text

    # 3. Build create parameters
    create_kwargs = {
        "model": args.model,
        "input": input_payload,
    }

    # Automatically request WAV format from API if output file ends with .wav
    if Path(args.output).suffix.lower() == ".wav":
        create_kwargs["response_format"] = {"type": "audio"}

    client = genai.Client(api_key=GEMINI_API_KEY)
    print(f"Generating music with model '{args.model}'...")

    # 4. Call API with retries
    audio_data = None
    lyrics_list = []
    retries = max(1, args.retry + 1)

    for attempt in range(1, retries + 1):
        try:
            interaction = client.interactions.create(**create_kwargs)

            # Check convenience properties
            if getattr(interaction, "output_audio", None) and getattr(
                interaction.output_audio, "data", None
            ):
                audio_data = base64.b64decode(interaction.output_audio.data)

            if getattr(interaction, "output_text", None):
                lyrics_list.append(interaction.output_text)

            # Fallback to steps if needed
            if (not audio_data or not lyrics_list) and getattr(
                interaction, "steps", None
            ):
                for step in interaction.steps:
                    if getattr(step, "type", None) == "model_output":
                        for content_block in getattr(step, "content", []):
                            c_type = getattr(content_block, "type", None)
                            if (
                                c_type == "audio"
                                and not audio_data
                                and getattr(content_block, "data", None)
                            ):
                                audio_data = base64.b64decode(content_block.data)
                            elif c_type == "text" and getattr(
                                content_block, "text", None
                            ):
                                text_val = content_block.text
                                if text_val not in lyrics_list:
                                    lyrics_list.append(text_val)

            if audio_data:
                break
            else:
                raise ValueError("No audio data returned by music generation service.")

        except Exception as e:  # noqa: BLE001
            if attempt < retries:
                wait_time = 2 ** (attempt - 1)
                print(
                    f"Warning: Music generation attempt {attempt} failed ({e}). Retrying in {wait_time}s...",
                    file=sys.stderr,
                )
                time.sleep(wait_time)
            else:
                print(f"Failed to generate music: {e}", file=sys.stderr)
                sys.exit(1)

    # 5. Save audio
    if audio_data:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(audio_data)
        print(f"Audio saved successfully to: {out_path.resolve()}")
    else:
        print("Warning: No audio data found in response.", file=sys.stderr)

    # 6. Save or print lyrics
    all_lyrics = "\n".join(lyrics_list).strip()
    if all_lyrics:
        if args.lyrics_output:
            lyrics_path = Path(args.lyrics_output)
            lyrics_path.parent.mkdir(parents=True, exist_ok=True)
            with open(lyrics_path, "w", encoding="utf-8") as f:
                f.write(all_lyrics + "\n")
            print(f"Lyrics saved successfully to: {lyrics_path.resolve()}")
        else:
            print("\n--- Generated Lyrics / Song Structure ---")
            print(all_lyrics)
            print("------------------------------------------\n")
    elif args.lyrics_output:
        print(
            "Note: No lyrics or text structure was returned to save.", file=sys.stderr
        )


if __name__ == "__main__":
    main()
