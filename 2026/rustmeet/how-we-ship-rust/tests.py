from elsie import Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import GITHUB_BG, code, \
    dimmed_list_item, \
    migration, render_tag


def tests(slides: Slides):
    # @slides.slide()
    # def testing_the_compiler(slide: Box):
    #     chapter(slide, "Running test suite(s)", TEST_ICON)

    @slides.slide()
    def test_suites(slide: Box):
        slide.box(p_bottom=40).text("Rust test suites", T(size=80))
        lst = unordered_list(slide.box())

        items = [
            ("Compiler unit/doc tests", "~2k"),
            ("Library unit/doc tests", "~15k"),
            ("Compiletest tests", "~24k"),
        ]
        for (suite, count) in items:
            row = lst.item(show="next+").box(horizontal=True)
            row.box(width=700).text(f"{suite}:")
            row.box(width=200).text(count, T(align="right"), escape_char="#")

    @slides.slide(bg_color="#0F1419")
    def compiletest_test_suites(slide: Box):
        render_tag(slide, "rustc-dev-guide", kind="docs")
        slide.box(width=1100, y=120).image("images/compiletest-test-suites.png")

    def test_suite(slide: Box, name: str):
        render_tag(slide, f"{name} testsuite", kind="tool")

    @slides.slide(bg_color="#2B2D30")
    def ui_tests_test(slide: Box):
        test_suite(slide, "ui")
        slide.box(width=1000).image("images/ui-tests-files.png")

    width = 1800
    code_y = 150

    @slides.slide()
    def ui_test_code(slide: Box):
        test_suite(slide, "ui")
        row = slide.box(horizontal=True, x="[90%]", y="[4%]")
        row.box().text("assign-imm-local-twice.rs", T(font="Ubuntu Mono"))
        row.box(width=30)
        row.box(width=80, y=0).image("images/memo.svg")
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
    def ui_test_fixed(slide: Box):
        test_suite(slide, "ui")
        row = slide.box(horizontal=True, x="[90%]", y="[4%]")
        row.box(p_bottom=40).text("assign-imm-local-twice.fixed", T(font="Ubuntu Mono"))
        row.box(width=30)
        row.box(width=80, y=0).image("images/stars.svg")
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
    def ui_test_stderr(slide: Box):
        test_suite(slide, "ui")
        slide.update_style("code", T(size=40))

        row = slide.box(horizontal=True, x="[90%]", y="[4%]")
        row.box(p_bottom=40).text("assign-imm-local-twice.stderr", T(font="Ubuntu Mono"))
        row.box(width=30)
        row.box(width=80, y=0).image("images/stars.svg")
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

    @slides.slide(bg_color=GITHUB_BG)
    def ui_test_diff(slide: Box):
        slide.box(width=1800).image("images/ui-test-diff.png")

    @slides.slide()
    def declarative_tests(slide: Box):
        slide.update_style("code", T(size=40))

        render_tag(slide, "compiletest", kind="tool")
        slide.box(p_bottom=40).text("Declarative test configuration")
        code(slide.box(), """
//@ add-minicore
//@ normalize-stderr: "randomization_seed: \\d+" -> "random: $$SEED"
//@ normalize-stderr: "(size): Size\\([48] bytes\\)" -> "$1: $$SOME_SIZE"
//@ normalize-stderr: "(can_unwind): (true|false)" -> "$1: $$SOME_BOOL"
// Some attributes are only computed for release builds:
//@ compile-flags: -O
//@ revisions: generic riscv64 loongarch64
//@ [riscv64] compile-flags: --target riscv64gc-unknown-linux-gnu
//@ [riscv64] needs-llvm-components: riscv
//@ [loongarch64] compile-flags: --target loongarch64-unknown-linux-gnu
//@ [loongarch64] needs-llvm-components: loongarch
//@ [generic] ignore-riscv64
//@ [generic] ignore-loongarch64
//@ ignore-backends: gcc
""")

    @slides.slide()
    def llvm_codegen_tests(slide: Box):
        slide.update_style("code", T(size=46))
        test_suite(slide, "LLVM codegen")
        code(slide.box(y=code_y), """
//@ compile-flags: -C no-prepopulate-passes -Z mir-opt-level=0

#![crate_type = "lib"]
#![feature(core_intrinsics)]

use std::intrinsics::disjoint_bitor;

// CHECK-LABEL: @disjoint_bitor_signed
#[no_mangle]
pub unsafe fn disjoint_bitor_signed(x: i32, y: i32) -> i32 {
    // CHECK: [[TEMP:%.+]] = or disjoint i32 %x, %y
    // CHECK: ret i32 [[TEMP]]
    disjoint_bitor(x, y)
}
""")

    @slides.slide()
    def assembly_tests(slide: Box):
        test_suite(slide, "assembly")
        code(slide.box(y=code_y), """
//@ assembly-output: emit-asm
//@ compile-flags: -Copt-level=1
//@ only-x86_64
#![crate_type = "rlib"]

// CHECK-LABEL: align_offset_byte_ptr
// CHECK: leaq {{31|28}}
// CHECK: andq $-32
// CHECK: subq
#[no_mangle]
pub fn align_offset_byte_ptr(ptr: *const u8) -> usize {
    ptr.align_offset(32)
}
""")

    @slides.slide()
    def debuginfo_tests(slide: Box):
        slide.update_style("code", T(size=42))
        test_suite(slide, "debuginfo")
        code(slide.box(y=code_y), """
//@ compile-flags:-g
//@ disable-gdb-pretty-printers

//@ lldb-command:run

//@ lldb-command:v three_simple_structs
//@ lldb-check:[...] {x:{x:1}, y:{x:2}, z:{x:3}}

struct Simple {
    x: i32,
}
struct ThreeSimpleStructs { x: Simple, y: Simple, z: Simple }

fn main() {
    let three_simple_structs = ThreeSimpleStructs {
        x: Simple { x: 1 }, y: Simple { x: 2 }, z: Simple { x: 3 } };
}
""")

    @slides.slide()
    def rustdoc_html(slide: Box):
        slide.update_style("code", T(size=38))
        test_suite(slide, "rustdoc HTML")
        code(slide.box(y=code_y), """
#![crate_name = "foo"]

//@ has foo/index.html \\
    '//*[@class="docblock"]/p/a[@href="struct.Foo.html#structfield.bar"]' \\
    'Foo::bar'
//@ has foo/index.html \\
    '//*[@class="docblock"]/p/a[@href="union.Bar.html#structfield.foo"]' \\
    'Bar::foo'

//! Test with [Foo::bar], [Bar::foo]

pub struct Foo {
    pub bar: usize,
}

pub union Bar {
    pub foo: u32,
}
""")

    @slides.slide()
    def rustdoc_gui(slide: Box):
        slide.update_style("code", T(size=36))
        test_suite(slide, "rustdoc GUI")
        code(slide.box(y=code_y), """
// The goal of this test is to check that the external trait implementors,
// generated with JS, have the same display than the "local" ones.
go-to: "file://" + |DOC_PATH| + "/implementors/trait.Whatever.html"
wait-for-css: ("#implementors-list", {"display": "block"})

// There are supposed to be four implementors listed.
assert-count: ("#implementors-list .impl", 4)

// There are supposed to be two non-negative implementors.
assert-count: ("#implementors-list .negative-marker ~ *", 2)

// Now we check that both implementors have an anchor, an ID and a similar DOM.
define-function: ( "check-dom", [id], block {
        assert-attribute: (|id| + " > a.anchor", {"href": |id|})
        assert: |id| + " > .code-header"
    },
)

call-function: ("check-dom", {"id": "#impl-Whatever-for-Struct2"})
call-function: ("check-dom", {"id": "#impl-Whatever-2"})
""", language="javascript")

    @slides.slide()
    def run_make_make(slide: Box):
        slide.update_style("code", T(size=26))
        test_suite(slide, "run-make")
        code(slide.box(y=code_y), """
# This test intentionally feeds invalid inputs to codegen and
# checks if the error message outputs contain specific helpful indications.

# ignore-cross-compile
include ../tools.mk

all:
	#Option taking a number
	$(RUSTC) -C codegen-units dummy.rs 2>&1 | \\
		$(CGREP) 'codegen option `codegen-units` requires a number'
	$(RUSTC) -C codegen-units= dummy.rs 2>&1 | \\
		$(CGREP) 'incorrect value `` for codegen option `codegen-units` - a number was expected'
	$(RUSTC) -C codegen-units=foo dummy.rs 2>&1 | \\
		$(CGREP) 'incorrect value `foo` for codegen option `codegen-units` - a number was expected'
	$(RUSTC) -C codegen-units=1 dummy.rs
	#Option taking a string
	$(RUSTC) -C extra-filename dummy.rs 2>&1 | \\
		$(CGREP) 'codegen option `extra-filename` requires a string'
	$(RUSTC) -C extra-filename= dummy.rs 2>&1
	$(RUSTC) -C extra-filename=foo dummy.rs 2>&1
	#Option taking no argument
	$(RUSTC) -C lto= dummy.rs 2>&1 | \\
		$(CGREP) 'codegen option `lto` - either a boolean, `thin`, `fat`, or omitted'
	$(RUSTC) -C lto=1 dummy.rs 2>&1 | \\
		$(CGREP) 'codegen option `lto` - either a boolean, `thin`, `fat`, or omitted'
	$(RUSTC) -C lto=foo dummy.rs 2>&1 | \\
		$(CGREP) 'codegen option `lto` - either a boolean, `thin`, `fat`, or omitted'
	$(RUSTC) -C lto dummy.rs
""", language="make")

    @slides.slide()
    def run_make_migration(slide: Box):
        test_suite(slide, "run-make")
        migration(slide.box(y=20), ["make", "rust"])
        slide.box(width=1800, y=140).image("images/run-make-migration.png")
        slide.box(x="[95%]", y="[99%]").text(
            "Google Summer of Code 2024: Rewriting Esoteric, Error-Prone Makefile Tests Using Robust Rust Features",
            T(size=34))

    @slides.slide()
    def x_tidy(slide: Box):
        """
        The nice thing about tidy is that it is relatively fast.
        """
        slide.update_style("code", T(size=46))

        render_tag(slide, "tidy", kind="tool")
        slide.box(p_bottom=40).text("Linting with ~tt{./x test tidy}", T(size=70))

        items = [
            "Check formatting and style",
            "Check alphabetical ordering",
            "Check license compatibility",
            "Check file placement",
            "Perform git sanity-checks",
            "Lint Python/JavaScript/C++ code"
        ]

        lst = unordered_list(slide.box())
        for (index, item) in enumerate(items):
            show = index + 3 if index > 1 else index + 2
            dimmed_list_item(lst, item, last=item == items[-1], show=show)

        code(slide.box(x="[50%]", y="[50%]", show="4"), """
// tidy-alphabetical-start
#![doc(test(attr(deny(warnings), allow(internal_features))))]
#![feature(associated_type_defaults)]
#![feature(deref_patterns)]
#![feature(iter_order_by)]
#![feature(macro_metavar_expr)]
#![recursion_limit = "256"]
// tidy-alphabetical-end    
""")

    @slides.slide(bg_color=GITHUB_BG)
    def tidy_python_to_rust(slide: Box):
        """
        tidy Python to Rust: https://github.com/rust-lang/rust/pull/32590
        """
        migration(slide.box(y=20), ["python", "rust"], bg="white")
        render_tag(slide, "tidy", kind="tool")
        slide.box(width=1600).image("images/tidy-python-to-rust.png")
