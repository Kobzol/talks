from elsie import Arrow, Slides, TextStyle as s

from utils import CODE_HIGHLIGHT_COLOR, code, list_item, slide_header, with_bg


def intro_slide(slides: Slides):
    slide = slides.new_slide()
    slide.set_style("text", s(size=60, bold=True))
    slide.set_style("orange", slide.get_style("text"), s(color="orange"))

    fast = slide.box()
    fast.text("~orange{Fast} & Safe", style="text")

    slide.box(height=100)

    line = slide.box(width="fill", horizontal=True)
    development = line.box(width="50%", y=0)
    development.overlay().text("Quick development")
    performance = line.box(width="50%", y=0)
    performance.text("High performance", style=s(color="orange"))

    arrow = Arrow(20)
    slide.box().line([fast.p("15%", "100%"), development.p("50%", 0)],
                     stroke_width=5, color="orange", end_arrow=arrow)
    slide.box().line([fast.p("15%", "100%"), performance.p("50%", 0)],
                     stroke_width=5, color="orange", end_arrow=arrow)


def zero_cost(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Zero-cost abstractions")
    content.box().text("Bjarne Stroustrup:", s(size=60))

    with_bg(content.box()).text("""What you don’t use, you don’t pay for.
What you do use, you couldn’t hand code any better.""")


def runtime(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("default", s(size=40))
    content = slide_header(slide, "Minimal runtime")

    list = content.box()
    list_item(list, show="next+").text("No GC")
    list.box(width=600, height=400, show="last+", padding=0).image("imgs/gc.svg")
    list_item(list, show="next+").text("No exceptions")
    list_item(list, show="next+").text("Tight data layout")
    list_item(list, show="next+").text("Supports embedded platforms")


def llvm_iterator(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Compiles to LLVM")
    content.box(height=600, x=350).image("imgs/llvm-flow.svg")

    slide = slides.new_slide()
    content = slide_header(slide, "Compiles to LLVM")
    src = content.box(width=700, height=100)
    src.image("imgs/godbolt-dot-product.svg")

    content.box(height=60)
    assembly = content.box(width="fill", height=400, show="2+")
    assembly.image("imgs/godbolt-dot-product-assembly.svg")

    arrow = Arrow(20)
    content.box(show="2+").line([src.p("50%", "100%"), assembly.p("50%", "0%").add(0, -10)],
                                stroke_width=5, color="orange", end_arrow=arrow)


def intrinsics(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=38))

    content = slide_header(slide, "Branch prediction")

    code(content.box(), """
if core::intrinsic::likely(condition) {
    ...
} else #[cold] {
    ...
}""")

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    content = slide_header(slide, "SIMD")

    code_width = 900
    code(content.box(), """
#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::_mm256_add_epi64;

_mm256_add_epi64(...);""", width=code_width)

    content.box(height=50)
    code(content.box(show="2+"), """
data.simd_iter()
    .simd_map(|v| {
        f32s(9.0) * v.abs().sqrt().ceil() -
        f32s(4.0) - f32s(2.0)
    })
    .scalar_collect();""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Inline assembly")

    code(content.box(), """
fn add(a: i32, b: i32) -> i32 {
    let c: i32;
    unsafe {
        asm!("add $2, $0"
             : "=r"(c)
             : "0"(a), "r"(b));
    }
    c
}""")


def constexpr(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=38))

    content = slide_header(slide, "Constexpr functions")

    code(content.box(), """
const fn double(x: i32) -> i32 {
    x * 2
}

const FIVE: i32 = 5;
const TEN: i32 = double(FIVE);
""")


def parallelization(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Concurrency primitives")

    list = content.box()
    list_item(list).text("Mutexes")
    list_item(list, show="next+").text("Condition variables")
    list_item(list, show="next+").text("Atomics")
    list_item(list, show="next+").text("Synchronized queues")

    slide = slides.new_slide()
    slide.update_style("code", s(size=30))
    content = slide_header(slide, "Shared-memory parallelism")
    content.box().text("No OpenMP ☹")

    code_width = 800

    content.box(height=40)
    rayon = content.box(show="2+")
    rayon_box = rayon.box(horizontal=True)
    rayon_box.box().text("Rayon (+ Rayon adaptive")
    rayon_box.box(width=20)
    rayon_box.box(width=60).image("imgs/saurabh.png")
    rayon_box.box().text(" )")
    rayon.box(height=30)
    code_box = code(rayon.box(), """
fn sum_of_squares(input: &[i32]) -> i32 {
    input.par_iter()
         .map(|&i| i * i)
         .sum()
}""", width=code_width)
    code_box.line_box(1, z_level=99,
                      x=165, width=165, show="3+").rect(bg_color=CODE_HIGHLIGHT_COLOR)

    code(rayon.box(show="4+"), """
#[parallel]
for x in 0..10 {
    println!("{}", x);
}""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=26))
    content = slide_header(slide, "Message-passing")
    code(content, """
let universe = mpi::initialize();
let world = universe.world();
let size = world.size();
let rank = world.rank();

if rank == 0 {
    let (msg, status) = world.any_process().receive_vec();
}
""")


def c_interop(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=26))

    content = slide_header(slide, "C/C++ interop")

    code_width = 940
    c_from_rust = content.box()
    c_from_rust.text("C from Rust")
    code(content, """
extern {
    fn snappy_max_compressed_length(len: size_t) -> size_t;
}

let length = unsafe { snappy_max_compressed_length(100) };
""", width=code_width)

    content.box(height=20)
    box = content.box(show="2+")
    rust_from_c = box.box()
    rust_from_c.text("Rust from C")
    code(box, """
#[repr(C)]
struct Object {
    bar: i32,
}

extern "C" fn foo(param: *mut Object) {
    unsafe {
        (*target).bar = 5;
    }
}""", width=code_width)


def caveats(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Performance caveats")

    l1_style = s(size=26)

    list = content.box()
    list_item(list).text("Out-of-bounds checks")
    list_item(list, level=1, show="2+").text("Can be optimized away (iterators)", style=l1_style)
    list_item(list, show="3+").text("Integer overflow is not undefined")
    list_item(list, level=1, show="4+").text("Runtime checks only in debug mode", style=l1_style)


def benchmark_game(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Benchmark game")
    content.box(width=900).image("imgs/benchmark-game.png")
    content.box().text("https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/gpp"
                       "-rust.html", style=s(size=20))


def performance(slides: Slides):
    intro_slide(slides)
    zero_cost(slides)
    runtime(slides)
    llvm_iterator(slides)
    intrinsics(slides)
    constexpr(slides)
    parallelization(slides)
    c_interop(slides)
    caveats(slides)
    benchmark_game(slides)
