#!/bin/bash
set -euo pipefail

# Image generation script for uiux-methodology skill.
# Adapted from aacassandra/anti-ai-slop-design (MIT license).
# Generates images via an OpenAI-compatible API endpoint.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ENV_SOURCE=""

_read_env_file() {
    local file="$1"
    while IFS='=' read -r key value || [ -n "$key" ]; do
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        value="${value#\"}"; value="${value%\"}"
        value="${value#'}"; value="${value%'}"
        export "$key=$value"
    done < "$file"
}

load_env() {
    # 1. Explicit override via env var
    if [ -n "${SKILL_ENV_FILE:-}" ] && [ -f "$SKILL_ENV_FILE" ]; then
        _read_env_file "$SKILL_ENV_FILE"
        ENV_SOURCE="override:$SKILL_ENV_FILE"
        return
    fi

    # 2. Project root .env — detect workspace path patterns:
    #    - OpenClaw: .../workspace/skills/<name>/scripts/ → go up 4 levels to workspace root
    #    - Claude:   .../skills/<name>/scripts/           → go up 4 levels (same logic)
    local project_root=""
    # Try OpenClaw workspace path (scripts → skill → skills → workspace)
    local candidate
    candidate="$(cd "$SCRIPT_DIR/../../../.." 2>/dev/null && pwd || true)"
    if [ -n "$candidate" ] && [ -f "$candidate/.env" ]; then
        project_root="$candidate"
    else
        # Fallback: walk up looking for .env (covers non-standard layouts)
        local dir="$SCRIPT_DIR"
        while [ "$dir" != "/" ]; do
            dir="$(dirname "$dir")"
            if [ -f "$dir/.env" ]; then
                project_root="$dir"
                break
            fi
        done
    fi

    if [ -n "$project_root" ]; then
        _read_env_file "$project_root/.env"
        ENV_SOURCE="project:$project_root/.env"
        return
    fi

    # 3. Skill directory .env (one level up from scripts/)
    local skill_root
    skill_root="$(cd "$SCRIPT_DIR/.." 2>/dev/null && pwd || true)"
    if [ -n "$skill_root" ] && [ -f "$skill_root/.env" ]; then
        _read_env_file "$skill_root/.env"
        ENV_SOURCE="global:$skill_root/.env"
        return
    fi

    ENV_SOURCE="none"
}
load_env

API_URL="${MY_IMAGE_API_URL:-https://xxxxx.my.id/v1/images/generations}"
API_KEY="${MY_IMAGE_API_KEY:-}"
API_TIMEOUT="${MY_IMAGE_API_TIMEOUT:-60}"

prompt="${1:-}"
model="${2:-${MY_IMAGE_MODEL:-chatgpt-web}}"
n="${3:-1}"
size="${4:-auto}"
quality="${5:-auto}"
output_format="${6:-png}"

if [ -z "$API_KEY" ]; then
    jq -n \
        --arg error "MY_IMAGE_API_KEY not set" \
        --arg source "custom-api" \
        --arg env_checked "$ENV_SOURCE" \
        '{error: $error, source: $source, env_checked: $env_checked}' >&2
    exit 1
fi

if [ -z "$prompt" ]; then
    echo '{"error": "prompt required", "usage": "generate.sh PROMPT [model] [n] [size] [quality] [format]"}' >&2
    exit 1
fi

if ! [[ "$n" =~ ^[0-9]+$ ]] || [ "$n" -lt 1 ] || [ "$n" -gt 10 ]; then
    echo '{"error": "n must be an integer between 1 and 10"}' >&2
    exit 1
fi

case "$output_format" in
    png|jpg|jpeg|webp) ;;
    *)
        echo '{"error": "format must be one of: png, jpg, jpeg, webp"}' >&2
        exit 1
        ;;
esac

case "$size" in
    auto|1024x1024|1024x1536|1536x1024) ;;
    *)
        echo '{"error": "size must be one of: auto, 1024x1024, 1024x1536, 1536x1024"}' >&2
        exit 1
        ;;
esac

case "$quality" in
    auto|low|medium|high) ;;
    *)
        echo '{"error": "quality must be one of: auto, low, medium, high"}' >&2
        exit 1
        ;;
esac

payload=$(jq -n \
    --arg model "$model" \
    --arg prompt "$prompt" \
    --argjson n "$n" \
    --arg size "$size" \
    --arg quality "$quality" \
    --arg format "$output_format" \
    '{
        model: $model,
        prompt: $prompt,
        n: $n,
        size: $size,
        quality: $quality,
        background: "auto",
        image_detail: "high",
        output_format: $format
    }')

response=$(curl -s -w "\n%{http_code}" \
    -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time "$API_TIMEOUT" \
    -d "$payload" 2>&1)

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

case "$http_code" in
    200)
        echo "$body" | jq \
            --arg source "custom-api" \
            --argjson http_code "$http_code" \
            --arg prompt "$prompt" \
            --arg model "$model" \
            '{source: $source, http_code: $http_code, prompt: $prompt, model: $model, data: .}'
        ;;
    *)
        jq -n \
            --arg source "custom-api" \
            --argjson http_code "$http_code" \
            --arg error "$body" \
            '{source: $source, http_code: $http_code, error: $error}'
        exit 1
        ;;
esac
