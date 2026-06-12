from typing import Optional

from elsie import Arrow, Slides
from elsie.boxtree.box import Box
from elsie.ext import ordered_list, unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import BUILD_ICON, GITHUB_BG, INTELLIJ_BG, SHELL_BG, bash, bootstrap_tag, chapter, \
    render_tag


def implementation(slides: Slides):
    @slides.slide(bg_color="#0F1419")
    def rustc_dev_guide(slide: Box):
        slide.box(p_bottom=40).image("images/rustc-dev-guide.png")
        slide.box().text("~tt{https://rustc-dev-guide.rust-lang.org}", T(color="white"))

    @slides.slide()
    def impl(slide: Box):
        chapter(slide, "Implementation", BUILD_ICON, sub="Managing git repositories")

    @slides.slide(bg_color="#2E3436")
    def git_clone(slide: Box):
        slide.box(width=1800).image("images/git-clone.png")

    @slides.slide()
    def repos(slide: Box):
        def box(x: int, y: int, name: str, kind: Optional[str] = None, show: str = "last+") -> Box:
            wrapper = slide.box(x=x, y=y, show=show)
            parent = wrapper.box()
            parent.rect(color="black", stroke_width=4, rx=10, ry=10)
            box = parent.box(padding=30)
            box.text(name, "tt")
            if kind is not None:
                wrapper.box().text(kind)
            return parent

        def arrow(src: Box, dst: Box, onesided: bool = False, x: Optional[str] = None):
            arrow = Arrow(size=30)
            y = src.y("100%").add(75)

            src_x = dst.x("50%") if x is None else src.x(x)
            slide.box(show="last+").line((
                (src_x, src.y("100%")),
                (src_x, y),
                (dst.x("50%"), y),
                (dst.x("50%"), dst.y("0"))
            ), color="black", stroke_width=4, start_arrow=None if onesided else arrow,
                end_arrow=arrow)

        rlr = box("[50%]", 100, "rust-lang/rust")
        llvm = box(100, 400, "LLVM", "submodule", show="next+")
        arrow(rlr, llvm, onesided=True, x="20%")

        clippy = box(800, 400, "Clippy", show="next+", kind="git subtree")
        arrow(rlr, clippy)
        miri = box(1200, 400, "Miri", show="next+", kind="Josh subtree")
        arrow(rlr, miri, x="80%")

        lst = unordered_list(slide.box(y=700))
        lst.item(show="2+").text("12 submodules")
        lst.item(show="3+").text("6 git subtrees")
        lst.item(show="4+").text("5 Josh subtrees")

    @slides.slide(bg_color="#161923")
    def josh(slide: Box):
        slide.box(width=1600).image("images/josh-blog-post.png")

    @slides.slide(bg_color=GITHUB_BG)
    def josh_sync(slide: Box):
        render_tag(slide, "josh-sync", kind="tool")
        slide.box(width=1600).image("images/josh-sync.png")

    width = 1500

    @slides.slide()
    def josh_sync_pull(slide: Box):
        render_tag(slide, "josh-sync", kind="tool")
        slide.box(p_bottom=40).text(
            "Pull changes from ~tt{rust-lang/rust} into e.g. ~tt{rust-analyzer}")
        bash(slide.box(), "$ rustc-josh-sync pull", width=width)
        slide.box(width=1300, x="[50%]", y=150, show="next+").image("images/josh-pull.png")

    @slides.slide()
    def josh_sync_push(slide: Box):
        render_tag(slide, "josh-sync", kind="tool")
        slide.box(p_bottom=40).text(
            "Push changes from e.g. ~tt{rust-analyzer} to ~tt{rust-lang/rust}")
        bash(slide.box(), "$ rustc-josh-sync push <branch> <fork>", width=width)
        slide.box(width=1300, x="[50%]", y=150, show="next+").image("images/josh-push.png")

    @slides.slide()
    def building_the_compiler(slide: Box):
        chapter(slide, "Implementation", BUILD_ICON, sub="Building the compiler")

    @slides.slide()
    def bootstrap(slide: Box):
        slide.box().text("Bootstrap", T(size=80))
        slide.box().text("= build system of the Rust toolchain")

    # @slides.slide(bg_color=GITHUB_BG)
    # def bootstrap_makefile_1(slide: Box):
    #     bootstrap_tag(slide)
    #     slide.box(width=1800).image("images/bootstrap-makefile-1.png")

    @slides.slide(bg_color=GITHUB_BG)
    def bootstrap_makefile_2(slide: Box):
        bootstrap_tag(slide)
        slide.box(width=1700, y=150).image("images/bootstrap-makefile-2.png")

    @slides.slide(bg_color=GITHUB_BG)
    def bootstrap_rust(slide: Box):
        bootstrap_tag(slide)
        slide.box(width=1500).image("images/bootstrap-rust.png")

    @slides.slide()
    def x(slide: Box):
        bootstrap_tag(slide)

        slide.box(p_bottom=80).text("~tt{./x <cmd>}", T(size=80))

        lst = ordered_list(slide.box())
        items = [
            ("Find the right Python interpreter", "bash-logo.png"),
            ("Run bootstrap.py", "bash-logo.png"),
            ("Download stage0 rustc and cargo", "python-logo.svg"),
            ("Build and execute (Rust) bootstrap", "python-logo.svg"),
            ("Checkout submodules", "rust-logo.png"),
            ("Download pre-compiled LLVM from CI", "rust-logo.png"),
            ("Execute <cmd>", "rust-logo.png")
        ]
        boxes = []
        for (index, (item, _)) in enumerate(items, start=2):
            row = lst.item(p_bottom=15, show="next+").text(item)
            boxes.append(row)
        for (index, (box, (_, lang))) in enumerate(zip(boxes, items)):
            slide.box(width=80, x=1600, y=box.y("0%"), show=f"{index + 2}+").image(f"images/{lang}")

    @slides.slide(bg_color=SHELL_BG)
    def x_help(slide: Box):
        bootstrap_tag(slide)
        slide.box(width=1600, y=200).image("images/x-help.png")

    @slides.slide(bg_color=SHELL_BG)
    def x_setup(slide: Box):
        bootstrap_tag(slide)
        slide.box().image("images/x-setup.png")

    @slides.slide(bg_color=INTELLIJ_BG)
    def bootstrap_toml(slide: Box):
        render_tag(slide, "bootstrap.toml", kind="config")
        slide.box(width=1600).image("images/bootstrap-toml.png")

    @slides.slide(bg_color=INTELLIJ_BG)
    def bootstrap_changelog(slide: Box):
        bootstrap_tag(slide)
        slide.box(width=1700).image("images/bootstrap-change-id.png")

    @slides.slide(bg_color=SHELL_BG)
    def x_setup_editor(slide: Box):
        bootstrap_tag(slide)
        slide.box(width=1400).image("images/x-setup-editor.png")

    @slides.slide()
    def bootstrap_diagram(slide: Box):
        slide.box(p_bottom=20).text("Bootstrapping rustc (~tt{./x build})", T(size=80))
        slide.box(width=1500).image("images/bootstrap-diagram.svg", show_begin=2)

    @slides.slide(bg_color="#161922")
    def dev_desktops(slide: Box):
        slide.box(width=1700).image("images/dev-desktops.png")

    @slides.slide(bg_color="#161922")
    def errs_compiler_talk(slide: Box):
        slide.box(width=1600).image("images/errs-compiler-talk.png")
