from elsie import SlideDeck, TextStyle as s
from elsie.boxtree.box import Box

from utils import COLOR_FRONTEND, bash, code, list_item, new_slide, slide_header


def branch_prediction(slides: SlideDeck, backup: bool):
    if backup:
        slide = new_slide(slides)
        content = slide_header(slide, "Code (backup)")
        code(content.box(), """std::vector<float> data = /* 32K random floats in [1, 10] */;
float sum = 0;
// std::sort(data.begin(), data.end());
for (auto x : data)
{
    if (x < 6.0f)
    {
        sum += x;
    }
}""")
        slide = new_slide(slides)
        content = slide_header(slide, "Result (backup)")
        content.box(width="90%").image("images/example0a-time.png")

    slide = new_slide(slides)
    content = slide_header(slide, "Most upvoted Stack Overflow question")
    content.box(height=600).image("images/stack-overflow.png")

    slide = new_slide(slides)
    content = slide_header(slide, "What is going on? (Intel Amplifier - VTune)")
    content.box(height=600).image("images/vtune.png")

    slide = new_slide(slides)
    content = slide_header(slide, "What is going on? (perf)")
    bash(content.box(), """$ perf stat ./example0a --benchmark_filter=nosort
    853,672012  task-clock (msec) #   0,997 CPUs utilized
            30  context-switches  #   0,035 K/sec          
             0  cpu-migrations    #   0,000 K/sec
           199  page-faults       #   0,233 K/sec
 3 159 530 915  cycles            #   3,701 GHz
 1 475 799 619  instructions      #   0,47  insn per cycle
   419 608 357  branches          # 491,533 M/sec
   102 425 035  branch-misses     #  24,41% of all branches""",
         text_style=s(align="left", size=34))

    slide = new_slide(slides)
    content = slide_header(slide, "Branch predictor")
    content.box(height=600).image("images/haswell-diagram.png")
    content.box(width=130, height=40, x=595, y=140).rect(color=COLOR_FRONTEND, stroke_width=3)

    slide = new_slide(slides)
    content = slide_header(slide, "CPU pipeline 101")
    content.box(height=400).image("images/branch-miss-pipeline.svg")

    slide = new_slide(slides)
    content = slide_header(slide, "Branch predictor")
    list_wrapper = content.box()
    list_item(list_wrapper).text("CPU tries to predict results of branches")
    list_item(list_wrapper, show="next+").text("Misprediction can cost ~15-20 cycles!",
                                               escape_char="#")

    slide = new_slide(slides)
    content = slide_header(slide, "Simple branch predictor - unsorted array")
    code(content.box(p_bottom=40), """if (data[i] < 6) {
    ...
}""")

    row = content.box(horizontal=True)
    box_dimension = 100

    def array(numbers, predictions, start=1, needle=6):
        stroke_width = 2
        size = 36
        for i in range(len(numbers)):
            box = row.box(width=box_dimension, height=box_dimension).rect(color="black",
                                                                          stroke_width=stroke_width)
            number = str(numbers[i])
            box.text(number, s(bold=True, size=size))

            predicted_correctly = (predictions[i] and numbers[i] < needle) or (
                        not predictions[i] and numbers[i] >= needle)
            prediction = "green" if predicted_correctly else "red"
            show_overlay = "{}+".format(start + i * 2 + 1)
            overlay = box.overlay(show=show_overlay).rect(color="black", bg_color=prediction,
                                                          stroke_width=stroke_width)
            overlay.text(number, s(color="white", bold=True, size=size))
            show_text = start + i * 2
            row.box(x=i * box_dimension, y=box_dimension, width=box_dimension,
                    show="{}-{}".format(show_text, show_text + 1)).text(
                "{} < {}?".format(number, needle))

    values = [6, 2, 1, 7, 4, 8, 3, 9]
    text_style = s(align="left", size=42)
    width = 400

    def predict_sequence(wrapper: Box, values, start=1):
        for i in range(len(values)):
            value = "Taken" if values[i] else "Not taken"
            show_start = start + i * 2
            wrapper.overlay(show="{}-{}".format(show_start, show_start + 1)).rect(
                bg_color="white").text("Prediction: {}".format(value), style=text_style)

    def predict_value(index):
        if index == 0:
            return False
        return values[index - 1] < 6

    predictions = [predict_value(i) for i in range(len(values))]

    array(values, predictions, start=2)
    prediction_wrapper = content.box(p_top=60, width=width).text("Prediction: Not taken",
                                                                 style=text_style)
    predict_sequence(prediction_wrapper, predictions, start=1)

    content.box(show="next+", p_top=40).text("2 hits, 6 misses (25% hit rate)")

    slide = new_slide(slides)
    content = slide_header(slide, "Simple branch predictor - sorted array")
    code(content.box(p_bottom=40), """if (data[i] < 6) {
    ...
}""")

    row = content.box(horizontal=True)
    values = [1, 2, 3, 4, 6, 7, 8, 9]
    predictions = [predict_value(i) for i in range(len(values))]

    array(values, predictions, start=2)
    prediction_wrapper = content.box(p_top=60, width=width).text("Prediction: Not taken",
                                                                 style=text_style)
    predict_sequence(prediction_wrapper, predictions, start=1)

    content.box(show="next+", p_top=40).text("6 hits, 2 misses (75% hit rate)")

    if backup:
        size = 40
        slide = new_slide(slides)
        content = slide_header(slide, "How can the compiler help?")
        row = content.box(horizontal=True)
        row.box(y=0, p_right=50, width=400).image("images/bm-float-code.png")
        row.box(y=0, width=600).image("images/bm-float-bin.png")
        content.box(p_top=20).text("With ~tt{float}, there are two branches per iteration",
                                   style=s(size=size))

        slide = new_slide(slides)
        content = slide_header(slide, "How can the compiler help?")
        row = content.box(horizontal=True)
        row.box(y=0, p_right=50, width=400).image("images/bm-int-code.png")
        row.box(y=0, width=600).image("images/bm-int-bin.png")
        content.box(p_top=20).text("With ~tt{int}, one branch is removed (using ~tt{cmov})",
                                   style=s(size=size))

    slide = new_slide(slides)
    content = slide_header(slide, "How to measure?")
    content.box().text("~tt{branch-misses}", style=s(size=48))
    content.box(p_top=20).text("How many times was a branch mispredicted?")

    if backup:
        bash(content.box(p_top=40, show="next+"), """$ perf stat -e branch-misses ./example0a
with    sort ->     383 902
without sort -> 101 652 009""", text_style=s(align="left"))

    slide = new_slide(slides)
    slide.update_style("code", s(size=40))
    content = slide_header(slide, "How to help the branch predictor?")
    list_wrapper = content.box()
    list_item(list_wrapper).text("More predictable data")
    list_item(list_wrapper, show="next+").text("Profile-guided optimization")
    list_item(list_wrapper, show="next+").text("Remove (unpredictable) branches")
    list_item(list_wrapper, show="next+").text("Compiler hints (use with caution)")
    code(list_wrapper.box(show="last+", p_top=20, p_bottom=20), """if (__builtin_expect(will_it_blend(), 0)) {
    // this branch is not likely to be taken
}""")

    slide = new_slide(slides)
    content = slide_header(slide, "Branch target prediction")
    list_wrapper = content.box()
    list_item(list_wrapper).text("Target of a jump is not known at compile time:")
    list_item(list_wrapper, show="next+", level=1).text("Function pointer")
    list_item(list_wrapper, show="next+", level=1).text("Function return address")
    list_item(list_wrapper, show="next+", level=1).text("Virtual method")

    if backup:
        slide = new_slide(slides)
        slide.update_style("code", s(size=26))
        content = slide_header(slide, "Code (backup)")
        code(content, """struct A { virtual void handle(size_t* data) const = 0; };
struct B: public A { void handle(size_t* data) const final { *data += 1; } };
struct C: public A { void handle(size_t* data) const final { *data += 2; } };

std::vector<std::unique_ptr<A>> data = /* 4K random B/C instances */;
// std::sort(data.begin(), data.end(), /* sort by instance type */);
size_t sum = 0;
for (auto& x : data)
{
    x->handle(&sum);
}""")

        slide = new_slide(slides)
        content = slide_header(slide, "Result (backup)")
        content.box(width="90%").image("images/example0b-time.png")

        slide = new_slide(slides)
        content = slide_header(slide, "perf (backup)")
        bash(content.box(), """$ perf stat -e branch-misses ./example0b
with sort   ->     337 274
without sort -> 84 183 161""", text_style=s(align="left"))
