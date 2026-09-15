<p align="center">
  <img src="assets/icon-96.png" width="96" height="96" alt="LinkReacher" />
</p>

<h1 align="center">LinkReacher MCP</h1>

<p align="center"><strong>Automated backlink outreach, operated from your AI assistant.</strong></p>

<p align="center">
  Discover linkable pages, find the decision maker to email, draft the ask, run the campaign,
  and triage the replies, all without leaving the chat.
</p>

<p align="center">
  <a href="https://linkreacher.com"><img alt="Website" src="https://img.shields.io/badge/website-linkreacher.com-f2590a?style=flat-square"></a>
  <a href="https://app.linkreacher.com"><img alt="App" src="https://img.shields.io/badge/app-app.linkreacher.com-0ea5e9?style=flat-square"></a>
  <a href="https://linkreacher.com/mcp"><img alt="Docs" src="https://img.shields.io/badge/docs-%2Fmcp-6E56CF?style=flat-square"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square"></a>
</p>

<p align="center">
  <img alt="MCP protocol" src="https://img.shields.io/badge/MCP-2025--06--18-6E56CF?style=flat-square">
  <img alt="Transport" src="https://img.shields.io/badge/transport-streamable--http-0ea5e9?style=flat-square">
  <img alt="Tools" src="https://img.shields.io/badge/tools-81%20(40%20free%20%2F%2041%20Pro)-f59e0b?style=flat-square">
  <img alt="Prompts" src="https://img.shields.io/badge/prompts-4-8b5cf6?style=flat-square">
  <img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-2ea44f?style=flat-square">
</p>

<p align="center">
  <a href="https://linkreacher.com">Website</a> ·
  <a href="https://app.linkreacher.com">Dashboard</a> ·
  <a href="https://linkreacher.com/mcp">MCP docs</a> ·
  <a href="https://linkreacher.com/pricing">Pricing</a>
</p>

---

LinkReacher MCP is a **remote MCP server** (Streamable HTTP, JSON-RPC 2.0). Nothing to install,
nothing to run locally. Add one URL, paste your API key, and your assistant can drive the whole
backlink pipeline.

| | |
|---|---|
| **Server URL** | `https://api.linkreacher.com/mcp` |
| **Transport** | Streamable HTTP (plain JSON responses, no SSE required) |
| **Protocol** | MCP `2025-06-18` (older versions are echoed back on `initialize`) |
| **Auth** | Workspace API key `lr_...` via `Authorization: Bearer` or `?api_key=` |
| **Docs page** | <https://linkreacher.com/mcp> |
| **Plan** | Reads and discovery are **free**. Sending and mutations require **Pro** |
| **Tools** | 81 live tools (40 free / 41 Pro). Enumerate with `tools/list` |
| **Prompts** | 4 native prompt workflows (slash commands where supported) |

> **The live catalog is the source of truth.** This repo intentionally does not enumerate every
> tool. Call `tools/list` (no auth needed) or open <https://linkreacher.com/mcp> for the current,
> always in sync catalog with Free/Pro badges and danger marks.

---

## Table of contents

