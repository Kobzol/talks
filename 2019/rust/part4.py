from elsie import Arrow, Slides, TextStyle as s

from utils import CODE_HIGHLIGHT_COLOR, bash, code, code_step, list_item, slide_header, with_border


def intro_slide(slides: Slides):
    slide = slides.new_slide()
    slide.set_style("text", s(size=60, bold=True))
    slide.set_style("orange", slide.get_style("text").compose(s(color="orange")))

    fast = slide.box()
    fast.text("Fast & ~orange{Safe}", style="text")

    slide.box(height=100)

    line = slide.box(width="fill", horizontal=True)
    development = line.box(width="50%", y=0)
    development.overlay().text("Memory safety")
    performance = line.box(width="50%", y=0)
    performance.text("Fearless concurrency", style=s(color="orange"))

    arrow = Arrow(20)
    slide.box().line([fast.p("80%", "100%"), development.p("50%", 0)],
                     stroke_width=5, color="orange", end_arrow=arrow)
    slide.box().line([fast.p("80%", "100%"), performance.p("50%", 0)],
                     stroke_width=5, color="orange", end_arrow=arrow)


def concurrency_issues(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Concurrency issues")

    content.box().text("Rust doesn't prevent:")
    list = content.box()
    list_item(list, show="next+").text("Deadlocks")
    list_item(list, show="next+").text("General race conditions")

    content.box(height=20)
    content.box(show="next+").text("Rust prevents (at compile time):")
    list = content.box()
    list_item(list, show="next+").text("Data races")

    slide = slides.new_slide()
    content = slide_header(slide, "What causes data races?")

    text_style = s(size=50)
    content.box(show="next+").text("Concurrent aliasing and mutability...", style=text_style)
    content.box(show="next+").text("...but Rust already disables that!", style=text_style)

    content.box(height=20)
    content.box(show="next+").text("So how do we get any concurrency at all...?", style=text_style)


def shared_state(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Spawning a thread")

    code(content.box(), "fn spawn<F: Fn + Send>(f: F)")

    content.box(height=20)
    content.box(show="next+").text("""Ownership of T can be transferred to another thread
only if T implements the ~emph{Send} trait""")

    content.box(height=20)
    content.box(show="next+").text("""Send is implemented automatically, unless the type
contains values that are not safe to be transferred between threads""", style=s(size=30))

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    content = slide_header(slide, "Shared state concurrency")
    content.box().text("Goal:", style=s(bold=True))
    list = content.box()
    list_item(list, show="next+").text("Spawn a thread")
    list_item(list, show="next+").text("Send a reference to some value to it")
    list_item(list, show="next+").text("Modify the value in the spawned thread")
    list_item(list, show="next+").text("Read the value in the original thread")

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    (content, header) = slide_header(slide, "Shared state concurrency", True)
    box = header.box(width=160, y=80)
    box.image("imgs/meme-face-1.jpg")
    box.overlay(show="4").image("imgs/meme-face-2.jpg")

    code_step(content.box(width=800, height=350), """
let value = 5;
let p = &value;
thread::spawn(|| {
    println!("{}", *p);
});
""", 1, [(0, None, None, None, None),
         (0, 1, None, None, None),
         (0, 1, 2, 3, 4)], width=500)

    content.box(height=10)
    with_border(content, show="4+").box(height=220).image("imgs/concurrent-error-1.png")

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    (content, header) = slide_header(slide, "Shared state concurrency", True)
    box = header.box(width=160, y=80)
    box.image("imgs/meme-face-2.jpg")
    box.overlay(show="4-5").image("imgs/meme-face-3.png")
    box.overlay(show="6+").image("imgs/meme-face-4.png")

    code_step(content.box(width=800, height=350), """
let p = Rc::new(5);
thread::spawn(|| {
    println!("{}", *p);
});
""", 1, [(0, None, None, None),
         (0, 1, None, None),
         (0, 1, 2, 3),
         (0, 1, 2, 3),
         (0, "thread::spawn(move || {", 2, 3)], width=500)

    border_box = content.box(width=1000, height=220)
    box = with_border(border_box.overlay(), show="4").box(width=800, height=180)
    box.box(show="4", height=220).image("imgs/concurrent-error-2.png")
    box = with_border(border_box.overlay(), show="6+").box(width=800, height=180)
    box.box(show="6+", width=900).image("imgs/concurrent-error-3.png")

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    (content, header) = slide_header(slide, "Shared state concurrency", True)
    box = header.box(width=160, y=80)
    box.overlay(show="1-2").image("imgs/meme-face-6.jpg")
    box.overlay(show="3+").image("imgs/meme-face-5.jpg")

    content.box(height=60)
    code_step(content.box(width=800, height=260), """
let p = Arc::new(5);
thread::spawn(move || {
    println!("{}", *p);
});
println!("{}", *p);
""", 1, [(0, 1, 2, 3, None),
         (0, 1, 2, 3, 4),
         ], width=500)
    with_border(content, show="3+").box(width=1000).image(
        "imgs/concurrent-error-4.png")

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    (content, header) = slide_header(slide, "Shared state concurrency", True)
    box = header.box(width=160, y=80, show="3+")
    box.image("imgs/meme-face-7.png")

    code_width = 800
    code(content.box(show="2+"), "fn clone(&self) -> Arc<T>;", width=code_width)

    content.box(height=20)
    code(content.box(), """
let p = Arc::new(5);
let tp = p.clone();
thread::spawn(move || {
    println!("{}", *tp);
});
println!("{}", *p);
""", width=code_width)

    content.box(height=10)
    content.box(show="2+").text("""Clone() creates a new Arc.
Multiple variables remove aliasing.""")
    content.box(show="3+").text("Arc only provides ~emph{read-only} access (shared borrow).")

    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    slide.set_style("code2", slide.get_style("code").compose(s(size=32)))
    content = slide_header(slide, "Shared state concurrency")

    code_width = 800
    code(content.box(show="4+"), """
// Mutex::lock
fn lock(&self) -> &mut T;""", code_style="code2", width=code_width)

    content.box(height=20)
    code_step(content.box(width=code_width, height=320), """
let p = Arc::new(Mutex::new(5));
let tp = p.clone();
thread::spawn(move || {
    *tp.lock() = 10;
});
println!("{}", *p.lock());""", "1", (
        ("                 Mutex::new(5)  ", None, None, None, None, None),
        (0, None, None, None, None, None),
        (0, 1, 2, 3, 4, 5)
    ), width=code_width)


def message_passing(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Message passing")

    code_width = 900
    code_step(content.box(width=code_width, height=300), """
let (tx, rx) = mpsc::channel();
thread::spawn(move || {
    tx.send(5);
});
let received = rx.recv();
""", "1", (
        ("               mpsc::channel();", None, None, None, None),
        (0, None, None, None, None),
        (0, 1, 2, 3, None),
        (0, 1, 2, 3, 4)
    ), width=code_width)

    content.box(height=20)
    content.box(show="next+").text("""Splitting a channel into a receiver + sender removes aliasing
    and allows moving the sender independently of the receiver.""", s(size=34))


def unsafe(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=32))
    content = slide_header(slide, "Where's the catch?")
    content.box().text("We have seen things that mutate through a shared borrow")

    code_width = 800
    code_step(content.box(width=code_width, height=400), """
// Arc::clone
fn clone(&self) -> Arc<T>;
// Mutex::lock
fn lock(&self) -> &mut T;
// AtomicU64::store
fn store(&self, val: u64, order: Ordering);
""", 2, [
        (0, 1, None, None, None, None),
        (0, 1, 2, 3, None, None),
        (0, 1, 2, 3, 4, 5)
    ], width=code_width)

    content.box(show="5+").text("This is called ~tt{interior mutability} and requires unsafe Rust",
                                s(size=32))

    slide = slides.new_slide()
    content = slide_header(slide, "Enter unsafe Rust")
    content.box().text("Some scenarios are not expressible in (safe) Rust")

    content.box(height=20)
    content.box(show="next+").text("In some cases, something more is required to:")

    list = content.box()
    list_item(list, show="next+").text("Express inherently unsafe paradigms")
    list_item(list, show="next+").text("Improve performance")
    list_item(list, show="next+").text("Interact with I/O, OS, hardware, network")

    slide = slides.new_slide()
    content = slide_header(slide, "Unsafe Rust")

    content.box().text("You can mark parts of code with the ~tt{unsafe} keyword")
    content.box(show="next+").text("Unsafe Rust is a ~emph{superset} of Rust")

    def unsafe_slide(header, code_body, content_show="1", code_size=36):
        slide = slides.new_slide()
        slide.update_style("code", s(size=code_size))
        content = slide_header(slide, "Unsafe Rust")
        content.box(y=0).text("Unsafe Rust allows:")

        content.box(height=20)
        content.box(show=content_show).text(header)
        content.box(height=10)
        code(content.box(show=content_show), code_body)

    unsafe_slide("Accessing a global mutable variable", """
static mut COUNTER: u32 = 0;

fn increment_count() {
    unsafe {
        COUNTER += 1;
    }
}""", content_show="2+")
    unsafe_slide("Dereferencing a raw pointer", """
let ptr = 0xCAFECAFE as *mut u32;
unsafe {
    *ptr = 5;
}""")
    unsafe_slide("Calling an unsafe function", """
unsafe {
    zlib_compress(&buffer, buffer.len());
}""")
    unsafe_slide("Implementing an unsafe trait", """
unsafe impl Send for MySuperSafeType {
    ...
}""")

    slide = slides.new_slide()
    slide.update_style("code", s(size=18))
    content = slide_header(slide, "Finding unsafe code - C++")
    code_box = code(content, """
std::atomic<LifecycleId> ArenaImpl::lifecycle_id_generator_;
GOOGLE_THREAD_LOCAL ArenaImpl::ThreadCache ArenaImpl::thread_cache_ = {-1, NULL};

void ArenaImpl::Init() {
  lifecycle_id_ =
      lifecycle_id_generator_.fetch_add(1, std::memory_order_relaxed);
  hint_.store(nullptr, std::memory_order_relaxed);
  threads_.store(nullptr, std::memory_order_relaxed);

  if (initial_block_) {
    // Thread which calls Init() owns the first block. This allows the
    // single-threaded case to allocate on the first block without having to
    // perform atomic operations.
    new (initial_block_) Block(options_.initial_block_size, NULL);
    SerialArena* serial =
        SerialArena::New(initial_block_, &thread_cache(), this);
    serial->set_next(NULL);
    threads_.store(serial, std::memory_order_relaxed);
    space_allocated_.store(options_.initial_block_size,
                           std::memory_order_relaxed);
    CacheSerialArena(serial);
  } else {
    space_allocated_.store(0, std::memory_order_relaxed);
  }
}
""")
    code_box.overlay(show="2+", z_level=99).rect(bg_color=CODE_HIGHLIGHT_COLOR)

    slide = slides.new_slide()
    content = slide_header(slide, "Finding unsafe code - Rust")
    bash(content.box(), '$ grep "unsafe" main.rs', text_style=s(size=40))

    slide = slides.new_slide()
    slide.box().text("""Rust builds safe abstractions
on top of unsafe foundations""", s(size=50))


def fearless_concurrency(slides: Slides):
    intro_slide(slides)
    concurrency_issues(slides)
    shared_state(slides)
    message_passing(slides)
    unsafe(slides)
