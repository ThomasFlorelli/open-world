import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Config:
    TEXTURE_PATH: str
    TEXTURE_SIZE: int
    DISPLAY_TEXTURE_SIZE: int
    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    VIEWPORT_WIDTH: int
    VIEWPORT_HEIGHT: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        return cls(
            TEXTURE_PATH=data["TEXTURE_PATH"],
            TEXTURE_SIZE=data["TEXTURE_SIZE"],
            DISPLAY_TEXTURE_SIZE=data["DISPLAY_TEXTURE_SIZE"],
            SCREEN_WIDTH=data["SCREEN_WIDTH"],
            SCREEN_HEIGHT=data["SCREEN_HEIGHT"],
            VIEWPORT_WIDTH=data["VIEWPORT_WIDTH"],
            VIEWPORT_HEIGHT=data["VIEWPORT_HEIGHT"],
        )

    @classmethod
    def from_json_file(cls, path: str) -> "Config":
        with open(path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)