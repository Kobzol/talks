from elsie import Arrow, Slides, TextStyle as s

from utils import CODE_HIGHLIGHT_COLOR, code, code_step, list_item, pointer_to_line, slide_header, \
    with_bg


def intro_slide(slides: Slides):
    slide = slides.new_slide()
    slide.set_style("text", s(size=60, bold=True))
    slide.set_style("orange", slide.get_style("text").compose(s(color="orange")))

    safe = slide.box()
    safe.text("Fast & ~orange{Safe}", style="text")

    slide.box(height=100)

    line = slide.box(width="fill", horizontal=True)
    development = line.box(width="50%", y=0)
    development.overlay(show="2-3").text("Memory safety")
    development.overlay(show="4").text("Memory safety", style=s(color="orange"))
    performance = line.box(width="50%", y=0, show="3+")
    performance.text("Fearless concurrency")

    arrow = Arrow(20)
    slide.box(show="2+").line([safe.p("80%", "100%"), development.p("50%", 0)],
                              stroke_width=5, color="orange", end_arrow=arrow)
    slide.box(show="3+").line([safe.p("80%", "100%"), performance.p("50%", 0)],
                              stroke_width=5, color="orange", end_arrow=arrow)


def rust_safety(slides: Slides):
    slide = slides.new_slide()
    slide.set_style("text", s(size=60, bold=True))

    slide.box().text("Rust is safe...", style="text")
    slide.box(show="2+").text("...but from what?", style="text")

    slide = slides.new_slide()
    content = slide_header(slide, "Undefined behaviour")
    content.box(width=800).image("imgs/cpp-undefined.png")

    slide = slides.new_slide()
    content = slide_header(slide, "UB in Java")
    content.box().text("Java::Iterator::remove")
    with_bg(content.box()).text("""“The behavior of an iterator is ~emph{unspecified} if the underlying
collection is modified while the iteration is in progress in any way
other than by calling this method, unless an overriding class has specified
a concurrent modification policy.”
""", style=s(size=28, align="left"))

    slide = slides.new_slide()
    content = slide_header(slide, "UB in Python")
    content.box().text("~tt{for} statement")
    with_bg(content.box()).text("""“There is a subtlety when the sequence is being modified by the loop (this can only
occur for mutable sequences, e.g. lists). An internal counter is used to keep track
of which item ... ~emph{This can lead to nasty bugs} that can be avoided by making a
temporary copy using a slice of the whole sequence ...”
""", style=s(size=24, align="left"))

    slide = slides.new_slide()
    content = slide_header(slide, "Sources of UB")
    list = content.box()
    items = [
        "Null pointer dereference",
        "Double-free",
        "Use-after-free",
        "Out-of-bounds access",
        "Integer conversion",
        "Integer overflow",
        "Iterator invalidation",
        "Invalid alignment",
        "…"
    ]
    for item in items:
        list_item(list, show="next+").text(item)

    content.box(height=20)
    content.box(show="next+").text("Rust tries very hard to avoid all of the above", style=s(
        size=44,
        bold=True
    ))


