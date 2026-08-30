# Nano Banana Image Generation & Editing Guide (`genimage.py`)

`scripts/genimage.py` provides a unified interface for Google's **Nano Banana** native multimodal image generation models via the Gemini Interactions API. It supports text-to-image generation, multi-image composition, conversational sequential editing, inpainting (semantic masking), style transfer, Google Search & Image Search Grounding, up to 4K resolution output, and video-to-image generation.

---

## 1. Supported Models & Model Selection

| Model Name | Model ID (`-m`) | Characteristics & Recommended Workflows |
| :--- | :--- | :--- |
| **Nano Banana 2** *(Default)* | `gemini-3.1-flash-image` | **Workhorse Model**: Best overall intelligence-to-latency/cost balance. Supports up to 4K resolution, mixes up to 14 reference images, Google Search & Image Search Grounding, and Video-to-Image. |
| **Nano Banana 2 Lite** | `gemini-3.1-flash-lite-image` | **Ultra-Fast & Cost-Effective**: Engineered for scale and speed. Optimized for single-turn high-volume generation. Not optimized for multi-turn sequential editing. |
| **Nano Banana Pro** | `gemini-3-pro-image` | **Professional Asset Production**: Utilizes advanced reasoning ("Thinking" process), excels at complex instructions, maintains brand consistency, and renders high-fidelity typography and interleaved layouts. |
| **Nano Banana** *(Legacy)* | `gemini-2.5-flash-image` | **Legacy**: Generates images at fixed 1024px resolution. Recommended to migrate to Nano Banana 2 or 2 Lite. |

---

## 2. Command-Line Options Reference

```bash
uv run scripts/genimage.py "PROMPT" [OPTIONS]
```

| Flag / Option | Short Alias | Default | Description |
| :--- | :--- | :--- | :--- |
| `prompt` | Positional | `""` | Text prompt for image generation or editing (ignored if `-f` or `--stdin` is used). |
| `-f, --file` | `--file` | `None` | Read prompt from a text file (recommended for long/complex prompts). |
| `--stdin` | `--stdin` | `False` | Read prompt from standard input (stdin). |
| `-m, --model` | `--model` | `gemini-3.1-flash-image` | Model ID (`gemini-3.1-flash-image`, `gemini-3.1-flash-lite-image`, `gemini-3-pro-image`, `gemini-2.5-flash-image`). |
| `-o, --output` | `--output` | `output.jpg` | Output image path (supports `.jpg`, `.png`, `.webp`). Automatically indexes multiple images if produced. |
| `-t, --text-output`| `--text-output` | `None` | Save conversational text explanation or metadata to a file instead of stdout. |
| `-a, --aspect-ratio`| `--aspect-ratio`| `None` (1:1 default) | Aspect ratio: `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`. |
| `-s, --size` | `--image-size` | `None` (1K default) | Output resolution size: `512px` (or `0.5K`), `1K`, `2K`, `4K` (must use uppercase 'K'). |
| `-i, --image` | `--image` | `[]` | Reference image path(s) for editing, masking, or composition. Can be passed multiple times (up to 14 images). |
| `--video` | `--video` | `None` | Local video file path or YouTube URL for Video-to-Image poster/keyframe extraction. |
| `--previous-id`| `--previous-interaction-id` | `None` | Previous interaction ID for multi-turn sequential editing without re-uploading source media. |
| `--search` | `--grounding` | `False` | Enable Grounding with Google Search for real-time web facts. |
| `--image-search` | `--image-search` | `False` | Enable Google Image Search Grounding alongside Web Search (Gemini 3.1 Flash Image only). |
| `--thinking-level`| `--thinking-level` | `None` (minimal) | Control reasoning depth for Gemini 3.1 Flash Image: `minimal` or `high`. |
| `--save-thoughts`| `--save-thoughts` | `False` | Save intermediate reasoning steps and thought images to disk. |
| `--retry` | `--retry` | `3` | Maximum automatic retries on transient server/network errors. |

---

## 3. Resolution & Aspect Ratio Specification

