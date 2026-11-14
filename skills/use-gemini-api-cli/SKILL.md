---
name: use-gemini-api-cli
description: Use the Gemini API CLI (`gemini-api`) from the shell to generate text and media (images, speech/TTS, music, video), analyze or transcribe documents, recordings, and YouTube URLs, manage uploads via the Files API, and run or manage Gemini managed agents (such as Deep Research). Activate when calling Gemini models or managed agents directly from the command line, scripts, or CI pipelines without adding SDK code.
metadata:
  author: Ecat
  version: "1.0.0"
---

# Gemini API CLI (`gemini-api`)

`gemini-api` is a stateless, zero-dependency command-line client built on the Gemini **Interactions API** for AI coding agents with shell access, scripts, and CI pipelines. Use it to generate text and media (images, speech, music, video), analyze or transcribe files and YouTube URLs, and delegate tasks to Gemini managed agents.

> **Note:** `gemini-api` is a stateless API client, not an interactive coding agent like `@google/gemini-cli`. You can invoke `gemini-api` directly from any coding agent subprocess or shell.

---

## Core Agent Rules

When invoking `gemini-api` as an AI agent, follow these operational rules:

1. **Check installation first — DO NOT auto-install:**
   - Before running workflows, verify that `gemini-api` is installed (`gemini-api version`).
   - **DO NOT automatically run installation commands or scripts yourself.** If `gemini-api` is not installed (or authentication is missing), stop and prompt the user with the installation/configuration instructions for their platform.
2. **Discover commands and schemas offline first:**
   - Run `gemini-api --help` or `gemini-api --usage` (prints the full command tree in KDL format) to choose a command, and `gemini-api --help-global` to inspect global flags.
   - Run `gemini-api <command> --schema` before constructing a `--body` JSON payload.
3. **Preview unfamiliar or complex calls offline:**
   - Pass `--dry-run` (or `--dry-run -o json`) to validate flags, redact credentials, and inspect the outgoing HTTP request without making network calls.
4. **Disable streaming when requesting structured JSON:**
   - For a single JSON object or `--jq` filtering on streaming commands (`generate` or `agent run`), always pass `--stream=false -o json` (or `--stream=false --jq '<expr>'`).
5. **Capture file paths and IDs to chain stateless workflows:**
   - Media (`image`, `tts`, `music`, `video`) and `transcribe` commands write binary/transcript artifacts to disk and print **only the output file path** to `stdout` (keeping binary data out of the context window).
   - Multi-turn or async workflows are chained explicitly using `--previous-interaction-id <id>`, uploaded `files/<id>` URIs, `video --resume <id>`, or `agent status <id>`.
6. **Use non-interactive, machine-readable diagnostics:**
   - Commands never prompt unless `--interactive` is set. Pass `--agent-mode` for structured JSON errors on `stderr` and check exit codes (`0` = ok, `1` = runtime/API error, `2` = usage/validation error, `3` = auth error).

---

## Choose the Right Gemini Tool

| Tool | What it does | When to use it |
| :--- | :--- | :--- |
| **Gemini API CLI (`gemini-api`)** | Calls Gemini models and managed agents directly from any shell. | Your coding agent, shell script, or CI job needs to generate media, analyze files, or run a background research agent with zero project dependencies. |
| **Google GenAI SDKs** | Imports Gemini client libraries into Python, TypeScript/JavaScript, Go, Java, or C# code. | You are building Gemini features into an application, backend service, or real-time Live API (bidirectional WebSocket) session. |
| **Gemini Docs MCP & skills** | Provides live documentation search and current SDK rules. | Your coding agent is writing application code that imports a Google GenAI SDK. |

---

## Prerequisites & Authentication

### 1. Verify `gemini-api` Installation

Check if `gemini-api` is available on `PATH`:

```bash
gemini-api version
```

> **IMPORTANT:** **Do NOT install `gemini-api` automatically.** If `gemini-api` is not found on `PATH`, inform the user that `gemini-api` is not installed and provide the installation command below for their operating system so they can install it themselves:

