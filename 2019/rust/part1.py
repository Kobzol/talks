from elsie import Arrow, Slides, TextStyle as s

from utils import CODE_HIGHLIGHT_COLOR, bash, code, code_step, list_item, slide_header


def intro_slide(slides: Slides):
    slide = slides.new_slide()
    slide.set_style("text", s(size=60, bold=True))
    slide.set_style("orange", slide.get_style("text").compose(s(color="orange")))

    fast = slide.box()
    fast.text("~orange{Fast} & Safe", style="text")

    slide.box(height=100)

    line = slide.box(width="fill", horizontal=True)
    development = line.box(width="50%", y=0)
    development.overlay(show="2-3").text("Quick development")
    development.overlay(show="4").text("Quick development", s(
        color="orange"
    ))
    performance = line.box(width="50%", y=0, show="3+")
    performance.text("High performance")

    arrow = Arrow(20)
    slide.box(show="2+").line([fast.p("15%", "100%"), development.p("50%", 0)],
                              stroke_width=5, color="orange", end_arrow=arrow)
    slide.box(show="3+").line([fast.p("15%", "100%"), performance.p("50%", 0)],
                              stroke_width=5, color="orange", end_arrow=arrow)


def project(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Project management (Cargo)")
    content.box(height=400).image("imgs/cargo.png")

    slide = slides.new_slide()
    slide.update_style("code", s(size=30))

    content = slide_header(slide, "Using libraries")

    line = content.box(width="fill", horizontal=True)

    cargo = line.box(width="50%", p_right=50)
    cargo.box().text("Cargo.toml")
    cargo_code = code(cargo.box(), """
[package]
name = "hello_world"
version = "0.1.0"

[dependencies]
ibverbs = "0.4"
json = "1.0"
protobuf = "2.0"
""", "toml")

    main = line.box(width="50%", show="2+", y=0)
    main.box().text("main.rs")
    main_code = code(main.box(), """
use json::parse;

fn main() {
    parse("data.json");
}""")

    arrow = Arrow(20)
    p1 = cargo_code.line_box(5).p("100%", "50%")
    p2 = main_code.line_box(0).p(0, "50%")
    slide.box(show="2+").line([p1.add(-40, 0), p1, p2.add(-10, 0)],
                              stroke_width=5, color="orange", end_arrow=arrow)

    content.box(height=10)
    content.box(show="3+").text("More than 26k libraries available")

    slide = slides.new_slide()
    content = slide_header(slide, "Unified documentation")
    content.box(width=900).image("imgs/rust-docs.png")

    slide = slides.new_slide()
    content = slide_header(slide, "Integrated tooling")

    def cargo_line(parent, text, code, show="1+", **text_args):
        wrapper = parent.box(width="fill", horizontal=True, show=show)
        textbox = wrapper.box(width="50%")
        textbox = textbox.text(text, **text_args)

        codebox = wrapper.box(width="40%")
        bash(codebox, code, x=0, width="fill")
        return textbox

    wrapper = content.box(width="fill")
    cargo_line(wrapper, "Build", "$ cargo build", "1+")
    cargo_line(wrapper, "Run", "$ cargo run", "2+")

    slide = slides.new_slide()
    slide.update_style("code", s(size=40))
    content = slide_header(slide, "Integrated tooling (tests)")

    code(content.box(), """
#[test]
fn test_add() {
    assert_eq!(add(1, 2), 3);
}
""")

    content.box(height=20)
    bash(content.box(show="2+"), "$ cargo test")

    slide = slides.new_slide()
    slide.update_style("code", s(size=40))
    content = slide_header(slide, "Integrated tooling (benchmarks)")

    code(content.box(), """
#[bench]
fn bench_add_two(b: &mut Bencher) {
    b.iter(|| add_two(2));
}
""")

    content.box(height=20)
    bash(content.box(show="2+"), "$ cargo bench")

    slide = slides.new_slide()
    content = slide_header(slide, "Integrated tooling")
    wrapper = content.box(width="fill")
    cargo_line(wrapper, "Format", "$ cargo fmt")
    cargo_line(wrapper, "Lint", "$ cargo clippy", "next+")
    box = cargo_line(wrapper, "Publish to SC", "$ cargo publish", "next+")
    box = box.line_box(0)
    box.line([box.p("53%", "55%"), box.p("73%", "55%")], stroke_width=3)

    slide = slides.new_slide()
    slide.update_style("code", s(size=24))
    content = slide_header(slide, "Build scripts")
    content.box().text("build.rs")

    code_width = 940
    code_step(content.box(width=code_width, height=400), """
fn main() {
    // generate Protobuf objects
    protoc_rust::run("protobuf/message.proto", "src/protos");

    // generate C headers
    cbindgen::Builder::new()
      .generate()
      .write_to_file("bindings.h");
}
""", "1", (
        (0, 1, 2, 3, None, None, None, None, 8),
        (0, 1, 2, 3, 4, 5, 6, 7, 8)
    ), width=code_width)

    slide = slides.new_slide()
    content = slide_header(slide, "(interlude)")
    content.box(height=600).image("imgs/meme-cargo.jpg")


def multiphase_compiler(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=34))
    content = slide_header(slide, "Multi-phase compiler")

    code(content.box(), """
fn main() {
    look_ma_no_forward_declaration();
}

fn look_ma_no_forward_declaration() { }
""")


