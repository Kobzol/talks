import random
from typing import Optional

import elsie
from elsie import Arrow, TextStyle
from elsie.boxtree.box import Box

from config import sh, sw
from tasks import cluster_1, node
from utils import image


def header(slide: Box, text: str, ok: Optional[bool] = None, step: Optional[str] = None):
    header = slide.box(horizontal=True, height=sh(120), y=sh(50), show=step)
    header.box(p_right=sw(40)).text(text, TextStyle(size=sw(70)))
    if ok is not None:
        img = "checkmark" if ok else "crossmark"
        header.box(width=sw(50)).image(f"imgs/{img}.png")


def challenges(slides: elsie.Slides):
    image(slides, "imgs/wrong.svg")

    @slides.slide()
    def large_jobs(slide: Box):
        header(slide, "A few large tasks", ok=True)

        cols = slide.box(horizontal=True)
        left = cols.box()

        for i in range(3):
            left.box(width=sw(100), p_top=sh(40)).image("imgs/task.svg")

        right = cols.box(p_left=sw(200))
        cluster_box = right.box()
        cluster_1(cluster_box.fbox(show=1), size=sw(100))

        def filled_node(box, x, y, size, diagonal, index):
            box = node(box, x=x, y=y, size=size)
            if index == 0:
                box.box(width=sw(80)).image("imgs/task.svg")
            return box

        cluster_1(cluster_box.overlay(show=2), size=sw(100), node_constructor=filled_node)

    @slides.slide()
    def many_jobs(slide: Box):
        header(slide, "Many tasks", ok=False, step="1-3")
        header(slide, "Heterogeneous tasks", ok=False, step="4")
        header(slide, "Task dependencies", ok=False, step="5")

        cols = slide.box(horizontal=True)
        left = cols.box()

        tasks = []
        task_rows = 8
        task_cols = 16
        for row in range(task_rows):
            row = left.box(horizontal=True, p_top=sh(20))
            for col in range(task_cols):
                task = row.box(width=sw(55), p_left=sw(10)).image("imgs/task.svg")
                task.fbox(padding=sw(10), show="5+").rect(bg_color="white")
                tasks.append(task)

        right = cols.box(p_left=sw(150), horizontal=True, show="2+")
        submits = right.box(show="2-3")
        for _ in range(15):
            submits.box().text("sbatch script.sh")
        submits.box().text("...")

        slurm = right.box()
        text = slurm.box(width=sw(100), height=sh(100))
        text.overlay(show="4").text("?", TextStyle(size=sw(70), bold=True))
        text.overlay(show="5").text("???!", TextStyle(size=sw(70), bold=True))
        slurm.box(p_left=sw(40)).image("imgs/slurm.svg")
        right.box(width=sw(300), x=sw(80), y=sh(180), show="3").image("imgs/prohibited.svg")

        colours = ["red", "green", "blue", "orange"]
        random.seed(42)
        for (index, task) in enumerate(tasks):
            path = f"imgs/task-{random.choice(colours)}.svg"
            task.overlay(show="4+").image(path)

            row = index // task_cols
            col = index % task_cols
            if row == task_rows - 1:
                continue

            candidates = [col -1] if col != 0 else []
            candidates.append(col)
            if col != task_cols - 1:
                candidates.append(col + 1)
            random.shuffle(candidates)
            targets = [c for c in candidates if random.random() < 0.5]
            for target_col in targets:
                offset = 0
                if target_col < col:
                    offset = 10
                elif target_col > col:
                    offset = -10
                target_index = (row + 1) * task_cols + target_col
                target = tasks[target_index]
                slide.box(show="5+", z_level=-1).line((
                    (task.x("50%"), task.y("50%")),
                    (target.x("50%").add(sw(offset)), target.y("10%"))
                ), stroke_width=sw(3), end_arrow=Arrow())

    @slides.slide()
    def heterogeneity(slide: Box):
        line_box = slide.overlay(show="2+")

        row = slide.box(horizontal=True)
        nodes = cluster_1(row.box(), size=sw(100))
        node = nodes[5]
        big_node = row.box(width=sw(1000)).image("imgs/heterogeneous-node.svg", show_begin=2)

        line_box.line((
            (node.x("25%"), node.y(0)),
            (big_node.x("32%"), big_node.y("25%"))
        ), stroke_width=sw(4), stroke_dasharray="4")
        line_box.line((
            (node.x("25%"), node.y("100%")),
            (big_node.x("32%"), big_node.y("79%"))
        ), stroke_width=sw(4), stroke_dasharray="4")

    image(slides, "imgs/map.svg")

    @slides.slide()
    def intertwined(slide: Box):
        slide.update_style("default", TextStyle(size=sw(60)))
        slide.box(p_bottom=sh(40)).text("Slurm/PBS approach:", style=TextStyle(bold=True))
        slide.box(show="next+").text("What to compute (tasks) +")
        slide.box(show="next+").text("Where to compute it (nodes)")
        slide.box(show="next+").text("=> always defined together")
