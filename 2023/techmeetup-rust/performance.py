import io
from typing import List

import pandas as pd
from elsie import SlideDeck, Arrow, TextStyle as T
from elsie.boxtree.box import Box

from config import sh, sw
from utils import quotation, code, QUOTATION_BG


def performance(slides: SlideDeck):
    @slides.slide()
    def zero_cost(slide: Box):
        """
        No GC, tight data layout, minimal runtime, embedded platforms.
        """
        content = slide.box()
        content.box(p_bottom=sh(80)).text("Zero-cost abstractions")

        quotation(content.box(show="next"), """What you don’t use, you don’t pay for.
What you do use, you couldn’t hand code any better.""", "Bjarne Stroustrup")

    @slides.slide()
    def no_gc(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(40)).text("No GC")
        content.box(width=sw(1400)).image("images/gc.svg")

    # @slides.slide()
    # def compilation_flow(slide: Box):
    #     content = slide.box()
    #     content.box(p_bottom=sh(40)).text("Compilation flow")
    #     content.box(width=sw(500), height=sh(600)).image("images/llvm-flow.svg")

    @slides.slide()
    def iterator(slide: Box):
        padding = 30

        content = slide.box()
        content.box(p_bottom=sh(40)).text("(LLVM) optimizations")

        src = content.box(width=sw(1600), p_bottom=sh(padding))
        src.image("images/godbolt-dot-product-u32.png")

        arrow = Arrow(30)
        arrow_box = content.box(show="next+", height=sh(80))
        arrow_box.line([
            arrow_box.p("50%", "0%"),
            arrow_box.p("50%", "100%")
        ], stroke_width=15, color="orange", end_arrow=arrow)

        assembly = content.box(width=sw(1200), show="last", p_top=sh(padding))
        assembly.image("images/godbolt-dot-product-assembly-u32.png")

    @slides.slide()
    def parallelization(slide: Box):
        slide.update_style("code", T(size=50))
        slide.set_style("red", T(color="red"))

        content = slide.box()
        content.box(p_bottom=sh(40)).text("Parallelization")

        code_width = sw(600)
        source_box = content.box(width=code_width)
        code(source_box.box(show="1"), """
fn sum_of_squares(input: &[i32]) -> i32 {
    input.iter()
         .map(|&i| i * i)
         .sum()
}""", width=code_width)
        code_box = code(source_box.overlay(show="next"), """
fn sum_of_squares(input: &[i32]) -> i32 {
    input.par_iter()
         .map(|&i| i * i)
         .sum()
}""", width=code_width)
        code_box.children[-1].line_box(1).box(x=sw(355), width=sw(400), height=sh(90)).rect(
            color="red", stroke_width=8)

    @slides.slide()
    def tenable(slide: Box):
        slide.overlay().box(width=sw(1600)).image("images/rust-tenable.png")
        slide.overlay(show="next").box(width=sw(1400)).image("images/tenable-cpu.png")
        slide.overlay(show="next").box(width=sw(1400)).image("images/tenable-memory.png")
        quotation(slide.overlay(show="next").box(), """With this small change, we were able
to optimize away over 700 CPU and 300GB of memory.
This was all implemented, tested and deployed in two weeks.""", "Tenable")

    @slides.slide()
    def tilde(slide: Box):
        slide.overlay().box(width=sw(1600)).image("images/rust-tilde.png")
        slide.overlay(show="next+").box(width=sw(1400)).image("images/tilde-memory.png")
        quotation(slide.overlay(show="next").box(), """After rewriting of the agent in Rust,
the agent consistently used 8 MB: 92% smaller!""", "Tilde")

    @slides.slide()
    def discord(slide: Box):
        slide.overlay(show="1").box(width=sw(1600)).image("images/discord-rust.png")
        overlay = slide.overlay(show="next+")

        def label(box: Box, text: str):
            box.box(width=sw(200)).rect(bg_color=QUOTATION_BG).box(padding=10).text(text)
            box.box(width=sw(100))

        chart_width = 1200
        top = overlay.box(width="fill", horizontal=True, p_bottom=sh(40))
        label(top, "Go")
        top.box(width=sw(chart_width)).image("images/discord-response-go.png")

        arrow = Arrow(30)
        arrow_box = overlay.box(height=sh(80))
        arrow_box.line([
            arrow_box.p("50%", "0%"),
            arrow_box.p("50%", "100%")
        ], stroke_width=15, color="orange", end_arrow=arrow)

        bottom = overlay.box(width="fill", horizontal=True, p_top=sh(40))
        label(bottom, "Rust")
        bottom.box(width=sw(chart_width)).image("images/discord-response-rust.png")
        quotation(slide.overlay(show="next").box(), """Notice the average time is now measured in microseconds.""",
                  "Discord")

    @slides.slide()
    def cloud_functions(slide: Box):
        slide.box(width=sw(1600)).image("images/rust-serverless.png")

    @slides.slide()
    def nodejs(slide: Box):
        slide.box(width=sw(1600)).image("images/rust-nodejs.png")

    def render_plot(data):
        import seaborn as sns
        import matplotlib.pyplot as plt

        seaborn_palette = sns.color_palette()
        palette = [seaborn_palette[0], seaborn_palette[3], seaborn_palette[1]]
        palette = palette[:len(data["language"].unique())]

        plt.clf()
        params = {"legend.handlelength": 4, "legend.handleheight": 4}
        plt.rcParams.update(params)
        with plt.xkcd():
            px = 1 / plt.rcParams["figure.dpi"]
            plt.figure(figsize=(sw(1800) * px, sh(900) * px))

            ax = sns.lineplot(data, x="time", y="perf", hue="language", palette=palette,
                              linewidth=5)
            ax.set(xticks=[], yticks=[])
            fontsize = 40
            ax.set_xlabel("Time", fontsize=fontsize)
            ax.set_ylabel("Performance", fontsize=fontsize)
            ax.set(ylim=[0, 15])

            sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
            plt.setp(ax.get_legend().get_texts(), fontsize="32")
            plt.setp(ax.get_legend().get_title(), fontsize="32")

            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
        return buffer

    @slides.slide()
    def time_to_performance(slide: Box):
        def make_data(name: str, y: List[int]) -> pd.DataFrame:
            assert len(y) == 10
            return pd.DataFrame(dict(time=list(range(len(y))), perf=y, language=[name] * len(y)))

        slide.box().text("Time to performance")
        chart_box = slide.box(width="fill")

        python_data = make_data("Python", [1, 3.2, 5, 6, 6.5, 7, 7.2, 7.3, 7.4, 7.5])
        cpp_data = make_data("C++", [1, 2, 4, 6, 7.5, 9, 10.5, 11, 11.4, 11.8])
        rust_data = make_data("Rust", [1, 5, 6.5, 7.5, 9, 10.5, 11, 11.2, 11.3, 11.4])

        plot1 = render_plot(python_data)
        chart_box.box().image(plot1, image_type="png")

        plot2 = render_plot(pd.concat((python_data, cpp_data)))
        chart_box.overlay(show="next+").image(plot2, image_type="png")

        plot3 = render_plot(pd.concat((python_data, cpp_data, rust_data)))
        chart_box.overlay(show="next+").image(plot3, image_type="png")
