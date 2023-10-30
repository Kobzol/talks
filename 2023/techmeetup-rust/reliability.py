from elsie import SlideDeck, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from config import sh, sw
from utils import CODE_HIGHLIGHT_COLOR, LOWER_OPACITY, code, code_step, dimmed_list_item, quotation


def cpp_alias_mutate(slides: SlideDeck):
    @slides.slide()
    def insight(slide: Box):
        content = slide.box()
        content.box().text("""Memory errors arise when
aliasing is combined with mutability""")

    @slides.slide()
    def cpp_vec_ub(slide: Box):
        slide.update_style("code", T(size=sw(50)))
        slide.set_style("gray", slide.get_style("code").compose(T(color="#BBBBBB")))

        content = slide.box()

        style_green = T(size=50, color="green")
        style_red = T(size=style_green.size, color="red")

        header = content.box(horizontal=True, width=sw(500), height=sh(100))
        header.overlay(show="2").text("Aliasing ✓", style=style_green)
        header.overlay(show="3").text("Mutability ✓", style=style_green)
        header.overlay(show="4+").text("Aliasing & Mutability", style=style_red)
        header.box(show="4+", width=sw(150), x=sw(600)).image("images/boom.svg")

        content.box(height=sh(40))
        wrapper = code_step(content.box(width=sw(1200), p_bottom=sh(400)), """
std::vector<int> vec = { 1, 2, 3 };
int& p = vec[0];
vec.push_back(4);
std::cout << p << std::endl;
    """, 1, [(0, None, None, None),
             (0, 1, None, 3),
             (0, None, 2, None),
             (0, 1, 2, 3)], language="cpp").children[-1]

        wrapper.line_box(2, show="4+", z_level=99, width=sw(510)).rect(
            bg_color=CODE_HIGHLIGHT_COLOR)
        wrapper.line_box(3, show="4+", z_level=99, x=sw(380), width=sw(50)).rect(
            bg_color=CODE_HIGHLIGHT_COLOR)

    @slides.slide()
    def what_to_do(slide: Box):
        content = slide.box()
        content.box().text("What to do?")
        content.box(width=sw(1800)).image("images/meme-rust-aliasing.jpg")

    @slides.slide()
    def solution(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(80)).text("Rust's solution")

        large = T(size=50, bold=True)

        row = content.box(horizontal=True)
        row.box().text("You can mutate", style=large)
        row.box(width=20)
        row.box(show="next+").text("||", style=large)
        row.box(width=20)
        row.box(show="next+").text("alias", style=large)

        content.box(height=10)
        content.box(show="next+").text("But not both at the same time (w.r.t. a single variable)")
        content.box(height=10)
        content.box(show="next+").text("Rust enforces this at compile time using its type system")


