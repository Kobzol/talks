import dataclasses
import io
from typing import Optional, Tuple, Union

import elsie
from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.boxtree.boxitem import BoxItem
from elsie.ext import unordered_list
from elsie.ext.list import ListBuilder
from elsie.text.textboxitem import TextBoxItem

from config import sh, sw

CODE_HIGHLIGHT_COLOR = "#FAAFAA"
CODE_HIDDEN_COLOR = "#BBBBBB"
COLOR_NOTE = "orange"
COLOR_BACKEND = "#001DB6"
COLOR_FRONTEND = "#FF0000"
DARK_GREEN = "#116466"

COLOR_ORANGE = "#F74C00"
QUOTATION_BG = "#CCCCCC"

LOWER_OPACITY = 0.4


def new_slides(width: int, height: int) -> Slides:
    return Slides(width=width, height=height)


def new_slide(slides: Slides):
    return slides.new_slide()


def slide_header(box: Box, text: str, return_header=False) -> Union[Box, Tuple[Box, Box]]:
    header = box.box(width="fill", height="10%").rect(bg_color=DARK_GREEN)
    row = header.box(horizontal=True)
    row.box().text(text, style=T(
        size=40,
        bold=True,
        color="#FFFFFF"
    ))

    content = box.box(height="fill", width="fill")
    if return_header:
        return (content, row)
    return content


def debug_steps(slides: Slides):
    for slide in slides._slides:
        for step in range(slide.steps()):
            slide.box().box(x=0, y=0, width=100, height=100, show=step + 1).text(f"Step {step + 1}")


# def slide_header(box: Box, text: str, text_style: Optional[TextStyle] = None, **box_args) -> Box:
#     text_style = text_style if text_style is not None else TextStyle(size=50)
#
#     if "p_bottom" not in box_args:
#         box_args["p_bottom"] = 40
#
#     box.box(**box_args).text(text, style=text_style)
#     return box


def list_item(parent, level=0, bullet="•", bullet_style="default", **box_args) -> Box:
    if level > 0 and "show" not in box_args:
        box_args["show"] = "last+"
    if level == 0 and "p_top" not in box_args and "padding" not in box_args:
        box_args["p_top"] = 10
    b = parent.box(x=level * 25, horizontal=True, **box_args)
    b.box(width=25, y=0).text(bullet, bullet_style)  # A bullet point
    return b.box(width="fill")


def code(parent: Box, code: str, language="python", width=None, code_style="code", p_right=50,
         return_parent: bool = False, **code_kwargs) -> TextBoxItem:
    content = parent.box(width=width)
    content.rect(bg_color="#EEEEEE")
    codebox = content.box(p_left=10, p_right=p_right, p_y=10, z_level=100, x=0)
    codebox = codebox.code(language, code.strip(), style=code_style, **code_kwargs)
    if return_parent:
        return content
    return codebox


def with_bg(parent: Box, bg_color="#DDDDDD", padding=10, **kwargs) -> Box:
    quote = parent.fbox()
    radius = 10
    quote.rect(bg_color=bg_color, rx=radius, ry=radius)
    return quote.fbox(p_x=sw(padding), p_y=sw(padding), z_level=100, **kwargs)


def bash(parent: Box, code: str, text_style=None, **box_args):
    if text_style is None:
        text_style = {}

    text_style.update({
        "color": "#E9E9ED",
        "font": "monospace",
        "align": "left"
    })

    wrapper = parent.box(**box_args)
    wrapper.rect(bg_color="#3F3F3F")
    code_wrapper = wrapper.box(x=0, p_x=10, p_y=5)
    return code_wrapper.text(code, style=T(**text_style))


def pointer_to_line(content, code_box, line, x, y, show,
                    textbox_pos=("0", "0"),
                    code_pos=("0", "0")):
    arrow = Arrow(20)
    line = code_box.line_box(line, show=show)
    text_box = content.box(x=x, y=y, show=show)
    content.box(show=show).line([text_box.p(textbox_pos[0], textbox_pos[1]),
                                 line.p(code_pos[0], code_pos[1])],
                                end_arrow=arrow, stroke_width=5, color="orange")
    return text_box


INVISIBLE_SPACE = "⠀"  # this is not a normal space, but U+2800


def code_step(parent: Box, code_content: str, show_start, line_steps, until_end=True, **code_args):
    show_start = int(show_start)

    code_content = code_content.strip()
    lines = code_content.split("\n")

    def get_line(lines, visible):
        if visible is None:
            return INVISIBLE_SPACE
        elif isinstance(visible, int):
            return lines[visible]
        else:
            return visible

    last = None
    for (step, visible_lines) in enumerate(line_steps):
        if len(visible_lines) < len(lines):
            visible_lines = list(visible_lines)
            visible_lines += [None] * (len(lines) - len(visible_lines))

        show = str(step + show_start)
        if step == len(line_steps) - 1 and until_end:
            show += "+"
        if step == 0:
            wrapper = parent.fbox(show=show)
        else:
            wrapper = parent.overlay(show=show)

        current_lines = [get_line(lines, visible) for visible in visible_lines]
        last = code(wrapper, "\n".join(current_lines), **code_args)
    return last


