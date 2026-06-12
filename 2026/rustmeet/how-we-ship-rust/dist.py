import datetime
from typing import Callable

from elsie import Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import bash, code, render_tag


def dist(slides: Slides):
    @slides.slide()
    def rust_distribution(slide: Box):
        """
        cargo-bisect-rustc can even unroll rollups.
        """
        slide.box().text("Every merged PR produces a full Rust distribution")

        code_size = 46
        width = 1700
        bash(slide.box(show="next+", p_top=80),
             "$ cargo bisect-rustc --start=2022-11-01 --end=1.92.0",
             text_style=dict(size=code_size), width=width)
        bash(slide.box(show="next+", p_top=-1), "$ rustup-toolchain-install-master <SHA>",
             text_style=dict(size=code_size), width=width)

    @slides.slide()
    def rustup_manifest(slide: Box):
        """
        rustup extracts all the required components into a single director (toolchain).
        """
        slide.update_style("code", T(size=30))

        render_tag(slide, "rustup manifest", kind="config")
        code(slide.box(y=200), """
[pkg.rustc.target.x86_64-unknown-linux-gnu]
available = true
url = "https://static.rust-lang.org/dist/2026-05-28/rustc-1.96.0-x86_64-unknown-linux-gnu.tar.gz"
hash = "71143d6075582b7e65233992c77e375aadbec4dfda6df2675160bf05b89410f9"
xz_url = "https://static.rust-lang.org/dist/2026-05-28/rustc-1.96.0-x86_64-unknown-linux-gnu.tar.xz"
xz_hash = "7d7fa1d0cfb0fab71a956bb78f41107202c17f30ab56c45288e869a37fd9633d"
components = []
extensions = []

[pkg.rustfmt-preview.target.x86_64-unknown-linux-gnu]
available = true
url = "https://static.rust-lang.org/dist/2026-05-28/rustfmt-1.96.0-x86_64-unknown-linux-gnu.tar.gz"
hash = "ffd93637216b3ea6792ea9677d0f16c2f8ac8e3ca1fdf0daef2d2de553933e63"
xz_url = "https://static.rust-lang.org/dist/2026-05-28/rustfmt-1.96.0-x86_64-unknown-linux-gnu.tar.xz"
xz_hash = "9754ab68f1b8871f8a714548f66d8d44e91f6d904505882945b27e6e3eeb08e2"
components = []
extensions = []

[pkg.rust-std.target.thumbv8r-none-eabihf]
available = false
components = []
extensions = []
""", language="toml")

    timeline_height = 5

    end_time = 3600 * 24 * 3
    baseline_date = datetime.datetime(year=2025, month=11, day=5)

    def render_tick(timeline: Box, pct: int, above: str, below: str, tick_width=8, width=120,
                    tick_color="black", **text_args):
        tick_height = tick_width * 4
        wrapper = timeline.box(
            width=width,
            x=timeline.x(f"{pct}%").add(-width / 2),
            y=timeline.y("50%").add(-tick_height / 2)
        )
        tick = wrapper.box(x="[50%]", y=0, width=tick_width, height=tick_height)
        tick.rect(bg_color=tick_color)

        ref_chars = 6 / len(below)
        ref_width = width / 100
        text_size = 30 * ref_chars * ref_width
        if "size" not in text_args:
            text_args["size"] = text_size

        wrapper.box(p_top=tick_height + width / 10).text(below, T(font="Ubuntu Mono", **text_args))
        wrapper.box(y=timeline.y("50%").add(-65)).text(above, T(size=30))

    def commit(timeline: Box, scale: int, time: int, commit: str):
        date = baseline_date + datetime.timedelta(seconds=time)

        is_nightly = "<nightly>" in commit
        above = ""

        width = 100
        tick_width = 8
        tick_color = "black"
        text_args = {}
        if is_nightly:
            commit = commit.replace("<nightly>", f'~bold{{nightly-{date.strftime("%Y-%m-%d")}}}')
            width = 400
            tick_width = 12
            tick_color = "blue"
            text_args = dict(size=30 * scale)

        width *= scale
        tick_width *= scale

        pct = round((time / end_time) * 100)
        render_tick(timeline, pct=pct, above=above, below=commit, tick_width=tick_width,
                    width=width, tick_color=tick_color, **text_args)

    def secs(h: int, m: int = 0, d: int = 0) -> int:
        return d * 3600 * 24 + h * 3600 + m * 60

    def render_nightlies(slide: Box, x: int, y: int, timeline_width: int,
                         show: Callable[[], str] = None, days: int = 4) -> Box:
        if show is None:
            show = lambda: "next+"
        scale = timeline_width / 1400
        wrapper = slide.box(x=x, y=y)
        timeline = wrapper.box(width=timeline_width, height=timeline_height)
        timeline.rect(bg_color="black")
        commit(timeline.fbox(show=show()), scale=scale, time=secs(h=4, m=31), commit="f5e2df")
        commit(timeline.fbox(show=show()), scale=scale, time=secs(h=14, m=2), commit="ab8741")
        commit(timeline.fbox(show=show()), scale, time=secs(h=2, m=50, d=1),
               commit="<nightly>\n(ab8741)")
        commit(timeline.fbox(show=show()), scale, time=secs(h=5, m=58, d=1), commit="082157")
        commit(timeline.fbox(show=show()), scale, time=secs(h=12, m=10, d=1), commit="292be5")
        commit(timeline.fbox(show=show()), scale, time=secs(h=18, m=37, d=1), commit="b2ee1b")
        commit(timeline.fbox(show=show()), scale, time=secs(h=3, m=14, d=2),
               commit="<nightly>\n(b2ee1b)")

        for d in range(days):
            time = d * 3600 * 24
            pct = round((time / end_time) * 100)
            height = 90 * scale
            date = baseline_date + datetime.timedelta(seconds=time)

            x = timeline.x(f"{pct}%")
            width = 100 * scale
            offset_y = 120 * scale
            slide.box(width=width, x=x.add(-width / 2), y=timeline.y(0).add(-offset_y)).text(
                date.strftime("%-d. %m."), T(size=30 * scale))
            slide.line(
                [
                    (x, timeline.y(0).add(-height / 2)),
                    (x, timeline.y("100%").add(height / 2))
                ],
                stroke_width=5 * scale,
                stroke_dasharray="4"
            )
        return timeline

    header_y = 120

    @slides.slide()
    def release_train(slide: Box):
        slide.box(y=header_y).text("Release train")

        step = 0

        def get_step():
            nonlocal step

            step += 1

            return f"{step + 1}+"

        render_nightlies(slide, x="[50%]", y="[50%]", timeline_width=1400, show=get_step)

    @slides.slide()
    def release_train_2(slide: Box):
        slide.set_style("mono", T(font="Ubuntu Mono", size=36))

        slide.box(y=header_y).text("Release train", T())
        timeline = render_nightlies(slide, x=300, y="300", timeline_width=100, show=lambda: "1+",
                                    days=46)

        nightly_y = timeline.y("50%")

        label_x = timeline.x(0).add(-220)
        slide.box(x=label_x, y=timeline.y(0).add(-45)).text("Nightly")

        beta_y = slide.box(x=label_x, y=timeline.y(0).add(200)).text("Beta").y("50%")
        stable_y = slide.box(x=label_x, y=timeline.y(0).add(400)).text("Stable").y(0)

        def ver_line(x: int, y_start: int, y_end: int, show: str):
            slide.fbox(show=show).line([
                (x, y_start),
                (x, y_end)
            ], color="black", stroke_width=timeline_height)

        def hor_line(x_start: int, x_end: int, y: int, show: str):
            slide.fbox(show=show).line([
                (x_start, y),
                (x_end, y)
            ], color="black", stroke_width=timeline_height)

        def label(x: int, y: int, text: str, show: str):
            slide.box(x=x, y=y.add(20), show=show).text(text, "mono")

        # Prolong nightly timeline
        hor_line(timeline.x("100%"), timeline.x(0).add(1500), nightly_y, show="1+")

        def branch(x: int, beta: str, stable: str, show: int):
            # Branch nightly => beta
            beta_x = x
            beta_x_end = beta_x + 400
            ver_line(beta_x, nightly_y, beta_y, show=f"{show}+")
            label(beta_x, beta_y, beta, show=f"{show}+")

            # Branch beta => stable
            hor_line(beta_x, beta_x_end, beta_y, show=f"{show + 1}+")
            ver_line(beta_x_end, beta_y, stable_y, show=f"{show + 2}+")
            label(beta_x_end - 50, stable_y, stable, show=f"{show + 2}+")

            slide.box(x=beta_x + 100, y=beta_y.add(-60), show=f"{show + 1}+").text("6 weeks",
                                                                                   T(size=50))

        branch(400, "beta-2025-11-05", "1.91.0", show=2)
        branch(820, "beta-2025-12-21", "1.92.0", show=5)

    # @slides.slide()
    # def release_train_3(slide: Box):
    #     slide.box(p_bottom=40).text("Release train", T(size=80))
    #
    #     items = [
    #         "New stable release every 6 weeks, no matter what",
    #         "No big deal if a feature misses the train",
    #         "Reduces contributor stress"
    #     ]
    #     lst = unordered_list(slide.box())
    #     for (step, item) in enumerate(items, start=1):
    #         dimmed_list_item(lst, item, show=step, last=item == items[-1])

    @slides.slide(bg_color="#2E2459")
    def release_team(slide: Box):
        slide.box(width=1400).image("images/team-release.png")

    @slides.slide()
    def release_thursday(slide: Box):
        """
        Cloud function (lambda) on AWS.
        Takes ~2 hours.
        """
        render_tag(slide, "promote-release", kind="tool")

        slide.box(p_bottom=40).text("Release Thursday (every 6 weeks)", T(size=80))
        bash(slide.box(), "$ ./scripts/start-release.py publish-rust-prod-stable",
             text_style=dict(size=50))

        lst = unordered_list(slide.box(p_top=80))
        lst.item(show="next+").text("Recompresses tarballs for maximum compression")
        lst.item(show="next+").text("Runs on a 72 vCPU cloud machine")
        lst.item(show="next+").text("Takes ~2 hours to complete", escape_char="#")

    @slides.slide()
    def rust_10_celebration(slide: Box):
        """
        If you're wondering where am I on this photo, this is my hand.
        """
        slide.box(p_bottom=40).text("Rust 10 year anniversary (1.87.0 release)", T(size=80))
        slide.box(width=1600).image("images/rust-10-year-celebration.jpg")

    @slides.slide(bg_color="#181A1B")
    def release_blog_post(slide: Box):
        slide.box(width=1400).image("images/rust-release-blog-post.png")
