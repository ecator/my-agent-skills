# Gemini Text-to-Speech Synthesis Guide (`text2speech.py`)

`scripts/text2speech.py` provides high-fidelity speech synthesis using Google's native **Gemini Text-to-Speech (TTS)** models via the Gemini Interactions API. It supports expressive single-speaker narration, emotional vocal nuances, long-form document reading, and multi-speaker scripted dialogue with 30 distinct prebuilt voices.

---

## 1. Supported Models

| Model Name | Model ID (`-m`) | Core Characteristics |
| :--- | :--- | :--- |
| **Gemini 3.1 Flash TTS** *(Default)* | `gemini-3.1-flash-tts-preview` | Latest generation TTS model: ultra-low latency, highly natural prosody, expressive emotional modulation (24kHz high fidelity). |
| **Gemini 2.5 Flash TTS** | `gemini-2.5-flash-preview-tts` | High-throughput, low-latency speech generation. |
| **Gemini 2.5 Pro TTS** | `gemini-2.5-pro-preview-tts` | Professional-grade speech synthesis with deep narrative nuance. |

---

## 2. Comprehensive Directory of 30 Prebuilt Voices

List all available voices from the command line anytime:
```bash
uv run scripts/text2speech.py --list-voices
```

| Voice Name | Tone / Style Description | Recommended Applications |
| :--- | :--- | :--- |
| **Zephyr** | Bright | Morning news briefings, voice assistants, smart displays |
| **Puck** | Upbeat | Video game characters, dynamic commercial intros, children's stories |
| **Charon** | Informative | Scientific documentaries, tech podcasts, educational explainers |
| **Kore** *(Default)* | Firm | Corporate presentations, brand manifestos, executive announcements |
| **Fenrir** | Excitable | Sports commentary, movie trailers, high-energy intros |
| **Leda** | Youthful | Lifestyle vlogs, teenage character dialogue, fashion content |
| **Orus** | Firm | Thriller audiobooks, military narratives, authoritative voiceover |
| **Aoede** | Breezy | Travel vlogs, lifestyle podcasts, casual talk shows |
| **Callirrhoe** | Easy-going | Conversational AI agents, customer support, cozy storytelling |
| **Autonoe** | Bright | Interactive product walkthroughs, tutorial guides, audiobooks |
| **Enceladus** | Breathy | Guided meditation, sleep stories, intimate emotional monologues |
| **Iapetus** | Clear | Language learning courses, ESL listening comprehension |
| **Umbriel** | Easy-going | Nature documentaries, relaxing essays, ambient narration |
| **Algieba** | Smooth | Late-night radio, jazz reviews, atmospheric poetry |
| **Despina** | Smooth | Museum audio guides, art critique, luxury brand storytelling |
| **Erinome** | Clear | Corporate compliance training, formal e-learning modules |
| **Algenib** | Gravelly | Noir detective monologues, gritty fantasy characters, elderly narrators |
| **Rasalgethi** | Informative | Financial analysis, historical retrospectives, deep-dive journalism |
| **Laomedeia** | Upbeat | Product promotions, fast-paced social media reels |
| **Achernar** | Soft | ASMR, whisper therapy, soothing bedtime reflections |
| **Alnilam** | Firm | Legal disclaimers, governmental public notices, news anchors |
| **Schedar** | Even | Statistical data reports, automated telemetry, neutral reports |
| **Gacrux** | Mature | Historical epics, memoirs, senior character voices |
| **Pulcherrima** | Forward | Startup pitch decks, motivational speeches, TED-style presentations |
| **Achird** | Friendly | Community management, customer onboarding, welcoming assistants |
| **Zubenelgenubi** | Casual | Street interviews, casual YouTube voiceover, buddy banter |
| **Vindemiatrix** | Gentle | Wellness podcasts, parenting guides, empathetic customer care |
| **Sadachbia** | Lively | Anime voice acting, playful science facts, animated skits |
| **Sadaltager** | Knowledgeable | Philosophical treatises, encyclopedia entries, masterclasses |
| **Sulafat** | Warm | Holiday greetings, thank-you messages, heartfelt personal letters |

---

## 3. Command-Line Options Reference

```bash
uv run scripts/text2speech.py "PROMPT" [OPTIONS]
```

| Flag / Option | Short Alias | Default | Description |
| :--- | :--- | :--- | :--- |
| `prompt` | Positional | `""` | Text or dialogue script to synthesize (ignored if `-f` or `--stdin` is passed). |
| `-f, --file` | `--file` | `None` | Read text transcript or script from a file. |
| `--stdin` | `--stdin` | `False` | Read text transcript from standard input (stdin). |
| `-m, --model` | `--model` | `gemini-3.1-flash-tts-preview` | TTS model ID. |
| `-o, --output` | `--output` | `output.wav` | Output audio file path (supports `.wav` and `.mp3`). |
| `-v, --voice` | `--voice` | `Kore` | Voice name for single-speaker TTS (choose from 30 prebuilt voices). |
| `-s, --speaker` | `--speaker` | `[]` | Multi-speaker voice mapping: `'SpeakerName:VoiceName'` (supports up to 2 speakers). |
| `--rate` | `--rate` | `24000` | Sample rate in Hz (default: 24000 Hz). *Note: Rarely needs modification; default 24kHz provides optimal clarity.* |
| `--channels` | `--channels` | `1` | Audio channels (1 for mono, 2 for stereo). *Note: Rarely needs modification; mono is standard for speech.* |
| `--sample-width`| `--sample-width`| `2` | Sample width in bytes (2 for 16-bit PCM). *Note: Rarely needs modification.* |
| `--list-voices` | `--list-voices` | `False` | Print all 30 available voices and exit. |
| `--retry` | `--retry` | `3` | Maximum automatic retries on transient errors. |

