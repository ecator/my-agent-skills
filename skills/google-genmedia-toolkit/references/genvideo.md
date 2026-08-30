# Gemini Omni Flash Video Generation & Editing Guide (`genvideo.py`)

`scripts/genvideo.py` provides an end-to-end interface for Google's **Gemini Omni Flash** (`gemini-omni-1.1-flash`) multimodal video foundation model. It supports text-to-video, image-to-video, first-and-last frame transition interpolation, subject reference generation, conversational multi-turn video editing, uploaded video modification, and temporal clip extension.

---

## 1. Supported Model & Core Capabilities

- **Model ID**: `gemini-omni-1.1-flash`
- **Native Multimodality**: Processes and synthesizes text descriptions, image references, temporal motions, and environmental sound design simultaneously.
- **Stateful Conversational Editing**: Modifies targeted video elements across conversation turns using `previous_interaction_id` while preserving unmentioned context.
- **Physical & Cinematic Coherence**: Simulates real-world lighting, fluid dynamics, camera physics, and natural object momentum.

---

## 2. Command-Line Options Reference

```bash
uv run scripts/genvideo.py "PROMPT" [OPTIONS]
```

| Flag / Option | Short Alias | Default | Description |
| :--- | :--- | :--- | :--- |
| `prompt` | Positional | `""` | Text prompt describing the scene, camera dynamics, lighting, and audio design. |
| `-f, --file` | `--file` | `None` | Read prompt from a text file. |
| `--stdin` | `--stdin` | `False` | Read prompt from standard input (stdin). |
| `-m, --model` | `--model` | `gemini-omni-1.1-flash` | Model ID. |
| `-o, --output` | `--output` | `output.mp4` | Output video file path (MP4 format). |
| `-t, --text-output`| `--text-output` | `None` | Save model response text/metadata to a specified file. |
| `-a, --aspect-ratio`| `--aspect-ratio`| `None` (16:9) | Aspect ratio: `16:9` (landscape widescreen [default]) or `9:16` (portrait/vertical). |
| `-r, --resolution` | `--resolution` | `720p` | Resolution: `360p`, `720p` (default), `1080p` (upscaled HD), `4k` (upscaled 4K). |
| `-i, --image` | `--image` | `[]` | Reference image path(s) for image-to-video, frame interpolation, or subject reference. |
| `-v, --video` | `--video` | `None` | Source video file path or URI for video editing or clip extension. |
| `--task` | `--task` | `None` (inferred) | Explicit task override: `text_to_video`, `image_to_video`, `reference_to_video`, `edit`, `extend`. <br>**Recommendation:** Rely primarily on natural prompt instructions to let the model infer the intended mode automatically. Only specify this parameter explicitly if prompting alone does not achieve the expected behavior, as explicit task flags impose stricter constraints on generation. |
| `--delivery` | `--delivery` | `None` (inline) | Delivery mode: `inline` (base64) or `uri` (asynchronous Google URI polling, recommended for >4MB / 1080p/4K). |
| `--previous-id` | `--previous-interaction-id`| `None` | Previous interaction ID for multi-turn sequential video editing or extension. |
| `--save-thoughts` | `--save-thoughts` | `False` | Save intermediate reasoning thoughts to disk. |
| `--retry` | `--retry` | `3` | Maximum automatic retries on transient server errors. |

---

## 3. Core Modes & Practical Usage Examples

### 3.1 Text-to-Video Generation

#### A. Single Unbroken Continuous Shot
- **Technique**: Omni Flash defaults to multi-shot narratives. If you require a continuous camera movement without cuts, explicitly state `"in a single continuous unbroken shot, no scene cuts"`.
- **Example**:
  ```bash
  uv run scripts/genvideo.py \
    "Continuous, unbroken handheld shot of a fluffy tabby cat sitting on a sunny windowsill, looking out into a leafy garden. The cat's tail twitches slowly. Sunbeams illuminate dust motes in the air. Sound design: Gentle breeze, distant bird chirps. No dialogue." \
    -a 16:9 -r 1080p -o cat_window.mp4
  ```

#### B. Cinematic Drone Landscape
- **Example**:
  ```bash
  uv run scripts/genvideo.py \
    "A majestic cinematic drone shot sweeping low over misty pine forest mountains at sunrise, golden morning light breaking through the mist. Sound design: rushing wind and ambient forest atmosphere." \
    -a 16:9 -r 1080p --delivery uri -o mountain_sunrise.mp4
  ```

#### C. Vertical Portrait Video (9:16 for Reels / Shorts)
- **Example**:
  ```bash
  uv run scripts/genvideo.py \
    "A stylish fashion model walking down a sunlit Paris boulevard during golden hour, wearing a trench coat, looking back at the camera and smiling naturally." \
    -a 9:16 -r 1080p -o paris_model.mp4
  ```

---

### 3.2 Image-to-Video Generation

Provide a static image reference (photo, illustration, architectural render) and animate it with camera and object motion.
- **Example**:
  ```bash
  # Animate a hand-drawn sketch into realistic ocean footage
  uv run scripts/genvideo.py \
    "Turn this drawing into realistic ocean footage, using the drawing only as a guide for movement. A clownfish swimming gracefully through swaying anemones. Do not show the drawing in the final video." \
    -i fish_sketch.png -o clownfish.mp4
  ```

