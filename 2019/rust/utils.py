from typing import Tuple, Union

from elsie import Arrow, TextStyle as s
from elsie.boxtree.box import Box
from elsie.text.textboxitem import TextBoxItem

CODE_HIGHLIGHT_COLOR = "#FAAFAA"
CODE_HIDDEN_COLOR = "#BBBBBB"


def slide_header(box: Box, text: str, return_header=False) -> Union[Box, Tuple[Box, Box]]:
    header = box.box(width="fill", height="10%")
    row = header.box(horizontal=True)
    row.box().text(text, style=s(
        size=40,
        bold=True
    ))

    content = box.box(height="fill", width="fill")
    if return_header:
        return (content, row)
    return content


def list_item(parent, level=0, **box_args) -> Box:
    b = parent.box(x=level * 25, horizontal=True, **box_args)
    b.box(width=25, y=0).text("•")  # A bullet point
    return b.box(width="fill")


def code(parent: Box, code: str, language="rust", width=None, code_style="code") -> TextBoxItem:
    content = parent.box(width=width)
    content.rect(bg_color="#EEEEEE")
    codebox = content.box(p_left=10, p_right=50, p_y=10, z_level=100, x=0)
    return codebox.code(language, code, style=code_style)


def with_bg(parent: Box, bg_color="#DDDDDD") -> Box:
    quote = parent.box()
    quote.rect(bg_color=bg_color)
    return quote.box(padding=10, z_level=100)


def bash(parent: Box, code: str, text_style=None, **box_args):
    if text_style is None:
        text_style = s()

    text_style = text_style.compose(s(
        color="#E9E9ED",
        font="monospace"
    ))

    wrapper = parent.box(**box_args)
    wrapper.rect(bg_color="#3F3F3F")
    code_wrapper = wrapper.box(x=0, p_x=10, p_y=5)
    return code_wrapper.text(code, style=text_style)


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


def code_step(parent: Box, code_content: str, show_start, line_steps, **code_args):
    invisible_space = "⠀"  # this is not a normal space, but U+2800
    show_start = int(show_start)

    code_content = code_content.strip()
    lines = code_content.split("\n")

    def get_line(lines, visible):
        if visible is None:
            return invisible_space
        elif isinstance(visible, int):
            return lines[visible]
        else:
            return visible

    last = None
    for (step, visible_lines) in enumerate(line_steps):
        assert len(visible_lines) == len(lines)

        show = str(step + show_start)
        if step == len(line_steps) - 1:
            show += "+"
        wrapper = parent.overlay(show=show)

        current_lines = [get_line(lines, visible) for visible in visible_lines]
        last = code(wrapper, "\n".join(current_lines), **code_args)
    return last


def with_border(parent: Box, color="red", padding=5, **box_args):
    return parent.box(**box_args).rect(color=color).box(padding=padding)