- **macOS and Linux:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.sh | bash
  # Pin a specific release tag in CI/automated environments:
  curl -fsSL https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.sh | GEMINI_VERSION=<release-tag> bash
  ```
- **Windows (PowerShell):**
  ```powershell
  iwr -useb https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.ps1 | iex
  ```
- **Go:**
  ```bash
  go install github.com/google-gemini/gemini-api-cli/cmd/gemini-api@latest
  ```
- **Prebuilt binaries:** Download versioned archives from [GitHub Releases](https://github.com/google-gemini/gemini-api-cli/releases) and place `gemini-api` on `PATH`.

### 2. Verify & Configure Authentication

Check the active authentication status with `gemini-api whoami`. If no API key is configured (or a command returns exit code `3`), prompt the user to create an API key in [Google AI Studio](https://aistudio.google.com/apikey) and configure it via `GEMINI_API_KEY` or the OS keychain (pass `--no-keyring` to store in `~/.config/gemini-api/config.yaml` instead):

```bash
# Option A: Environment variable
export GEMINI_API_KEY="YOUR_API_KEY"

# Option B: Save to OS keychain
gemini-api configure --api-key "YOUR_API_KEY"

# Verify active credential source and test offline
gemini-api whoami
gemini-api generate "Confirm CLI setup in one sentence." --dry-run
```

> **Security Warning:** Treat `GEMINI_API_KEY` as a secret. Never hardcode or commit it to version control.

---

## Command Reference

Each command defaults to a model suited for its task. Override with `--model` (`-m`), and run `gemini-api models` to list available models.

| Group | Command | Default Model | Description |
| :--- | :--- | :--- | :--- |
| **Create** | `image` | `gemini-nano-banana-2.1` | Generates or edits images (`-i`), writes an image file to disk, and prints its path. |
| **Create** | `tts` | `gemini-3.8-flash-tts` | Synthesizes 24 kHz mono WAV speech (single or two-speaker) and prints the output path. |
| **Create** | `music` | `lyria-3.5` | Generates music tracks or loops, writes the audio file, and prints its path. |
| **Create** | `video` | `gemini-omni-1.2-flash` | Generates or edits MP4 clips and polls until done (`--async` returns an ID immediately). |
| **Create** | `generate` | `gemini-3.8-flash` | Generates text and streams to `stdout` (`--stream=false` returns one complete result). |
| **Understand** | `analyze` | `gemini-3.8-flash` | Answers questions about PDFs, images, audio, video, CSV/text files, or public YouTube URLs. |
| **Understand** | `transcribe` | `gemini-3.5-transcribe` | Writes speaker-labeled, timestamped transcripts (`md`, `text`, `json`, or `srt`) and prints output paths. |
| **Manage agents** | `agent` | `gemini-3.8-flash` | Runs managed agents (`run`, `status`, `cancel`, `delete-interaction`) and manages custom agent definitions (`create`, `list`, `get`, `delete`). |
| **Manage agents** | `environments`, `credentials`, `webhooks`, `triggers` | — | Configures sandbox environments, stored credentials, webhook delivery, and scheduled cron runs for managed agents. |
| **Setup & files** | `configure`, `auth`, `whoami` | — | Configures credentials/defaults and displays active auth state. |
| **Setup & files** | `files` | — | Uploads, lists, inspects, registers, and deletes files in the Files API (48-hour TTL). |
| **Setup & files** | `models` | — | Shows the curated offline model catalog (`models list` / `models get` query the live API). |

With `-o json`, media commands still write the file to disk and print structured metadata to `stdout`:

```json
{
  "kind": "image",
  "mime_type": "image/jpeg",
  "path": "/path/to/project/assets/db-icon.jpg",
  "response_id": "v1_...",
  "size_bytes": 2914159,
  "status": "completed"
}
```

---

## Workflows & Examples

### 1. Image Generation and Editing (`image`)

Generate UI placeholders, icons, and hero images, or pass existing images back in with `-i` (repeatable for combining multiple reference images) or `--previous-interaction-id` to edit:

```bash
# Generate a 16:9 image at 2K resolution (options: 512, 1K, 2K, 4K) and capture its path
HERO_PATH=$(gemini-api image "Friendly robot mascot in a sunlit workshop, space on left for headline" \
  --aspect-ratio 16:9 \
  --image-size 2K \
  --out ./public/images/hero.jpg)

