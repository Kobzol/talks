import io
from typing import Optional, Tuple, Union

import elsie
import pandas as pd
from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.boxtree.boxitem import BoxItem
from elsie.ext import unordered_list
from elsie.ext.list import ListBuilder
from matplotlib.ticker import FuncFormatter

from config import sh, sw

CODE_HIGHLIGHT_COLOR = "#FAAFAA"
CODE_HIDDEN_COLOR = "#BBBBBB"
COLOR_NOTE = "orange"
COLOR_BACKEND = "#001DB6"
COLOR_FRONTEND = "#FF0000"
DARK_GREEN = "#116466"

COLOR_ORANGE = "#F74C00"
QUOTATION_BG = "#CCCCCC"

LOWER_OPACITY = 0.3


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


def code(parent: Box, code: str, language="rust", width=None, code_style="code", p_right=50,
         **code_kwargs) -> Box:
    content = parent.box(width=width)
    content.rect(bg_color="#EEEEEE")
    codebox = content.box(p_left=10, p_right=p_right, p_y=10, z_level=100, x=0)
    codebox.code(language, code.strip(), style=code_style, **code_kwargs)
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


def code_step(parent: Box, code_content: str, show_start, line_steps, **code_args):
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
        if step == len(line_steps) - 1:
            show += "+"
        wrapper = parent.overlay(show=show)

        current_lines = [get_line(lines, visible) for visible in visible_lines]
        last = code(wrapper, "\n".join(current_lines), **code_args)
    return last


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


def quotation(box: Box, quotation: str, source: str, **text_args) -> BoxItem:
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
              p_bottom=sh(20)).text(source, style=T(align="right", size=sw(70)))
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
                     highlight_steps=0, **text_style):
    wrapper = parent.item(show=f"{show}+")
    wrapper.box(show=f"{show + highlight_steps + 1}+").text(text, T(opacity=LOWER_OPACITY))
    wrapper.overlay(show=f"{show}-{(show + highlight_steps)}").text(text, T(**text_style))


def source(slide: Box, text: str, show: Optional[str] = None):
    text = f"Source: {text}"
    slide.box(show=show, x="[96%]", y="[98%]").text(text, T(size=sw(40)))


def render_plot(data, yaxis_formatter=None):
    import seaborn as sns
    import matplotlib.pyplot as plt

    data["date"] = pd.to_datetime(data["date"])

    plt.clf()
    with plt.xkcd():
        px = 1 / plt.rcParams["figure.dpi"]
        plt.figure(figsize=(1200 * px, 700 * px))

        ax = sns.lineplot(data=data, x="date", y="count")
        ax.tick_params(labelsize=20)
        ax.set_xlabel("Year", fontsize=20)
        ax.set_ylabel("Count", fontsize=20)
        ax.ticklabel_format(style="plain", axis="y")
        ax.set_xlim(pd.Timestamp("2014-07-01"), pd.Timestamp("2024-04-14"))
        if yaxis_formatter is not None:
            ax.yaxis.set_major_formatter(FuncFormatter(yaxis_formatter))

        # ticks, labels = plt.xticks()
        # ticks = list(ticks)
        # x_diff = ticks[-1] - ticks[-2]
        # ticks = ticks + [ticks[-1] + x_diff]
        # labels = labels + [plt.Text(ticks[-1] + x_diff, 0, "2025")]
        # assert len(ticks) == len(labels)
        # plt.xticks(ticks=ticks, labels=labels)

        buffer = io.BytesIO()

        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
    return buffer


def survey_quotation(slide: Box, question: str, answer: str, percent: float, question_size: int = 55):
    wrapper = slide.box(x="[50%]", y="[50%]").rect(bg_color="#ACE2E1", rx=10, ry=10)
    inner = wrapper.box(padding=30)
    inner.box().text(question, T(size=sw(question_size), italic=True))
    inner.box(width="100%", height=sh(8), p_top=sh(4)).rect(bg_color="black")
    inner.box(p_top=sh(80)).text(f'"{answer.strip()}"', T(size=sw(60)))

    text = f"{percent:.2f}"
    if text.endswith("00"):
        text = text[:text.index(".")]
    elif text.endswith("0"):
        text = text[:-1]
    inner.box(p_top=sh(40)).text(f"{text}%", T(bold=True))

    inner.box(x="[100%]", y="[100%]", width=sw(120)).image("images/chart-icon.svg")

    survey_source(slide, str(slide.current_fragment()))

def survey_source(slide: Box, show: Optional[str] = None):
    source(slide, "Rust Annual 2023 survey", show=show)
