---
name: google-genmedia-toolkit
description: Multimodal generative toolkit using Google Gemini native models for image generation and conversational editing (Nano Banana), video generation and editing (Gemini Omni Flash), music creation (Google Lyria 3), and speech synthesis (Gemini Text-to-Speech).
metadata:
  author: Ecat
  version: "1.0.0"
---

# Google GenMedia Toolkit

A unified command-line and scripting toolkit powered by Google's native multimodal Gemini models for generative media creation and conversational editing.

## Prerequisites

All scripts in this toolkit must be executed using `uv run`.

```bash
uv run scripts/<script_name>.py "PROMPT" [OPTIONS]
```

---

## Tools & Reference Index

| Tool | Script | Reference Guide | Description |
| :--- | :--- | :--- | :--- |
| **Image Generation** | [`scripts/genimage.py`](scripts/genimage.py) | [`references/genimage.md`](references/genimage.md) | Nano Banana series (Gemini 3.1 Flash / Pro): Text-to-image, 4K, inpainting, style transfer, 14 ref images, Search Grounding, and multi-turn editing. |
| **Video Generation** | [`scripts/genvideo.py`](scripts/genvideo.py) | [`references/genvideo.md`](references/genvideo.md) | Gemini Omni Flash (`gemini-omni-1.1-flash`): Text/image-to-video, frame interpolation, multi-turn video editing, and temporal extension. |
| **Music Generation** | [`scripts/genmusic.py`](scripts/genmusic.py) | [`references/genmusic.md`](references/genmusic.md) | Google Lyria 3 (Clip & Pro): 30s clips, full structured songs with lyrics, and image-to-music scoring. |
| **Speech Synthesis** | [`scripts/text2speech.py`](scripts/text2speech.py) | [`references/text2speech.md`](references/text2speech.md) | Gemini TTS: 30 prebuilt expressive voices, single-speaker narration, and scripted multi-speaker dialogue. |

---

## 1. Image Generation & Editing: `genimage.py`

Generate and edit images using the **Nano Banana** model series (`gemini-3.1-flash-image` by default, `gemini-3-pro-image`, `gemini-3.1-flash-lite-image`). Supports up to 4K resolution across 14 aspect ratios, multi-image composition (up to 14 reference images), Google Search Grounding, and multi-turn conversational editing.

### Quick Examples

```bash
# Text-to-Image (2K resolution, 16:9 widescreen)
uv run scripts/genimage.py "A futuristic cyberpunk city with neon lights and flying cars in rain, cinematic lighting" -a 16:9 -s 2K -o city.jpg

# Object Inpainting / Element Modification
uv run scripts/genimage.py "Using the provided image of my cat, please add a small, knitted wizard hat on its head. Make it look like it's sitting comfortably." -i cat.png -o cat_with_hat.png

# Multi-turn Conversational Editing
uv run scripts/genimage.py "Update this infographic to be in Spanish. Do not change any other elements." --previous-id "v1_interaction_id..." -o infographic_spanish.png
```

👉 *For detailed prompt engineering templates (photorealism, stickers, typography, product mockups, style transfer) and resolution tables, see [`references/genimage.md`](references/genimage.md).*

---

## 2. Video Generation & Editing: `genvideo.py`

Create, edit, and extend cinematic videos with integrated sound design using **Gemini Omni Flash** (`gemini-omni-1.1-flash`). Supports text-to-video, image-to-video, first-and-last frame interpolation, stateful multi-turn conversational editing, and video clip extension.

### Quick Examples

```bash
# Text-to-Video (1080p continuous unbroken shot with sound design)
uv run scripts/genvideo.py "Continuous smooth drone shot gliding over misty pine forest mountains at sunrise. Sound design: gentle wind breeze, distant bird chirps. No dialogue." -a 16:9 -r 1080p -o sunrise.mp4

# First and Last Frame Interpolation
uv run scripts/genvideo.py "A smooth cinematic transition from a lush green summer forest at sunrise to a snowy forest under a starry night sky." -i summer.jpg -i winter.jpg -o season_transition.mp4

# Stateful Video Editing (Multi-turn)
uv run scripts/genvideo.py "Make the violin invisible. Keep everything else the same." --previous-id "v1_video_id..." -o invisible_violin.mp4

# Video Extension (Appends 3-10s to end of clip)
uv run scripts/genvideo.py "Continue the scene: the camera pans across the mountains as twilight sets in." -v clip.mp4 --task extend -o extended_clip.mp4
```

👉 *For camera motion techniques, audio design strategies, and URI delivery options for large/4K videos, see [`references/genvideo.md`](references/genvideo.md).*

---

## 3. Music & Song Generation: `genmusic.py`

Synthesize high-fidelity music tracks and soundtracks using **Google Lyria 3** (`lyria-3-clip-preview` for 30s clips/loops, `lyria-3-pro-preview` for full multi-section songs).

### Quick Examples

```bash
# Instrumental Soundtrack Theme
uv run scripts/genmusic.py "Uplifting cinematic orchestral soundtrack with energetic strings and inspiring brass crescendo, 120 BPM, instrumental only" -o epic_theme.mp3

# Full Song with Structured Lyrics & Vocals
uv run scripts/genmusic.py "Melodic synthwave track with nostalgic 80s analog synth leads, punchy drums, and vocoder vocals singing about neon dreams" -m lyria-3-pro-preview -l lyrics.txt -o synthwave_song.mp3

# Image-to-Music (Visual Mood Soundtrack)
uv run scripts/genmusic.py "Compose ambient soundtrack that captures the mystical and tranquil atmosphere of this fantasy landscape." -i landscape.jpg -o ambient_bgm.mp3
```

👉 *For 5-dimension prompt engineering (genre, mood, instrumentation, tempo, vocals) and structured lyric tags, see [`references/genmusic.md`](references/genmusic.md).*

---

## 4. Text-to-Speech Synthesis: `text2speech.py`

Synthesize natural, expressive speech audio using **Gemini TTS** (`gemini-3.1-flash-tts-preview`). Supports 30 distinct prebuilt voices, inline emotional cues (`[sighs]`, `[laughs]`, `[whispering]`, `[excitedly]`), single-speaker narration, and scripted multi-speaker dialogue.

### Quick Examples

```bash
# Single Speaker Narration with Vocal Cues
uv run scripts/text2speech.py "[sighs] Welcome back... [excitedly] Let's create something extraordinary today!" -v Puck -o welcome.wav

# Read Article from File
uv run scripts/text2speech.py -f article.txt -v Charon -o article_narration.wav

# Multi-Speaker Scripted Dialogue
uv run scripts/text2speech.py "Alice: [excitedly] Good morning Bob! Have you checked out the new Gemini image model?
Bob: [laughs] Absolutely Alice! The text rendering and thinking mode are mind-blowing." -s "Alice:Aoede" -s "Bob:Fenrir" -o podcast_dialogue.wav
```

👉 *For the complete directory of all 30 prebuilt voices, emotional tag directory (`[xxx]`), and dialogue script formatting guidelines, see [`references/text2speech.md`](references/text2speech.md).*
