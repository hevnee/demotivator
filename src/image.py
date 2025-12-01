from typing import Optional, Union, Tuple
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont


class Options:
    mode: str = "RGB"
    size: Tuple[int, int] = 512, 512
    width = size[0]
    height = size[1]
    background_color: Union[float, Tuple[float, ...], str, None] = "black"
    text_color: Union[float, Tuple[float, ...], str, None] = "white"
    frame_outline_color: Union[float, Tuple[float, ...], str, None] = "white"
    frame_outline_divide_by: int = 12
    frame_outline_width: int = int(height / 256)
    frame_padding: int = int(height / 128)
    font_family_path: str = "times.ttf"
    title_font_size: float = height / 12.048
    subtitle_font_size: float = height / 22.261


class Template:
    def generate_template(self) -> Image.Image:
        self.__generate_background()
        self.__generate_border()

        return self._template

    def __generate_background(self) -> None:
        self._template = Image.new(
            Options.mode,
            Options.size,
            Options.background_color
        )

    def __generate_border(self) -> None:
        x1 = int(Options.width / Options.frame_outline_divide_by)
        y1 = int(Options.height / Options.frame_outline_divide_by / 2.2)
        x2 = int(Options.width - Options.width / Options.frame_outline_divide_by)
        y2 = int(Options.height - Options.height / Options.frame_outline_divide_by * 2.2)

        image_draw = ImageDraw.Draw(self._template)
        image_draw.rectangle(
            (x1, y1, x2, y2),
            outline=Options.frame_outline_color,
            width=Options.frame_outline_width
        )

        self._frame_box = (x1, y1, x2, y2)


@dataclass
class ImageCreation(Template):
    file_path: str
    title_text: str
    subtitle_text: Optional[str] = None

    def __post_init__(self):
        self.__image = self.generate_template()
    
    def generate_image(self) -> Image.Image:
        self.__generate_image()
        self.__generate_title_text()

        if self.subtitle_text:
            self.__generate_subtitle_text()
        
        return self.__image

    def __generate_image(self) -> None:
        image = Image.open(self.file_path)

        x1, y1, x2, y2 = self._frame_box

        inner_x1 = x1 + Options.frame_padding
        inner_y1 = y1 + Options.frame_padding
        inner_x2 = x2 - Options.frame_padding
        inner_y2 = y2 - Options.frame_padding

        inner_width = inner_x2 - inner_x1
        inner_height = inner_y2 - inner_y1

        image = image.resize((inner_width, inner_height), Image.LANCZOS)
        self.__image.paste(image, (inner_x1, inner_y1))

    def __generate_title_text(self) -> None:
        image_draw = ImageDraw.Draw(self.__image)

        xy = Options.width / 2, Options.height / 1.113
        font_size = Options.title_font_size
        anchor = "ms" if self.subtitle_text else "mm"

        while True:
            text_box = image_draw.textbbox(
                xy=xy,
                text=self.title_text,
                anchor=anchor,
                align="center",
                font_size=font_size
            )
            if text_box[0] > 0:
                break
            font_size -= 1

        font = ImageFont.truetype(Options.font_family_path, font_size)
        image_draw.text(xy, self.title_text, fill=Options.text_color, font=font, anchor=anchor, align="center")

    def __generate_subtitle_text(self) -> None:
        image_draw = ImageDraw.Draw(self.__image)

        xy = Options.width / 2, Options.height / 1.069
        font_size = Options.subtitle_font_size

        while True:
            text_box = image_draw.textbbox(
                xy=xy,
                text=self.subtitle_text,
                anchor="mt",
                align="center",
                font_size=font_size
            )
            if text_box[0] > 0:
                break
            font_size -= 1

        font = ImageFont.truetype(Options.font_family_path, font_size)
        image_draw.text(xy, self.subtitle_text, fill=Options.text_color, font=font, anchor="mt", align="center")