def code_reveal(parent: Box, code_content: str, show_start, reveal_steps, until_end=True, **code_step_args):
    code_content = code_content.strip()
    lines = code_content.split("\n")
    steps = []
    revealed = 0
    for to_reveal in reveal_steps:
        revealed += to_reveal
        assert revealed <= len(lines)
        steps.append(list(range(revealed)) + [None] * (len(lines) - revealed))
    return code_step(parent, code_content, show_start=show_start, line_steps=steps, until_end=until_end,
                     **code_step_args)


def code_line_by_line(parent: Box, code_content: str, show_start: int = 1, **code_args):
    line_count = len(code_content.strip().split("\n"))
    steps = [list(range(n + 1)) for n in range(line_count)]
    return code_step(parent, code_content, show_start=show_start, line_steps=steps, **code_args)


def with_border(parent: Box, color="red", padding=5, **box_args):
    return parent.box(**box_args).rect(color=color).box(padding=padding)


def with_coauthors(content: Box, authors):
    coauthors = content.box(x="[100%]", y=20, p_right=20)
    for author in authors:
        coauthors.box(x="[100%]", z_level=999).text(f"with {author}",
                                                    style=elsie.TextStyle(align="right"))


def left_side_list(box: Box) -> ListBuilder:
    return unordered_list(box.box(x=50, y=80))


def iterate_grid(rows: int, cols: int, width: int, height: int, p_horizontal: int = 0,
                 p_vertical: int = 0):
    row = 0
    col = 0
    for row_index in range(rows):
        for col_index in range(cols):
            yield (row, col)
            col += width + p_horizontal
        row += height + p_vertical
        col = 0


def big_text_slide(slide: Box, text: str):
    slide.box().text(text, style=T(size=60, bold=True))


def labeled_image(box: Box, img: str, label: str,
                  width: int, height: int,
                  x: Optional[int] = None, y: Optional[int] = None,
                  **box_args):
    box = box.box(x=x, y=y, width=width, height=height, **box_args)
    im_box = box.box(width=width, height=height)
    im_box.image(img)
    label_box = box.box(width=width, height=30)
    label_box.rect(bg_color=DARK_GREEN)
    label_box.fbox(p_top=5, p_bottom=5).text(label, style=T(color="white", bold=True))


def quotation(box: Box, quotation: str, source: str = "", **text_args) -> BoxItem:
    wrapper = box.fbox().rect(bg_color=QUOTATION_BG, rx=10, ry=10)
    inner = wrapper.box(padding=sw(30))

    if "size" not in text_args:
        text_args["size"] = sw(60)
    if "align" not in text_args:
        text_args["align"] = "left"

    quote_width = sw(60)
    inner.box(x=0, y=0, width=quote_width).image("images/quote.png", rotation=180)
    inner.box(x=inner.x("100%").add(-quote_width), y=inner.y("100%").add(-quote_width),
              width=quote_width).image("images/quote.png")
    inner.box(p_top=quote_width).text(quotation, style=T(**text_args))
    inner.box(width="100%", height=quote_width, p_top=sh(10), p_right=quote_width * 1.5,
              p_bottom=sh(20)).text(source, style=T(align="right", size=sw(50)))
    return wrapper


def generate_qr_code(content: str, scale=14) -> io.BytesIO:
    import segno
    qrcode = segno.make(content)
    buffer = io.BytesIO()
    qrcode.save(buffer, scale=scale, kind="png")
    buffer.seek(0)
    return buffer


def next_two_slides(box: Box, start=False) -> str:
    if start:
        return "1-2"
    return f"{box.current_fragment() + 1}-{box.current_fragment() + 2}"


def dimmed_list_item(parent: ListBuilder, text: str, show: int,
                     highlight_steps=0, **text_style) -> Box:
    wrapper = parent.item(show=f"{show}+")
    wrapper.box(show=f"{show + highlight_steps + 1}+").text(text, T(opacity=LOWER_OPACITY))
    wrapper.overlay(show=f"{show}-{(show + highlight_steps)}").text(text, T(**text_style))
    return wrapper


@dataclasses.dataclass
class Grid:
    top_left: Box
    top_right: Box
    bottom_left: Box
    bottom_right: Box


def create_grid(slide: Box) -> Grid:
    row = slide.box(horizontal=True, width="100%", height="50%")
    top_left, top_right = (row.box(width="50%", height="100%"), row.box(width="50%", height="100%"))

    row = slide.box(horizontal=True, width="100%", height="50%")
    bottom_left, bottom_right = (row.box(width="50%", height="100%"), row.box(width="50%", height="100%"))
    return Grid(
        top_left=top_left,
        top_right=top_right,
        bottom_left=bottom_left,
        bottom_right=bottom_right,
    )
