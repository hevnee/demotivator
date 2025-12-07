from typing import Optional
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

from .options import Options, get_options


class Template:
    def __init__(self):
        self.options = Options(get_options())

    def generate_template(self) -> Image.Image:
        self.__generate_background()
        self.__generate_border()

        return self._template

    def __generate_background(self) -> None:
        self._template = Image.new(
            self.options.mode,
            self.options.size,
            self.options.background_color
        )

    def __generate_border(self) -> None:
        x1 = round(self.options.width / self.options.frame_outline_divide_by)
        y1 = round(self.options.height / self.options.frame_outline_divide_by / 2.2)
        x2 = round(self.options.width - self.options.width / self.options.frame_outline_divide_by)
        y2 = round(self.options.height - self.options.height / self.options.frame_outline_divide_by * 2.2)

        image_draw = ImageDraw.Draw(self._template)
        image_draw.rectangle(
            (x1, y1, x2, y2),
            outline=self.options.frame_outline_color,
            width=self.options.frame_outline_width
        )

        self.frame_box = (x1, y1, x2, y2)


@dataclass
class ImageCreation:
    file_path: str
    title_text: str
    subtitle_text: Optional[str] = None

    def __post_init__(self):
        template = Template()
        self.options = template.options
        self.__image = template.generate_template()
        self.__frame_box = template.frame_box
    
    def generate_image(self) -> Image.Image:
        self.__generate_image()
        self.__generate_title_text()

        if self.subtitle_text:
            self.__generate_subtitle_text()
        
        return self.__image

    def __generate_image(self) -> None:
        image = Image.open(self.file_path)

        x1, y1, x2, y2 = self.__frame_box
        frame_padding = self.options.frame_padding

        inner_x1 = x1 + frame_padding
        inner_y1 = y1 + frame_padding
        inner_x2 = x2 - frame_padding
        inner_y2 = y2 - frame_padding

        inner_width = inner_x2 - inner_x1
        inner_height = inner_y2 - inner_y1

        image = image.resize((inner_width, inner_height), Image.Resampling.LANCZOS)
        self.__image.paste(image, (inner_x1, inner_y1))

    def __generate_title_text(self) -> None:
        image_draw = ImageDraw.Draw(self.__image)

        xy = self.options.width / 2, self.options.height / 1.113
        font_size = self.options.title_font_size
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

        font = ImageFont.truetype(self.options.font_family, font_size)
        image_draw.text(xy, self.title_text, fill=self.options.text_color, font=font, anchor=anchor, align="center")

    def __generate_subtitle_text(self) -> None:
        image_draw = ImageDraw.Draw(self.__image)

        xy = self.options.width / 2, self.options.height / 1.069
        font_size = self.options.subtitle_font_size

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

        font = ImageFont.truetype(self.options.font_family, font_size)
        image_draw.text(xy, self.subtitle_text, fill=self.options.text_color, font=font, anchor="mt", align="center")