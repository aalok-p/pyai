import json
import os
import re
from pathlib import Path
from typing import Any


def strip_jsonc_comments(text: str) -> str:
    result = []
    i = 0
    in_string = False
    escape = False
    while i < len(text):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            result.append(ch)
            i += 1
        else:
            if text[i : i + 2] == "//":
                while i < len(text) and text[i] != "\n":
                    i += 1
            elif text[i : i + 2] == "/*":
                i += 2
                while i < len(text) - 1 and text[i : i + 2] != "*/":
                    i += 1
                i += 2
            else:
                if ch == '"':
                    in_string = True
                result.append(ch)
                i += 1
    return "".join(result)


def interpolate_env_vars(value: Any) -> Any:
    if isinstance(value, str):
        pattern = re.compile(r"\$\{(\w+)(?::-([^}]*))?\}")

        def replacer(match: re.Match) -> str:
            var_name = match.group(1)
            default = match.group(2)
            return os.getenv(var_name, default if default is not None else "")

        return pattern.sub(replacer, value)
    if isinstance(value, dict):
        return {k: interpolate_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [interpolate_env_vars(item) for item in value]
    return value


class Config:
    def __init__(self, data: dict):
        self.raw = data
        self.providers = data.get("providers", {})
        self.default_provider = data.get("default_provider")
        self.default_model = data.get("default_model")
        self.agent = data.get("agent", {})
        self.mcp = data.get("mcp", {})
        self.skills = data.get("skills", {})

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Config":
        if path is None:
            cwd_config = Path.cwd() / "pyai.jsonc"
            home_config = Path.home() / ".config" / "pyai" / "config.jsonc"
            if cwd_config.exists():
                path = cwd_config
            elif home_config.exists():
                path = home_config
            else:
                return cls({})

        path = Path(path)
        text = path.read_text(encoding="utf-8")
        clean = strip_jsonc_comments(text)
        data = json.loads(clean)
        data = interpolate_env_vars(data)
        return cls(data)

    def get_provider(self, name: str | None = None) -> dict:
        name = name or self.default_provider
        if not name:
            raise ValueError("No provider specified and no default_provider set in config")
        provider = self.providers.get(name)
        if not provider:
            raise ValueError(f"Provider '{name}' not found in config")
        return provider

    def get_model_string(self, provider_name: str | None = None) -> str:
        provider = self.get_provider(provider_name)
        default_model = provider.get("default_model")
        if not default_model:
            raise ValueError(f"Provider '{provider_name or self.default_provider}' has no default_model")
        return f"{provider_name or self.default_provider}:{default_model}"
