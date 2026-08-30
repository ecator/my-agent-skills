# Google Lyria 3 Music & Song Generation Guide (`genmusic.py`)

`scripts/genmusic.py` provides access to Google's **Lyria 3** native music generation models (`lyria-3-clip-preview` and `lyria-3-pro-preview`) via the Gemini Interactions API. It supports generating instrumental tracks, background scores, structured vocal songs with full lyrics, and image-inspired soundtracks (Image-to-Music).

---

## 1. Supported Models & Selection Guide

| Model Name | Model ID (`-m`) | Characteristics & Recommended Use Cases |
| :--- | :--- | :--- |
| **Lyria 3 Clip** *(Default)* | `lyria-3-clip-preview` | **Rapid Short Form**: Generates ~30-second high-quality music clips, background loops, video soundscapes, and transitions. |
| **Lyria 3 Pro** | `lyria-3-pro-preview` | **Full Production Tracks**: Generates full-length multi-section songs with complex multi-instrument arrangements and vocal lyrics. |

---

## 2. Command-Line Options Reference

```bash
uv run scripts/genmusic.py "PROMPT" [OPTIONS]
```

| Flag / Option | Short Alias | Default | Description |
| :--- | :--- | :--- | :--- |
| `prompt` | Positional | `""` | Music prompt describing genre, instruments, tempo, mood, and vocal styles. Ignored if `-f` or `--stdin` is passed. |
| `-f, --file` | `--file` | `None` | Read prompt or structured lyrics from a text file. |
| `--stdin` | `--stdin` | `False` | Read prompt from standard input (stdin). |
| `-m, --model` | `--model` | `lyria-3-clip-preview` | Model ID (`lyria-3-clip-preview` or `lyria-3-pro-preview`). |
| `-o, --output` | `--output` | `output.mp3` | Output audio file path (supports `.mp3` and `.wav` for uncompressed audio). |
| `-l, --lyrics` | `--lyrics-output`| `None` | Save generated lyrics and song structure to a text file. |
| `-i, --image` | `--image` | `[]` | Reference image path(s) for Image-to-Music soundtrack generation (up to 10 images). |
| `--retry` | `--retry` | `3` | Maximum automatic retries on transient errors. |

---

## 3. Music Prompting Strategy: The 5 Core Dimensions

When drafting a prompt for Lyria 3, incorporate the following 5 dimensions for maximum musical precision:

1. **Genre & Subgenre**: e.g., `Synthwave`, `Lo-Fi Hip Hop`, `Cinematic Orchestral`, `Cyberpunk Industrial`, `Acoustic Folk Pop`, `Jazz Fusion`.
2. **Mood & Energy**: e.g., `Uplifting & Inspiring`, `Melancholic & Nostalgic`, `High-energy & Euphoric`, `Dark & Mysterious`, `Chill & Relaxing`.
3. **Instrumentation**: e.g., `Warm analog vintage synths, 808 sub-bass, punchy acoustic drums, fingerstyle acoustic guitar, dramatic string ensemble`.
4. **Tempo & Rhythm**: e.g., `Slow tempo 75 BPM`, `Mid-tempo 110 BPM driving groove`, `Fast-paced 140 BPM electronic beat`.
5. **Vocals & Delivery (Optional)**: e.g., `Ethereal female vocals with reverb`, `Soulful male tenor`, `Robotic vocoder hook`, or `Instrumental only, no vocals`.

---

## 4. Usage Examples & Practical Workflows

### 4.1 Cinematic Orchestral Epic Theme
```bash
uv run scripts/genmusic.py \
  "Uplifting cinematic orchestral soundtrack with powerful French horns, energetic rolling strings, massive taiko drum impacts, and an inspiring brass crescendo. 120 BPM, heroic adventure theme, instrumental only." \
  -o epic_soundtrack.mp3
```

### 4.2 80s Retro Synthwave Track
```bash
uv run scripts/genmusic.py \
  "80s retro synthwave track with warm analog synthesizer arpeggios, gated reverb snare drums, pulsing bassline, and catchy neon lead melody. Nostalgic summer night vibe." \
  -o synthwave_night.mp3
```

### 4.3 Relaxing Lo-Fi Study Beat
```bash
uv run scripts/genmusic.py \
  "Relaxing chillhop lo-fi study beat with dusty vinyl crackle, gentle jazz piano chords, laid-back boom-bap drum loop, and warm upright bass. 80 BPM." \
  -o lofi_study.mp3
```

### 4.4 Full Structured Song with Lyrics & Vocals
Use `lyria-3-pro-preview` and format the prompt using bracketed section tags (`[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`):
```bash
uv run scripts/genmusic.py \
  "Pop-rock anthem about chasing dreams under city lights. Powerful female lead vocals.
[Verse 1]
Walking down the neon street, feeling every heartbeat in the concrete.
[Chorus]
We're flying higher than the sky tonight,
Blazing through the darkest night!
[Bridge]
No looking back, the road is clear.
[Outro]
Holding on to the light." \
  -m lyria-3-pro-preview -l song_lyrics.txt -o dream_anthem.mp3
```

### 4.5 Image-to-Music Soundtrack Generation
Provide landscape or artwork images, and Lyria 3 will compose a soundtrack reflecting the aesthetic and emotional tone:
```bash
uv run scripts/genmusic.py \
  "Compose an ethereal, ambient space soundtrack that perfectly reflects the visual mood of this cosmic landscape. Soft shimmering synth pads and subtle acoustic piano." \
  -i galaxy.jpg -o ambient_space.mp3
```

### 4.6 Uncompressed WAV Audio Output
```bash
uv run scripts/genmusic.py \
  "Acoustic fingerstyle guitar melody with gentle wooden body resonance, clean studio recording." \
  -o guitar_theme.wav
```

---

## 5. Best Practices & Pro Tips

1. **Be Explicit About Vocals**: If you do not want singing or vocal chops, explicitly state `"Instrumental only, no vocals"`.
2. **Use Bracketed Structural Tags**: For multi-stanza tracks, using `[Intro]`, `[Verse 1]`, `[Chorus]`, `[Guitar Solo]`, `[Bridge]`, and `[Outro]` helps the model time chord progressions and vocal arrangements accurately.
3. **Avoid Generic Prompts**: Replace `"make a cool beat"` with specific instrument names and tempo descriptions.