---

### 3.3 First and Last Frame Transition Interpolation

Provide two images via `-i` (the 1st is the start frame, the 2nd is the end frame) to synthesize a smooth transitional sequence.
- **Example**:
  ```bash
  uv run scripts/genvideo.py \
    "A smooth cinematic camera transition from a lush green summer forest at sunrise to a snow-covered winter forest under a starry night sky." \
    -i forest_summer.jpg -i forest_winter.jpg -a 16:9 -r 1080p -o season_morph.mp4
  ```

---

### 3.4 Subject Reference Generation

Supply multiple reference images to maintain identity and generate a coherent interaction.
- **Example**:
  ```bash
  # Provide specific cat image and specific yarn ball image
  uv run scripts/genvideo.py \
    "A cat playfully batting at a ball of yarn across a hardwood floor." \
    -i cat_ref.png -i yarn_ref.png -o cat_playing.mp4
  ```

---

### 3.5 Conversational Multi-Turn Video Editing (Stateful Editing)

Edit generated videos sequentially using `--previous-id`.
- **Golden Rule**: Keep edit prompts concise! State only what changes and append `"Keep everything else the same"`.
- **Step-by-Step Workflow**:
  1. **Turn 1 (Initial Generation)**:
     ```bash
     uv run scripts/genvideo.py \
       "A woman playing violin outdoors on a sunny green meadow." \
       -o turn1_violin.mp4
     ```
     *(Terminal prints: `Interaction ID: v1_video_12345...`)*
  2. **Turn 2 (Selective Object Edit)**:
     ```bash
     uv run scripts/genvideo.py \
       "Make the violin invisible. Keep everything else the same." \
       --previous-id "v1_video_12345..." -o turn2_invisible_violin.mp4
     ```
  3. **Turn 3 (Atmosphere & Lighting Edit)**:
     ```bash
     uv run scripts/genvideo.py \
       "Change the lighting from sunny afternoon to twilight with gentle fireflies. Keep everything else the same." \
       --previous-id "v1_video_step2..." -o turn3_twilight.mp4
     ```

---

### 3.6 Editing Uploaded Custom Videos

Upload a local video file (`-v, --video`) to apply transformation effects.
- **Constraint**: Uploaded video length must be **10 seconds or less**.
- **Example**:
  ```bash
  uv run scripts/genvideo.py \
    "When the person touches the mirror, make the mirror ripple like liquid and their arm turn into reflective chrome." \
    -v original_clip.mp4 -o edited_mirror.mp4
  ```

---

### 3.7 Temporal Video Extension (Clip Continuation)

Append a seamless 3–10 second continuation to the tail end of an existing clip (`-v` or `--previous-id`).
- **Example (Scene Continuation)**:
  ```bash
  uv run scripts/genvideo.py \
    "Extend this video: continue the scene as the camera pans up to reveal starry constellations in the night sky." \
    -v clip.mp4 --task extend -o clip_extended.mp4
  ```
- **Example (Extending with Reference Media)**:
  ```bash
  uv run scripts/genvideo.py \
    "Extend this video: have the character shown in the reference image enter the scene from the right and wave." \
    -v clip.mp4 -i character.png --task extend -o clip_extended_character.mp4
  ```

---

### 3.8 Handling Large Videos with URI Delivery: `--delivery uri`

For videos larger than 4MB or when requesting `1080p` / `4k` upscaling, pass `--delivery uri`. The script automatically polls the Google Files API until processing completes and downloads the file.
- **Example**:
  ```bash
  uv run scripts/genvideo.py \
    "Hyper-realistic underwater 4k drone shot of a giant blue whale breaching surface in crystal clear ocean." \
    -r 4k --delivery uri -o whale_4k.mp4
  ```

---

## 4. Prompt Engineering & Audio Design Strategies

### 4.1 Camera & Cinematic Terms
- `Continuous unbroken handheld shot`
- `Low-angle dynamic tracking shot`
- `Smooth slow-motion 360-degree orbital pan`
- `Wide-angle establishing shot`
- `Macro close-up with shallow depth of field`

### 4.2 Integrated Sound Design
Gemini Omni Flash automatically generates synchronous ambient audio and sound effects. Specify audio requirements at the end of the prompt:
- `"Sound design: Roaring ocean waves crashing against rocks, distant wind gust, no dialogue."`
- `"Sound design: Futuristic magnetic engine hum, soft electric beeps, no background music."`

### 4.3 Concise Editing Prompts Comparison
- ❌ **Overly Complex (High Drift Risk)**: `In the video of the man sitting on the sofa, please add a small black cat that runs from the right side of the screen, jumps onto his lap, and then he starts to stroke its head while looking down.`
- ✅ **Concise & Direct (Recommended)**: `Add a small black cat jumping onto his lap; he begins to pet it. Keep everything else the same.`

---

## 5. Constraints & Limitations

1. **Uploaded Video Length**: Custom input videos for editing or extension must be 10 seconds or less.
2. **Extension Direction**: Video extension only supports appending to the end of a clip; prepending or inserting into the middle is not supported.
3. **Dialogue Constraints**: Adding new spoken dialogue to uploaded talking-head videos is not supported. Multi-turn generated videos support conversational speech extension via `--previous-id`.
4. **Reference Clips**: Video references support up to 3 clips (maximum 3 seconds each).
