from typing import List, Optional, Tuple, Union

from elsie import Arrow, TextStyle
from elsie.boxtree.box import Box

from config import sh, sw


def draw_node(box: Box, color="black", bg_color: Optional[str] = None, **kwargs):
    box.polygon([
        (box.x("25%"), box.y(0)),
        (box.x("75%"), box.y(0)),
        (box.x("100%"), box.y("50%")),
        (box.x("75%"), box.y("100%")),
        (box.x("25%"), box.y("100%")),
        (box.x(0), box.y("50%")),
    ], color=color, bg_color=bg_color, **kwargs)


def node(box: Box, x=0, y=0, size=30, color="black", bg_color: Optional[str] = None,
         node_args=None, **box_args) -> Box:
    node_box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size, **box_args)
    node_args = {
        "stroke_width": sw((size / 30) * 3)
    } if node_args is None else node_args
    draw_node(node_box, color=color, bg_color=bg_color, **node_args)
    return node_box


def cluster_1(box: Box, size: int, node_constructor=None, **box_args) -> List[Box]:
    height = size * 3
    box = box.box(width=size * 3, height=height, **box_args)
    x_increment = size * 0.9
    y_increment = size / 2 + sh(6)

    if node_constructor is None:
        node_constructor = lambda box, x, y, size, diagonal, index: node(box, x=x, y=y, size=size)

    nodes = []
    for diagonal in range(3):
        items = 3 - diagonal
        x = size / 2 + (x_increment * diagonal)
        y = (height * 0.5) - (y_increment * diagonal)

        for index in range(items):
            node_box = node_constructor(box=box, x=x, y=y, size=size, diagonal=diagonal,
                                        index=index)
            nodes.append(node_box)
            x += x_increment
            y += y_increment
    return nodes


def task(box: Box, x=0, y=0, size=100, name: Optional[str] = None,
         style: Union[str, TextStyle] = "default", bg_color="white",
         color="black", show: Optional[str] = None) -> Box:
    box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size, z_level=2, show=show)
    box.box(width="50%", height="50").rect(bg_color="white")
    box.image("imgs/task.svg")
    return box


BoxOrPos = Union[Box, Tuple[int, int]]


def edge(box: Box, start: BoxOrPos, end: BoxOrPos, dep=True):
    arrow = Arrow(size=16, stroke_width=5)

    def normalize(pos: BoxOrPos) -> Tuple[int, int]:
        if isinstance(pos, Box):
            return (pos.x("50%"), pos.y("50%"))
        return pos

    box.line(
        points=(normalize(start), normalize(end)),
        end_arrow=arrow,
        color="black",
        stroke_width=5,
        stroke_dasharray=4 if not dep else None
    )


def task_top(box: Box) -> Tuple[int, int]:
    return (box.x("50%"), box.y(-5))


def task_bottom(box: Box) -> Tuple[int, int]:
    return (box.x("50%"), box.y("100%"))


def task_point(box: Box, x: Union[int, str], y: Union[int, str]) -> Tuple[int, int]:
    return (box.x(x), box.y(y))


def task_graph_3(box: Box, size: int) -> Tuple[Box, Box, Box, Box]:
    dim = size * 3
    box = box.box(width=dim, height=dim)

    y = size / 2
    x = size / 2

    style = TextStyle(size=size / 2)
    t1 = task(box, x, y, name="t1", size=size, style=style)
    t2 = task(box, x + size * 2, y, name="t2", size=size, style=style)
    t3 = task(box, x, y + size * 2, name="t3", size=size, style=style)
    t4 = task(box, x + size * 2, y + size * 2, name="t4", size=size, style=style)
    t5 = task(box, x + size, y + size * 4, name="t5", size=size, style=style)
    edge(box, task_point(t1, "50%", "50%"), task_top(t3))
    edge(box, task_point(t1, "50%", "50%"), task_point(t4, "25%", 0))
    edge(box, task_point(t2, "50%", "50%"), task_top(t4))
    edge(box, task_point(t3, "50%", "50%"), task_point(t5, "25%", 0))
    edge(box, task_point(t4, "50%", "50%"), task_point(t5, "75%", 0))

    return (t1, t2, t3, t4)