def reliability(slides: SlideDeck):
    @slides.slide()
    def safety(slide: Box):
        content = slide.box()
        content.box().text("(Memory) Safety", T(size=80))

    @slides.slide()
    def safety_in_the_wild(slide: Box):
        slide.overlay().box(width=sw(1500), show="1").image("images/microsoft-safety.png")
        slide.overlay().box(width=sw(1500), show="next").image("images/chrome-safety.png")
        slide.overlay().box(width=sw(1200), show="next").image("images/android-safety.png")
        slide.overlay().box(width=sw(1500), show="next").image("images/nsa-safety.png")

    @slides.slide()
    def undefined_behavior(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(40)).text("Caused by undefined behaviour (UB)")
        list = unordered_list(content.box(show="next+"))
        items = [
            "Null pointer dereference",
            "Double-free",
            "Use-after-free",
            "Out-of-bounds access",
            "Iterator invalidation",
            "…"
        ]
        for item in items:
            list.item().text(item)

        content.box(p_top=sh(40), show="next").text("Rust: avoid UB at all costs")

    cpp_alias_mutate(slides)

    @slides.slide()
    def rewrites(slide: Box):
        width = sw(1500)
        rewrites = ("rewrite-video-decoder", "rewrite-sudo", "rewrite-ntp", "rewrite-dns")
        for (index, rewrite) in enumerate(rewrites):
            slide.overlay().box(width=width, show="1" if index == 0 else "next").image(
                f"images/{rewrite}.png"
            )
        slide.overlay().box(width=sw(1100), show="next").image("images/rewrite-tls.png")

    @slides.slide()
    def undefined_behavior_java(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(40)).text("UB in Java", T(size=sw(80)))

        content.box(p_bottom=sh(10)).text("~tt{Iterator::remove}")
        quotation(content.box(), """~bold{The behavior of an iterator is unspecified if the underlying
collection is modified while the iteration is in progress} in any way
other than by calling this method, unless an overriding class has specified
a concurrent modification policy.""", "Java docs", size=sw(50))

    @slides.slide()
    def undefined_behavior_python(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(40)).text("UB in Python", T(size=sw(80)))

        content.box(p_bottom=sh(10)).text("~tt{for} cycle")
        quotation(content.box(), """There is a subtlety when the ~bold{sequence is being modified by the loop}
(this can only occur for mutable sequences, e.g. lists).
…~bold{This can lead to nasty bugs}…""",
                  "Python docs", size=sw(50))

    @slides.slide()
    def iterator_invalidation(slide: Box):
        slide.update_style("code", T(size=50))
        content = slide.box()
        code(content.box(), """let mut items = vec![1, 2, 3];
for item in items.iter() {
    items.push(1);
}""")
        slide.box(show="next", p_top=sh(40), width=sw(1800)).image("images/error-message-1.png")

    @slides.slide()
    def correctness(slide: Box):
        content = slide.box()
        content.box(p_bottom=sh(80)).text("Correctness", T(size=80))
        content.box().text("Design APIs that cannot be misused")

    @slides.slide()
    def ownership(slide: Box):
        slide.update_style("code", T(size=50))
        content = slide.box(width="fill")
        content.box(p_bottom=sh(40)).text("Ownership")
        code_step(content.box(width="fill", height=sh(200)), """file.close();
let data = file.read();""", show_start=1, line_steps=[[0], [0, 1]], width=sw(1000))
        slide.box(show="3", p_top=sh(40), width=sw(1800)).image(
            "images/error-message-file-ownership.png")

    @slides.slide()
    def enums(slide: Box):
        slide.update_style("code", T(size=40))
        content = slide.box(width="fill")
        content.box(p_bottom=sh(40)).text("Sum types (\"enums on steroids\")")
        code_step(content.box(width="fill", height=sh(700)), """
enum PrintJob {
    Created {
        source: Document
    },
    Finished {
        printer: Printer,
        printed_pages: u32
    },
    Failed {
        printer: Printer,
        error: PrintError
    }
}
""", show_start=1, line_steps=[
            [0, *([None] * 11), 12],
            [0, 1, 2, 3, *([None] * 8), 12],
            [0, 1, 2, 3, 4, 5, 6, 7, None, None, None, None, 12],
            list(range(13))
        ], width=sw(1400))

    @slides.slide()
    def pattern_matching(slide: Box):
        slide.update_style("code", T(size=40))
        content = slide.box()
        content.box(p_bottom=sh(40)).text("Pattern matching")
        code(content.box(), """
let printer = match job {
    PrintJob::Created  { .. } => None,
    PrintJob::Finished { printer, .. } |
    PrintJob::Failed   { printer, .. } => Some(printer) 
};
""")

    @slides.slide()
    def no_null(slide: Box):
        slide.update_style("code", T(size=50))
        slide.set_style("code-muted", T(opacity=LOWER_OPACITY), base="code")
        slide.set_style("code-small", T(size=40), base="code")

        content = slide.box()
        content.box(p_bottom=sh(40)).text("No implicit ~tt{null}")

        top_code_width = sw(1500)
        code_box = content.box(p_bottom=sh(40))
        code(code_box.box(show="next"), """
fn max(items: &[u32]) ->
""", width=top_code_width)
        code(code_box.overlay(show="next"), """
fn max(items: &[u32]) -> Option<usize>
""", width=top_code_width)
        code(code_box.overlay(show="next+"), """
fn max(items: &[u32]) -> Option<usize>
""", width=top_code_width, code_style="code-muted")

        row = content.box(show="4+", horizontal=True)
        code(row.box(p_right=sw(40)), """enum Option<T> {
    Some(T),
    None
}
""", code_style="code-small")

        box = row.box()
        code(box.fbox(show="next"), """
match opt_value {
    Some(value) => ...,
    None => println!("Value is missing")
}
""", code_style="code-small", width=sw(1250))

    @slides.slide()
    def error_handling(slide: Box):
        slide.update_style("code", T(size=36))
        slide.set_style("code-muted", T(opacity=LOWER_OPACITY), base="code")
        content = slide.box()

        text_top = "Forces you to think about possible errors"
        text = content.box(p_bottom=sh(40))
        text.box(show="1-2").text(text_top)
        text.overlay(show="3+").text(text_top, T(opacity=LOWER_OPACITY))

        code_top = """
match read_file("src.txt") {
    Ok(content) => write_file("dst.txt", content),
    Err(Error::PermissionDenied) => eprintln!("Permission denied"),
    Err(Error::NotFound) => eprintln!("File not found")
}
"""

        code_box = content.box(p_bottom=sh(60))
        code(code_box.box(show="3+"), code_top, code_style="code-muted")
        code(code_box.overlay(show="2"), code_top)

        content.box(show="last", p_bottom=sh(40)).text("But tries to make it ergonomic")
        code(content.box(show="last"), """
let content = read_file("src.txt")?;
write_file("dst.txt", content)?; 
""", use_styles=True)

    @slides.slide()
    def mutex(slide: Box):
        slide.update_style("code", T(size=50))

        content = slide.box(width="fill")
        content.box(p_bottom=sh(40)).text("Safe(r) mutexes")
        code_step(content.box(width="fill"), """let value = Mutex::new(vec![1, 2]);
value.lock().push(3);
""", show_start=1, line_steps=[[0], [0, 1]], width=sw(1000))

    @slides.slide()
    def fearless_concurrency(slide: Box):
        slide.update_style("code", T(size=50))

        content = slide.box(width="fill")
        content.box(p_bottom=sh(40)).text("Compile-time data race detection")
        code_step(content.box(width="fill", p_bottom=sh(400)), """let mut items = vec![1, 2];

std::thread::spawn(|| items.push(3));
items.push(4);
""", show_start=1, line_steps=[[0], [0, 1, 2], [0, 1, 2, 3]], width=sw(1400))
        content.box(show="next").text("Compile-time error!", T(color="red"))

    @slides.slide()
    def confidence(slide: Box):
        content = slide.box()
        content.box().text("~bold{Confidence}")
        lst = unordered_list(content.box())
        dimmed_list_item(lst, "\"If it compiles, it works\"", show=2)
        dimmed_list_item(lst, "Easier code review", show=3)
        lst.item(show="last").text("Better discipline in other languages")
