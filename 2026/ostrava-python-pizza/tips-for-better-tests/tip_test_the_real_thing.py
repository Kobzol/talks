from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import StateCounter, aka, code, code_step, project, show, HideRest, ShowRest, skip, arrow_box, \
    text_box, dimmed_list_item, last


def test_the_real_thing(slides: Slides, tips: StateCounter):
    @slides.slide()
    def test_the_real_thing(slide: Box):
        """
        Maintain confidence in tests.
        """
        tips.tip(slide, "Test the ~emph{real thing}")
        aka(slide, "Don't (over)use mocks", width=None)

    @slides.slide()
    def kelvin_pr_diff(slide: Box):
        slide.box(width=800).image("images/pr-diff.png")

    @slides.slide()
    def useless_mock_tests(slide: Box):
        slide.box(width=1800).image("images/tests-with-mock.png")

    @slides.slide()
    def arthas(slide: Box):
        box = slide.box(width=1800).image("images/arthas.png")
        # slide.line([
        #     (box.x("35%"), box.y("30%")),
        #     (box.x("35%").add(180), box.y("30%")),
        # ], color="red", stroke_width=8)
        slide.line([
            (box.x("53%"), box.y("46%")),
            (box.x("53%").add(120), box.y("46%")),
        ], color="red", stroke_width=8)
        slide.box(x=box.x("45%"), y=box.y("50%")).text("TEST SUITE",
                                                       T(color="red", bold=True, size=50))
        # slide.box(x=box.x("34%"), y=box.y("12%")).text("ME", T(color="red", bold=True, size=50))

    width = 1800
    code_size = 70

    @slides.slide()
    def db_value(slide: Box):
        slide.update_style("code", T(size=code_size))
        code_step(slide.fbox(), """
class WebService:
    def __init__(self, db: Database):
        self.db = db

def test_web_service():
    service = WebService(???)
    …
""", [
            show(3) + [HideRest],
            [ShowRest]
        ], width=width)

    @slides.slide()
    def test_db(slide: Box):
        slide.update_style("code", T(size=code_size))
        code_step(slide.fbox(), """
class TestDatabase:
    def __init__(self):
        users = {}

def test_web_service():
    service = BorsService(TestDatabase())
    …
""", [
            show(3) + [HideRest],
            [ShowRest]
        ], width=width)

    @slides.slide()
    def postgres_production_error(slide: Box):
        row = slide.box(p_bottom=40, horizontal=True)
        for _ in range(3):
            row.box().image("images/tada.svg")
        slide.box(width=1700).image("images/postgres-int-datatype-error.png")

    @slides.slide()
    def real_test_in_db(slide: Box):
        slide.update_style("code", T(size=code_size))

        project(slide, "pytest-databases")
        code(slide, """
def test_web_service(db: PostgresService):
    service = WebService(db)
    …
""", width=width)

    @slides.slide()
    def isnt_that_slow(slide: Box):
        """
        Skip slow tests locally.
        It gives me confidence in the test suite.
        """
        slide.box(p_bottom=50).text("Isn't that slow?")
        slide.box(show="next+", p_bottom=30).text("pytest-xdist => run tests in parallel")
        code_step(slide.box(width="fill", height=500, show="next+"), """
services:
  db:
    image: postgres:16.9
    # Turn off durability
    command: -c fsync=off
    # Use RAMdisk for storage
    tmpfs:
      - /var/lib/postgresql/data
""", [
            show(3) + [HideRest],
            show(5) + [HideRest],
            [ShowRest],
        ], language="python", width=width)

    @slides.slide()
    def test_layers(slide: Box):
        row = slide.box(horizontal=True)
        service = row.box().rect(color="black", stroke_width=4).box(padding=20).text("Command handler")
        space = row.box(width=400)
        parser = row.box().rect(color="black", stroke_width=4).box(padding=20).text(
            "Command parser")

        arrow_box(space, "Depends on", size=50)

        def marker(parent: Box, center: Box, width: int, height: int, color: str, x_offset: int = 0):
            parent.box(
                x=center.x("50%").add(-width / 2 + x_offset), y=center.y("50%").add(-height / 2),
                width=width, height=height
            ).rect(color=color, stroke_width=10, stroke_dasharray="10")

        unit_test_1 = slide.box(show="next")
        marker(unit_test_1, parser, width=700, height=250, color="green")
        col = unit_test_1.box(x=parser.x("50%").add(-150), y=parser.y("100%"))
        col.box(height=200)
        col.box().text("Parser tests", T(color="green"))

        unit_test_2 = slide.box(show="next")
        marker(unit_test_2, service, width=700, height=250, color="red")
        col = unit_test_2.box(x=service.x("50%").add(-200), y=service.y("100%"))
        col.box(height=200)
        col.box().text("Handler tests", T(color="red"))

        unit_test_3 = slide.box(show="next+")
        marker(unit_test_3, space, width=1720, height=400, color="green", x_offset=-10)
        col = unit_test_3.box(x=service.x("50%").add(-200), y=service.y("100%"))
        col.box(height=200)
        col.box().text("Handler tests", T(color="green"))