# Edit the generated image using -i
gemini-api image "Add a winter scarf and soft snowfall outside the window" \
  -i "$HERO_PATH" \
  --out ./public/images/hero-winter.jpg
```

### 2. Speech Synthesis (`tts`)

Synthesize 24 kHz mono WAV audio. Default voice is `Kore`; pick another with `--voice` (`-v`, e.g., `Kore`, `Puck`, `Zephyr`, `Charon`, `Fenrir`, `Aoede`). For two-speaker dialogue, prefix turns with speaker names and map speakers via `--multi-speaker`:

```bash
# Single speaker
gemini-api tts "Build succeeded. All integration tests passed." \
  --voice Aoede \
  --out ./public/audio/build-ok.wav

# Multi-speaker dialogue
gemini-api tts "Alice: Welcome to the release walkthrough! Bob: Let's look at what shipped today." \
  --multi-speaker "Alice=Kore,Bob=Puck" \
  --out ./public/audio/release-intro.wav
```

### 3. Music and Video Generation (`music`, `video`)

Compose music tracks with Lyria and generate or animate MP4 clips with Gemini Omni:

```bash
# Music generation
gemini-api music "Warm ambient synth and acoustic guitar background loop, 95 BPM" \
  --out ./public/audio/bg-loop.mp3

# Video generation (waits for completion by default)
gemini-api video "A drone shot of a mountain landscape at sunrise." \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --out ./public/video/mountain-sunrise.mp4

# Async video generation: return interaction ID immediately, resume later
VIDEO_ID=$(gemini-api video "A timelapse of a city at night" --async)
gemini-api video --resume "$VIDEO_ID" --out ./public/video/city-night.mp4
```

Pass `-i <image-path>` to `gemini-api video` to animate an existing image, or `--previous-interaction-id <id>` to extend/edit a prior video interaction.

### 4. Text Generation (`generate`)

Streams text deltas to `stdout` by default:

```bash
gemini-api generate "Write a one-paragraph welcome message for new users of a note-taking app."

# Pipe input via --stdin, set system instruction, or get a single JSON response
cat draft.md | gemini-api generate "Rewrite this more concisely." --stdin --system "Use technical documentation style."
gemini-api generate "List 3 key benefits of rust" --stream=false -o json
```

Use `--previous-interaction-id <id>` to continue a multi-turn conversation.

### 5. Document Analysis & Transcription (`analyze`, `transcribe`, `files`)

- `analyze` answers questions about PDFs, spreadsheets, screenshots, audio, video, CSV/text files, or public YouTube URLs. Pass `-i` multiple times to compare files (e.g., before-and-after screenshots).
- `transcribe` outputs speaker-labeled, timestamped transcripts in `md` (default), `text`, `json`, or `srt` format.

```bash
# Analyze a PDF document
gemini-api analyze -i ./docs/product-brief.pdf "List the open questions and who owns each one." > open-questions.md

# Compare two images
gemini-api analyze -i before.png -i after.png "What changed between these two UI screenshots?"

# Analyze a YouTube video
gemini-api analyze -i https://youtu.be/dQw4w9WgXcQ "Summarize the main sections with timestamps."

# Transcribe audio/video to SRT captions
gemini-api transcribe -i ./fixtures/customer-call.mp4 --format srt --out ./fixtures/customer-call.srt
```

#### Handling Large Files (>14 MB) with `files upload`

Inline `-i` file inputs are capped at **14 MB** raw file size (20 MB base64-encoded request payload). For larger files (up to 2 GB per file, 50 MB for PDFs), upload once via the Files API (48-hour retention) with `--wait` and reuse the `files/<id>` URI:

```bash
FILE_URI=$(gemini-api files upload ./recordings/all-hands.mp4 --wait)

