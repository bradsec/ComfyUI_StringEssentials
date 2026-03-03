# Technology Stack

**Analysis Date:** 2026-03-03

## Languages

**Primary:**
- Python 3.x - Core node implementation and string manipulation logic
- JavaScript - Frontend UI extensions and ComfyUI widget integration

## Runtime

**Environment:**
- ComfyUI - Custom node framework for AI image generation workflows

**Package Manager:**
- pip - Python dependency management
- No Python dependencies or external modules required (pure Python implementation)

## Frameworks

**Core:**
- ComfyUI Custom Nodes Framework - Node registration and execution
  - Uses `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS` for node registration
  - Located: `__init__.py`

**Testing:**
- unittest - Python standard library testing framework
- Config: No external test configuration file (uses unittest defaults)
- Test file: `test_string_nodes.py`

**Build/Dev:**
- No formal build system required
- Direct Python module installation into ComfyUI custom_nodes directory

## Key Dependencies

**Critical:**
- None - This is a zero-dependency ComfyUI custom node package
- All functionality implemented using Python standard library only (re module for regex)

**Infrastructure:**
- None - Standalone custom node implementation

## Configuration

**Environment:**
- No environment variables required
- No configuration files needed
- Simple cloning into ComfyUI custom_nodes directory

**Build:**
- `pyproject.toml` - Package metadata and ComfyUI registry information
  - Version: 2.0.7
  - Publisher: bradsec (ComfyUI Registry identifier)
  - License: Included in LICENSE file

## Platform Requirements

**Development:**
- Python 3.x
- ComfyUI installation (as parent application)
- Git for repository cloning

**Production:**
- ComfyUI application
- Python 3.x runtime
- Custom node installed in `custom_nodes/ComfyUI_StringEssentials/` directory

## Platform Support

**Deployment Target:**
- ComfyUI custom nodes directory
- Cross-platform (Windows, macOS, Linux)
- Web-based ComfyUI interface with JavaScript frontend integration

---

*Stack analysis: 2026-03-03*
