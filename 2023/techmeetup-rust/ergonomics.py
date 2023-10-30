from elsie import Arrow, SlideDeck, TextStyle as T
from elsie.boxtree.box import Box

from utils import bash, code, sh, sw


def ergonomics(slides: SlideDeck):
    @slides.slide()
    def cargo(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(20)).text("Cargo", T(bold=True))
        content.box(p_bottom=sh(40)).text("Integrated package manager")
        content.box(width=sw(800)).image("images/cargo-logo.svg")

    def cargo_cmd(parent: Box, title: str, command: str):
        parent.box(p_bottom=sh(20)).text(title)
        bash(parent.box(), f"$ cargo {command}", width=sw(600))

    @slides.slide()
    def cargo_check(slide: Box):
        cargo_cmd(slide.box(), "Type check", "check")

    @slides.slide()
    def cargo_build(slide: Box):
        content = slide.box()
        cargo_cmd(content, "Build", "build")
        content.box(show="next", p_top=sh(80)).image("images/target-binary.png")

    @slides.slide()
    def cargo_run(slide: Box):
        cargo_cmd(slide.box(), "Run", "run")

    @slides.slide()
    def cargo_test(slide: Box):
        slide.update_style("code", T(size=40))
        content = slide.box()
        row = content.box(horizontal=True)

        code_box = row.box()
        code(code_box, """
#[test]
fn test_add() {
    assert_eq!(add(1, 2), 3);
}""")
        row.box(padding=sw(50)).text("+", T(size=160))
        cargo_cmd(row.box(), "Test", "test")

        content.box(show="next").image("images/cargo-test.png")

    @slides.slide()
    def cargo_bench(slide: Box):
        slide.update_style("code", T(size=40))
        content = slide.box()
        row = content.box(horizontal=True)

        code_box = row.box()
        code(code_box, """
#[bench]
fn bench_add(b: &mut Bencher) {
    b.iter(|| add(1, 2));
}""")
        row.box(padding=sw(50)).text("+", T(size=160))
        cargo_cmd(row.box(), "Benchmark", "bench")

        content.box(show="next").image("images/cargo-bench.png")

    @slides.slide()
    def cargo_fmt(slide: Box):
        cargo_cmd(slide.box(), "Format code", "fmt")

    @slides.slide()
    def cargo_doc(slide: Box):
        slide.update_style("code", T(size=40))
        content = slide.box()
        row = content.box(show="1", horizontal=True)

        code_box = row.box()
        code(code_box, """
/// This function does something
fn my_func(a: u32) -> u32 {
    a + 1
}""")
        row.box(padding=sw(50)).text("+", T(size=160))
        cargo_cmd(row.box(), "Build documentation", "doc")

        slide.overlay(show="next").box().image("images/rust-docs.png")

    @slides.slide()
    def docs_rs(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(40)).text("Library (crate) documentation")
        content.box().text("~tt{https://docs.rs/<crate-name>}")

    @slides.slide()
    def cargo_semver_checks(slide: Box):
        slide.update_style("code", T(size=40))
        content = slide.box()
        cargo_cmd(content.box(), "Custom commands", "semver-checks")
        box = slide.overlay(show="next").box(width=sw(1800)).image("images/cargo-semver-checks.png")
        box.box(x=sw(500), y=box.y("100%").add(-sh(50)), width=sw(650), height=sh(60)).rect(
            color="red",
            stroke_width=8
        )

    @slides.slide()
    def dependencies(slide: Box):
        slide.update_style("code", T(size=40))

        content = slide.box()
        line = content.box(width="fill", horizontal=True)

        cargo = line.box(p_right=sw(250))
        cargo.box(p_bottom=sh(40)).text("Cargo.toml")
        cargo_code = code(cargo.box(), """
[package]
name = "hello_world"
version = "0.1.0"

[dependencies]
json = "1.0"
""", "toml")

        main = line.box(show="next+", y=0)
        main.box(p_bottom=sh(40)).text("main.rs")
        main_code = code(main.box(), """
use json::parse;

fn main() {
    parse(...);
}""")

        arrow = Arrow(20)
        p1 = cargo_code.children[-1].line_box(5).p("100%", "50%")
        p2 = main_code.children[-1].line_box(0).p(0, "50%")
        slide.box(show="last+").line([p1.add(-40, 0), p1, p2.add(-10, 0)],
                                     stroke_width=5, color="orange", end_arrow=arrow)

        content.box(show="next", p_top=sh(40)).text("120k+ crates available on crates.io")

    @slides.slide()
    def error_messages(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(40)).text("Error messages")
        msg_box = content.box(width=sw(1600), height=sh(600))
        for (index, msg) in enumerate((6, 4, 2, 3, 5)):
            msg_box.overlay(show="last" if index == 0 else "next").image(
                f"images/error-message-{msg}.png")

    # @slides.slide()
    # def utf8_strings(slide: Box):
    #     slide.update_style("code", T(size=50))
    #
    #     content = slide.box()
    #     content.box(p_bottom=sh(40)).text("Strings are UTF-8")
    #     code(content.box(), """let s = "Čau TechMeetupe ♥!";""")