gemini-api analyze -i "$FILE_URI" "List action items with owners and timestamps."
gemini-api transcribe -i "$FILE_URI" --format json --out ./recordings/all-hands.json
```

### 6. Running and Managing Agents (`agent`)

Delegate multi-step research or sandboxed tasks to Gemini managed agents (such as `deep-research-preview-04-2026` or `antigravity-preview-05-2026`). Pass `--background --stream=false` to get an interaction ID immediately without holding a stream open:

```bash
# Launch a Deep Research job in the background and capture its interaction ID
RESEARCH_ID=$(gemini-api agent run "Compare open-source vector index benchmarks and cite primary papers." \
  --agent deep-research-preview-04-2026 \
  --background \
  --stream=false \
  --jq '.id')

# Poll status or retrieve the finished result while continuing other work
gemini-api agent status "$RESEARCH_ID" -o json

# Cancel a running background interaction if needed
gemini-api agent cancel "$RESEARCH_ID"
```

Manage custom agent definitions with `gemini-api agent create`, `list`, `get`, and `delete`. Note that `agent status` and `agent cancel` take an **interaction ID**, whereas `agent get` and `agent delete` take an **agent definition ID**.

---

## Custom Request Bodies (`--body` & `--schema`)

For advanced Interactions API options without dedicated flags (such as `response_format` JSON schemas, function-calling tools, `generation_config`, or `"store": false`), pass a JSON payload with `--body` (inline string, `@file.json`, or `@-` for stdin).

Always inspect the command's JSON Schema first:

```bash
# 1. Inspect the exact JSON Schema for the request body
gemini-api generate --schema > generate-schema.json

# 2. Return schema-constrained JSON and skip storing the interaction server-side
cat logs.txt | gemini-api generate "Extract every error message from these logs." \
  --stdin \
  --body '{
    "response_format": {
      "type": "text",
      "mime_type": "application/json",
      "schema": {
        "type": "object",
        "properties": {"errors": {"type": "array", "items": {"type": "string"}}},
        "required": ["errors"]
      }
    },
    "store": false
  }'
```

> **Conflict Rule:** `--body` merges with command flags. If both specify the same key, `gemini-api` fails immediately with exit code `2` so conflicting inputs fail fast.

---

## Global Flags, Exit Codes & Limitations

### Useful Global Flags (`gemini-api --help-global`)

- `-o, --output-format <format>`: `pretty` (default), `json`, `yaml`, `table`, `toon`.
- `-q, --jq <expr>`: Filter JSON output using a `jq` expression (writes raw text for strings by default via `--raw-output`).
- `--agent-mode`: Enable structured JSON errors on `stderr` and default TOON output for AI coding agents.
- `--dry-run`: Preview HTTP requests offline without network or keychain access.
- `--usage`: Print the CLI command schema in KDL format.
- `--timeout <duration>`: Set HTTP request timeout (e.g., `30s`, `5m`).

### Exit Codes

| Code | Meaning |
| :--- | :--- |
| `0` | Command succeeded. |
| `1` | Runtime or API error (network failure, rate limit, or failed background job). |
| `2` | Usage or validation error (unknown flag, missing input, or duplicate `--body` key). |
| `3` | Authentication or authorization failure (missing or invalid API key/token). |

### Known Limitations

- **Streaming vs. JSON output:** `generate` and `agent run` stream by default and require `--stream=false` when combined with `-o json` or `--jq` to emit a single JSON response object.
- **Inline file size limit:** Inline `-i` inputs cap at 14 MB raw data (20 MB payload with base64). Use `gemini-api files upload <path> --wait` for larger files (deleted automatically after 48 hours).
- **No bidirectional WebSockets:** `gemini-api` supports HTTP requests, SSE streaming, and async polling. For real-time bidirectional voice/video streaming, use the Live API via the Google GenAI SDKs.
