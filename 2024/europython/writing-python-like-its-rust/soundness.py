from typing import Tuple, Optional

from elsie import SlideDeck, Arrow
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from config import sh, sw, EXTENDED
from utils import code, code_line_by_line, LOWER_OPACITY, create_grid, code_reveal, generate_qr_code


def soundness(slides: SlideDeck):
    def sound_definition(slide: Box, highlight: Optional[str] = None):
        slide.set_style("style1", T(bold=highlight == "style1"))
        slide.set_style("style2", T(bold=highlight == "style2"))
        slide.box(y="20%").text("Sound code = ~style1{impossible}* to ~style2{misuse}")
        # slide.box(show="next+", x="[95%]", y="[95%]").text("*or at least difficult")

    @slides.slide()
    def soundness_1(slide: Box):
        sound_definition(slide)

    @slides.slide()
    def soundness_2(slide: Box):
        sound_definition(slide, highlight="style2")
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("Break invariants")
        lst.item(show="next+").text("Unintended usage")
        lst.item(show="next+").text("Runtime failures, bugs")

    @slides.slide()
    def soundness_3(slide: Box):
        sound_definition(slide, highlight="style1")
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("Rust: compile-error")
        lst.item(show="next+").text("Python: type-check error")

    def cols(parent: Box, margin: int = 120) -> Tuple[Box, Box]:
        row = parent.box(width="100%", horizontal=True)
        left = row.box(p_right=sw(margin))
        right = row.box()
        return (left, right)

    ##### Newtype pattern #####

    @slides.slide()
    def newtype_db(slide: Box):
        slide.update_style("code", T(size=sw(60)))

        width = sw(1800)

        box = code_line_by_line(slide.box(p_bottom=sh(80)), """
def get_car_id(brand: str) -> int:
def get_driver_id(name: str) -> int:
def get_race(~#car{car}: int, ~#driver{driver}: int) -> Race:
""", width=width, use_styles=True)
        driver = box.inline_box("#driver")
        car = box.inline_box("#car")

        box = code_line_by_line(slide.box(show="next+"), """
car_id    = get_car_id("Mazda")
driver_id = get_driver_id("Stig")
race      = get_race(~#driver{driver_id}, ~#car{car_id})
""", width=width, use_styles=True, show_start=4)
        driver2 = box.inline_box("#driver")
        car2 = box.inline_box("#car")

        arrow = Arrow(size=sw(40))
        slide.box(show="next+", z_level=999).line((
            driver.p("50%", "100%"),
            driver2.p("50%", "0")
        ), color="red", stroke_width=sw(12), end_arrow=arrow, start_arrow=arrow)
        slide.box(show="last+", z_level=999).line((
            car.p("50%", "100%"),
            car2.p("50%", "0")
        ), color="red", stroke_width=sw(12), end_arrow=arrow, start_arrow=arrow)

    @slides.slide()
    def newtype_pattern(slide: Box):
        slide.update_style("code", T(size=sw(60)))
        slide.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")
        slide.box(p_bottom=sh(60)).text("Newtype pattern", T(bold=True))

        def code1(parent: Box, style: str = "code"):
            code(parent, """
# New type "CarId", internally an int
CarId    =  typing.NewType("CarId",    int)
DriverId =  typing.NewType("DriverId", int)
""", code_style=style)

        def code2(parent: Box, style: str = "code"):
            code(parent, """
def get_car_id(brand: str) -> CarId:
def race(car: CarId, driver: DriverId) -> Race:
""", code_style=style)

        code1_wrapper = slide.box(p_bottom=sh(60))
        code1(code1_wrapper.fbox(show="1-2"))

        code2_wrapper = slide.box(p_bottom=sh(60))
        code2(code2_wrapper.fbox(show="2"))

        code(slide.box(show="next+", p_bottom=sh(40)), """
get_race(driver_id, car_id)
""")
        code1(code1_wrapper.overlay(show="last+"), "code_muted")
        code2(code2_wrapper.overlay(show="last+"), "code_muted")
        slide.box(show="next+", width=sw(1800)).image("images/mypy-error-newtype.png")

    @slides.slide()
    def client_api_bad(slide: Box):
        slide.update_style("code", T(size=sw(50)))

        client_width = sw(900)
        (left, right) = cols(slide)
        code_reveal(left.box(), """
class Client:
  def connect(self):
  def send(self):
  def close(self):
""", 1, [1, 1, 1, 1], width=client_width)

        width_right = sw(700)
        def bad_code(code_contents: str):
            box = code(right.box(show="next+", p_bottom=sh(40)), code_contents, width=width_right,
                       return_parent=True)
            box.box(width=sw(100), x=box.x("[80%]"), y="[50%]").image("images/cross.png")

        bad_code("""
c.send()
c.connect()
""")
        bad_code("""
c.connect()
c.connect()
""")
        bad_code("""
c.close()
c.send()
""")
        bad_code("""
c.connect()
c.send()
# forgot to close
""")

    @slides.slide()
    def client_api_good(slide: Box):
        slide.update_style("code", T(size=sw(60)))
        slide.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")

        client_width = sw(1600)

        def show_and_fade(box: Box, code_contents: str):
            wrapper = box.box()
            code(wrapper.box(show=str(box.current_fragment())), code_contents, width=client_width)
            code(wrapper.overlay(show="next+"), code_contents, code_style="code_muted", width=client_width)

        def code2() -> str:
            return """
@contextmanager
def connect(address: str):
  client = create_client(address)
  try:
    yield client
  except:
    close_client(client)
"""

        show_and_fade(slide.box(p_bottom=sh(40)), """
class ConnectedClient:
  def send(self):
""")
        wrapper = slide.box(show="last+", p_bottom=sh(40))
        code_reveal(wrapper.box(), code2(), 2, [2, 1, 2, 2], width=client_width,
                    until_end=False)
        code(wrapper.overlay(show="next+"), code2(), code_style="code_muted", width=client_width)

        code(slide.box(show="last+"), """
with connect("localhost:80") as client:
  client.send()
""", width=client_width)

    @slides.slide()
    def invalid_states(slide: Box):
        """
        Prevent issues by construction.
        """
        slide.box().text("Make illegal states unrepresentable")

    @slides.slide()
    def api_auth_bad(slide: Box):
        slide.update_style("code", T(size=sw(50)))
        slide.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")

        client_width = sw(1700)

        def code1() -> str:
            return """
class RequestBuilder:
  def api_token(self, token: str):
  def password(self,  username: str, password: str):
  def build(self) -> Request:
"""

        wrapper = slide.box(p_bottom=sh(60))
        code_reveal(wrapper.box(), code1(), 1, [1, 1, 1, 1], width=client_width, until_end=False)
        code(wrapper.overlay(show="next+"), code1(), width=client_width, code_style="code_muted")

        def code2() -> str:
            return """
class RequestWithToken:
  def build(self) -> Request:
"""

        wrapper = slide.box(show="last+", p_bottom=sh(40))
        code(wrapper.box(show="5-6"), code2())
        code(wrapper.overlay(show="last+"), code2(), code_style="code_muted")

        def code3() -> str:
            return """
class RequestWithPassword:
  def build(self) -> Request:
"""

        wrapper = slide.box(show="6+", p_bottom=sh(40))
        code(wrapper.box(show="6"), code3())
        code(wrapper.overlay(show="7+"), code3(), code_style="code_muted")

        code(slide.box(show="last+"), """
class RequestBuilder:
  def api_token(...) -> RequestWithToken:
  def password(...) -> RequestWithPassword:
""", width=client_width)

    def button_slide(slides: SlideDeck, hover: bool, timer_ms: Optional[int] = None):
        slide = slides.new_slide()
        row = slide.box(horizontal=True)
        radius = 10
        width = sw(500)
        height = sh(140)

        border_color = "black"
        if hover:
            border_color = "red"

        bg_color = None
        font_color = "black"
        if timer_ms is not None and timer_ms >= 3000:
            bg_color = "#FF7B7B"
            font_color = "white"

        button = row.box(
            width=width,
            height=height,
            p_right=sw(100)
        ).rect(color=border_color, bg_color=bg_color, rx=sw(radius), ry=sh(radius), stroke_width=sw(10))
        button.text("Select me", T(color=font_color))

        args = dict(width=sw(100), x=button.x("120%"), y="10%", z_level=999)
        if hover:
            args["x"] = button.x("55%")
        row.box(**args).image("images/hand-icon.png")

        if timer_ms is not None:
            row.box(x=button.x("150%"), width=sw(200)).text(f"{timer_ms / 1000:.1f}s", T(align="right"))

    button_slide(slides, hover=False)
    button_slide(slides, hover=True, timer_ms=0)
    button_slide(slides, hover=True, timer_ms=800)
    button_slide(slides, hover=True, timer_ms=1500)
    button_slide(slides, hover=True, timer_ms=3000)

    @slides.slide()
    def button_dataclass(slide: Box):
        width = sw(1500)
        code_reveal(slide.box(p_bottom=sh(40)), """
@dataclass
class ButtonState:
  hover: bool
  selected: bool
  timer: Optional[timedelta]
""", 1, [2, 1, 1, 1], width=width)
        slide.box(show="next+").text("~tt{hover == False + selected == True?}")
        slide.box(show="next+").text("~tt{selected == True + timer < 3s?}")

    @slides.slide()
    def button_mistake(slide: Box):
        slide.update_style("code", T(size=sw(60)))
        code_reveal(slide.box(p_bottom=sh(40)), """
def on_hand_leave(state: ButtonState):
  state.hover = False
  # What about selected/timer?
""", 1, [2, 1])

    @slides.slide()
    def button_sumtype(slide: Box):
        slide.update_style("code", T(size=sw(50)))
        slide.box(p_bottom=sh(60)).text("State machine + sum types", T(bold=True))

        width = sw(1800)
        code_reveal(slide.box(p_bottom=sh(40)), """
@dataclass
class ButtonInactive:
  pass

@dataclass
class ButtonHover:
  timer: timedelta

@dataclass
class ButtonSelected:
  pass

ButtonState = ButtonInactive | ButtonHover | ButtonSelected
""", 1, [3, 4, 4, 2], width=width)

    @slides.slide()
    def button_handle_1(slide: Box):
        slide.update_style("code", T(size=sw(50)))

        width = sw(1700)
        code_reveal(slide.box(), """
def update_state(
  state: ButtonState,
  hover: bool,
  delta_time: timedelta
) -> ButtonState:
  match state:
    case ButtonInactive():
      if hover:
        return ButtonHover(timer=timedelta())
      return state
    ...
""", 1, [1, 1, 1, 1, 1, 1, 1, 2, 2], width=width)

    @slides.slide()
    def button_handle_2(slide: Box):
        slide.update_style("code", T(size=sw(50)))

        width = sw(1700)
        code_reveal(slide.box(), """
...
match state:
  case ButtonHover(timer):
    if not hover:
      return ButtonInactive()
    if timer + delta_time >= SELECT_TIME:
      return ButtonSelected()
    return ButtonHover(timer=state.timer + delta_time)
  case ButtonSelected():
    if not hover:
      return ButtonInactive()
    return state
  case _ as unreachable:
    typing.assert_never(unreachable)
""", 1, [2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2], width=width)

    ##### HTTP request builder #####
    ##### Many parameters #####
    ##### Construction functions #####
    ##### Normalized/denormalized BBox #####
    ##### Mutex #####

