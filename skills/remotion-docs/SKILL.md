---
name: remotion-docs
description: Local knowledge base mirroring the official Remotion documentation (React-based video generation framework).
metadata:
  author: Ecat
  version: "4.0.57"
---

# Remotion Documentation

This skill provides the local documentation and guides for Remotion, a framework that allows you to build videos and animations programmatically using React, TypeScript, HTML, and CSS.

## ⚠️ Important Note on References

Because this documentation is a local mirror, internal links found within the text (often written as `/docs/xxx`) may not map exactly to file paths. When you encounter a reference link:
1. **Try adding `.md` to it**: For example, `/docs/composition` maps to `docs/composition.md`.
2. **Check for a directory index**: If it is a directory reference (e.g., `/docs/lambda`), look for `docs/lambda.md` or `docs/lambda/index.md`.
3. **Check subdirectories**: If a file is not in the root `docs/` folder, check if it resides in a subdirectory (e.g., `docs/audio/trimming.md` or `docs/troubleshooting/player-flicker.md`).

> **Note on directories without `index.md`**: Some package directories do not have an `index.md` entry point. In these cases, use the following alternatives:
>
> | Directory | Entry Point |
> |---|---|
> | `docs/effects/` | `docs/effects.md` (overview at root) or `docs/effects/api.md` |
> | `docs/skia/` | `docs/skia/enable-skia.md` |
> | `docs/google-fonts/` | `docs/google-fonts/load-font.md` |
> | `docs/tailwind-v4/` | `docs/tailwind-v4/overview.md` |
> | `docs/cli/` | No index — browse individual files like `docs/cli/render.md`, `docs/cli/still.md` |
> | `docs/studio/` | No index — browse individual files like `docs/studio/api.md`, `docs/studio/shortcuts.md` |
> | `docs/lottie/` | `docs/lottie/lottie.md` |
> | `docs/renderer/` | `docs/renderer.md` (overview at root) or individual files like `docs/renderer/render-media.md` |

---

## 📚 Documentation Directory

### 🚀 Getting Started & Fundamentals
- [Installation / Creating a Project](docs/index.md) - How to start a new Remotion project.
- [The Fundamentals](docs/the-fundamentals.md) - React video components, composition properties, rendering.
- [Compositions](docs/composition.md) - Registering components, width, height, duration, fps.
- [Sequences](docs/sequence.md) & [Series](docs/series.md) - Time shifting, trimming, and playing items sequentially.
- [Assets](docs/assets.md) - Importing and referencing static assets.
- [Animation Guide](docs/animating-properties.md) - Easing, spring, and interpolation.
- [Fonts](docs/fonts.md) - Loading and using custom fonts.

### 🧠 Core APIs & Hooks
- [API Overview](docs/api.md) - High-level API overview.
- [useVideoConfig](docs/use-video-config.md) & [useCurrentFrame](docs/use-current-frame.md) - Accessing current frame and config.
- [spring](docs/spring.md) & [interpolate](docs/interpolate.md) - Animation drivers.
- [interpolateColors](docs/interpolate-colors.md) - Color interpolation.
- [Easing](docs/easing.md) - Easing functions for animations.
- [delayRender](docs/delay-render.md) / [useDelayRender](docs/use-delay-render.md) - Handling asynchronous resource loading.
- [Loop](docs/loop.md) & [Freeze](docs/freeze.md) - Looping and freezing frames.
- [random](docs/random.md) - Deterministic random number generation.
- [@remotion/zod-types](docs/zod-types/index.md) - Defining parameter schemas with Zod.

### 🎥 Media & Video
- [Video Tags](docs/video-tags.md) - Working with `<video>` and `<Audio>` elements.
- [Using Audio](docs/using-audio.md) - Mixing audio, visualization, and volume adjustment.
- [OffthreadVideo](docs/offthreadvideo.md) - High-performance video rendering.
- [Animated Image](docs/animatedimage.md) & [Canvas Image](docs/canvasimage.md) - Rendering GIFs/APNGs and raw canvas content.
- [Encoding & Codecs](docs/encoding.md) - Output formats, codecs, and quality settings.
- [@remotion/media-utils](docs/media-utils/index.md) - Waveform extraction, audio processing.