### 3.1 Gemini 3.1 Flash Image Dimensions Table
| Aspect Ratio | 512px (0.5K) | 1K Resolution | 2K Resolution | 4K Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **1:1** | 512×512 | 1024×1024 | 2048×2048 | 4096×4096 |
| **16:9** | 688×384 | 1376×768 | 2752×1536 | 5504×3072 |
| **9:16** | 384×688 | 768×1376 | 1536×2752 | 3072×5504 |
| **4:3** | 600×448 | 1200×896 | 2400×1792 | 4800×3584 |
| **3:4** | 448×600 | 896×1200 | 1792×2400 | 3584×4800 |
| **3:2** | 632×424 | 1264×848 | 2528×1696 | 5056×3392 |
| **2:3** | 424×632 | 848×1264 | 1696×2528 | 3392×5056 |
| **21:9** | 792×168 | 1584×672 | 3168×1344 | 6336×2688 |
| **1:4 / 4:1** | 256×1024 / 1024×256 | 512×2048 / 2048×512 | 1024×4096 / 4096×1024 | 2048×8192 / 8192×2048 |
| **1:8 / 8:1** | 192×1536 / 1536×192 | 384×3072 / 3072×384 | 768×6144 / 6144×768 | 1536×12288 / 12288×1536 |

---

## 4. Prompt Engineering Templates & Examples

### 4.1 Photorealistic Scenes
- **Formula**: `[Shot Type & Angle] + [Subject Description] + [Setting/Environment] + [Lighting & Atmosphere] + [Lens & Technical Quality]`
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "A photorealistic wide-angle shot of a vibrant coral reef teeming with tropical fish. Crystal-clear turquoise water with sunbeams filtering down from the surface, illuminating a sea turtle gliding gracefully over the coral. Shot from a low perspective with a wide-angle lens. 8k resolution, cinematic lighting." \
    -a 16:9 -s 2K -o coral_reef.jpg
  ```

### 4.2 Stylized Illustrations & Stickers
- **Formula**: `[Art Style] + [Subject & Action/Accessories] + [Visual Characteristics (outlines, shading, palette)] + [Background Preference]`
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat. It's munching on a green bamboo leaf. The design features bold, clean outlines, simple cel-shading, and a vibrant color palette. Pure white background." \
    -a 1:1 -s 1K -o red_panda_sticker.png
  ```

### 4.3 Accurate Text Rendering & Logo Design
- **Formula**: Explicitly quote the exact text `with the text "..."`, specify font characteristics (e.g. `clean, bold sans-serif`), layout geometry, and brand concept.
- **Recommended Model**: `gemini-3-pro-image`
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'. The text 'The Daily Grind' must be rendered in a clean, bold, sans-serif font. The color scheme is black and white. Put the logo in a circle. Cleverly integrate a coffee bean into the typography." \
    -m gemini-3-pro-image -a 1:1 -s 2K -o daily_grind_logo.png
  ```

### 4.4 Commercial Photography & Product Mockups
- **Formula**: `[Product Material & Color] + [Surface/Podium & Setting] + [Studio Lighting Setup (three-point softbox)] + [Camera Angle & Focus Key Detail]`
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug in matte black, presented on a polished concrete surface. The lighting is a three-point softbox setup creating soft, diffused highlights. Slightly elevated 45-degree angle. Ultra-realistic, sharp focus on steam rising." \
    -a 1:1 -s 2K -o mug_mockup.jpg
  ```

### 4.5 Minimalist & Negative Space Design
- **Technique**: Define the exact coordinate/anchor of the subject (`bottom-right`, `top-left`) and state the vast canvas for text overlay.
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "A minimalist composition featuring a single, delicate red maple leaf positioned in the bottom-right of the frame. The background is a vast, empty off-white canvas, creating significant negative space for text overlay. Soft, diffused lighting." \
    -a 16:9 -s 2K -o minimalist_banner.png
  ```

### 4.6 Adding/Removing Elements & Inpainting (Semantic Masking)
- **Technique**: Start with `"Using the provided image..."`, specify the exact modification, and emphasize `"Keep everything else exactly the same, preserving lighting and composition"`.
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "Using the provided image of a living room, change only the blue sofa to be a vintage, brown leather chesterfield sofa. Keep the rest of the room, including the pillows on the sofa and ambient lighting, unchanged." \
    -i living_room.png -o living_room_edited.png
  ```

