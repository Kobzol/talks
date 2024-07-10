from typing import Optional, Tuple, List

from elsie import SlideDeck, Arrow
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from config import sh, sw, EXTENDED
from utils import code, code_line_by_line, quotation


def up_arrow(slide: Box, target: Box, text: Optional[str] = None, offset: int = -300):
    box = slide.box(x=target.x("50%"), y=target.y("100%"),
                    z_level=999,
                    height=sh(200)).line((
        (target.x("50%"), target.y("100%").add(sh(200))),
        (target.x("50%"), target.y("100%")),
    ), end_arrow=Arrow(size=sw(40)), stroke_width=sw(20), color="red")
    if text is not None:
        slide.box(x=box.x("0").add(sw(offset)), y=box.y("100%")).text(text, T(color="red"))


def type_hints(slides: SlideDeck):
    @slides.slide()
    def what_is_typing(slide: Box):
        slide.update_style("code", T(size=sw(65)))
        box = code(slide.box(), """
def visit_europython(visitor: ~#visitor{Visitor}):
  ...
""", use_styles=True)
        box = box.inline_box("#visitor")
        up_arrow(slide, box)

    @slides.slide()
    def pep_484(slide: Box):
        """
        Python 3.5, 2014.
        """
        slide.box(width=sw(1400)).image("images/pep-484.png")

    # if EXTENDED:
    @slides.slide()
    def where_to_use_type_hints(slide: Box):
        slide.box().text("Where to use type hints?", T(size=sw(100)))

    @slides.slide()
    def interface_boundaries(slide: Box):
        slide.box(p_bottom=sh(80), y=sh(150)).text("Interface boundaries", T(size=sw(100)))
        box = code(slide.box(show="last+"), """
def add(x: ~#param1{int}, b: ~#param2{int}) -> ~#rettype{int}:
  ...
""", use_styles=True)
        up_arrow(slide.box(show="next"), box.inline_box("#param1"))
        up_arrow(slide.box(show="last"), box.inline_box("#param2"))
        up_arrow(slide.box(show="next+"), box.inline_box("#rettype"))

    @slides.slide()
    def classes(slide: Box):
        slide.box(p_bottom=sh(80), y=sh(150)).text("(Data)class fields", T(size=sw(100)))
        code(slide.box(show="last+"), """
@dataclass
class Person:
  name: str
  age: int
""", width=sw(1000))

    @slides.slide()
    def variables(slide: Box):
            slide.update_style("code", T(size=sw(60)))
            slide.box(p_bottom=sh(80), y=sh(150)).text("(Rarely) variables", T(size=sw(100)))
            box = code_line_by_line(slide.box(show="last+"), """
result: MyClass = foo().get("bar")[0]
x: int = 0
""", width=sw(1000))
            line_0 = box.line_box(0)
            line_1 = box.line_box(1)
            slide.box(x=line_0.x("100%").add(sw(100)), y=line_0.y("0"), width=sw(80)).image("images/checkmark.png")
            slide.box(x=line_1.x("100%").add(sw(100)), y=line_1.y("0"), width=sw(70), show="last").image(
                "images/cross.png")

    @slides.slide()
    def type_hint_examples(slide: Box):
        code_line_by_line(slide.box(width=sw(1400), x="[50%]", y="[50%]"), """
x: int
x: Person
x: List[int]
x: Dict[str, int]
x: int  | str
x: bool | None
x: Literal["GET", "POST"]
from typing import ...
""", width="fill")

    @slides.slide()
    def why_type_hints(slide: Box):
        slide.box().text("Why type hints?", T(size=sw(100)))

    @slides.slide()
    def types_help_me_understand(slide: Box):
        slide.box().text("Types help me understand…", T(size=sw(100)))

    @slides.slide()
    def missing_type_hints(slide: Box):
        """
        More thinking when writing code => better
        Easier to understand
        Foreign code
        """
        code(slide.box(), """
def find_item(items, check):
""")

    @slides.slide()
    def present_type_hints(slide: Box):
        box = code_line_by_line(slide.box(x="[50%]", y="[50%]"), """
def find_item(
  items: Iterable[Item],
  check: Callable[[Item], bool]
) -> Item | None:
""", width=sw(1700))
        slide.box(show="next+", y=box.y("120%")).text("Documentation", T(size=sw(80)))

    @slides.slide()
    def and_remember(slide: Box):
        slide.box().text("…and remember", T(size=sw(100)))

    @slides.slide()
    def bp_code(slide: Box):
        """
        https://github.com/Kobzol/debug-visualizer/blob/master/debugger/debugee.py#L138C1-L139C29
        """
        code(slide.box(), """
def __init__(
  self,
  address=None,
  name=None,
  value=None,
  type=None,
  path=None
):
""")

    @slides.slide()
    def gandalf_meme(slide: Box):
        slide.box(width=sw(750)).image("images/gandalf-meme.jpg")

    @slides.slide()
    def faster_writing(slide: Box):
        slide.box().text("Types help me write code faster", T(size=sw(100)))

    @slides.slide()
    def completion(slide: Box):
        row = slide.box(horizontal=True)
        height = 700
        row.box(height=sh(height)).image("images/completion-missing.png")
        row.box(p_x=sw(60), show="next+").text("vs")
        row.box(height=sh(height), show="last+").image("images/completion-present.png")

    @slides.slide()
    def navigation(slide: Box):
        row = slide.box(horizontal=True)
        height = 350
        row.box(height=sh(height)).image("images/navigation-click.png")
        row.box(width=sw(100), show="next+").line([(20, 0), (80, 0)], end_arrow=Arrow(size=sw(40)),
                                                  stroke_width=sw(20))
        row.box(height=sh(height), show="last+").image("images/navigation-target.png")

    @slides.slide()
    def detect_complex_code(slide: Box):
        slide.box().text("Types help me detect complex code", T(size=sw(100)))

    @slides.slide()
    def detect_complex_code(slide: Box):
        """
        Just because we can write code like this, doesn't mean we have to
        """
        slide.update_style("code", T(size=sw(50)))
        code(slide.box(p_bottom=sh(40)), """
def store_visited_talks(
  visitors: Visitor | List[Visitor] | Dict[str, Visitor],
  talks: List[str | Dict[str, Dict[str, int]]]
) -> List[Tuple[str | Dict[str, str], int]] | int
""")
        slide.box(show="next+").text("Hard to type => hard to understand?")

    @slides.slide()
    def type_hints_are_optional(slide: Box):
        slide.box(p_bottom=sh(60)).text("Type hints are still optional!", T(size=sw(80)))
        box = code(slide.box(show="next+"), """
def log_data(data: ~#arg{Any}):
  ...
""", use_styles=True)
        up_arrow(slide.box(show="next+"), box.inline_box("#arg"), "This is fine!", -200)

    @slides.slide()
    def types_are_introspectable(slide: Box):
        slide.box().text("Types are introspectable", T(size=sw(100)))

    @slides.slide()
    def fastapi(slide: Box):
        """
        Mention typer.
        """
        box = code(slide.box(), """
app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: ~#param{int}):
  ...
""", use_styles=True)
        up_arrow(slide.box(show="next+"), box.inline_box("#param"), "Parsed as a number")

    # if EXTENDED:
    #     @slides.slide()
    #     def typer(slide: Box):
    #       box = code(slide.box(), """
    # app = Typer()
    #
    # @app.command()
    # def visit_ep(
    #   name: str,
    #   ~#arg{party}: bool = False
    # ):
    #     ...
    # """, use_styles=True)
    #         up_arrow(slide.box(show="next+"), box.inline_box("#arg"), "~tt{--party}", offset=-150)

    @slides.slide()
    def type_checking(slide: Box):
        """
        Notice that I haven't mentioned any type checking so far!
        """
        slide.box(p_bottom=sh(60)).text("Type checking", T(size=sw(80)))
        slide.box(show="next+").text("~tt{pyright}, ~tt{mypy}, …")

    @slides.slide()
    def type_checker(slide: Box):
        slide.box(width=sw(1600), p_bottom=sh(40)).image("images/mypy-error.png")
        slide.box(show="next+").text("Configure type-checking in CI!")

    @slides.slide()
    def types_are_tests(slide: Box):
        slide.box(p_bottom=sh(40)).text("Each type becomes a mini-test", T(size=sw(80)))
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("Does not need maintenance/refactoring")
        lst.item(show="next+").text("Low-latency feedback")

    @slides.slide()
    def type_checking_sequence(slide: Box):
        """
        Detect big and trivial errors through an annoying debugging loop.
        """

        def horizontal_bar(parent: Box, boxes: List[Tuple[Optional[str], int, str]]):
            row = parent.box(horizontal=True, width=sw(1400), height=sh(100))
            row.rect(color="black", stroke_width=sw(10))
            inner = row.box(width="100%", height="100%", p_x=sw(5), p_y=sh(5), horizontal=True)

            border_width = 10
            x = 0
            for (name, width, color) in boxes:
                wrapper = inner.box(show="next+", x=sw(x), width=sw(width), height="100%").rect(bg_color=color)
                if name is not None:
                    wrapper.box(show="last+", padding=15).text(name, T(color="white", size=sw(36), bold=True))
                x += width
                inner.box(x=sw(x), show="last+", width=sw(border_width), height="100%").rect(bg_color="black")
                x += border_width

        slide.box(p_bottom=sh(100)).text("Making a code change")

        run_fix = [
            ("Run", 140, "blue"),
            ("Fix error", 165, "red")
        ]
        boxes = [
            *run_fix,
            *run_fix,
            *run_fix,
            *run_fix
        ]
        slide.box(show="next+", p_bottom=sh(40)).text("Without type checking")
        horizontal_bar(slide.box(show="last+", p_bottom=sh(80)), boxes)

        boxes = [
            ("TC", 100, "green"),
            ("Fix type errors", 300, "red"),
            *run_fix
        ]
        slide.box(show="next+", p_bottom=sh(40)).text("With type checking")
        horizontal_bar(slide.box(show="last+", p_bottom=sh(80)), boxes)

        slide.box(show="next+").text("You can combine both!")

    @slides.slide()
    def type_checking_benchmark(slide: Box):
        slide.box(p_bottom=sh(40)).text('FastAPI "benchmark"')
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("pytest: ~30s", escape_char="|")
        lst.item(show="next+").text("mypy: ~1s", escape_char="|")

    # if EXTENDED:
    #     @slides.slide()
    #     def documentation(slide: Box):
    #         """
    #         Not a full substitute for documentation
    #         """
    #         slide.box().text("Types serve as documentation", T(size=sw(100)))
    #         slide.box(show="next+").text("…that doesn't get stale")

    @slides.slide()
    def runtime_checks(slide: Box):
        slide.box(p_bottom=sh(60)).text("Runtime type checks")
        code(slide.box(show="next+", p_bottom=sh(60)), """
@beartype
def get_visitor(name: str):
  ...

get_visitor(1)
""")
        slide.box(show="next+", width=sw(1800)).image("images/beartype-error.png")

    @slides.slide()
    def confidence(slide: Box):
        slide.box(p_bottom=sh(40)).text("Improves ~bold{confidence} in code", T(size=sw(80)))
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("Easier code review", T(size=sw(80)))
        lst.item(show="next+").text('"Fearless" refactoring', T(size=sw(80)))

    @slides.slide()
    def disadvantages(slide: Box):
        slide.box().text("Disadvantages?", T(size=sw(100)))

    @slides.slide()
    def longer_to_type(slide: Box):
        quotation(slide.box(p_bottom=sh(60)), "More characters to type",
                  size=sw(80))
        slide.box(show="next+", width=sw(400)).image("images/shrug.png")

    @slides.slide()
    def longer_to_type(slide: Box):
        quotation(slide.box(), "Useless for throwaway code",
                  size=sw(80))

    @slides.slide()
    def a_familiar_story(slide: Box):
        """
        If you're programming for more than 5 minutes, it is worth it.
        """
        style = T(align="left")

        col = slide.box(x="[50%]")
        col.box(width="100%", p_bottom=sh(20)).text("Me: <gets an idea>", style)
        col.box(show="next+", width="100%", p_bottom=sh(20)).text("Let's write a prototype to evaluate it!", style)
        box = col.box(show="next+", width="100%", p_bottom=sh(20)).text("Should I use type hints?", style)
        slide.box(show="last+", x=box.x("60%"), y=box.y("0"), width=sw(100)).image("images/thinking-emoji.png")
        col.box(show="next+", width="100%", p_bottom=sh(20)).text("Nah, this code will be gone by next week", style)
        box = col.box(width="100%", p_bottom=sh(20))
        box.box(show="next+").text("(three years later)", style)
        col.box(show="next+", width="100%").text("Sh*t! It crashed in production again…", style)
        col.box(show="next+", width="100%").text("Wait, how did this ever work?!", style)

        slide.box(p_top=sh(80), show="next+").text("Sounds familiar? :)", T(size=sw(80)))

    @slides.slide()
    def false_sense_of_security(slide: Box):
        quotation(slide.box(p_bottom=sh(60)), "False sense of security",
                  size=sw(80))
        slide.box(show="next+").text("Remember: type hints are not perfect!", T(size=sw(80)))

    @slides.slide()
    def lipstick_on_a_pig(slide: Box):
        quotation(slide.box(), "It feels like lipstick on a pig.", "HackerNews user",
                  size=sw(80))
