# External Integrations

**Analysis Date:** 2026-03-03

## APIs & External Services

**LLM Integration:**
- Compatible with outputs from Ollama, Claude.ai, OpenAI ChatGPT
- No direct SDK/client integration - processes text output from LLM services
- Purpose: Clean and transform LLM-generated prompts and descriptions

## Data Storage

**Databases:**
- Not applicable - Nodes process in-memory strings only, no persistent storage

**File Storage:**
- Local filesystem only - Custom node installed in ComfyUI custom_nodes directory
- No external file storage integrations

**Caching:**
- None - All operations are stateless transformations

## Authentication & Identity

**Auth Provider:**
- Not applicable - Standalone utility nodes with no authentication requirements
- Custom node registration managed by ComfyUI framework

## Monitoring & Observability

**Error Tracking:**
- None - Uses ComfyUI's native error handling and logging

**Logs:**
- ComfyUI application logs
- No external log aggregation

## CI/CD & Deployment

**Hosting:**
- GitHub repository: https://github.com/bradsec/ComfyUI_StringEssentials
- ComfyUI Registry: Registered via ComfyUI package registry (PublisherId: bradsec)

**CI Pipeline:**
- GitHub Actions workflow: `.github/workflows/publish.yml`
- Automated publishing to ComfyUI registry on release

## Environment Configuration

**Required env vars:**
- None - Zero environment variable dependencies

**Secrets location:**
- Not applicable - No secrets or credentials used

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

## Frontend Integration

**ComfyUI Web Interface:**
- JavaScript extensions in `js/string_essentials.js`
- Custom node widget initialization via ComfyUI's extension API
- Widget API: `ComfyWidgets` for STRING input display
- App API: `app.registerExtension()` for node lifecycle hooks

**Node Widget Configuration:**
- Multiline text inputs for string configuration
- Boolean toggles for matching options (case-sensitive, whole word, etc.)
- Dropdown selections for position (beginning/end)
- Custom separators configurable via STRING inputs

---

*Integration audit: 2026-03-03*
