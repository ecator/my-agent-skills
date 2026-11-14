---
name: acp-python-sdk-docs
description: Local knowledge base mirroring the official Agent Client Protocol (ACP) Python SDK (agent-client-protocol) documentation and runnable examples. Use when building, integrating, debugging, or migrating ACP-compatible AI agents and clients in Python over stdio, Streamable HTTP (HTTP/2 + SSE), or WebSocket transports, working with acp.schema Pydantic models, acp.contrib helpers (SessionAccumulator, ToolCallTracker, PermissionBroker), or experimental Protocol v2 (acp.experimental.v2).
metadata:
  author: Ecat
  version: "1.0.0"
  source: https://github.com/agentclientprotocol/python-sdk
---

# Agent Client Protocol (ACP) Python SDK Documentation

This skill provides the official documentation, migration guides, and runnable example scripts for the **Agent Client Protocol (ACP) Python SDK** (`agent-client-protocol`), enabling Python applications to implement ACP-compatible AI agents and clients without rebuilding JSON-RPC transports or schema models.

---

## ⚠️ Important Note on Reference Links & Path Mapping

This skill directory (`skills/acp-python-sdk-docs`) is a local mirror of the official [`agentclientprotocol/python-sdk`](https://github.com/agentclientprotocol/python-sdk) repository. When reading the Markdown files in `docs/`, resolve reference links using these rules:

1. **GitHub Repository Links (`blob/main/` & `tree/main/`)**:
   Any link starting with `https://github.com/agentclientprotocol/python-sdk/blob/main/` or `https://github.com/agentclientprotocol/python-sdk/tree/main/` maps directly to the root of this skill directory (`skills/acp-python-sdk-docs/`).
   - The local [`examples/`](examples/) directory is a direct mirror of the GitHub repository's `examples/` folder:
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/echo_agent.py` ➔ [`examples/echo_agent.py`](examples/echo_agent.py)
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/agent.py` ➔ [`examples/agent.py`](examples/agent.py)
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/client.py` ➔ [`examples/client.py`](examples/client.py)
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/duet.py` ➔ [`examples/duet.py`](examples/duet.py)
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/gemini.py` ➔ [`examples/gemini.py`](examples/gemini.py)
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/http_server.py` ➔ [`examples/http_server.py`](examples/http_server.py)
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/http_client.py` ➔ [`examples/http_client.py`](examples/http_client.py)
     - `https://github.com/agentclientprotocol/python-sdk/blob/main/examples/ws_client.py` ➔ [`examples/ws_client.py`](examples/ws_client.py)
     - `https://github.com/agentclientprotocol/python-sdk/tree/main/examples` ➔ [`examples/`](examples/)
2. **Relative Documentation Links**:
   Links within `docs/*.md` such as `[Quickstart](quickstart.md)`, `[Use Cases](use-cases.md)`, or `[contrib.md](contrib.md)` are relative to the `docs/` directory (e.g., `docs/quickstart.md`, `docs/use-cases.md`, `docs/contrib.md`).
3. **Unmirrored Internal SDK Source Files (`src/acp/`, `tests/`, `schema/`)**:
   Mentions of internal repository paths like `src/acp/interfaces.py`, `src/acp/schema.py`, `src/acp/core.py`, or `tests/` refer to the upstream SDK source code and are not included in this documentation mirror. Use `docs/` and `examples/` for API signatures and usage patterns.

---

## 📦 Package & Environment Overview

- **PyPI Package**: `agent-client-protocol`
- **Import Root**: `acp`
- **Python Requirement**: Python `>=3.10` (3.10–3.14+)
- **Bundled Protocol Schemas**:
  - **Stable v1**: `schema-v1.23.0` (`acp`, `acp.schema`, `acp.interfaces`)
  - **Experimental v2**: `schema-v2.0.0-alpha.5` (`acp.experimental.v2`)

```bash
# Core SDK (stdio transport + Pydantic schema models)
pip install agent-client-protocol
# or
uv add agent-client-protocol

# Optional web transports (Streamable HTTP over HTTP/2 + SSE, WebSocket, Starlette ASGI server)
pip install "agent-client-protocol[http]"
```

---

## 📚 Documentation Index (`docs/`)

| Document | Topic | Key Contents |
|---|---|---|
| [`docs/index.md`](docs/index.md) | **Overview & Architecture** | High-level overview of ACP, SDK building blocks (`acp.schema`, `acp.agent`/`acp.client`, `acp.contrib`), and navigation links. |
| [`docs/quickstart.md`](docs/quickstart.md) | **Quickstart & v1 Guide** | Installation, running the echo agent, Zed `settings.json` wiring, `spawn_agent_process`, subclassing `acp.Agent`, session notices (`SessionUpdateNotice`), additional v1 methods (`session/delete`, `providers/*`, `logout`, `mcp/*`, `nes/*`, `document/*`), request cancellation (`$/cancel_request`), `@param_model` routing, and Gemini CLI bridge. |
| [`docs/web-transport.md`](docs/web-transport.md) | **Web Transports (HTTP & WS)** | Experimental remote transports (`agent-client-protocol[http]`): Streamable HTTP (`create_http_stream`) and WebSocket (`create_websocket_stream`), Starlette server (`create_asgi_app`), sub-app mounting with lifespan, `load_session` / `resume_session` SSE routing, and HTTP/2 server setup with Hypercorn. |
| [`docs/contrib.md`](docs/contrib.md) | **Experimental Contrib Helpers** | Production utilities in `acp.contrib`: `SessionAccumulator` (`acp.contrib.session_state`), `ToolCallTracker` (`acp.contrib.tool_calls`), and `PermissionBroker` (`acp.contrib.permissions`). |
| [`docs/experimental-v2.md`](docs/experimental-v2.md) | **Experimental Protocol v2** | Draft v2 bindings (`acp.experimental.v2`, `schema-v2.0.0-alpha.5`), v2 `Agent`/`Client` handlers, non-blocking `prompt` with `message_id`, session notices, patch semantics (`None` vs omitted), and serving v1+v2 simultaneously via `AgentProtocolRouter`. |
| [`docs/use-cases.md`](docs/use-cases.md) | **Real-World Use Cases** | Production agents and clients built with the SDK (kimi-cli, Mini-Agent, OpenHands-CLI, fast-agent, agent-client-kernel, simple-acp-client). |
| [`docs/migration-guide-0.11.md`](docs/migration-guide-0.11.md) | **Migration Guide: 0.11** | Upgrading to 0.11 (`schema-v1.16.0`): `session_id`-first parameter ordering on `Client` and `Agent`, removal of `PromptRequest.message_id` and `set_session_model`, elicitation support (`create_elicitation`, `complete_elicitation`), `AgentPlanContentUpdate` / `AgentPlanRemovedUpdate`, and `AcpMcpServer`. |
| [`docs/migration-guide-0.8.md`](docs/migration-guide-0.8.md) | **Migration Guide: 0.8** | Upgrading to 0.8 (`schema-v0.10.8`): removal of `TerminalHandle` (use `CreateTerminalResponse.terminal_id`), `SessionInfoUpdate`, and 50MB default `stdio_buffer_limit_bytes`. |
| [`docs/migration-guide-0.7.md`](docs/migration-guide-0.7.md) | **Migration Guide: 0.7** | Upgrading to 0.7: `snake_case` Pydantic fields (`by_alias=True` when dumping), `run_agent` / `connect_to_agent` replacing manual `AgentSideConnection` / `ClientSideConnection`, and expanded method signatures. |
| [`docs/releasing.md`](docs/releasing.md) | **Releasing & Schema Sync** | Regenerating schema bindings (`ACP_SCHEMA_VERSION=... make gen-all`), running `make check` / `make test`, and publishing releases. |

---

## 💻 Mirrored Code Examples (`examples/`)

All upstream example scripts are mirrored locally under [`examples/`](examples/):

| File | Role / Transport | Description & Key APIs Demonstrated |
|---|---|---|
| [`examples/echo_agent.py`](examples/echo_agent.py) | Minimal Agent (stdio) | Smallest streaming agent: subclasses `Agent`, captures `Client` connection in `on_connect`, handles `initialize`, `new_session`, and streams `AgentMessageChunk` via `self._conn.session_update()` inside `prompt()`, launched with `run_agent()`. |
| [`examples/agent.py`](examples/agent.py) | Full-Featured Agent (stdio) | Implements `initialize` (with `AgentCapabilities` and `Implementation`), `authenticate`, `new_session`, `load_session`, `set_session_mode`, `prompt`, `cancel`, `ext_method`, and `ext_notification`. |
| [`examples/client.py`](examples/client.py) | Interactive Client (stdio) | Spawns an agent subprocess, wires stdio with `connect_to_agent()`, implements `Client` callbacks (`request_permission`, `read_text_file`, `write_text_file`, terminal methods, `create_elicitation`, `complete_elicitation`, `session_update`), and runs an interactive console prompt loop. |
| [`examples/duet.py`](examples/duet.py) | Client + Agent Duet (stdio) | Uses `spawn_agent_process(client, sys.executable, str(agent_path))` context manager to launch [`examples/agent.py`](examples/agent.py) and drive it interactively with `ExampleClient` from [`examples/client.py`](examples/client.py). |
| [`examples/gemini.py`](examples/gemini.py) | Gemini CLI Bridge (stdio) | Complete ACP client driving `gemini --acp` (or `--experimental-acp`): implements file read/write (`FileSystemCapabilities`), terminal callbacks, interactive or `--yolo` auto-approval permission flows (`AllowedOutcome` / `DeniedOutcome`), and `:cancel` handling. |
| [`examples/http_server.py`](examples/http_server.py) | Remote Agent Server (HTTP/2 + WS) | Wraps an `EchoAgent` in a Starlette ASGI app using `create_asgi_app(lambda conn: EchoAgent())` and serves both Streamable HTTP and WebSocket on `http://localhost:8000/acp` via Hypercorn with HTTP/2 enabled (`alpn_protocols = ["h2", "http/1.1"]`). |
| [`examples/http_client.py`](examples/http_client.py) | Remote Client (Streamable HTTP) | Connects to a remote ACP server using `create_http_stream("http://localhost:8000/acp")` and `connect_to_agent()`. |
| [`examples/ws_client.py`](examples/ws_client.py) | Remote Client (WebSocket) | Connects to a remote ACP server using `await create_websocket_stream("ws://localhost:8000/acp")` and `connect_to_agent()`. |

---

## 🚀 Core Usage Patterns & Quick Reference

### 1. Implementing a Streaming ACP Agent (stdio)

Subclass `acp.Agent`, store the peer `Client` connection in `on_connect`, stream updates via `session_update`, and start the stdio loop with `run_agent()`:

```python
import asyncio
from typing import Any
from uuid import uuid4

from acp import Agent, InitializeResponse, NewSessionResponse, PromptResponse, run_agent
from acp.interfaces import Client
from acp.schema import AgentMessageChunk, ClientCapabilities, Implementation, TextContentBlock


class MyAgent(Agent):
    _conn: Client

    def on_connect(self, conn: Client) -> None:
        self._conn = conn

    async def initialize(
        self,
        protocol_version: int,
        client_capabilities: ClientCapabilities | None = None,
        client_info: Implementation | None = None,
        **kwargs: Any,
    ) -> InitializeResponse:
        return InitializeResponse(protocol_version=protocol_version)

    async def new_session(self, cwd: str, **kwargs: Any) -> NewSessionResponse:
        return NewSessionResponse(session_id=uuid4().hex)

    async def prompt(self, session_id: str, prompt: list[Any], **kwargs: Any) -> PromptResponse:
        await self._conn.session_update(
            session_id=session_id,
            update=AgentMessageChunk(content=TextContentBlock(text="Processing prompt...")),
        )
        return PromptResponse(stop_reason="end_turn")


if __name__ == "__main__":
    asyncio.run(run_agent(MyAgent()))
```

### 2. Programmatically Spawning & Driving an Agent from Python

Use `spawn_agent_process` (or `spawn_client_process`) to manage child process lifecycle and stdio framing automatically:

```python
import asyncio
import sys
from typing import Any

from acp import PROTOCOL_VERSION, spawn_agent_process
from acp.interfaces import Client
from acp.schema import TextContentBlock


class SimpleClient(Client):
    async def request_permission(self, session_id: str, tool_call: Any, options: Any, **kwargs: Any) -> Any:
        return {"outcome": {"outcome": "cancelled"}}

    async def session_update(self, session_id: str, update: Any, **kwargs: Any) -> None:
        print("update:", session_id, update)


async def main() -> None:
    async with spawn_agent_process(SimpleClient(), sys.executable, "examples/echo_agent.py") as (conn, _proc):
        await conn.initialize(protocol_version=PROTOCOL_VERSION)
        session = await conn.new_session(cwd=".", mcp_servers=[])
        await conn.prompt(
            session_id=session.session_id,
            prompt=[TextContentBlock(text="Hello from Python client!")],
        )


asyncio.run(main())
```

### 3. Remote Web Transports (Streamable HTTP & WebSocket)

Requires `pip install "agent-client-protocol[http]"`. See [`docs/web-transport.md`](docs/web-transport.md) for full details.

- **Server (`acp.http.asgi.create_asgi_app`)**:
  Creates a Starlette application serving both Streamable HTTP (`POST`/`GET` SSE/`DELETE`) and WebSocket upgrades at `/acp` (configurable via `path="/rpc"`).
  > ⚠️ **HTTP/2 Requirement**: Streamable HTTP requires an HTTP/2-capable ASGI server such as **Hypercorn**, Daphne, or Granian (Uvicorn only supports WebSocket, not HTTP/2).
- **Client (`acp.http.create_http_stream` / `acp.ws.create_websocket_stream`)**:
  ```python
  from acp import connect_to_agent
  from acp.http import create_http_stream
  from acp.ws import create_websocket_stream

  # Streamable HTTP
  transport = create_http_stream("http://localhost:8000/acp")
  conn = connect_to_agent(my_client, transport)

  # Or WebSocket
  transport = await create_websocket_stream("ws://localhost:8000/acp")
  conn = connect_to_agent(my_client, transport)
  ```

### 4. Additional v1 Protocol Methods & Unstable Opt-In

In `schema-v1.23.0`, `session/delete` (`delete_session`) and `logout` (`logout`) are stable. Unstable methods require `use_unstable_protocol=True` on the receiving connection or `run_agent()`:
- **Agent receivers**: `delete_session` (stable), `logout` (stable), `list_providers`, `set_provider`, `disable_provider`, `start_nes`, `suggest_nes`, `close_nes`, `accept_nes`, `reject_nes`, `did_open`, `did_change`, `did_close`, `did_save`, `did_focus`.
- **Client receivers**: `connect_mcp`, `disconnect_mcp`, `create_elicitation`, `complete_elicitation`.
- **Either peer**: `mcp_message` (request), `notify_mcp` (notification).

See [`docs/quickstart.md`](docs/quickstart.md#additional-v1-protocol-methods) and [`docs/migration-guide-0.11.md`](docs/migration-guide-0.11.md#4-handle-elicitation-if-your-agent-or-client-advertises-it) for handler signatures.

### 5. Experimental Contrib Utilities (`acp.contrib`)

See [`docs/contrib.md`](docs/contrib.md) for stateful helpers:
- **`acp.contrib.session_state.SessionAccumulator`**: Reconciles streamed `SessionNotification` events (`tool_call`, `tool_call_update`, plans, messages) into immutable `SessionSnapshot` Pydantic models with `apply()`, `snapshot()`, and `subscribe()`.
- **`acp.contrib.tool_calls.ToolCallTracker`**: Emits canonical `ToolCallStart` / `ToolCallProgress` updates (`start()`, `progress()`, `append_stream_text()`) and tracks in-memory tool call views.
- **`acp.contrib.permissions.PermissionBroker`**: Wraps `requestPermission` RPCs (`request_for()`) with default Approve / Approve for session / Reject options (`default_permission_options()`), syncing state with `ToolCallTracker`.

### 6. Experimental Protocol v2 & Dual-Version Routing (`acp.experimental`)

See [`docs/experimental-v2.md`](docs/experimental-v2.md) for draft `schema-v2.0.0-alpha.5` support:
- Import `from acp.experimental import v2` for `v2.Agent`, `v2.Client`, `v2.connect_to_agent`, `v2.run_agent`, and `v2.schema`.
- Use `AgentProtocolRouter(v1=lambda conn: V1Agent(conn), v2=lambda conn: V2Agent(conn))` from `acp.experimental` to serve both v1 and v2 clients from a single agent process.