- [What you can do](#what-you-can-do)
- [Quickstart (60 seconds)](#quickstart-60-seconds)
- [Connect your assistant](#connect-your-assistant)
  - [Claude Code](#claude-code)
  - [Claude Desktop](#claude-desktop)
  - [Cursor, Windsurf, VS Code, Cline](#cursor-windsurf-vs-code-cline)
  - [ChatGPT](#chatgpt)
  - [Any HTTP client (curl / Python)](#any-http-client-curl--python)
- [Authentication](#authentication)
- [Plans, gating and cost](#plans-gating-and-cost)
- [Native rendering: tables, links and prompts](#native-rendering-tables-links-and-prompts)
- [Tool catalog (live)](#tool-catalog-live)
- [Prompts reference](#prompts-reference)
- [Errors, limits and idempotency](#errors-limits-and-idempotency)
- [How it works](#how-it-works)
- [Security and privacy](#security-and-privacy)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Repository layout](#repository-layout)
- [Publishing / registry](#publishing--registry)
- [Support](#support)
- [License](#license)

---

## What you can do

| Job to be done | What the assistant does |
|---|---|
| **Find link targets** | Analyses your site, expands keywords, searches the web, and returns linkable pages with Domain Rating and a linkability score. |
| **Find who to email** | OSINT pass (role searches, team and about pages) plus email pattern generation and verification. Returns ranked decision makers, not `info@`. |
| **Draft the ask** | Writes and scores a short, specific link request email. You see the rendered subject and body before anything sends. |
| **Run outreach** | Creates a campaign, attaches your sending mailbox, schedules it, and can launch it, with per mailbox and per day caps. |
| **Handle replies** | Reads the unified inbox, classifies replies (interested / wants payment / declined / opt out / OOO / bounce), and drafts answers. |
| **Track results** | Records won placements, rechecks whether the link is still live, and reports sent, replies, bounces and won. |
| **Engagement opportunities** | Surfaces high authority platforms (forums, Q&A, wikis, social) where participating earns links. This is the parasite list. |

Typical end to end chat:

> "My site is example.com. Find link targets, pick the best 10, find who to email, and draft the
> first message. Show me everything before you send anything."

---

## Quickstart (60 seconds)

1. **Create an account** at <https://app.linkreacher.com> (free, no card) and add your site.
2. **Mint an API key**: open the **API Keys** page, create a key, copy the `lr_...` value. You only see it once.
3. **Connect your assistant** (pick one):

```bash
# Claude Code
claude mcp add --transport http linkreacher https://api.linkreacher.com/mcp \
  --header "Authorization: Bearer lr_your_api_key"
```

```jsonc
// Claude Desktop / Cursor / any mcpServers client (via the mcp-remote bridge)
{ "mcpServers": { "linkreacher": {
    "command": "npx", "args": ["-y", "mcp-remote", "https://api.linkreacher.com/mcp",
      "--header", "Authorization: Bearer lr_your_api_key"] } } }
```

4. **Sanity check**: ask your assistant to *"Call `get_me` and tell me my plan and remaining contact budget."*

That is it. If `get_me` answers, discovery, enrichment and campaigns are all reachable.

---

## Connect your assistant

Everything below points at the same remote server. There is no package to install and no local
process to keep alive.

### Claude Code

```bash
claude mcp add --transport http linkreacher https://api.linkreacher.com/mcp \
  --header "Authorization: Bearer lr_your_api_key"
```

Verify with `claude mcp list`, then `/mcp` inside Claude Code. For a project scoped setup, commit a
`.mcp.json` at your repo root with the same `url` and `headers` shape.

### Claude Desktop

Claude Desktop speaks stdio, so bridge to the remote server with `mcp-remote`. Edit
`claude_desktop_config.json` (Settings > Developer > Edit Config):

```json
{
  "mcpServers": {
    "linkreacher": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "https://api.linkreacher.com/mcp",
        "--header", "Authorization: Bearer lr_your_api_key"
      ]
    }
  }
}
```

Restart Claude Desktop. The tools appear under the plug icon, and the four prompts appear in the
`/` command menu. Requires Node.js (`npx`).

### Cursor, Windsurf, VS Code, Cline

Most editors accept either a native remote server or the `mcp-remote` bridge. Native shape:

```json
{
  "mcpServers": {
    "linkreacher": {
      "url": "https://api.linkreacher.com/mcp",
      "headers": { "Authorization": "Bearer lr_your_api_key" }
    }
  }
}
```

- **VS Code (Copilot)**: `.vscode/mcp.json` uses the same `servers` shape with `"type": "http"`.
- **Cline / Roo**: MCP Servers, then Remote / HTTP, then paste the URL and header.
- If a client only does stdio, use the `mcp-remote` bridge from the Claude Desktop example.

### ChatGPT

The ChatGPT connector form offers only "OAuth" or "No Auth", so, like most API key MCP servers,
the key rides in the URL as a query parameter:

1. Settings > **Connectors** > **Advanced** > **Create**. Set the URL to
   `https://api.linkreacher.com/mcp?api_key=lr_your_api_key` and choose **No Auth**.
2. In a chat, enable **Developer mode**, attach the connector, then ask it to call `get_me`.

> Treat that URL as a password. URLs are logged by intermediaries. Prefer the header form on any
> client that supports it, and rotate the key if it leaks. Query param auth exists **only** for
> `/mcp`. It is never honoured on any other path.

### Any HTTP client (curl / Python)

Discovery needs no credential, so you can inspect the server before authenticating:

```bash
# List every tool (no auth). This is the live catalog.
curl -s https://api.linkreacher.com/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# Call a tool (auth required)
curl -s https://api.linkreacher.com/mcp \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LINKREACHER_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"get_me","arguments":{}}}'
```

See [`examples/`](examples) for copy paste scripts (curl, Python, client configs).

---

## Authentication

Two transport level credentials are accepted on `tools/call`:

| Method | Example | When to use |
|---|---|---|
| **Header** (preferred) | `Authorization: Bearer lr_...` | Every client that supports headers. |
| **Query param** (fallback) | `https://api.linkreacher.com/mcp?api_key=lr_...` | ChatGPT connectors and any client whose UI cannot set headers. |
| User access token | `Authorization: Bearer <session token>` | First party dashboard sessions. Not intended for third parties. |

Rules:

- **Keys are workspace scoped.** A key only ever sees its own workspace. There is no cross tenant access and no header based tenancy override.
- Keys are stored hashed server side (SHA-256). The plaintext exists only in your copy.
- `tools/call` with **no credential or an invalid key** returns HTTP `401` with JSON-RPC error
  `-32001`. Discovery (`initialize`, `tools/list`, `ping`) is deliberately **public** so you and
  directory validators can inspect the server without a key.
- Query param auth is scoped **strictly to `/mcp`**. Never send keys in the URL to any other path.
- Rotate or revoke keys on the API Keys page at any time. Revocation is immediate.

---

## Plans, gating and cost

LinkReacher is pay as you go. There is no per seat or per email metering in the MCP surface.

| | Free | Pro |
|---|---|---|
| Keywords, discovery, prospect lists | Yes | Yes |
| Contact reveals (who to email) | 15 per workspace | Unlimited |
| All read tools (prospects, campaigns, inbox, analytics, placements) | Yes | Yes |
| Engagement / parasite list | Capped sample | Full |
| Connect mailboxes, create and launch campaigns | No | Yes |
| Send, reply, compose, manage templates | No | Yes |
| Autopilot (auto discover, auto campaign, auto send) | No | Yes |

**Gating is server enforced.** A free plan call to a Pro tool returns a normal tool result with
`isError: true` and a message pointing at the upgrade page, never a raw 403 JSON.

**Discovery and contact finding are not metered.** You are never billed per call, per keyword or per
search, and there is no usage ceiling on Pro: run discovery and enrichment as often as you want.
Free workspaces are limited to 15 contact reveals and a sample of the engagement list, which is the
only customer facing limit in the MCP surface. We do keep internal API spend guardrails for our own
costs (visible through `get_costs`); those exist for us and never surface to you as a limit or a bill.

---

## Native rendering: tables, links and prompts

The server is built so results **feel native** in chat clients instead of dumping JSON.

**`content` is for the model.** List results are returned as a **markdown table** with a one line
summary above it, so ChatGPT, Claude and Cursor render a real table:

```
**list_prospects** · 16 rows

plan: free · lockedCount: 1

| domain | site | type | dr | linkability_score | enrichmentState |
| --- | --- | --- | --- | --- | --- |
| zapier.com | zapier.com | linkable | 91 | 0.9 | done |
```

URLs are emitted as clickable markdown links, and long values are truncated with an ellipsis so a
table never wraps into a wall of text. Rows are capped (50 per table, with a `... N more` marker).
Narrow the query or page through the JSON when you need more.

**`structuredContent` is for code.** Every successful call also returns the same data as a JSON
object, per the MCP spec, so code mode clients and type safe orchestrators can consume it directly.

**Annotations are for trust.** Every tool advertises `title`, `readOnlyHint`, `destructiveHint` and
`openWorldHint`. Tools that **send email** (`send_now`, `reply`, `compose_email`, `start_campaign`)
are marked so clients can confirm before acting. Clients must treat these hints as untrusted unless
the server itself is trusted.

**Prompts are for onboarding.** Four prompt workflows are exposed through `prompts/list` and
`prompts/get`, which appear as slash commands where the client supports prompts.

---

## Tool catalog (live)

The full, always current catalog (with descriptions, Free/Pro badges and danger marks) lives on the
server and at <https://linkreacher.com/mcp>. Get it any time, no auth required:

```bash
curl -s https://api.linkreacher.com/mcp \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -H 'Content-Type: application/json' | jq '.result.tools[].name'
```

Categories you will find (81 tools total, 40 free and 41 Pro):

| Category | What is in it | Examples |
|---|---|---|
| **Keywords** | The phrases discovery searches for, plus keyword ideas | `list_keywords`, `add_keyword`, `suggest_keywords` |
| **Discovery** | Site analysis, keyword expansion, SERP sweep, scored prospects | `start_discovery`, `get_discovery_status` |
| **Prospects and contacts** | Linkable pages, ranked contacts, engagement opportunities | `list_prospects`, `find_contact`, `list_participation` |
| **Workspace** | Plan, budget, spend, settings | `get_me`, `get_workspace`, `get_costs` |
| **Mailboxes** | Connect and manage sending inboxes (SMTP/IMAP plus deliverability checks) | `list_mailboxes`, `connect_gmail` |
| **Campaigns** | Sequences, senders, schedules, launch and stop, logs, previews | `create_campaign`, `add_campaign_step`, `preview_next_send` |
| **Autopilot** | Three tier autonomy: auto discover, auto campaign, auto send | `get_autopilot`, `update_autopilot` |
| **Inbox** | Unified replies: search, read, classify, snooze, resolve, reply | `search_threads`, `get_thread`, `reply` |
| **Templates** | Reusable subject and body with merge tokens plus spam scoring | `create_template`, `render_template`, `score_template` |
| **Analytics** | Sent, replies, bounces and won, usage against caps, deliverability | `analytics_dashboard`, `analytics_deliverability` |
| **Placements** | Won links, live rechecks, placement stats | `list_placements`, `track_placement`, `recheck_placement` |

Merge tokens in templates and campaign steps: `{{first_name}}`, `{{company}}`, `{{site}}`,
`{{keyword}}` and any custom lead field. Plain text only. No HTML, no open or click tracking.

---

<p align="center">
  <img src="assets/mascot.svg" width="200" alt="LinkReacher mascot" />
</p>

<p align="center"><em>You are halfway through a README. Respect. The mascot would like you to close the tab and go find some backlinks.</em></p>

---

## Prompts reference

| Prompt | Arguments | What it drives |
|---|---|---|
| `find-backlink-prospects` | `site` (required), `keywords` (optional) | Budget check, discovery, then a markdown table of the best targets plus engagement opportunities. |
| `start-link-outreach` | `goal` (optional) | Top prospects, contacts, campaign, step, senders, then **preview before launch**. |
| `write-link-request` | `prospect` (required) | Reads the prospect and contacts, then renders a short, non spammy link request. |
| `triage-replies` | none | Inbox overview, unseen threads, grouped by classification, then drafts replies. |

Prompts are instructions to your assistant, not server side automation. They ask the model to call
the right tools in the right order, and to confirm before sending.

---

## Errors, limits and idempotency

**JSON-RPC level**

| Code | HTTP | Meaning |
|---|---|---|
| `-32700` | `400` | Parse error (malformed JSON). |
| `-32601` | `200` | Method not found (unknown JSON-RPC method). |
| `-32602` | `200` | Invalid params, for example an unknown tool or prompt name. |
| `-32001` | `401` | Unauthorized. No credential or an invalid one on `tools/call`. |

**Tool level.** A tool that fails returns a normal result with `isError: true` and a human readable
message in `content` (for example `Error (404): Campaign not found`, or a Pro gate message). The
transport stays `200`, and the model can read the message and recover.

**Behaviour worth knowing**

- **Nothing sends by accident.** `start_campaign`, `send_now`, `reply` and `compose_email` are annotated as email senders. `preview_next_send` renders exactly what would go out.
- **Idempotent where it matters.** Duplicate keywords and contacts, plus cross workspace writes, are rejected rather than duplicated. Prospect to campaign ingestion is idempotent per prospect.
- **Unmetered, not unlimited chaos.** Discovery and contact finding carry no customer usage limit on Pro. Run them as often as you like.
- **Free contact reveals** are counted per workspace. `get_me` reports used and remaining.
- **No warmup, no rotation, no tracking pixels.** Plain text outreach only.

---

## How it works

```
keywords -> discovery -------------> prospects -> find_contact -> campaign -> send -> inbox
            site analysis            linkable     decision        sequence     SMTP   replies
            keyword expansion        pages        makers          schedule            classified
            SERP sweep                                                       -> placements (won / live)
```

- **Discovery** analyses the site, expands keywords, runs SERP searches, scores each candidate for linkability, and separates *linkable* pages from *engagement* opportunities.
- **Enrichment** runs only when you ask (`find_contact`): role based searches, team and about page extraction, email pattern generation, and verification. Results are cached and reused.
- **Campaigns** are the same engine the web app uses: per lead sticky mailbox, threaded follow ups, day and window caps, and stop on reply.
- **Inbox** unifies replies across mailboxes, strips quoted text, classifies intent, and treats opt outs as suppression list entries.
- **Placements** records won links and rechecks whether they are still live.

---

## Security and privacy

- API keys are workspace scoped and stored hashed. Mailbox passwords are encrypted at rest.
- Every request resolves tenancy from the authenticated principal only. There is no header or parameter that can point the server at a different workspace.
- Discovery and reads are publicly inspectable. Anything that touches your data requires a key.
- Keys in URLs (the ChatGPT fallback) are a deliberate tradeoff for clients that cannot send headers. Prefer headers elsewhere, and rotate if exposed.
- We never sell or share prospect data. Contact lookups use public web data plus verification.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `401` with `-32001` | Missing or invalid key on `tools/call` | Set the `Authorization: Bearer lr_...` header, or use `?api_key=`. |
| Tools missing in the client | The client did not finish `initialize` | Restart the client. Check the server URL has no trailing slash. |
| `mcp-remote` bridge errors | Node or `npx` missing, or a stale npx cache | Install Node 20 or newer, retry, or run `npx -y mcp-remote@latest`. |
| "requires LinkReacher Pro" | Free plan calling a send or mutation tool | Upgrade, or stick to reads, which are free. |
| Empty tables | No data yet for that workspace | Run `start_discovery` or `find_contact` first. |
| ChatGPT connector shows nothing | Developer mode is off | Enable Developer mode for the connector in settings. |
| Duplicate or unexpected sends | Multiple clients connected with the same key | Use one key per client. Keys are listed and revocable on the API Keys page. |

The server is healthy when this returns `200`:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://api.linkreacher.com/health
```

---

## FAQ

**Is it free?** Reads and the whole discovery funnel are free. Sending and mutations are Pro
($129/mo, cancel anytime). See <https://linkreacher.com/pricing>.

**Do I need to host anything?** No. It is a remote server at a fixed URL.

**Does it send email on its own?** Only if you ask it to, or if you enable autopilot on Pro. Every
sending tool is marked, and `preview_next_send` shows the exact message first.

**Which MCP protocol versions work?** `2025-06-18` is advertised. The server echoes your requested
version on `initialize`, so older clients connect too.

**Why no SSE?** Request and response is enough for all tools, and plain JSON avoids the long lived
stream failure modes of proxy fronted deployments.

**Why is my key in the URL on ChatGPT?** Its connector UI only offers OAuth or No Auth. Header auth
is used everywhere else.

**Can multiple people share one key?** Technically yes, but the key maps to one workspace. Mint one
key per client or teammate so you can revoke individually.

---

## Repository layout

```
README.md          Setup, auth, plans, rendering, troubleshooting
server.json        Official MCP Registry metadata (remote record)
assets/            Logo, favicon and mascot pulled from linkreacher.com
examples/          Copy paste client configs and scripts
LICENSE
```

This repo is **documentation and registry metadata only**. The tool catalog is fetched from the live
server at runtime so it can never drift from what the server actually exposes.

## Publishing / registry

`server.json` describes the remote server for the official MCP Registry:

```bash
# one time
curl -L https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_amd64.tar.gz | tar xz
./mcp-publisher login github
./mcp-publisher publish
```

Verify:

```bash
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.rshiv/linkreacher"
```

Listing on directories (mcp.so, Smithery, Glama, PulseMCP and others) is a submission each. Most
ingest the official registry record.

## Support

- Docs and catalog: <https://linkreacher.com/mcp>
- Dashboard: <https://app.linkreacher.com>
- Email: support@linkreacher.com
- Bugs in this repo (docs or config): open an issue.

## License

MIT. See [LICENSE](LICENSE). This covers this repository (docs and metadata). The LinkReacher
service itself is proprietary and governed by its terms of service.