### ✨ Effects & Visual Design
- [@remotion/effects](docs/effects.md) - Visual effects (blur, glow, grayscale, etc.) for canvas-based components.
- [@remotion/transitions](docs/transitions/index.md) - High-performance transitions (fade, slide, zoom, etc.).
- [@remotion/shapes](docs/shapes/index.md) & [@remotion/paths](docs/paths/index.md) - SVG shapes and path manipulation.
- [@remotion/noise](docs/noise/index.md) - Procedural noise generation.
- [@remotion/skia](docs/skia/enable-skia.md) - Rendering Skia graphics in Remotion.

### 🎨 Styling & Fonts
- [Tailwind CSS v3](docs/tailwind.md) / [Tailwind CSS v4](docs/tailwind-v4/overview.md) - Integrating Tailwind CSS.
- [@remotion/google-fonts](docs/google-fonts/load-font.md) - Dynamic Google Fonts loader.

### 🌐 Player & Browser Rendering
- [@remotion/player](docs/player.md) - Embedding Remotion videos into React/NextJS/HTML pages (see also `docs/player/` for detailed API).
- [@remotion/web-renderer](docs/web-renderer/index.md) - Rendering videos purely in the browser.
- [@remotion/webcodecs](docs/webcodecs/index.md) - Fast encoding and decoding using WebCodecs API.
- [@remotion/media-parser](docs/media-parser/index.md) - Advanced media parsing in browser and node.
- [@remotion/whisper-web](docs/whisper-web/index.md) - Browser-based audio transcription using Whisper.

### ☁️ Server-Side & Cloud Rendering
- [@remotion/renderer](docs/renderer.md) - Render and export videos programmatically via NodeJS (see also `docs/renderer/` for individual APIs).
- [Server-Side Rendering (SSR)](docs/ssr.md) & [SSR Node](docs/ssr-node.md) - Setting up SSR in NodeJS environments.
- [AWS Lambda Integration](docs/lambda.md) - Distributing rendering across Lambda functions (see also `docs/lambda/` for detailed APIs).
- [Google Cloud Run Integration](docs/cloudrun.md) - Hosting render endpoints on Cloud Run.
- [Vercel Integration](docs/vercel.md) - Deploying and rendering on Vercel.
- [Docker](docs/docker.md) - Deploying Remotion renderer inside containers.

### 💻 Tooling & Ecosystem
- [CLI Reference](docs/cli/render.md) - Command-line interface (browse `docs/cli/` for all commands).
- [Remotion Studio](docs/studio/api.md) - Interactive development preview and editor (browse `docs/studio/` for features).
- [Configuration](docs/config.md) - Bundle, Chromium, concurrency, and output defaults.
- [Captions & Transcriptions](docs/captions/index.md) - Generating, styling, and syncing subtitles.
- [3D with Three.js](docs/three.md) - Using Three.js inside Remotion.
- [Lottie](docs/lottie/lottie.md) & [Rive](docs/rive/index.md) - Integrating Lottie and Rive animations.
- [GIF](docs/gif/index.md) - Rendering GIFs in Remotion.
- [Testing](docs/testing.md) - Testing Remotion compositions.

### 💡 Advanced Guides & Troubleshooting
- [Data Fetching](docs/data-fetching.md) - Fetching API data dynamically inside compositions.
- [Parameterized Rendering](docs/parameterized-rendering.md) - Customizing videos at render time using input props.
- [Dynamic Metadata](docs/dynamic-metadata.md) - Calculating composition metadata dynamically.
- [Environment Variables](docs/env-variables.md) - Using environment variables in Remotion.
- [Performance Optimization](docs/performance.md) - Speeding up renders.
- [Chromium Flags](docs/chromium-flags.md) - Browser flags for rendering behavior.
- [Troubleshooting Common Issues](docs/troubleshooting/) - Player flicker, failed renders, font loading, etc.
- [Migration Guides](docs/upgrading.md) - Upgrading major versions ([2.0](docs/2-0-migration.md), [3.0](docs/3-0-migration.md), [4.0](docs/4-0-migration.md), [5.0](docs/5-0-migration.md)).