def modules(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=24))
    slide.set_style("bold", s(bold=True))
    content = slide_header(slide, "Proper module system")

    line = content.box(width="fill", horizontal=True)
    lib = line.box(width="50%", y=0)
    text_box = lib.box()
    text_box.box(show="1").text("foo.rs")
    text_box.overlay(show="next+").text("~bold{foo}.rs")
    code(lib.box(), """
pub fn fun1() {
    println!("fun1");
}
fn fun2() {
    println!("fun2");
}
""")

    main = line.box(width="50%", y=0, show="2+")
    main.box().text("main.rs")
    code(main.box(), """
use foo;

fn main() {
    foo::fun1();
    // foo::fun2(); private
}""")

    content.box(height=60)
    advantages = content.box(show="3+")
    advantages.update_style("default", s(size=40))
    list_item(advantages).text("visibility control")
    list_item(advantages).text("self-contained")


def structures(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=26))
    content = slide_header(slide, "Structures")

    code_width = 920
    code(content.box(), """
struct Person {
    pub age: u32,
    name: String
}
""", width=code_width)

    code(content.box(show="next+"), """
impl Person {
    pub fn new(age: u32, name: String) -> Person {
        Person { age, name }
    }
    pub fn is_adult(&self) -> bool {
        self.age >= 18
    }
}    
""", width=code_width)


def traits(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=26))
    content = slide_header(slide, "Traits")

    code_width = 960
    code(content.box(), """
trait Buffer {
    fn size(&self) -> usize;
    fn read(&self) -> u8;
}""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), "struct MemBuffer { data: Vec<u8> }", width=code_width)
    code(content.box(show="next+"), """
impl Buffer for MemBuffer {
    fn size(&self) -> usize { self.data.size() }
    fn read(&self) -> u8 { ... }
}""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), "struct FileBuffer { path: String }", width=code_width)
    code(content.box(show="next+"), """
impl Buffer for FileBuffer {
    fn size() -> usize { fs::metadata(self.path).len() }
    fn read(&self) -> u8 { ... }
}
""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=32))
    content = slide_header(slide, "Built-in traits")
    code(content.box(), """
impl Display for Person {
    fn fmt(&self, f: Formatter) -> Result { ... }
}
println!("{}", person);
""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), """
impl From<String> for IPAddress {
    fn from(value: String) -> IPAddress { ... }
}
let ip: IPAddress = "127.0.0.1".into();
""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), """
impl Add for Matrix {
    fn add(self, other: Matrix) -> Matrix { ... }
}
let c: Matrix = matA + matB;
""", width=code_width)


def generics(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=30))
    content = slide_header(slide, "Generics")

    code_width = 900

    code(content.box(), """
struct KeyValue<K, V> {
    key: K,
    value: V
}""", width=code_width)
    code(content.box(show="next+"), """
