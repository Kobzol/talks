from typing import Any, Iterable, Tuple

from elsie import Arrow, Slides
from elsie.boxtree.box import Box
from elsie.boxtree.lazy import LazyPoint
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import CI_ICON, GITHUB_BG, INTELLIJ_BG, bors_tag, chapter, code, dimmed_list_item, \
    migration, opt_dist_tag, render_tag, rustc_perf_tag, source, triagebot_tag


def ci(slides: Slides):
    chapter_name = "Continous integration pipelines"

    @slides.slide()
    def ci_scale(slide: Box):
        chapter(slide, chapter_name, CI_ICON, sub="Dealing with our scale")

    @slides.slide(bg_color=GITHUB_BG)
    def ci_job_statistics(slide: Box):
        slide.box(width=1800).image("images/gh-jobs-statistics.png")

    @slides.slide(bg_color=GITHUB_BG)
    def ci_usage_statistics(slide: Box):
        slide.box(width=1700).image("images/gh-usage-statistics.png")

    @slides.slide()
    def github_agreement(slide: Box):
        slide.box(width=1600).image("images/github-agreement.png")

    @slides.slide()
    def marco_optimizations(slide: Box):
        """
        At most 8 PRs merged per day.
        """
        slide.box(width=1600).image("images/marco-optimizations.png")
        source(slide, 'How We Made the Rust CI 75% Cheaper by Marco Ieni @ RustConf 2025')

    @slides.slide()
    def rollup_creation(slide: Box):
        """
        This is one of the reasons why we cannot use GitHub merge queues directly.
        """
        bors_tag(slide)
        slide.box().text("Rollups (PR batching)")
        slide.box(width=1800).image("images/rollup-creation.png")

    @slides.slide(bg_color=GITHUB_BG)
    def rollup(slide: Box):
        bors_tag(slide)
        slide.box(width=1400).image("images/rollup.png")

    @slides.slide()
    def ci_definition(slide: Box):
        chapter(slide, chapter_name, CI_ICON, sub="Defining CI jobs")

    arrow = Arrow(size=30)

    def connect(slide: Box, a: Box, b: Box, src: str | Tuple[Any, Any] = "bottom",
                dst: str | Tuple[Any, Any] = "top"):
        def get(box: Box, anchor: str | Tuple[Any, Any]) -> LazyPoint | Tuple[Any, Any]:
            if anchor == "bottom":
                x, y = ("50%", "100%")
            elif anchor == "right":
                x, y = ("100%", "50%")
            elif anchor == "top":
                x, y = ("50%", "0")
            elif anchor == "left":
                x, y = ("0", "50%")
            else:
                return anchor
            return box.p(x, y)

        slide.box(show="last+").line((
            get(a, src),
            get(b, dst),
        ), color="black", stroke_width=8, end_arrow=arrow)

    @slides.slide()
    def ci_diagram(slide: Box):
        slide.box(y=20).text("~tt{rust-lang/rust} GitHub Actions workflow")

        x_start = 100
        y_start = 20

        def box(x: int, y: int, name: str, icon: str, show="last+") -> Box:
            box = slide.box(x=x_start + x, y=y_start + y, show=show)
            box.rect(color="black", stroke_width=8)
            inner = box.box(padding=20, horizontal=True)
            inner.box(width=80).image(f"images/{icon}")
            inner.box(width=20)
            inner.box().text(name)
            return box

        ci = box(100, 100, "ci.yml", "memo.svg")
        citool = box(100, 300, "citool", "rust-logo.png", show="next+")
        connect(slide, ci, citool)
        jobs = box(600, 300, "jobs.yml", "memo.svg", show="next+")
        connect(slide, jobs, citool, "left", "right")
        gh_env = box(600, 460, "GitHub env", "github-logo.png", show="next+")
        connect(slide, gh_env, citool, "left", "right")

        def step_right(a: Box, b: Box):
            slide.box(show="last+").line((
                a.p("50%", "100%"),
                (a.x("50%"), b.y("50%")),
                b.p("0", "50%")
            ), color="black", stroke_width=8, end_arrow=arrow)

        x = 600
        docker = box(x, 700, "Docker", "docker-logo.svg", show="next+")
        bootstrap = box(x + 500, 700, "bootstrap", "rust-logo.png")
        connect(slide, docker, bootstrap, "right", "left")
        slide.box(x=400, y=y_start + 620, width=100, show="last+").image("images/linux-logo.svg")
        step_right(citool, docker)

        makefile = box(x, 900, "Makefile", "make-logo.svg", show="next+")
        bootstrap = box(x + 500, 900, "bootstrap", "rust-logo.png")
        connect(slide, makefile, bootstrap, "right", "left")
        slide.box(x=400, y=y_start + 840, width=100, show="last+").image("images/windows-logo.svg")
        slide.box(x=550, y=y_start + 840, width=100, show="last+").image("images/macos-logo.svg")
        step_right(citool, makefile)

        lst = unordered_list(slide.box(x="[90%]", y="[20%]"))
        items = [
            ("PR CI", "10"),
            ("Try build", "1-20"),
            ("Merge", "85")
        ]
        for (name, count) in items:
            row = lst.item(show="next+").box(horizontal=True)
            row.box(width=280).text(f"{name}:")
            row.box(width=260).text(f"{count} jobs", T(align="right"))

    @slides.slide()
    def job_matrix(slide: Box):
        slide.box(p_bottom=40).text("Job matrix", T(size=80))

        lst = unordered_list(slide.box())
        lst.item(show="last+").text("Architectures (x64, x86, ARM64, RISC-V, PowerPC, …)")
        lst.item(show="next+").text("OSes (Linux, Windows, macOS, NetBSD, Illumos, …)")
        lst.item(show="next+").text("Special use-cases (Cranelift/GCC backend, Rust for Linux, …)")

    @slides.slide(bg_color=INTELLIJ_BG)
    def jobs_yml(slide: Box):
        """
        If the job definition looks small, that is because it is redirected to a Dockerfile.
        """
        render_tag(slide, "jobs.yml", kind="config")
        slide.box(x=500, width=800).image("images/jobs-yml.png")

    @slides.slide()
    def dockerfile(slide: Box):
        render_tag(slide, "Dockerfile", kind="config")

        slide.update_style("code", T(size=38))
        code(slide.box(y=130), """
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \\
  g++ \\
  make \\
  libssl-dev \\
  pkg-config \\
  xz-utils \\
  zlib1g-dev \\
  && rm -rf /var/lib/apt/lists/*

COPY scripts/sccache.sh /scripts/
RUN sh /scripts/sccache.sh

ENV RUST_CONFIGURE_ARGS="--build=x86_64-unknown-linux-gnu \\
 --enable-sanitizers \\
 --enable-profiler \\
 --enable-compiler-docs \\
 --set llvm.libzstd=true"
ENV SCRIPT="python3 ../x.py --stage 2 test"
""", language="Dockerfile")

    @slides.slide()
    def test_vs_dist(slide: Box):
        slide.box().text("~bold{test} vs ~bold{dist} jobs", T(size=80))

    @slides.slide()
    def platform_support(slide: Box):
        slide.box(p_bottom=40).text("Rust platform support", T(size=80))

        style = dict(size=50)

        lst = unordered_list(slide.box(x=500), show=None)
        dimmed_list_item(lst, "Tier 1", show=2, highlight_steps=3)
        lst2 = lst.ul()
        dimmed_list_item(lst2, "x64 Linux/Windows, ARM64 macOS, …", show=3, highlight_steps=2,
                         **style)
        dimmed_list_item(lst2, "Must pass tests", show=4, highlight_steps=1, **style)
        dimmed_list_item(lst2, "~bold{test} + ~bold{dist} CI jobs", show=5, **style)
        dimmed_list_item(lst, "Tier 2", show=6, highlight_steps=3)
        lst2 = lst.ul()
        dimmed_list_item(lst2, "PowerPC/RISC-V/LoongArch Linux, ARM64 iOS, …", show=7,
                         highlight_steps=2, **style)
        dimmed_list_item(lst2, "Must build", show=8, highlight_steps=1, **style)
        dimmed_list_item(lst2, "~bold{dist} CI jobs", show=9, **style)
        lst.item(show="last+").text("Tier 3")
        lst2 = lst.ul()
        lst2.item(show="next+").text("AVR, Nintendo Switch, …", T(**style))
        lst2.item(show="next+").text("Usually not tested or built on CI", T(**style))

    @slides.slide(bg_color=GITHUB_BG)
    def citool_rewrite(slide: Box):
        """
        https://github.com/rust-lang/rust/pull/136864
        """
        migration(slide, ["python", "rust"], bg="white")
        slide.box(width=1600).image("images/citool-rewrite-python-rust.png")

    @slides.slide()
    def optimizations(slide: Box):
        chapter(slide, chapter_name, CI_ICON, sub="Build optimizations")

    @slides.slide()
    def pgoltoboltwtfbbq(slide: Box):
        slide.box(p_bottom=40).text("PGOLTOBOLTWTFBBQ pipeline", T(size=80))
        slide.box(show="next+").text("Goal: optimize the heck out of ~tt{rustc} (and LLVM)")

    step_counter = 0

    def step(slide: Box, text: str):
        nonlocal step_counter
        slide.box(y=60).text(f"Step {step_counter}: {text}", T(size=70))
        step_counter += 1

    @slides.slide()
    def pgo_diagram_0(slide: Box):
        """
        CentOS 7 (glibc 2.17)
        GCC 4.8 => GCC 9.5
        GCC 9.5 => CMake and zstd
        GCC 9.5 => Clang 22.1
        Build rustc-perf
        """
        step(slide, "prepare build environment")

        lst = unordered_list(slide.box())
        lst.item(show="next+").text("CentOS 7 (glibc 2.17)")
        lst.item(show="next+").text("GCC 4.8 builds GCC 9.5")
        lst.item(show="next+").text("GCC 9.5 builds CMake")
        lst.item(show="next+").text("GCC 9.5 builds Clang 22.1")
        lst.item(show="next+").text("Clang 22.1 builds zstd")
        lst.item(show="next+").text("Beta rustc builds ~tt{rustc-perf}")

    legend = (
        ("llvm-logo.png", "LLVM", "llvm"),
        ("rust-logo.png", "rustc", "rustc"),
        ("stopwatch.svg", "rustc-perf", "rustc-perf"),
        ("bar-chart.svg", "Profile", "profile"),
        ("gear.svg", "PGO", "pgo"),
        ("bolt.svg", "BOLT", "bolt"),
        ("racing-car.svg", "Optimized", "opt"),
        ("looking-glass.svg", "Instrumented", "instr"),
    )

    def render_legend(slide: Box):
        lst = unordered_list(slide.box(x="[98%]", y="[50%]"), label="")
        for (logo, name, _) in legend:
            row = lst.item(label="").box(horizontal=True, p_bottom=5)
            row.box(width=80).image(f"images/{logo}")
            row.box(width=20)
            row.box().text(name)

    def tag_to_icon(target: str) -> str:
        for (icon, _, tag) in legend:
            if tag == target:
                return icon
        raise Exception(f"Icon for tag {target} not found")

    x_start = 50
    y_start = 300

    def item(slide: Box, x: int, y: int, item: str, tags: Iterable[str] = (),
             show: str = "next+", reuse: bool = False) -> Box:
        box = slide.box(x=x_start + x, y=y_start + y, width=150, show=show)
        box.image(f"images/{tag_to_icon(item)}")
        if tags:
            row = box.box(x="100%", y=-40, horizontal=True)
            col = row.box(y=0)
            for (index, tag) in enumerate(tags):
                if index % 2 == 0 and index != 0:
                    col = row.box(y=0)
                col.box(height=70).image(f"images/{tag_to_icon(tag)}")
        if reuse:
            box.box(x=-30, y="60%", width=60).image("images/repeat.svg")
        return box

    @slides.slide()
    def pgo_diagram_rustc_pgo(slide: Box):
        """
        Build LLVM
        Build PGO instrumented rustc
        Gather rustc PGO profiles with PGO instrumented rustc and LLVM
        Build PGO-optimized rustc
        """
        opt_dist_tag(slide)
        render_legend(slide)
        step(slide, "Optimize rustc with PGO")

        x = 50
        item(slide, x, 100, "llvm")
        rustc = item(slide, x, 260, "rustc", ("pgo", "instr"))

        def move(amount: int) -> int:
            nonlocal x
            x += amount
            return x

        y = 180
        perf = item(slide, move(350), y, "rustc-perf")
        connect(slide, rustc, perf, (rustc.x("150%"), perf.y("50%")), "left")
        profile = item(slide, move(280), y, "profile", ("pgo", "rustc"))
        connect(slide, perf, profile, "right", "left")
        pgo_rustc = item(slide, move(350), y, "rustc", ("pgo", "opt"))
        connect(slide, profile, pgo_rustc, (profile.x("150%"), pgo_rustc.y("50%")), "left")

    @slides.slide()
    def pgo_diagram_llvm_pgo(slide: Box):
        """
        Build PGO instrumented LLVM
        Gather LLVM PGO profiles with PGO optimized rustc and PGO instrumented LLVM
        Build PGO optimized LLVM
        """
        opt_dist_tag(slide)
        render_legend(slide)
        step(slide, "Optimize LLVM with PGO")

        x = 50
        item(slide, x, 100, "llvm", ("pgo", "instr"))
        rustc = item(slide, x, 240, "rustc", ("pgo", "opt"), reuse=True)

        def move(amount: int) -> int:
            nonlocal x
            x += amount
            return x

        y = 180
        perf = item(slide, move(350), y, "rustc-perf")
        connect(slide, rustc, perf, (rustc.x("150%"), perf.y("50%")), "left")
        profile = item(slide, move(280), y, "profile", ("pgo", "llvm"))
        connect(slide, perf, profile, "right", "left")
        pgo_llvm = item(slide, move(350), y, "llvm", ("pgo", "opt"))
        connect(slide, profile, pgo_llvm, (profile.x("150%"), pgo_llvm.y("50%")), "left")

    @slides.slide()
    def pgo_diagram_llvm_bolt(slide: Box):
        """
        Prepare BOLT instrumented PGO optimized LLVM
        Gather BOLT LLVM profiles
        Generate PGO + BOLT optimized LLVM
        """
        opt_dist_tag(slide)
        render_legend(slide)
        step(slide, "Gather LLVM BOLT profiles")

        x = 50
        item(slide, x, 100, "llvm", ("pgo", "opt", "bolt", "instr"))
        rustc = item(slide, x, 240, "rustc", ("pgo", "opt"), reuse=True)

        def move(amount: int) -> int:
            nonlocal x
            x += amount
            return x

        y = 180
        perf = item(slide, move(350), y, "rustc-perf")
        connect(slide, rustc, perf, (rustc.x("150%"), perf.y("50%")), "left")
        profile = item(slide, move(280), y, "profile", ("bolt", "llvm"))
        connect(slide, perf, profile, "right", "left")
        bolt_llvm = item(slide, move(350), y, "llvm", ("pgo", "opt", "bolt", "opt"))
        connect(slide, profile, bolt_llvm, (profile.x("150%"), bolt_llvm.y("50%")), "left")

    @slides.slide()
    def pgo_diagram_rustc_bolt(slide: Box):
        """
        Prepare BOLT instrumented PGO optimized rustc
        Gather BOLT rustc profiles
        Generate PGO + BOLT optimized rustc
        """
        opt_dist_tag(slide)
        render_legend(slide)
        step(slide, "Gather rustc BOLT profiles")

        x = 50
        item(slide, x, 100, "llvm", ("pgo", "opt", "bolt", "opt"), reuse=True)
        rustc = item(slide, x, 240, "rustc", ("pgo", "opt", "bolt", "instr"))

        def move(amount: int) -> int:
            nonlocal x
            x += amount
            return x

        y = 180
        perf = item(slide, move(400), y, "rustc-perf")
        connect(slide, rustc, perf, (rustc.x("200%"), perf.y("50%")), "left")
        profile = item(slide, move(250), y, "profile", ("bolt", "rustc"))
        connect(slide, perf, profile, "right", "left")
        bolt_rustc = item(slide, move(350), y, "rustc", ("pgo", "opt", "bolt", "opt"))
        connect(slide, profile, bolt_rustc, (profile.x("150%"), bolt_rustc.y("50%")), "left")

    @slides.slide()
    def pgo_artifacts(slide: Box):
        opt_dist_tag(slide)
        render_legend(slide)

        x = 50
        y = 0
        item(slide, x, y, "rustc", ("pgo", "opt", "bolt", "opt"), show="last+")
        item(slide, x + 350, y, "llvm", ("pgo", "opt", "bolt", "opt"), show="last+")
        radius = 30
        wrapper = slide.box(x=80, y=y + 240, width=700, height=220, show="next+").rect(color="black", stroke_width=8, rx=radius, ry=radius)
        package = slide.box(x=1000, y=y + 275, width=150, show="last+").image(f"images/package.svg")
        connect(slide, wrapper, package, "right", "left")

        y = 300
        x_orig = x

        def move(amount: int) -> int:
            nonlocal x
            x += amount
            return x

        item(slide, x, y, "profile", ("pgo", "rustc"))
        item(slide, move(250), y, "profile", ("pgo", "llvm"), show="last+")
        x = x_orig
        y += 200
        item(slide, x, y, "profile", ("bolt", "rustc"), show="last+")
        item(slide, move(250), y, "profile", ("bolt", "llvm"), show="last+")
        wrapper = slide.box(x=80, y=y + 50, width=520, height=420, show="next+").rect(color="black", stroke_width=8, rx=radius, ry=radius)
        package = slide.box(x=1000, y=y + 185, width=150, show="last+").image(f"images/package.svg")
        connect(slide, wrapper, package, "right", "left")

        @slides.slide()
        def opt_dist_log(slide: Box):
            slide.update_style("code", T(size=40))
            code(slide.box(), """
-----------------------------------------------------------------
Stage 1 (Rustc PGO):                            2483.80s (25.11%)
  Build PGO instrumented rustc and LLVM:        1483.16s (14.99%)
  Gather profiles:                               618.16s ( 6.25%)
  Build PGO optimized rustc:                     382.48s ( 3.87%)
Stage 2 (LLVM PGO):                              662.24s ( 6.69%)
  Build PGO instrumented LLVM:                   316.84s ( 3.20%)
  Gather profiles:                               343.60s ( 3.47%)
Stage 3 (BOLT):                                 3462.31s (35.00%)
  Build PGO optimized LLVM:                      789.52s ( 7.98%)
  Gather LLVM profiles:                          526.34s ( 5.32%)
  Gather rustc profiles:                        1568.64s (15.86%)
Stage 5 (final build):                          3115.98s (31.50%)
Run tests:                                       168.81s ( 1.71%)

Total duration:                                        2h 44m 53s
-----------------------------------------------------------------
""", language="text")

            box = slide.box(show="next+", x="[50%]", y="[50%]", z_level=999)
            box.rect(color="black", stroke_width=8, bg_color="white", rx=30, ry=30)
            inner = box.box(p_x=40, p_y=20)
            inner.text("~40% performance win", T(size=100), escape_char="#")

    @slides.slide(bg_color=GITHUB_BG)
    def opt_dist_bash(slide: Box):
        render_tag(slide, "pgo.sh", kind="tool")
        slide.box(width=1400, x=300).image("images/pgo-sh.png")

    @slides.slide(bg_color=GITHUB_BG)
    def opt_dist_rewrite_bash_python(slide: Box):
        """
        https://github.com/rust-lang/rust/pull/103019
        """
        migration(slide.box(p_bottom=10), ["bash", "python"], bg="white")
        slide.box(width=1200).image("images/opt-dist-rewrite-bash-python.png")

    @slides.slide(bg_color=GITHUB_BG)
    def opt_dist_rewrite_rust_question(slide: Box):
        slide.box(width=1600).image("images/opt-dist-rewrite-rust-question.png")

    @slides.slide()
    def a_few_months_later(slide: Box):
        slide.box().image("images/a-few-months-later.png")

    @slides.slide(bg_color=GITHUB_BG)
    def opt_dist_rewrite_python_rust(slide: Box):
        """
        https://github.com/rust-lang/rust/pull/112235
        """
        migration(slide, ["python", "rust"], bg="white")
        slide.box(width=1600).image("images/opt-dist-rewrite-python-rust.png")

    @slides.slide()
    def merge(slide: Box):
        chapter(slide, chapter_name, CI_ICON, sub="Post-merge operations")

    @slides.slide(bg_color=GITHUB_BG)
    def bors_pr_merged(slide: Box):
        bors_tag(slide)
        slide.box(width=1600).image("images/bors-pr-merged.png")
        slide.box(p_top=40).image("images/tada.svg")

    @slides.slide()
    def dist(slide: Box):
        slide.box(p_bottom=40).text("Every ~bold{dist} job ends with uploading artifacts to S3")

    @slides.slide(bg_color=GITHUB_BG)
    def dist_artifacts(slide: Box):
        slide.box(y=100).text("CI dist artifacts", T(size=80, color="white"))

        width = 900
        y = 300
        slide.box(width=width, x=100, y=y).image("images/dist-artifacts-1.png")
        slide.box(width=width, x=1000, y=y + 5).image("images/dist-artifacts-2.png")

    @slides.slide(bg_color=GITHUB_BG)
    def post_merge_analysis(slide: Box):
        render_tag(slide, "citool", kind="tool")
        slide.box(width=1200).image("images/post-merge-analysis.png")

    @slides.slide(bg_color=GITHUB_BG)
    def rollup_unrolled(slide: Box):
        """
        We will of course run compiler performance benchmarks on the merged PR.
        """
        rustc_perf_tag(slide)
        slide.box(width=1300).image("images/rollup-unrolled.png")

    @slides.slide(bg_color=GITHUB_BG)
    def pr_relnotes_tag(slide: Box):
        slide.box().image("images/pr-relnotes-tag.png")

    @slides.slide(bg_color=GITHUB_BG)
    def pr_relnotes_tracking_issue(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1400, y=100).image("images/pr-relnotes-tracking-issue.png")

    @slides.slide()
    def thanks_1(slide: Box):
        render_tag(slide, "thanks", kind="tool")
        slide.box(width=1600).image("images/thanks-rlo.png")

    @slides.slide()
    def thanks_2(slide: Box):
        render_tag(slide, "thanks", kind="tool")
        slide.box(width=1400).image("images/thanks-1.96.0.png")