### 4.7 Artistic Style Transfer
- **Technique**: Retain the original composition while prescribing the target artist's medium, brushstrokes, and palette.
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "Transform the provided photograph of a modern city street at night into the artistic style of Vincent van Gogh's 'Starry Night'. Preserve the original composition of buildings and cars, but render all elements with swirling, impasto brushstrokes and deep blues with bright yellows." \
    -i city.jpg -o city_starry.jpg
  ```

### 4.8 Advanced Composition: Combining Multiple Reference Images (Up to 14 Images)
- **Reference Image Budgets**:
  - `gemini-3.1-flash-image`: Up to 10 high-fidelity objects + up to 4 consistent characters.
  - `gemini-3-pro-image`: Up to 6 objects + up to 5 characters + up to 3 style references.
- **Example**:
  ```bash
  # Take the dress from image 1 and let the model from image 2 wear it
  uv run scripts/genimage.py \
    "Create a professional e-commerce fashion photo. Take the blue floral dress from the first image and let the woman from the second image wear it. Generate a realistic, full-body shot of the woman wearing the dress with outdoor lighting." \
    -i dress.png -i model.png -a 3:4 -s 2K -o fashion_ecommerce.jpg
  ```

### 4.9 High-Fidelity Feature Preservation
- **Technique**: Provide granular descriptions of unchanged features (e.g. facial likeness) to anchor consistency.
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "Take the first image of the woman with brown hair, blue eyes, and neutral expression. Add the logo from the second image onto her black t-shirt. Ensure the woman's face and facial features remain completely unchanged. The logo should naturally fold along the shirt fabric wrinkles." \
    -i woman.png -i logo.png -o woman_branded.png
  ```

### 4.10 Rough Sketch to Polished Concept (Bring Something to Life)
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "Turn this rough pencil sketch of a futuristic sports car into a polished photograph of the finished concept car in a modern showroom. Keep the sleek lines and low profile from the sketch but add metallic blue paint and glowing LED rims." \
    -i car_sketch.png -o concept_car.jpg
  ```

### 4.11 Character Consistency: 360° Turnaround View
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "A studio portrait of this man against white background, in profile looking right, maintaining exact facial resemblance, glasses, and hairstyle." \
    -i man_front.jpg -o man_profile_right.jpg
  ```

### 4.12 Real-Time Grounding with Google Search & Image Search
- **Example**:
  ```bash
  # Grounding with real-time web & image search
  uv run scripts/genimage.py \
    "A detailed botanical scientific painting of a Timareta butterfly resting on a native Amazonian orchid." \
    --search --image-search -a 16:9 -s 2K -o butterfly.png
  ```

### 4.13 Video-to-Image Generation (Poster & Keyframe Extraction)
- **Example**:
  ```bash
  uv run scripts/genimage.py \
    "Generate a cinematic movie poster that captures the climax, key characters, and atmosphere of this video." \
    --video "https://www.youtube.com/watch?v=EXAMPLE_VIDEO" -a 16:9 -s 2K -o video_poster.jpg
  ```

### 4.14 Multi-Turn Conversational Image Editing
- **Turn 1 (Initial Generation)**:
  ```bash
  uv run scripts/genimage.py \
    "Create a vibrant infographic explaining photosynthesis as a kids cookbook recipe." \
    -o infographic.png
  ```
  *(Output displays: `Interaction ID: v1_abc123...`)*
- **Turn 2 (Sequential Modification)**:
  ```bash
  uv run scripts/genimage.py \
    "Update this infographic to be in Spanish. Do not change any other elements of the image." \
    --previous-id "v1_abc123..." -o infographic_spanish.png
  ```

---

## 5. Best Practices & Troubleshooting

1. **Resolution Capitalization**: The `-s` / `--size` argument requires an uppercase 'K' (`1K`, `2K`, `4K`, `512px`). Lowercase `1k` will be rejected by the API schema.
2. **Use Positive Semantic Descriptions**: Instead of negative prompts like `"no cars, no people"`, write `"an empty, deserted city street with clean asphalt and clear sidewalks"`.
3. **Step-by-Step Spatial Prompting**: For complex multi-object scenes, organize descriptions spatially: `"First, in the background... Next, in the midground... Finally, in the foreground..."`.