def cpp_alias_mutate(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("default", s(size=50, bold=True))
    content = slide_header(slide, "Rust's insight")
    content.box(show="next+").text("""Memory errors arise when
aliasing is combined with mutability""")

    slide = slides.new_slide()
    slide.update_style("code", s(size=32))
    slide.set_style("gray", slide.get_style("code").compose(s(color="#BBBBBB")))
    content = slide_header(slide, "C++ UB example")

    style_green = s(
        size=40,
        color="green"
    )
    style_red = s(
        size=style_green.size,
        color="red"
    )

    header = content.box(width=500, height=50, horizontal=True)
    header.overlay(show="2").text("Aliasing ✓", style=style_green)
    header.overlay(show="3").text("Mutability ✓", style=style_green)
    header.overlay(show="4+").text("Aliasing & Mutability", style=style_red)
    header.box(show="4+", width=100, x=450).image("imgs/boom.svg")

    content.box(height=20)
    wrapper = code_step(content.box(width=700, height=200), """
std::vector<int> vec = { 1, 2, 3 };
int& p = vec[0];
vec.push_back(4);
std::cout << p << std::endl;
""", 1, [(0, None, None, None),
         (0, 1, None, 3),
         (0, None, 2, None),
         (0, 1, 2, 3)], language="cpp")

    wrapper.line_box(2, show="4+", z_level=99, width=320).rect(bg_color=CODE_HIGHLIGHT_COLOR)
    wrapper.line_box(3, show="4+", z_level=99, x=235, width=45).rect(bg_color=CODE_HIGHLIGHT_COLOR)

    slide = slides.new_slide()
    content = slide_header(slide, "What to do?")
    content.box(width=1000).image("imgs/meme-rust-aliasing.jpg")

    slide = slides.new_slide()
    content = slide_header(slide, "Rust's solution")

    large = s(
        size=50,
        bold=True
    )

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


def ownership(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Memory safety using the type system")
    list = content.box()
    list_item(list).text("Ownership")
    list_item(list, show="next+").text("Borrowing")
    list_item(list, show="next+").text("Lifetimes")

    slide = slides.new_slide()
    content = slide_header(slide, "Ownership")
    content.box().text("Every value in Rust has exactly one owner", s(size=50))
    content.box(height=10)
    content.box(show="next+").text("When that owner goes out of scope, the value is dropped",
                                   style=s(size=36))

    def person_slide(end=""):
        slide = slides.new_slide()
        slide.update_style("code", s(size=50))
        content = slide_header(slide, "Ownership")
        return (slide, code(content, """
fn foo(bitmap: Bitmap) {{
    ...
}}{}""".format(end), width=840))

    (slide, box) = person_slide()
    pointer_to_line(slide, box, 0, 100, 150, "2+",
                    textbox_pos=("50%", "100%"),
                    code_pos=("40%", "10%")).text("""No one else has any access to `bitmap`.
It can be mutated arbitrarily.""", style=s(color="orange", size=40))

    person_slide(" // bitmap is dropped here")

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Ownership - move semantics")
    code_box = code(content.box(), """
fn foo(bitmap: Bitmap) { ... }

fn main() {
    let bitmap = Bitmap::load(...);
    foo(bitmap);
    ...
}
""")
    pointer_to_line(slide, code_box, 4, 200, 120, "2+",
                    textbox_pos=("40%", "100%"),
                    code_pos=("46%", "60%")).text("""`bitmap` is moved here.
It will not be `dropped` in the current scope.
""", style=s(color="orange", align="left"))

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Ownership - move semantics")
    code(content.box(), """
fn foo(bitmap: Bitmap) { ... }

fn main() {
    let bitmap = Bitmap::load(...);
    foo(bitmap);
    println!("{}", bitmap.width);
}
""")
    content.box(height=20)
    content.box(height=180, show="2+").image("imgs/ownership-moved.png")

    slide = slides.new_slide()
    content = slide_header(slide, "Constructors")
    list = content.box()
    list_item(list).text("Move constructors? Nope.")
    list_item(list, show="next+").text("Move assignment constructors? Nope.")

    slide = slides.new_slide()
    content = slide_header(slide, "Why are they needed in C++?")
    content.box(height=600).image("imgs/meme-lvalue.jpg")

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Why are they needed in C++?")
    box = code(content, """
void foo(Bitmap&& bitmap) { ... }

Bitmap bitmap(...);
foo(std::move(bitmap));
std::cout << bitmap.width << std::endl;""", "cpp")
    pointer_to_line(slide, box, 4, 100, 600, "2+",
                    textbox_pos=("40%", "0"),
                    code_pos=("40%", "100%")).text("""`bitmap` is still accessible here.
It will be `dropped` at the end of scope.
Its state HAD to be reset in the move constructor.""", style=s(color="orange", align="left"))

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, '"Copy" semantics')
    content.box().text("""Values are copied instead of moved
if they implement the `Copy` trait""", style=s(bold=True))

    content.box(height=20)
    content.box(show="next+").text("Types are `Copy` if:")
    list = content.box()
    list_item(list, show="next+").text("they are primitive (integers, floats, etc.)")
    list_item(list, show="next+").text("they are marked as Copy")

    content.box(height=20)
    code(content.box(show="next+"), """
#[derive(Copy)]
struct Person {
    age: u32,
    male: bool
}""", width=500)

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, '"Copy" semantics')
    box = code(content.box(), """
fn foo(num: u32) { ... }

let number = 5;
foo(number);
println!("{}", number); // no error""")

    pointer_to_line(slide, box, 3, 200, 600, "2+",
                    textbox_pos=("40%", "0"),
                    code_pos=("34%", "60%")).text("""`number` is copied here.
    It can be still accessed after the call.""", style=s(color="orange"))


