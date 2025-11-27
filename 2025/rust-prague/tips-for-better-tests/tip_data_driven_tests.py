from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box

from shared import BOOTSTRAP_TEST_CODE, BOOTSTRAP_TEST_CODE_ASSERT
from utils import StateCounter, project, code, aka, bash


def data_driven_tests(slides: Slides, tips: StateCounter):
    @slides.slide()
    def data_driven_tests(slide: Box):
        """
        Tests no longer compile (refactoring) vs tests fail.
        """
        tips.tip(slide, "Make tests data-driven")
        width = 1000
        aka(slide, "Make tests blessable", width=width)
        aka(slide, "Use snapshot/expect tests", width=width)

    @slides.slide()
    def bootstrap(slide: Box):
        slide.update_style("code", T(size=40))
        project(slide, "bootstrap (Rust compiler build system)")
        code(slide.box(y=130), BOOTSTRAP_TEST_CODE_ASSERT)

    @slides.slide()
    def bootstrap_insta(slide: Box):
        slide.update_style("code", T(size=40))
        project(slide, "bootstrap (Rust compiler build system)")
        code(slide.box(y=130), BOOTSTRAP_TEST_CODE)

    @slides.slide()
    def cargo_insta(slide: Box):
        """
        Code review to check validity.
        """
        bash(slide, "$ cargo insta review", width=1000, height=100)
        slide.box(width=1400, p_top=40, show="next+").image("images/cargo-insta.png")

    @slides.slide()
    def bors_snapshot_test(slide: Box):
        project(slide, "bors")
        slide.update_style("code", T(size=44))
        code(slide.box(), """
bors
    .post_comment("@bors try parent=last")
    .await?;

insta::assert_snapshot!(
    bors.get_next_comment_text(()).await?,
    @":exclamation: There was no previous build.
    Please set an explicit parent or remove the
    `parent=last` argument to use the default parent."
);
""")

    @slides.slide()
    def ui_tests_test(slide: Box):
        project(slide, "Rust compiler UI test suite")
        slide.box(width=1000).image("images/ui-tests-files.png")

    width = 1800
    code_y = 150

    @slides.slide()
    def ui_test_code(slide: Box):
        project(slide, "Rust compiler UI test suite")

        row = slide.box(horizontal=True, x="[90%]", y="[4%]")
        row.box(p_bottom=40).text("assign-imm-local-twice.rs", T(font="Ubuntu Mono"))
        row.box(width=50)
        row.box(width=80, y=10).image("images/write.svg")
        code(slide.box(y=code_y), """
//@ run-rustfix

fn main() {
    let v: isize;
    //~^ HELP consider making this binding mutable
    //~| SUGGESTION mut
    v = 1;
    //~^ NOTE first assignment
    println!("v={}", v);
    v = 2;
    //~^ ERROR cannot assign twice to immutable variable
    //~| NOTE cannot assign twice to immutable
    println!("v={}", v);
}
""", width=width)

    @slides.slide()
    def ui_test_stderr(slide: Box):
        project(slide, "Rust compiler UI test suite")
        slide.update_style("code", T(size=40))

        row = slide.box(horizontal=True, x="[90%]", y="[4%]")
        row.box(p_bottom=40).text("assign-imm-local-twice.stderr", T(font="Ubuntu Mono"))
        row.box(width=50)
        row.box(width=80, y=10).image("images/stars.svg")
        code(slide.box(y=code_y), """
error[E0384]: cannot assign twice to immutable variable `v`
  --> $DIR/assign-imm-local-twice.rs:17:5
   |
LL |     v = 1;
   |     ----- first assignment to `v`
…
LL |     v = 2;
   |     ^^^^^ cannot assign twice to immutable variable
   |
help: consider making this binding mutable
   |
LL |     let mut v: isize;
   |         +++

error: aborting due to 1 previous error

For more information about this error, try `rustc --explain E0384`.    
""", width=width)

    @slides.slide()
    def ui_test_fixed(slide: Box):
        project(slide, "Rust compiler UI test suite")

        row = slide.box(horizontal=True, x="[90%]", y="[4%]")
        row.box(p_bottom=40).text("assign-imm-local-twice.fixed", T(font="Ubuntu Mono"))
        row.box(width=50)
        row.box(width=80, y=10).image("images/stars.svg")
        code(slide.box(y=code_y), """
//@ run-rustfix

fn main() {
    let mut v: isize;
    //~^ HELP consider making this binding mutable
    //~| SUGGESTION mut
    v = 1;
    //~^ NOTE first assignment
    println!("v={}", v);
    v = 2;
    //~^ ERROR cannot assign twice to immutable variable
    //~| NOTE cannot assign twice to immutable
    println!("v={}", v);
}
""", width=width)

    @slides.slide()
    def ui_test_diff(slide: Box):
        slide.box(width=1800).image("images/ui-test-diff.png")

#     @slides.slide()
#     def declarative_tests(slide: Box):
#         project(slide, "Rust compiler UI test suite")
#         slide.update_style("code", T(size=40))
#
#         slide.box(p_bottom=40).text("Declarative test configuration:")
#         code(slide.box(), """
# //@ add-minicore
# //@ normalize-stderr: "randomization_seed: \d+" -> "random: $$SEED"
# //@ normalize-stderr: "(size): Size\([48] bytes\)" -> "$1: $$SOME_SIZE"
# //@ normalize-stderr: "(can_unwind): (true|false)" -> "$1: $$SOME_BOOL"
# // Some attributes are only computed for release builds:
# //@ compile-flags: -O
# //@ revisions: generic riscv64 loongarch64
# //@ [riscv64] compile-flags: --target riscv64gc-unknown-linux-gnu
# //@ [riscv64] needs-llvm-components: riscv
# //@ [loongarch64] compile-flags: --target loongarch64-unknown-linux-gnu
# //@ [loongarch64] needs-llvm-components: loongarch
# //@ [generic] ignore-riscv64
# //@ [generic] ignore-loongarch64
# //@ ignore-backends: gcc
# """)

    @slides.slide()
    def cargo_test(slide: Box):
        project(slide, "Cargo")

        slide.update_style("code", T(size=40))
        code(slide.box(y=code_y), """
#[cargo_test]
fn build_lib_only() {
    let p = project()
        .file("src/main.rs", "fn main() {}")
        .file("src/lib.rs", r#" "#)
        .build();

    p.cargo("build --lib -v")
        .with_stderr_data(str![[r#"
[COMPILING] foo v0.0.1 ([ROOT]/foo)
[RUNNING] `rustc --crate-name foo --edition=2015 src/lib.rs [..]
    --crate-type lib --emit=[..]link[..]
    -L dependency=[ROOT]/foo/target/debug/deps`
[FINISHED] `dev` profile [unoptimized + debuginfo] target(s) in [ELAPSED]s

"#]])
        .run();
}
""")