> **Audio Parameter Tip:** Under normal circumstances, you do **not** need to change `--rate`, `--channels`, or `--sample-width`. The defaults (24kHz, mono, 16-bit PCM) are already tuned for industry-standard studio vocal clarity and maximum cross-platform compatibility.

---

## 4. Usage Examples & Workflows

### 4.1 Emotional Expressions & Vocal Cues (`[xxx]` Syntax)
Gemini TTS natively interprets inline bracketed natural language cues `[cue]` to render authentic vocal behaviors, emotions, and pacing shifts.

> **💡 Customization & Language Tip:**
> - **Open-ended & Customizable**: Cues are **not** limited to a fixed keyword list. You can freely describe arbitrary nuances, delivery styles, or vocal dynamics (e.g. `[sighs softly]`, `[speaking with rising urgency]`, `[whispering conspiratorially]`, `[chuckles nervously]`).
> - **Use English for Cues**: **Always write cue directives inside `[...]` in English** for optimal model instruction-following and nuance fidelity, even when synthesizing dialogue in other languages (e.g. `[laughs] 这是一个很棒的发现！`).

**Common Examples & Categories:**
- **Non-Verbal Sounds**: `[sighs]`, `[laughs]`, `[giggles]`, `[chuckles]`, `[gasps]`, `[clears throat]`, `[coughs]`, `[yawns]`, `[snickers]`, `[groans]`, etc.
- **Tone & Delivery Dynamics**: `[whispering]`, `[excitedly]`, `[sarcastically]`, `[hesitantly]`, `[nervously]`, `[confidently]`, `[sadly]`, `[cheerfully]`, `[annoyed]`, `[speaking fast]`, `[solemnly]`, etc.
- **Pacing & Breathing**: `[short pause]`, `[dramatic pause]`, `[takes a deep breath]`, `[out of breath]`, etc.

```bash
uv run scripts/text2speech.py \
  "[sighs softly] I really thought we had more time... [whispering] but now, everything has changed. [excitedly] Wait! Did you hear that? [laughs] We actually did it!" \
  -v Puck -o emotional_sample.wav
```

### 4.2 Single-Speaker Narration
```bash
uv run scripts/text2speech.py \
  "Welcome to the next frontier of multimodal intelligence with Google Gemini. Everything you imagine can now be created with precision." \
  -v Puck -o welcome.wav
```

### 4.3 Documentary & Scientific Narration
```bash
uv run scripts/text2speech.py \
  "Deep in the heart of the Orion Nebula, vast clouds of cosmic dust collapse under gravity, giving birth to millions of new stars." \
  -v Charon -o cosmos_narration.wav
```

### 4.4 Long-Form Article Reading from File
```bash
uv run scripts/text2speech.py \
  -f article.txt -v Erinome -o article_audio.wav
```

### 4.5 Multi-Speaker Dialogue with Emotional Cues

Format your transcript using `SpeakerName: Dialogue line`, bind each speaker to a chosen voice via `-s`, and freely incorporate bracketed vocal cues:

```bash
uv run scripts/text2speech.py \
  "Alice: [excitedly] Hey Bob! Did you see the new update for Gemini 3.1 Flash?
Bob: [laughs] I sure did, Alice! The multi-turn video editing and 4K image generation are absolutely mind-blowing.
Alice: [whispering] It honestly feels like we are living in the future of creative tools." \
  -s "Alice:Aoede" -s "Bob:Fenrir" \
  -o podcast_chat.wav
```

### 4.6 Piped Input via Standard Input (stdin)
```bash
cat << 'EOF' | uv run scripts/text2speech.py --stdin -s "Host:Puck" -s "Guest:Rasalgethi" -o interview.wav
Host: [cheerfully] Welcome back to AI Weekly! Today we are joined by Dr. Vance.
Guest: [clears throat nervously] Thank you for having me. The rate of progress in generative media this year is truly unprecedented.
Host: [excitedly] Let's dive right into the details!
EOF
```

---

## 5. Best Practices & Audio Tuning

1. **Custom English Vocal Cues**: Bracketed cues are open-ended and can be customized with descriptive natural language. Always write cue instructions in English inside the brackets (e.g. `[sighs softly]`, `[speaking with urgency]`) for optimal model interpretation.
2. **Punctuation Controls Prosody**: Ellipses (`...`) create contemplative pauses, em-dashes (`—`) indicate parenthetical thoughts, and exclamation marks (`!`) elevate intensity.
3. **Multi-Speaker Formatting**: Ensure every dialogue line begins with `SpeakerName: ` (with a trailing space), matching the exact names declared in the `-s` arguments.
4. **Leave Audio Parameters at Defaults**: Do not customize `--rate`, `--channels`, or `--sample-width` unless you have explicit constraints requiring legacy formats (e.g. 8kHz telephony or 16kHz specialized embedded hardware).
