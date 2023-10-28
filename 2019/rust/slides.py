from elsie import Slides, TextStyle as s

from part1 import features
from part2 import performance
from part3 import memory_safety
from part4 import fearless_concurrency
from utils import slide_header

COLOR1 = "black"
COLOR2 = "#f74f00"

slides = Slides()

slides.update_style("default", s(font="Raleway-v4020", size=36, color=COLOR1))  # Default font
slides.update_style("emph", s(color=COLOR2))     # Emphasis
slides.set_style("code2", slides.get_style("code").compose(s(size=40, align="left")))


def intro(slides: Slides):
    slide = slides.new_slide()
    slide.set_style("title", s(size=60, bold=True))
    slide.set_style("name", s(size=30))

    slide.sbox(height="30%").image("imgs/logo.svg")
    slide.box(height=80)
    slide.box().text("Rust: Fast & Safe", "title")
    slide.box(height=20)
    slide.box().text("Jakub Beránek, Mathieu Fehr, Saurabh Raje", "name")

    slide = slides.new_slide()
    slide.box(width=500).image("imgs/meme-rust-meeting.jpg")

    slide = slides.new_slide()
    content = slide_header(slide, "What is Rust?")
    content.box().text("""
System programming language for building
reliable and efficient software.""")

    content.box(height=20)
    content.box(width="fill", height=150, show="2+").image("imgs/history.svg")
    content.box(height=20)
    content.box(width="fill", height=350, show="3+").image("imgs/users.svg")


def outro(slides: Slides):
    slide = slides.new_slide()
    slide.box().text("Thanks, our curse has finally been lifted", s(size=50))
    slide.box(height=20)
    slide.box(show="next+").text("Now YOU have to go and spread the word about Rust",
                                 s(size=40))


intro(slides)
features(slides)
performance(slides)
memory_safety(slides)
fearless_concurrency(slides)
outro(slides)

slides.render("slides.pdf")
