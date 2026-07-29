---
name: openai-api-docs
description: Comprehensive OpenAI API Documentation. Contains docs for OpenAI GPT models, Whisper, DALL-E, Assistants API, Function Calling, Embeddings, etc.
metadata:
  author: Ecat
  version: "1.0.0"
---

# OpenAI API Documentation

This skill provides comprehensive documentation and guides for integrating OpenAI's models into your applications. OpenAI offers a highly capable AI platform providing industry-leading text, vision, and audio models for a wide variety of tasks.

## ⚠️ Important Note on References

Because this documentation is a local mirror, internal links found within the text may not map exactly to file paths. When you encounter a reference link (e.g., `/docs/quickstart` or `/reference/chat-completions`):

1. **Handle absolute URLs**: If the link is a full URL like `https://developers.openai.com/api/docs/gpts/release-notes.md`, extract the relevant path portion (e.g., `api/docs/gpts/release-notes.md`) and check if it exists locally first.
2. **Try appending `.md`**: Search for `api/docs/quickstart.md` or `api/reference/chat-completions.md`.
3. **Check for an overview**: If the file doesn't exist, the path is likely a directory. Try looking for an `overview.md` inside it (e.g., `api/reference/chat-completions/overview.md`).
4. **Check the base files**: Sometimes top level pages are named similarly, like `api/docs.md` or `api/reference.md`.

## Entry Points & Documentation Index

- **[Quickstart](api/docs/quickstart.md)**: A step-by-step guide to get up and running with the OpenAI API.
- **[Models](api/docs/models.md)**: Overview of OpenAI's models (e.g., GPT-4o, GPT-4 Turbo, GPT-3.5, DALL-E, Whisper).
- **[Concepts](api/docs/concepts.md)**: Core concepts for understanding how to work with the OpenAI API.

### Detailed Directory & Documentation Index

- **[api/docs](api/docs)**: Core developer documentation and guides.
  - **[actions](api/docs/actions)**: Guides for GPT Actions, including data retrieval, authentication, and the actions library.
  - **[assistants](api/docs/assistants)**: Guides for the Assistants API. Includes deep dive, migration guide, and tool specifics (`code-interpreter.md`, `file-search.md`, `function-calling.md`).
  - **[gpts](api/docs/gpts)**: GPT release notes.
  - **[guides](api/docs/guides)**: Comprehensive guides covering:
    - **Modality guides**: Text, Audio, Images/Vision, Video generation with Sora.
    - **Tool guides**: Function calling, Code Interpreter, File Search, Web Search, Computer Use, Local Shell, MCP.
    - **Optimization & Best Practices**: Prompt engineering, Fine-tuning, Cost optimization, Latency optimization, Reasoning best practices.
    - **Agent building**: Agent SDK, Agent Builder, Multi-agent orchestration, ChatKit.
    - **Infrastructure & Deployment**: Batch API, Rate limits, Terraform provider, Private Link, Webhooks.
    - **Realtime API**: WebRTC, WebSocket, SIP, Voice agents, Server-side controls.
  - **[libraries](api/docs/libraries)**: Official SDKs and OpenAI CLI instructions.
  - **[tutorials](api/docs/tutorials)**: Step-by-step tutorials (e.g., meeting minutes, Web QA with embeddings).
  - **Standalone Core Docs**:
    - `quickstart.md`: Developer quickstart.
    - `models.md`: Model catalog and capabilities.
    - `concepts.md`: Key API concepts.
    - `changelog.md`: API and model updates.
    - `deprecations.md`: Deprecated endpoints and replacements.
    - `pricing.md`: Platform pricing details.
    - `bots.md`: OpenAI Crawlers overview.
    - `mcp.md`: Building MCP servers.
- **[api/reference](api/reference)**: Comprehensive API endpoint reference.
  - **[overview.md](api/reference/overview.md)**: API reference overview.
  - **[administration](api/reference/administration)**: Endpoints for managing organizations, users, and billing.
  - **[chat-completions](api/reference/chat-completions)**: Detailed parameters for Chat Completions API.
  - **[realtime-beta](api/reference/realtime-beta)**: Endpoints for the Realtime API.
  - **[responses](api/reference/responses)**: Documentation on API responses format and error codes.
  - **[resources](api/reference/resources)**: Complete endpoint documentation for:
    - Audio (Speech, Transcriptions, Translations, Voices)
    - Assistants & Threads (Messages, Runs, Steps)
    - Batches & Completions
    - Embeddings & Evals
    - Files & Fine Tuning
    - Images & Moderations
    - Uploads & Vector Stores

## Key Capabilities

- **Text Generation (Chat Completions)**: Generate text and code, power chatbots, and perform complex reasoning using models like GPT-4o.
- **Vision**: Understand and analyze images using the vision capabilities of GPT-4o.
- **Audio (Speech-to-Text & Text-to-Speech)**: Transcribe audio using Whisper, or generate lifelike speech from text.
- **Image Generation (DALL-E)**: Generate and edit images from natural language prompts.
- **Embeddings**: Create vector representations of text for search, clustering, and retrieval-augmented generation (RAG).
- **Assistants API**: Build AI assistants with instructions and leverage tools like Code Interpreter and File Search.
- **Function Calling (Tool Use)**: Connect models to external tools and APIs by defining functions they can call.
- **Realtime API**: Build low-latency, multimodal real-time voice and audio applications.
- **Fine-tuning**: Customize OpenAI models with your own data for better performance on specific tasks.

## Getting Started

To make your first API call, you will need an OpenAI account and an API key from the dashboard.

1. Install the official SDK (e.g., Python: `pip install openai` or Node.js: `npm install openai`).
2. Set your API key in your environment variables: `export OPENAI_API_KEY='your-api-key-here'`.
3. Create a client and make a request to the `chat/completions` endpoint.

Review the [Quickstart](api/docs/quickstart.md) for detailed instructions for your preferred programming language.