#     @slides.slide(debug_boxes=True)
#     def mutex_api(slide: Box):
#         # (top_left, top_right) = cols(slide.box())
#         # (bottom_left, bottom_right) = cols(slide.box())
#
#         grid = create_grid(slide)
#
#         slide.update_style("code", T(size=sw(60)))
#
#         width = sw(750)
#         code(grid.top_left.box(), """
# class Mutex:
#   def lock():
#   def unlock():
# """, width=width)
#         code_line_by_line(grid.top_right.box(show="next+"), """
# mutex = Mutex()
# mutex.lock()
# mutex.lock()
# """, show_start=2, width=width)
#         code_line_by_line(grid.bottom_left.box(show="next+"), """
# mutex = Mutex()
# mutex.lock()
# # no unlock
# """, show_start=4, width=width)
#         code_line_by_line(grid.bottom_right.box(show="next+"), """
# mutex = Mutex()
# data = []
# data.append(5)
# # forgot to lock
# """, show_start=4, width=width)
#
#     if EXTENDED:
#         @slides.slide()
#         def mutex_rust(slide: Box):
#             code_line_by_line(slide.box(), """
# let mutex = Mutex::new(1);
# let guard = mutex.lock();
# *guard += 1;
# // mutex.lock(); // compile error
# // guard automatically unlocked
# """, language="rust")
#
#     @slides.slide()
#     def mutex_with(slide: Box):
#         code(slide.box(), """
# """)

    ##### Parse, don't validate #####
    ##### Pyserde #####

    @slides.slide()
    def more_examples_in_blog(slide: Box):
        slide.box().text("More examples in my blog post")
        url = "https://kobzol.github.io/rust/python/2023/05/20/writing-python-like-its-rust.html"
        qr_code = generate_qr_code(url, scale=16)
        slide.box().image(qr_code, image_type="png")
        slide.box().text("~tt{kobzol.github.io}")

    @slides.slide()
    def soundness_summary(slide: Box):
        """
        Beware complexity
        """
        slide.box(p_bottom=sh(40)).text("Soundness", T(bold=True, size=sw(80)))

        lst = unordered_list(slide.box())
        lst.item(show="next+").text("Make it hard to make mistakes")
        lst.item(show="next+", p_bottom=sh(80)).text("Pit of success")

        slide.box(width=sw(150), show="next+", p_bottom=sh(20)).image("images/warning-icon.png")

        lst = unordered_list(slide.box())
        lst.item(show="last+").text("Not always possible")
        lst.item(show="next+").text("Not always worth it!")

        # Possible to use in a wrong way = bug in API, not in the caller!
        # Parse, don't validate