def borrowing(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Where's the aliasing?")
    content.box().text("So far, we only have mutability, there's no aliasing:")

    content.box(height=20)
    list = content.box()
    list_item(list, show="next+").text("After a move, the original value is not accessible")
    list_item(list, show="next+").text("After a copy, a new value is created")

    slide = slides.new_slide()
    content = slide_header(slide, "Borrowing")
    content.box().text("Aliasing happens when you create a reference to a value")
    content.box(show="next+").text("This is called borrowing in Rust")

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Shared borrows")

    code_width = 800

    code(content, """
let value = Bitmap::load(...);
let a = &value;
let b = &value;
""", width=code_width)

    content.box(height=20)
    list = content.box()
    list_item(list, show="next+").text("Multiple shared borrows of a value may exist")

    list.box(height=10)
    list_item(list, show="next+").text("You can't mutate using a shared borrow")
    list.box(height=10)
    code(list.box(show="last+"), "a.width = 10; // does not compile", width=code_width)

    list.box(height=10)
    list_item(list, show="next+").text("You can't move out of a shared borrow")
    list.box(height=10)
    code(list.box(show="last+"), """
fn foo(bitmap: Bitmap) { }
foo(a); // does not compile""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Unique borrows")

    code_width = 800

    code(content, """
let value = Bitmap::load(...);
let c = &mut value;
""", width=code_width)

    content.box(height=20)
    list = content.box()
    list_item(list, show="next+").text("""If a unique borrow exists, there are no other references
to the same value""", style=s(align="left"))
    list_item(list, show="next+").text("You can only create a unique borrow if you own the value")

    list.box(height=10)
    list_item(list, show="next+").text("You can mutate using a unique borrow")
    list.box(height=10)
    code(list.box(show="last+"), "c.width = 10;", width=code_width)

    list.box(height=10)
    list_item(list, show="next+").text("You can't move out of a unique borrow")
    list.box(height=10)
    code(list.box(show="last+"), """
fn foo(bitmap: Bitmap) { }
foo(c); // does not compile""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Vector example (Rust)")

    code_width = 800
    code(content.box(show="3+"), """
// Vec::push
fn push(&mut self, value: T)
""", width=code_width)
    content.box(height=10)
    code_step(content.box(width=code_width, height=300), """
let vec = vec!(1, 2, 3);
let p = &vec[0];
vec.push(4);
println!("{}", p);
""", "1", (
        (0, None, None, None),
        (0, 1, None, None),
        (0, 1, 2, None),
        (0, 1, 2, 3)
    ), width=code_width)

    content.box(height=10)
    content.box(height=220, show="next+").image("imgs/borrowck-error.png")

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    content = slide_header(slide, "What if compile time is not enough?")
    content.box().text("""If you can't prove to the compiler that your borrows are safe,
borrow checking can be done at runtime.""")
    content.box(show="next+").text("If any rules are broken, the program panics.")

    content.box(height=20)
    code_box = code(content.box(show="next+"), """
let value = RefCell::new(5);
let a = value.borrow();     // shared borrow
let b = value.borrow_mut(); // unique borrow""")
    pointer_to_line(slide, code_box, 2, 100, 600, "4+",
                    textbox_pos=("40%", 0),
                    code_pos=("40%", "100%")).text("""This would panic, since there already is
a shared borrow""", style=s(color="orange", align="left"))


def lifetimes(slides: Slides):
    def cpp_lifetime(comment=""):
        slide = slides.new_slide()
        slide.update_style("code", s(size=38))
        content = slide_header(slide, "Lifetimes (C++)")
        code(content, """
int* p;
{{
    int value = 5;
    p = &value;
}}{comment}
std::cout << *p << std::endl;
""".format(comment=comment), "cpp", width=800)

    cpp_lifetime()
    cpp_lifetime(" // <-- `value` is destroyed here")

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Lifetimes (Rust)")
    code_box = code(content.box(), """
let p;
{
    let value = 5;
    p = &value;
}
println!("{}", *p);""", width=800)

    def line(start, end, start_x, end_x, right_x, offset_x, color, show, y="65%"):
        line_start = code_box.line_box(start, width="fill")
        line_end = code_box.line_box(end, width="fill")
        arrow = Arrow(20)

        start = line_start.p(start_x, y)
        end = line_end.p(end_x, y)

        content.box(show=show).line([
            start,
            line_start.p(right_x, y).add(offset_x, 0),
            line_end.p(right_x, y).add(offset_x, 0),
            end
        ], start_arrow=arrow, end_arrow=arrow, stroke_width=5, color=color)

    content.box(height=20)
    content.box(width=500, show="2+").text("Lifetime of reference `p`",
                                           style=s(color="orange", align="left"))
    line(0, 5, "40%", "100%", "90%", 200, "orange", "2+")

    content.box(height=10)
    content.box(width=500, show="3+").text("Lifetime of `value`",
                                           style=s(color="green", align="left"))
    line(2, 4, "100%", "10%", "100%", 50, "green", "3+")

    content.box(height=30)
    content.box(show="4+").text("""Lifetime of a value must be
>= lifetime of a reference to it""", style=s(size=50))

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Lifetimes (Rust)")
    code_box = code(content.box(), """
let p;
{
    let value = 5;
    p = &value;
}
println!("{}", *p);""", width=800)

    content.box(height=20)
    content.box(height=280).image("imgs/lifetime-error.png")

    slide = slides.new_slide()
    slide.update_style("code", s(size=32))
    content = slide_header(slide, "What if compile time is not enough?")
    content.box().text("""If you can't prove to the compiler that the lifetimes
are correct, lifetime can be managed at runtime.""")

    code_width = 1000
    content.box(height=20)
    code_step(content.box(width=code_width, height=400), """
fn main() {
    let value = Rc::new(5); // refcount == 1
    {
        let a = value.clone(); // refcount == 2
    } // refcount == 1
} // refcount == 0, value is dropped
""", "2", (
        (0, 1, None, None, None, None),
        (0, 1, 2, 3, None, None),
        (0, 1, 2, 3, 4, None),
        (0, 1, 2, 3, 4, 5)
    ), width=code_width)


def memory_safety(slides: Slides):
    intro_slide(slides)
    rust_safety(slides)
    cpp_alias_mutate(slides)
    ownership(slides)
    borrowing(slides)
    lifetimes(slides)