trait Buffer<T> {
    fn read(&self) -> T;    
}""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), """
fn print_buffer<B: Buffer<T>, T: Display>(buffer: B) {
    println!("{}", buffer.read());
}""", width=code_width)
    code(content.box(show="next+"), """
fn print_bigger<T: PartialEq + Display>(a: T, b: T) {
    if (a > b) { println!("{}", a); }
}
""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), """
impl <T: Display> Serialize for T {
    ...
}
""", width=code_width)


def adt(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=26))
    content = slide_header(slide, """Algebraic data types/tagged unions/sum types/
discriminated unions/variants""")

    code_width = 960
    code(content.box(), """
enum Packet {
    Header { source: u32, tag: u32, data: Vec<u8> },
    Payload { data: Vec<u8> },
    Ack { seq: u64 }
}""", width=code_width)

    content.box(height=10)
    content.box(show="next+").text("Pattern matching", style=s(bold=True, size=40))

    code(content.box(show="last+"), """
match socket.get_packet() {
    Header {data, ..} | Payload {data, ..} => { },
    _ => { println!("Packet without data"); }
}
""", width=code_width)

    content.box(height=10)
    content.box(show="next+").text("The compiler forces you to handle all variants")


def error_handling(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=24))
    content = slide_header(slide, "Error handling")

    code_width = 940
    code(content.box(), """
enum Option<T> {
    None,
    Some(T)
}
""", width=code_width)

    content.box(height=20)
    code(content.box(show="next+"), """
fn find_index(items: &[u32], item: u32) -> Option<usize> {
    ...
}""", width=code_width)

    code(content.box(show="next+"), """
let index = match find_index(&[1, 2, 3], 4) {
    Some(index) => println!("index found: {}", index),
    None => println!("index not found")
}
""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=26))
    content = slide_header(slide, "Error handling")

    code(content.box(), """
enum Result<T, E> {
    Ok(T),
    Err(E),
}
""", width=code_width)

    content.box(height=20)
    code(content.box(show="next+"), """
fn find_in_db(...) -> Result<Vec<DbRow>, DbError> {
    ...
}""", width=code_width)

    code(content.box(show="next+"), """
let item = match find_in_db(...) {
    Ok(item) => item,
    Err(error) => {
        println!("Error: {}", error);
        vec!()
    }
}
""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=30))
    content = slide_header(slide, "Error handling")
    box = code(content.box(), """
fn download(address: String) -> Result<Vec<u8>> {
    let ip = address.parse()?;
    let client = TcpStream::connect(ip)?;

    let mut buf = vec!();
    client.read(&mut buf)?;
    buf
}
""", width=code_width)
    box.line_box(1, x=420, width=15, show="last+", z_level=99).rect(bg_color=CODE_HIGHLIGHT_COLOR)
    box.line_box(2, x=585, width=15, show="last+", z_level=99).rect(bg_color=CODE_HIGHLIGHT_COLOR)
    box.line_box(5, x=375, width=15, show="last+", z_level=99).rect(bg_color=CODE_HIGHLIGHT_COLOR)

    content.box(height=20)
    code(content.box(show="next+"), "let item = value?;", width=code_width)
    code(content.box(show="next+"), """// expands to
let item = match value {
    Ok(v) => v,
    Err(e) => return Err(e)
};
""", width=code_width)


def macros(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=22))
    content = slide_header(slide, "Macros")

    code_width = 920
    code_step(content.box(width=code_width, height=200), """
macro_rules! find_min {
    ($x:expr) => ($x);
    ($x:expr, $($y:expr),+) => (
        std::cmp::min($x, find_min!($($y),+))
    )
}    
""", "1", (
        (0, 1, None, None, None, 5),
        (0, 1, 2, 3, 4, 5)
    ), width=code_width)
    code(content.box(show="next+"), """
find_min!(5);       // 5
find_min!(2, 1, 3); // 1    
""", width=code_width)

    content.box(height=20)
    code(content.box(show="next+"), """
macro_rules! create_function {
    ($func_name:ident) => (
        fn $func_name() {
            println!("You called {:?}()", stringify!($func_name));
        }
    )
}""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=22))
    content = slide_header(slide, "Procedural macros")

    code_width = 920
    code(content.box(), """
fn my_macro(attr: TokenStream, item: TokenStream) -> TokenStream {
    ...
}""", width=code_width)

    code(content.box(show="next+"), """
#[derive(my_macro)]
struct Record {
    #[my_macro]
    pub id: u32
}    
""", width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=26))
    content = slide_header(slide, "Procedural macros")

    code_width = 700
    code(content.box(), """
#[derive(Serialize, Deserialize)]
struct Person { name: String, age: u32 }""", width=code_width)
    code(content.box(show="next+"), """
json::to_string(person);
yaml::to_string(person);
let person = json::parse(person_str);""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), """
#[derive(CmdArgs)]
struct Args {
    #[arg(short = "d", long = "debug")]
    debug: bool,
    #[arg(parse(from_os_str))]
    path: PathBuf,
}
""", width=code_width)

    content.box(height=10)
    code(content.box(show="next+"), """
#[derive(Debug)]
struct Person { name: String, age: u32 }

println!("{:?}", person);
""", width=code_width)


def qol(slides: Slides):
    slide = slides.new_slide()
    slide.update_style("code", s(size=50))
    content = slide_header(slide, "Type inference")

    code_width = 900
    code_step(content.box(width=code_width, height=400), """
let elem = 5u8;
let mut vec = Vec::new();
vec.push(elem);
// vec is now Vec<u8>
""", "1", (
        (0, None, None, None),
        (0, 1, None, None),
        (0, 1, 2, None),
        (0, 1, 2, 3)
    ), width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=50))
    content = slide_header(slide, "Iterators")

    code_step(content.box(width=code_width, height=400), """
vec.iter()
   .zip(iter2)
   .filter(|(a, b)| a > b)
   .map(|(a, b)| a * b)
   .sum::<i32>();
""", "1", (
        (0, None, None, None, None),
        (0, 1, None, None, None),
        (0, 1, 2, None, None),
        (0, 1, 2, 3, None),
        (0, 1, 2, 3, 4)
    ), width=code_width)

    slide = slides.new_slide()
    slide.update_style("code", s(size=32))
    content = slide_header(slide, "Generators")

    code(content.box(), """
let mut fibonacci = || {
    yield 1;

    let mut a = 0;
    let mut b = 1;
    loop {
        yield a + b;
        a = b;
        b = a + b;
    }
};
let f = fibonacci().iter().take(5).collect();
""")

    slide = slides.new_slide()
    slide.update_style("code", s(size=26))
    content = slide_header(slide, "Async/await")

    code(content.box(), """
async fn compute_job(job: Job) -> Result<Data, Error> {
    let worker = await!(query_broker());
    match worker {
        Some(worker) => await!(send_job(worker)),
        None => await!(process_job_locally(job))
    }
}
""")


def design(slides: Slides):
    slide = slides.new_slide()
    content = slide_header(slide, "Design by community")

    list = content.box()
    list_item(list).text("Open source")
    list_item(list).text("RFC")
    list.box(width=700, height=200, p_top=40).image("imgs/rust-rfc.png")

    slide = slides.new_slide()
    content = slide_header(slide, "Backwards compatibility")

    small = s(size=28)

    list = content.box()
    list_item(list).text("Strong BC guarantees")
    list_item(list, show="2+").text("New version every 6 weeks")
    list_item(list, show="2+", level=1).text("Thousands of libraries tested to spot regressions",
                                             style=small)
    list_item(list, show="3+").text("Big changes => new edition")
    list_item(list, show="3+", level=1).text("Rust 2015 vs Rust 2018", style=small)

    slide = slides.new_slide()
    slide.update_style("code", s(size=38))
    content = slide_header(slide, "Unstable features")

    code(content.box(), """
#![feature(async_await)]
async fn foo() {
    ...
}""")

    content.box(height=20)
    bash(content.box(show="2+"), "$ cargo +nightly build")


def features(slides: Slides):
    """
    Very quick overview of Rust's features, focusing on ease of usage.
    Direct comparison to C++.

    Who uses C++?
    Who likes C++?
    Will NOT explain features, just list them.
    """

    intro_slide(slides)
    project(slides)
    multiphase_compiler(slides)
    modules(slides)
    structures(slides)
    traits(slides)
    generics(slides)
    adt(slides)
    error_handling(slides)
    macros(slides)
    qol(slides)
    design(slides)
