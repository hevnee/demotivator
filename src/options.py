import json
from typing import Optional, Tuple


def create_options() -> dict:
    options = { # default options for 1024x1024
        "mode": "RGB",
        "size": (1024, 1024),
        "background_color": (0, 0, 0),
        "text_color": (255, 255, 255),
        "frame_outline_color": (255, 255, 255),
        "frame_outline_divide_by": 12,
        "frame_outline_width": 3,
        "frame_padding": 4,
        "font_family": "times.ttf",
        "title_font_size": 85,
        "subtitle_font_size": 46
    }
    with open("options.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(options, indent=4))
    return options


def get_options() -> Optional[dict]:
    try:
        with open("options.json", "r", encoding="utf-8") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return create_options()
    except Exception as e:
        print(e)


def change_options(options: dict) -> None:
    with open("options.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(options, indent=4))


class Options:
    def __init__(self, options: dict):
        self.options = options

    @property
    def mode(self) -> str:
        return self.options.get("mode")

    @property
    def size(self) -> Tuple[int, int]:
        return tuple(self.options.get("size"))

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    @property
    def background_color(self) -> Tuple[float, ...]:
        return tuple(self.options.get("background_color"))

    @property
    def text_color(self) -> Tuple[float, ...]:
        return tuple(self.options.get("text_color"))

    @property
    def frame_outline_color(self) -> Tuple[float, ...]: 
        return tuple(self.options.get("frame_outline_color"))

    @property
    def frame_outline_divide_by(self) -> int:
        return self.options.get("frame_outline_divide_by")

    @property
    def frame_outline_width(self) -> int:
        return self.options.get("frame_outline_width")

    @property
    def frame_padding(self) -> int:
        return self.options.get("frame_padding") + self.frame_outline_width

    @property
    def font_family(self) -> str:
        return self.options.get("font_family")

    @property
    def title_font_size(self) -> float:
        return self.options.get("title_font_size")

    @property
    def subtitle_font_size(self) -> float:
        return self.options.get("subtitle_font_size")