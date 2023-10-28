from elsie import SlideDeck, TextStyle as s
from elsie.boxtree.box import Box

from utils import new_slide, slide_header, list_item, bash, code, COLOR_BACKEND, COLOR_FRONTEND


def denormals(slides: SlideDeck, backup: bool):
    if backup:
        slide = new_slide(slides)
        content = slide_header(slide, "Code (backup)")
        code(content.box(), """float F = static_cast<float>(std::stof(argv[1]));
std::vector<float> data(4 * 1024 * 1024, 1);

for (int r = 0; r < 100; r++)
{
    for (auto& item: data)
    {
        item *= F;
    }
}""")
        slide = new_slide(slides)
        content = slide_header(slide, "Result (backup)")
        content.box(width="50%").image("images/example2-time.png")

    slide = new_slide(slides)
    colors = ["#B22222", "#007944", "#0018AE"]
    styles = ["sign", "exponent", "significand"]
    for i, style in enumerate(styles):
        slide.set_style(style, s(color=colors[i], size=42))
    content = slide_header(slide, "Denormal floating point numbers")

    row = content.box(horizontal=True)
    box_dimension = 60

    def floating_point(wrapper: Box, colors, values):
        for i in range(len(colors)):
            box = wrapper.box(width=box_dimension, height=box_dimension)
            box.rect(color="black", bg_color=colors[i], stroke_width=2)
            box.text(str(values[i]), s(color="white", bold=True))

    floating_point(row, [colors[0]] + [colors[1]] * 5 + [colors[2]] * 10, [
        0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1
    ])
    row_label = content.box(x=0, horizontal=True, show="next+")
    row_label.box(x=250, y=0).text("Zero exponent")
    row_label.box(x=670, y=0).text("Non-zero significand")

    content.box(p_top=80, width=700, height=50).image("images/float.svg")

    list_wrapper = content.box(p_top=20)
    list_item(list_wrapper, show="next+").text("Numbers close to zero")
    list_item(list_wrapper, show="last+").text("Hidden bit = 0, smaller bias")

    content.box(p_top=40, show="next+").text("Operations on denormal numbers are slow!", style=s(size=46))

    slide = new_slide(slides)
    content = slide_header(slide, "Floating point handling")
    content.box(height=600).image("images/haswell-diagram.png")
    content.box(width=130, height=32, x=800, y=52).rect(color=COLOR_FRONTEND, stroke_width=3)
    content.box(width=35, height=100, x=988, y=80).rect(color=COLOR_FRONTEND, stroke_width=3)
    content.box(width=80, height=165, x=212, y=335).rect(color=COLOR_BACKEND, stroke_width=3)

    slide = new_slide(slides)
    content = slide_header(slide, "How to measure?")
    content.box().text("~tt{fp_assist.any}", style=s(size=48))
    content.box(p_top=20).text("How many times the CPU switched to the microcode FP handler?")

    if backup:
        bash(content.box(p_top=40, show="next+"), """$ perf stat -e fp_assist.any ./example2
0   ->          0
0.3 -> 15 728 640""", text_style=s(align="left"))

    slide = new_slide(slides)
    slide.update_style("code", s(size=40))
    content = slide_header(slide, "How to fix it?")
    list_wrapper = content.box()
    list_item(list_wrapper).text("The nuclear option: ~tt{-ffast-math}")
    list_item(list_wrapper, level=1).text("Sacrifice correctness to gain more FP performance")
    list_item(list_wrapper, show="next+").text("Set CPU flags:")
    list_item(list_wrapper, level=1, show="last+").text("Flush-to-zero - treat denormal outputs as 0")
    list_item(list_wrapper, level=1, show="last+").text("Denormals-to-zero - treat denormal inputs as 0")

    code(list_wrapper.box(p_top=40, show="next+"), """_mm_setcsr(_mm_getcsr() | 0x8040);
// or
_MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON);
_MM_SET_DENORMALS_ZERO_MODE(_MM_DENORMALS_ZERO_ON);
""")
