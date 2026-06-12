import io
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union

import elsie
import pandas as pd
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
GITHUB_BG = "#0D1117"
INTELLIJ_BG = "#1E1F22"
ZULIP_BG = "#222222"
SHELL_BG = "#2E3436"

LOWER_OPACITY = 0.3

DESIGN_ICON = "lightbulb.svg"
BUILD_ICON = "hammer-and-spanner.svg"
TEST_ICON = "checkmark.svg"
REVIEW_ICON = "looking-glass.svg"
CI_ICON = "gear.svg"
OPT_ICON = "racing-car.svg"
CRATER_ICON = "checkmark.svg"
GIT_ICON = "git-logo.svg"
RELEASE_ICON = "package.svg"


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
         return_codebox=False, **code_kwargs) -> Union[Box, TextBoxItem]:
    content = parent.box(width=width)
    content.rect(bg_color="#EEEEEE")
    box = content.box(p_left=10, p_right=p_right, p_y=10, z_level=100, x=0)
    codebox = box.code(language, code.strip(), style=code_style, **code_kwargs)
    if return_codebox:
        return codebox
    return box


def with_bg(parent: Box, bg_color="#DDDDDD") -> Box:
    quote = parent.box()
    quote.rect(bg_color=bg_color)
    return quote.box(padding=10, z_level=100)


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
    code_wrapper = wrapper.box(x=0, p_left=10, p_right=50, p_y=10)
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


def quotation(box: Box, quotation: str, source: Optional[str] = None, **text_args) -> BoxItem:
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
    source = source or ""
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
                     highlight_steps=0, last=False, **text_style):
    if not last:
        wrapper = parent.item(show=f"{show}+")
        wrapper.box(show=f"{show + highlight_steps + 1}+").text(text, T(opacity=LOWER_OPACITY, **text_style))
        wrapper.overlay(show=f"{show}-{(show + highlight_steps)}").text(text, T(**text_style))
    else:
        parent.item(show=f"{show}+").text(text, **text_style)


def render_tag(slide: Box, name: str, show=None, kind: str = "bot"):
    if kind == "bot":
        image = "robot"
    elif kind == "docs":
        image = "docs"
    elif kind == "config":
        image = "memo"
    elif kind == "tool":
        image = "hammer-and-spanner"
    else:
        raise Exception(f"Invalid tag {kind}")

    box = slide.box(x=15, y=15, show=show, z_level=999)
    radius = 30
    box.rect(bg_color=QUOTATION_BG, rx=radius, ry=radius, color="black", stroke_width=4)
    wrapper = box.fbox(padding=10, p_right=15, horizontal=True)
    wrapper.box(width=90, p_right=20).image(f"images/{image}.svg")
    wrapper.box().text(name, T(color="black", size=60))


def triagebot_tag(slide: Box, **kwargs):
    render_tag(slide, "triagebot", **kwargs)


def triagebot_config_tag(slide: Box):
    render_tag(slide, "triagebot.toml", kind="config")


def crater_tag(slide: Box):
    render_tag(slide, "crater")


def rustc_perf_tag(slide: Box):
    render_tag(slide, "rustc-perf")


def bors_tag(slide: Box):
    render_tag(slide, "bors")


def bootstrap_tag(slide: Box):
    render_tag(slide, "bootstrap", kind="tool")


def opt_dist_tag(slide: Box):
    render_tag(slide, "opt-dist", kind="tool")


def topic(box: Box, name: str, icon: str, show=None):
    row = box.fbox(horizontal=True, show=show, p_bottom=10)
    row.box(width=140).image(f"images/{icon}")
    row.fbox(p_left=30).text(name, T(align="left", size=70))


def render_plot(data, ylabel: str = "Count"):
    import seaborn as sns
    import matplotlib.pyplot as plt

    data["date"] = pd.to_datetime(data["date"])

    plt.clf()
    with plt.xkcd():
        px = 1 / plt.rcParams["figure.dpi"]
        plt.figure(figsize=(1440 * px, 810 * px))

        ax = sns.lineplot(data=data, x="date", y="count")
        ax.tick_params(labelsize=20)
        ax.set_xlabel("Year", fontsize=32)
        ax.set_ylabel(ylabel, fontsize=32)
        ax.set_xlim(pd.Timestamp("2014-07-01"), pd.Timestamp("2026-04-01"))

        buffer = io.BytesIO()

        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
    return buffer


def source(slide: Box, text: str, show: Optional[str] = None):
    text = f"Source: {text}"
    slide.box(show=show, x="[96%]", y="[98%]").text(text, T(size=sw(40)))


@dataclass
class Chapter:
    name: str
    sub_chapters: List[str] = field(default_factory=list)


CHAPTERS: List[Chapter] = []


def chapter(slide: Box, name: str, icon: str, sub: Optional[str] = None):
    global CHAPTERS

    start = len(CHAPTERS) == 0 or name != CHAPTERS[-1].name

    if sub is not None and not start:
        CHAPTERS[-1].sub_chapters.append(sub)
    else:
        subs = [] if sub is None else [sub]
        CHAPTERS.append(Chapter(name=name, sub_chapters=subs))

    chapter = CHAPTERS[-1]

    col = slide.box()
    row = col.box(horizontal=True)
    row.box(p_right=50, width=160).image(f"images/{icon}")
    row.box().text(chapter.name, T(size=80))

    lst = unordered_list(col.box(p_top=30))
    for (index, sub) in enumerate(chapter.sub_chapters):
        opacity = LOWER_OPACITY if index != len(chapter.sub_chapters) - 1 else 1.0
        lst.item().text(sub, T(opacity=opacity))


MIGRATION_COUNTERS = {}

def migration(slide: Box, languages: List[str], size: int = 100, bg: Optional[str] = None):
    global MIGRATION_COUNTERS

    assert len(languages) == 2

    lang_tuple = tuple(languages)
    if lang_tuple in MIGRATION_COUNTERS:
        MIGRATION_COUNTERS[lang_tuple] += 1
    else:
        MIGRATION_COUNTERS[lang_tuple] = 1

    row = slide.box()
    if bg is not None:
        row.rect(bg_color=bg, rx=30, ry=30)
    row = row.fbox(horizontal=True, padding=10)
    images = {
        "bash": "bash-logo.png",
        "python": "python-logo.svg",
        "rust": "rust-logo.png",
        "make": "make-logo.svg"
    }
    arrow = Arrow(size=30)
    padding = 30
    for (index, lang) in enumerate(languages):
        row.box(width=size).image(f"images/{images[lang]}")
        if index != len(languages) - 1:
            box = row.box(width=150)
            box.line((
                (box.x("0").add(padding), box.y("50%")),
                (box.x("100%").add(-padding), box.y("50%"))
            ), color="black", stroke_width=8, end_arrow=arrow)
