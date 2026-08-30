# /// script
# dependencies = [
#   "google-genai",
#   "python-dotenv",
#   "httpx[socks]"
# ]
# ///

import argparse
import base64
import os
import sys
import time
import wave
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

# 30 prebuilt voices supported by Gemini TTS models
VOICE_OPTIONS = {
    "Zephyr": "Bright",
    "Puck": "Upbeat",
    "Charon": "Informative",
    "Kore": "Firm",
    "Fenrir": "Excitable",
    "Leda": "Youthful",
    "Orus": "Firm",
    "Aoede": "Breezy",
    "Callirrhoe": "Easy-going",
    "Autonoe": "Bright",
    "Enceladus": "Breathy",
    "Iapetus": "Clear",
    "Umbriel": "Easy-going",
    "Algieba": "Smooth",
    "Despina": "Smooth",
    "Erinome": "Clear",
    "Algenib": "Gravelly",
    "Rasalgethi": "Informative",
    "Laomedeia": "Upbeat",
    "Achernar": "Soft",
    "Alnilam": "Firm",
    "Schedar": "Even",
    "Gacrux": "Mature",
    "Pulcherrima": "Forward",
    "Achird": "Friendly",
    "Zubenelgenubi": "Casual",
    "Vindemiatrix": "Gentle",
    "Sadachbia": "Lively",
    "Sadaltager": "Knowledgeable",
    "Sulafat": "Warm",
}

SUPPORTED_MODELS = [
    "gemini-3.1-flash-tts-preview",
    "gemini-2.5-flash-preview-tts",
    "gemini-2.5-pro-preview-tts",
]


def print_voices():
    print("\n--- Gemini TTS Available Voice Options (30 Voices) ---")
    print(f"{'Voice Name':<18} | {'Tone / Style Description'}")
    print("-" * 50)
    for name, desc in VOICE_OPTIONS.items():
        print(f"{name:<18} | {desc}")
    print("-" * 50 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate single-speaker or multi-speaker speech audio using Gemini Text-to-Speech (TTS) models."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default="",
        help="Text prompt or script for speech synthesis (ignored if --stdin or --file is used).",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="input_file",
        default=None,
        help="Read the prompt / transcript from a text file.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read the prompt / transcript from standard input (stdin).",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gemini-3.1-flash-tts-preview",
        choices=SUPPORTED_MODELS,
        help="TTS model ID (default: gemini-3.1-flash-tts-preview).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.wav",
        help="Output audio file path (default: out.wav).",
    )
    parser.add_argument(
        "-v",
        "--voice",
        default="Kore",
        help="Voice name for single-speaker TTS (default: Kore). Use --list-voices to view all 30 options.",
    )
    parser.add_argument(
        "-s",
        "--speaker",
        action="append",
        dest="speakers",
        default=[],
        help="Speaker voice mapping for multi-speaker TTS in 'SpeakerName:VoiceName' or 'SpeakerName=VoiceName' format (can be specified up to 2 times). Example: -s 'Joe:Kore' -s 'Jane:Puck'",
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=24000,
        help="Sample rate in Hz when writing WAV audio file (default: 24000).",
    )
    parser.add_argument(
        "--channels",
        type=int,
        default=1,
        help="Number of audio channels when writing WAV file (default: 1 for mono).",
    )
    parser.add_argument(
        "--sample-width",
        type=int,
        default=2,
        help="Audio sample width in bytes when writing WAV file (default: 2 for 16-bit PCM).",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="Number of automatic retries on transient server/token errors (default: 3).",
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List all supported 30 voice options and exit.",
    )
    return parser.parse_args()


def save_audio_file(
    filename: str,
    pcm_or_raw: bytes,
    channels: int = 1,
    rate: int = 24000,
    sample_width: int = 2,
):
    out_path = Path(filename)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # If the payload already contains a RIFF/WAV header or isn't .wav, write raw bytes
    if pcm_or_raw.startswith(b"RIFF") or out_path.suffix.lower() != ".wav":
        with open(out_path, "wb") as f:
            f.write(pcm_or_raw)
    else:
        with wave.open(str(out_path), "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_or_raw)


def build_speech_config(voice: str, speakers: list[str]) -> list[dict]:
    if speakers:
        speech_config = []
        if len(speakers) > 2:
            print(
                "Warning: Gemini TTS multi-speaker supports up to 2 speakers. Using the first 2 speakers.",
                file=sys.stderr,
            )
            speakers = speakers[:2]

        for item in speakers:
            sep = ":" if ":" in item else ("=" if "=" in item else None)
            if not sep:
                print(
                    f"Error: Invalid speaker format '{item}'. Expected 'SpeakerName:VoiceName' or 'SpeakerName=VoiceName'.",
                    file=sys.stderr,
                )
                sys.exit(1)
            spk_name, v_name = item.split(sep, 1)
            spk_name = spk_name.strip()
            v_name = v_name.strip()
            speech_config.append({"speaker": spk_name, "voice": v_name})
        return speech_config
    else:
        return [{"voice": voice.strip()}]


def main():
    args = parse_args()

    if args.list_voices:
        print_voices()
        sys.exit(0)

    # 1. Resolve prompt / transcript text
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

    if not prompt_text:
        print(
            "Error: Prompt text is required. Provide text as argument, pass --file, or pipe via --stdin.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2. Build speech_config
    speech_config = build_speech_config(args.voice, args.speakers)

    # 3. Setup client & request parameters
    client = genai.Client(api_key=GEMINI_API_KEY)
    speaker_desc = (
        ", ".join([f"{s['speaker']} ({s['voice']})" for s in speech_config])
        if args.speakers
        else f"Voice: {speech_config[0]['voice']}"
    )
    print(f"Synthesizing speech with model '{args.model}' [{speaker_desc}]...")

    # 4. Execute interaction with automated retry for transient errors
    audio_data = None
    retries = max(1, args.retry + 1)

    for attempt in range(1, retries + 1):
        try:
            interaction = client.interactions.create(
                model=args.model,
                input=prompt_text,
                response_format={"type": "audio"},
                generation_config={
                    "speech_config": speech_config,
                },
            )

            # Extract audio from convenience property
            if getattr(interaction, "output_audio", None) and getattr(
                interaction.output_audio, "data", None
            ):
                audio_data = base64.b64decode(interaction.output_audio.data)

            # Fallback to steps if needed
            if not audio_data and getattr(interaction, "steps", None):
                for step in interaction.steps:
                    if getattr(step, "type", None) == "model_output":
                        for block in getattr(step, "content", []):
                            if getattr(block, "type", None) == "audio" and getattr(
                                block, "data", None
                            ):
                                audio_data = base64.b64decode(block.data)
                                break
                    if audio_data:
                        break

            if audio_data:
                break
            else:
                raise ValueError("No audio data returned by TTS service.")

        except Exception as e:  # noqa: BLE001
            if attempt < retries:
                wait_time = 2 ** (attempt - 1)
                print(
                    f"Warning: TTS generation attempt {attempt} failed ({e}). Retrying in {wait_time}s...",
                    file=sys.stderr,
                )
                time.sleep(wait_time)
            else:
                print(f"Failed to generate speech: {e}", file=sys.stderr)
                sys.exit(1)

    # 5. Save audio output
    try:
        save_audio_file(
            args.output,
            audio_data,
            channels=args.channels,
            rate=args.rate,
            sample_width=args.sample_width,
        )
        print(f"Speech audio saved successfully to: {Path(args.output).resolve()}")
    except Exception as e:  # noqa: BLE001
        print(f"Error saving audio file '{args.output}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
