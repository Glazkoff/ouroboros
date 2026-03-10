# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **GLM API Support**: Ouroboros now supports GLM API (z.ai coding plan) as an alternative to OpenRouter
  - New environment variables: `LLM_PROVIDER`, `GLM_API_KEY`, `GLM_BASE_URL`, `GLM_MODEL`
  - Set `LLM_PROVIDER=glm` to use GLM API
  - Default GLM model: `glm-4-plus`
  - Automatic cost estimation for GLM (OpenRouter provides exact costs)
  - Full tool support (function calling)

### Changed
- **Multi-provider LLM client**: `ouroboros/llm.py` now supports multiple providers
  - OpenRouter (default, backward compatible)
  - GLM API (new)
  - Provider detection via `LLM_PROVIDER` env var
- **Documentation**: Updated README with GLM API setup instructions

### Configuration

#### For GLM API:
```bash
export LLM_PROVIDER=glm
export GLM_API_KEY=your_api_key_here
export GLM_BASE_URL=https://api.z.ai/api/coding/paas/v4
export GLM_MODEL=glm-4-plus
```

#### For OpenRouter (default):
```bash
export LLM_PROVIDER=openrouter  # or omit, it's the default
export OPENROUTER_API_KEY=your_key_here
export OUROBOROS_MODEL=anthropic/claude-sonnet-4.6
```

### Testing
- Added `test_glm.py` script to verify GLM API integration
- Run with: `python test_glm.py` (requires .env file with GLM credentials)
