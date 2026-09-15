#!/usr/bin/env bash
# LinkReacher MCP curl cookbook.
# Usage: LINKREACHER_API_KEY=lr_... ./examples/curl.sh
set -euo pipefail

URL="${LINKREACHER_MCP_URL:-https://api.linkreacher.com/mcp}"
KEY="${LINKREACHER_API_KEY:-}"

post() {
  curl -s "$URL" -H 'Content-Type: application/json' "$@"
}

echo "# Discovery needs no auth (catalog is public)"
post -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}'
echo
post -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | jq -r '.result.tools[].name'
echo
post -d '{"jsonrpc":"2.0","id":3,"method":"prompts/list"}' | jq -r '.result.prompts[].name'
echo

if [[ -z "$KEY" ]]; then
  echo "Set LINKREACHER_API_KEY=lr_... to run the authenticated calls below."
  exit 0
fi

AUTH=(-H "Authorization: Bearer $KEY")

echo "# tools/call needs a key"
post "${AUTH[@]}" -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_me","arguments":{}}}' | jq '.result.content[0].text'
echo
post "${AUTH[@]}" -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"list_prospects","arguments":{}}}' \
  | jq -r '.result.content[0].text'      # markdown table for the model
echo
post "${AUTH[@]}" -d '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"list_prospects","arguments":{}}}' \
  | jq '.result.structuredContent'       # same data for code
