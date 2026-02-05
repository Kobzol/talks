import io
from typing import List, Tuple

from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import HideRest, ShowRest, StateCounter, code_step, last, quotation, show, skip


def do_not_stress_metrics(slides: Slides, tips: StateCounter):
    @slides.slide()
    def overheard(slide: Box):
        slide.box().text("Overheard on the internet:")
        quotation(slide.box(p_top=40), """We only have 90% test coverage,
but we want to reach 100% someday.""")

    @slides.slide()
    def coverage_types(slide: Box):
        """
        This is mostly what you get from tooling!
        """
        slide.box().text("Coverage types", T(size=80))

        lst = unordered_list(slide.box(p_top=80))
        lst.item(show="next+").text("Line coverage")
        lst2 = lst.ul()
        lst2.item(show="next+").text("This is usually what you get from tooling!", "small")
        lst.item(show="next+").text("Branch coverage")
        lst.item(show="next+").text("Path coverage")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Exponential!", "small")

    @slides.slide()
    def coverage_example(slide: Box):
        slide.update_style("code", T(size=44))
        width = 1750
        code_step(slide.fbox(), """
fn get_host_without_tld(mut text: &str) -> &str {
    if let Some(pos) = text.find("@") {
        text = &text[pos..];
    }
    &text[text.find(".").unwrap()..]
}

#[test]
fn test1() {
    get_host_without_tld("foo@bar.cz"); // 100% line coverage
    get_host_without_tld("bar.cz");     // 100% branch coverage
    get_host_without_tld("bar");        // Panic :-(
}
""", [
            show(6) + [HideRest],
            show(10) + skip(2) + last(1),
            show(11) + skip(1) + last(1),
            [ShowRest]
        ], width=width)

    @slides.slide()
    def coverage_chart(slide: Box):
        import seaborn as sns
        import matplotlib.pyplot as plt

        def render_chart(x: List[int], y: List[int]) -> io.BytesIO:
            plt.clf()
            with plt.xkcd():
                px = 1 / plt.rcParams["figure.dpi"]
                plt.figure(figsize=(1200 * px, 700 * px))

                ax = sns.lineplot(x=x, y=y)
                ax.tick_params(labelsize=20)
                ax.set_xlabel("Situations covered by tests", fontsize=36)
                ax.set_ylabel("(Line) code coverage (%)", fontsize=36)
                ax.ticklabel_format(style="plain", axis="y")
                ax.set_ylim(0.0, 119.0)
                ax.set_xlim(0.0, 100.0)
                ax.get_xaxis().set_ticks([])

                buffer = io.BytesIO()

                plt.tight_layout()
                plt.savefig(buffer, format="png")
                buffer.seek(0)
            return buffer

        def draw_arrow(src: Tuple[int, int], dst: Tuple[int, int], text: str, show: str,
                       xoffset: int = -150, yoffset: int = -50, color: str = "red"):
            slide.fbox(x=0, y=0, show=show).line((
                (src[0], src[1]),
                (dst[0], dst[1])
            ), color=color, stroke_width=6, end_arrow=Arrow(20))
            slide.box(x=src[0] + xoffset, y=src[1] + yoffset, show=show).text(text, T(size=40, bold=True, color=color))

        plot_a = render_chart([], [])
        slide.box(show="1", x="[50%]", y="[50%]").image(plot_a, image_type="png")

        plot_b = render_chart([0, 5, 10, 100], [0, 90, 100, 100])
        slide.box(show="next+", x="[50%]", y="[50%]").image(plot_b, image_type="png")

        draw_arrow((300, 150), (545, 358), "90% coverage", show="3+", color="red")
        draw_arrow((900, 500), (610, 315), "100% coverage", show="4+", xoffset=-120, yoffset=10, color="green")

        slide.fbox(x=0, y=0, show="next+").line((
            (610, 290),
            (610, 240),
            (1520, 240),
            (1520, 290),
        ), stroke_width=6, color="green")
        slide.box(x=800, y=120, show="last+").text("Also 100% coverage!", T(color="green", bold=True))

    @slides.slide()
    def dont_worry_about_metrics(slide: Box):
        tips.tip(slide, """Metrics can be useful
But don't worry about them too much""")
