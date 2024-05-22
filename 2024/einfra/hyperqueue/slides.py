import io
from typing import Tuple

import elsie
from elsie import TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell

from challenges import challenges
from config import sw, sh
from utils import image

COLOR1 = "#4d4d4d"

slides = elsie.Slides(
    width=1680,
    height=1050,
    backend=InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
)
slides.update_style("default", TextStyle(font="Raleway-v4020", size=36, color=COLOR1))

slides.set_style(
    "shell", elsie.TextStyle(color="white", font="DejaVu Sans Mono"), base="code"
)
slides.set_style("prompt", elsie.TextStyle(color="#aaaaff"))
slides.set_style("cmd", elsie.TextStyle(color="#dddd00"))
slides.set_style("args", elsie.TextStyle(color="orange", italic=True))

slides.set_style("hl", elsie.TextStyle(color="#77ff77", bold=True))
slides.set_style("green", elsie.TextStyle(color="#66FF00"))
slides.set_style("running", elsie.TextStyle(color="orange"))
slides.set_style("teal", elsie.TextStyle(color="aqua"))
slides.set_style("wait", elsie.TextStyle(color="orange"))
slides.set_style("nr", elsie.TextStyle(color="gray"))

CONSOLE_OUT = TextStyle(font="Ubuntu Mono", color="white", size=sw(30))
CONSOLE_OUT_SMALL = TextStyle(font="Ubuntu Mono", color="white", size=sw(20), align="left")


@slides.slide()
def intro(slide):
    slide.set_style("title", TextStyle(size=sw(60), bold=True))
    slide.set_style("name", TextStyle(size=sw(50)))
    slide.set_style("contact", TextStyle(size=sw(30), color="gray"))

    slide.box(height=sh(80))
    slide.box(width=sw(1000)).image("imgs/hq.svg")
    # slide.box().text("HyperQueue", TextStyle(size=40, bold=True))
    slide.box(height=sh(80))
    slide.box().text("Jakub Beránek, Ada Böhm", "name")
    slide.box(height=sh(40))
    slide.box().text("IT4Innovations", "name")
    slide.box(height=sh(80))
    slide.box().text("jakub.beranek@vsb.cz                   github.com/kobzol", "contact")


slides.set_style("syms", TextStyle(color="gray"))
slides.set_style("cmd", TextStyle(color="yellow"))
slides.set_style("prompt", TextStyle(color="aaaaff"))


class Console:
    def __init__(self, prompt="~prompt{$}", step=1):
        self.prompt = prompt
        self.printers = []
        self.step = step

    def command(self, command, show=True, overwrite=False, steps=1, upto=None):
        text = self.prompt + f" ~cmd{{{command}}}"
        self.output(text, show, overwrite, steps=steps, upto=upto)

    def output(
            self,
            text,
            show: bool = True,
            overwrite=False,
            style=CONSOLE_OUT,
            steps=1,
            upto=None,
    ):
        self.printers.append((overwrite, lambda box: box.text(text, style)))
        if show:
            if isinstance(upto, int):
                self.printers.append(f"{self.step}-{upto}")
            elif upto == "end":
                self.printers.append(f"{self.step}+")
            else:
                self.printers.append(f"{self.step}-{self.step + steps - 1}")
            self.step += steps

    def _get_real_printers(self, upto):
        filtered = [p for p in self.printers[:upto] if isinstance(p, tuple)]
        for j, printer in enumerate(filtered):
            if j + 1 < len(filtered) and filtered[j + 1][0]:
                continue
            yield printer[1]

    def render(self, parent_box_builder):
        for i, printer in enumerate(self.printers):
            if not isinstance(printer, (str, int)):
                continue
            parent = parent_box_builder(printer)
            for p in self._get_real_printers(i):
                p(parent.box(x=0, p_top=10))


image(slides, "imgs/nodes.svg", width="100%")
image(slides, "imgs/loginnodes.svg", width="100%")


@slides.slide()
def connect(slide):
    box = slide.fbox(height="90%")
    box.image("imgs/pbs.svg")

    console = Console()
    console.command("_")
    console.command("ssh karolina.it4i.cz", overwrite=True, steps=2)
    console.output(
        """
  _  __               _ _
 | |/ /              | (_)
 | ' / __ _ _ __ ___ | |_ _ __   __ _
 |  < / _` | '__/ _ \| | | '_ \ / _` |
 | . \ (_| | | | (_) | | | | | | (_| |
 |_|\_\__,_|_|  \___/|_|_|_| |_|\__,_|

 ...running on Red Hat Enterprise Linux 7.x
""",
        show=None,
        style=TextStyle(font="Consolas", color="white", size=sw(24), align="left"),
    )
    console.prompt = "login1.karolina$"
    console.command("_")
    console.command("./my-computation", overwrite=True, steps=2)
    console.command("~hl{sbatch} ./my-computation", overwrite=True, steps=5)
    console.render(lambda show: slide.box(x=sw(300), y=sh(520), show=show))

    slide.box(x=sw(630), y=sh(820), width=sw(100), height=sh(100), show=6).image(
        "imgs/prohibited.svg")


challenges(slides)


@slides.slide()
def hq(slide: Box):
    slide.box(width=sw(1200)).image("imgs/hq.svg")
    slide.box(p_top=sh(80)).text(
        "~tt{https://github.com/it4innovations/hyperqueue}", style=TextStyle(size=sw(40))
    )
    slide.box(p_top=sh(100), show="next+").text(
        "Distributed task runtime",
        style=TextStyle(size=sw(60))
    )
    slide.box(show="next+").text("Efficient and ergonomic task (graph) execution on HPC clusters",
                     style=TextStyle(size=sw(50)))


image(slides, "imgs/layers.svg")


@slides.slide()
def installation(slide: Box):
    slide.update_style("default", TextStyle(size=sw(60)))

    slide.box(width=sw(500), p_bottom=sh(10)).image("imgs/hq.svg")
    slide.box().text("Installation", TextStyle(size=sw(60), bold=True))
    lst = unordered_list(slide.box(p_top=sh(100)))
    lst.item(show="next+").text("Single binary")
    lst.item(show="next+").text("No dependencies")
    lst.item(show="next+").text("No admin privileges needed")
    lst.item(show="next+").text("No configuration")

    slide.box(x=sw(100), y=sh(100), show="next+").image("imgs/hq-releases.png")
    slide.box(width=sw(1000), x=sw(500), y=sh(500), show="next+").image("imgs/hq-archive.png")


@slides.slide()
def laptop1(slide):
    box = slide.fbox(width="80%")
    box.image("imgs/serverstart.svg")

    console_x = 260
    console_y = 550

    console = Console()
    console.prompt = "login1.karolina$"
    console.command("_")
    console.command("hq server start", steps=2, overwrite=True)
    console.output(
        """~green{INFO} No online server found, starting a new server
~green{INFO} Saving access file as '/home/boh126/.hq-server/046/access.json'
+------------------+-------------------------+
| Server directory | /home/boh126/.hq-server |
| Server UID       | xaTcNZ                  |
| Host             | login1.karolina         |
| Pid              | 51752                   |
| HQ port          | 44367                   |
| Workers port     | 44783                   |
| Start date       | 2024-04-30 12:05:00 UTC |
| Version          | 0.18.0                  |
+------------------+-------------------------+
""",
        style=CONSOLE_OUT_SMALL,
    )
    console.render(lambda show: slide.box(x=sw(console_x), y=sh(console_y), show=show))

    console = Console(step=5)
    console.prompt = "login1.karolina$"
    console.command("_")
    console.command("hq submit ./my-computation", overwrite=True)
    console.output(
        "Job submitted ~green{successfully}, job ID: 1",
        steps=2,
        style=CONSOLE_OUT_SMALL,
    )
    console.command("hq job list", show=None)
    console.output(
        """+----+----------------+---------+-------+
| ID | Name           | State   | Tasks |
+----+----------------+---------+-------+
| 1  | my-computation | ~teal{WAITING} | 1     |
+----+----------------+---------+-------+
""",
        show="9+",
        style=CONSOLE_OUT_SMALL,
        steps=3,
    )
    console.command("hq alloc add ~hl{<SYSTEM_SCHEDULER>}")
    console.command("hq alloc add slurm", overwrite=True)
    console.command("hq alloc add slurm --timelimit=1h", overwrite=True)
    console.command("hq alloc add slurm --timelimit=1h -- -pstandard", overwrite=True)
    console.render(lambda show: slide.box(x=sw(console_x), y=sh(console_y), show=show))

    console = Console(step=10)
    console.prompt = "machine$"
    console.command("_")
    console.command("hq worker start", overwrite=True)
    console.render(lambda show: slide.box(x=sw(260), y=sh(5), show=show))

    console = Console(step=5)
    console.prompt = "login1.karolina$"
    console.command("_")
    console.command("hq submit ./my-computation", overwrite=True)
    console.output(
        "Job submitted ~green{successfully}, job ID: 1",
        steps=2,
        style=CONSOLE_OUT_SMALL,
    )

    console.command("hq job list", show=None)
    console.output(
        """+----+----------------+---------+-------+
| ID | Name           | State   | Tasks |
+----+----------------+---------+-------+
| 1  | my-computation | ~teal{WAITING} | 1     |
+----+----------------+---------+-------+
""",
        show="9+",
        style=CONSOLE_OUT_SMALL,
        steps=3,
    )
    console.command("hq alloc add ~hl{<SYSTEM_SCHEDULER>}")
    console.command("hq alloc add slurm", overwrite=True)
    console.command("hq alloc add slurm --timelimit=1h", overwrite=True)
    console.command(
        "hq alloc add slurm --timelimit=1h -- -pstandard", overwrite=True, upto=20
    )
    console.render(lambda show: slide.box(x=sw(console_x), y=sh(console_y), show=show))

    console = Console(step=21)
    console.prompt = "login1.karolina$"
    console.command("hq worker list", overwrite=True)
    console.output(
        """
+----+---------+-----------------+-----------+---------+----------------+
| Id | State   | Hostname        | Resources | Manager | Manager Job Id |
+----+---------+-----------------+-----------+---------+----------------+
| 1  | ~green{RUNNING} | cn.lumi         | 2x64 cpus | SLURM   | 550463         |
+----+---------+-----------------+-----------+---------+----------------+
""".strip(),
        style=CONSOLE_OUT_SMALL,
        upto=24,
    )
    console.render(lambda show: slide.box(x=sw(console_x), y=sh(console_y), show=show))

    console = Console(step=25)
    console.command("hq job list", show=None)
    console.output(
        """+----+----------------+---------+-------+
| ID | Name           | State   | Tasks |
+----+----------------+---------+-------+
| 1  | my-computation | ~running{RUNNING} | 1     |
+----+----------------+---------+-------+
""",
        show="9+",
        style=CONSOLE_OUT_SMALL,
        steps=1,
    )
    console.output(
        """+----+----------------+---------+-------+
| ID | Name           | State   | Tasks |
+----+----------------+---------+-------+
| 1  | my-computation | ~running{RUNNING} | 1     |
+----+----------------+---------+-------+
| 2  | my-workflow    | ~teal{WAITING} | 3     |
+----+----------------+---------+-------+
""",
        show="9+",
        style=CONSOLE_OUT_SMALL,
        steps=1,
        overwrite=True
    )
    console.output(
        """+----+----------------+----------+-------+
| ID | Name           | State    | Tasks |
+----+----------------+----------+-------+
| 1  | my-computation | ~green{FINISHED} | 1     |
+----+----------------+----------+-------+
| 2  | my-workflow    | ~teal{WAITING}  | 3     |
+----+----------------+----------+-------+
    """,
        show="9+",
        style=CONSOLE_OUT_SMALL,
        overwrite=True,
        steps=2
    )
    console.output(
        """+----+----------------+----------+-------+
| ID | Name           | State    | Tasks |
+----+----------------+----------+-------+
| 1  | my-computation | ~green{FINISHED} | 1     |
+----+----------------+----------+-------+
| 2  | my-workflow    | ~running{RUNNING}  | 3     |
+----+----------------+----------+-------+
    """,
        show="9+",
        style=CONSOLE_OUT_SMALL,
        overwrite=True,
        steps=5
    )
    console.render(lambda show: slide.box(x=sw(console_x), y=sh(console_y), show=show))


@slides.slide()
def hq_approach(slide: Box):
    slide.update_style("default", TextStyle(size=sw(60)))
    slide.box(p_bottom=sh(40)).text("HyperQueue approach:", style=TextStyle(bold=True))
    slide.box(show="next+").text("What to compute (tasks) +")
    slide.box(show="next+").text("Where to compute it (nodes)")
    slide.box(show="next+").text("=> disentangled")

    slide.box(show="next+", p_top=sh(40)).text("Load balancing across all available resources", TextStyle(bold=True))


image(slides, "imgs/fix.svg")


def header(slide: Box, text: str):
    slide.box(y=sh(20)).text(text, TextStyle(size=sw(60), bold=True))


@slides.slide()
def array(slide: Box):
    header(slide, "Task arrays")
    box = slide.fbox(height="80%")
    box.image("imgs/array.svg")

    console = Console()
    console.prompt = "$"
    console.command("hq submit ./my-computation", steps=2)
    console.command(
        "hq submit ~hl{--array=1-10_000} ./my-computation", show=False, overwrite=True
    )
    console.output(
        "Job submitted ~green{successfully}, job ID: 1",
        steps=3,
        style=CONSOLE_OUT_SMALL,
    )
    console.command("hq progress 1", show=False)
    console.output(
        "[~green{##}~running{#}..................................] 0/1 jobs, 232/10000 tasks (~running{4 RUNNING}, ~green{232 FINISHED})",
        style=CONSOLE_OUT_SMALL,
        steps=2,
    )
    console.command(
        "hq submit ~hl{--each-line=~teal{myfile.txt}} ./my-computation", steps=4, upto="end"
    )
    console.command(
        "hq submit ~hl{--from-json=~teal{items.json}} ./my-computation", upto="end"
    )
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))


@slides.slide()
def cpus(slide):
    header(slide, "CPU resource requirements")

    box = slide.fbox(height="80%")
    box.image("imgs/cpus.svg")

    console = Console(step=2)
    console.prompt = "$"
    console.command("hq submit ./my-computation", steps=1)
    console.command(
        "hq submit ~hl{--cpus=~teal{<NUMBER_OF_CPUS>}} ./my-computation", overwrite=True
    )
    console.command(
        "hq submit ~hl{--cpus=~teal{4}} ./my-computation", overwrite=True, steps=3
    )
    console.command(
        "hq submit --array=1-4 ~hl{--cpus=~teal{2}} ./my-computation", upto="end"
    )
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))


@slides.slide()
def resources(slide):
    header(slide, "General resource requirements")
    box = slide.fbox(height="80%")
    box.image("imgs/resources.svg")

    console = Console(step=2)
    console.prompt = "$"
    console.command(
        "hq submit ~hl{--resource ~teal{NAME}=~teal{AMOUNT}} ./my-computation"
    )
    console.command(
        "hq submit ~hl{--resource foo=2} ./my-computation", upto="end", overwrite=True, steps=3
    )
    console.command(
        "hq submit ~hl{--resource gpus/nvidia=4} ./my-computation", steps=2
    )
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))


@slides.slide()
def detection(slide: Box):
    slide.update_style("default", TextStyle(size=sw(60)))
    slide.box().text("Automatic detection of worker resources", TextStyle(bold=True))
    lst = unordered_list(slide.box())
    lst.item(show="next+").text("CPUs (including NUMA sockets)")
    lst.item(show="next+").text("Memory")
    lst.item(show="next+").text("Nvidia/AMD GPUs")


@slides.slide()
def numa(slide):
    header(slide, "NUMA handling")
    box = slide.fbox(height="80%")
    box.image("imgs/numa.svg")

    console = Console(step=3)
    console.prompt = "$"
    console.command("hq submit ~hl{--cpus=~teal{4}} ./my-computation", steps=4)
    console.command('hq submit ~hl{--cpus=~teal{"4 compact"}} ./my-computation')
    console.command('hq submit ~hl{--cpus=~teal{"4 compact!"}} ./my-computation')
    console.command('hq submit ~hl{--cpus=~teal{"8 scatter"}} ./my-computation', steps=2)
    console.command("hq submit ~hl{--pin} --cpus=... ./my-computation", upto="end")
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))


@slides.slide()
def resources_advanced(slide):
    """
    Alternative resources.
    """
    header(slide, "Complex resource requirements")
    box = slide.fbox(height="80%")
    box.image("imgs/console.svg")

    console = Console()
    console.prompt = "$"
    # console.command('hq submit --cpus=\"~hl{4 compact}\" ./my-computation')
    # console.command('hq submit --cpus=\"~hl{8 scatter}\" ./my-computation')
    # console.command("hq submit ~hl{--pin} --cpus=... ./my-computation", upto="end")
    console.command('hq submit ~hl{--time-limit=1h} ./my-computation')
    console.command('hq submit ~hl{--time-request=10m} ./my-computation')
    console.command("hq submit --resource=gpus/nvidia=~hl{0.5} ./my-computation")
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))


@slides.slide()
def multinode_tasks(slide):
    header(slide, "Multinode tasks")
    box = slide.fbox(height="80%")
    box.image("imgs/multinodetasks.svg")

    console = Console(step=2)
    console.prompt = "$"
    console.command("hq submit ~hl{--nodes=16} ...")
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))


@slides.slide()
def streaming(slide):
    header(slide, "I/O streaming")
    box = slide.fbox(height="80%")
    box.image("imgs/streaming.svg")

    console = Console(step=1)
    console.prompt = "$"
    console.command("hq submit --array 1-4 ./my-computation")
    console.command("ls job-1")
    console.output(
        "1.stderr   2.stderr   3.stderr    4.stderr\n1.stdout   2.stdout   3.stdout    4.stdout",
        style=CONSOLE_OUT_SMALL,
    )
    console.command("hq submit --array 1-1000_000 ./my-computation")
    console.command("ls job-2", steps=2)
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))

    slide.box(x=160, y="[86%]", width=60, height=60, show="6").image("imgs/sad.svg")

    console = Console(step=7)
    console.prompt = "$"
    console.command(
        "hq submit --array 1-4 ~hl{--log=~teal{my.log}} ./my-computation", steps=5
    )
    console.command("hq ~hl{log ~teal{my.log} show}", overwrite=True)

    slide.set_style("red", TextStyle(color="red"))
    slide.set_style("blue", TextStyle(color="green"))
    slide.set_style("orange", TextStyle(color="orange"))

    console.output(
        """~red{2:0>} Computation started ...
~blue{1:0>} Computation started ...
~teal{3:0>} Computation started ...
~orange{4:0>} Computation started ...
~teal{3:0>} Result is 3.2
~teal{3: > stream closed}
~red{2:0>} Result is 5.2
~red{2: > stream closed}
~blue{1:0>} Result is 1.2
~blue{1: > stream closed}
~orange{4:0>} Result is 4.0
~orange{4: > stream closed}
""".rstrip(),
        style=CONSOLE_OUT_SMALL,
    )
    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))

    console = Console(step=14)
    console.prompt = "$"
    console.command("hq log ~hl{~teal{my.log} cat stdout --task=1}", show=False)
    console.output(
        """Computation started ...\nResult is 1.2""", style=CONSOLE_OUT_SMALL
    )

    console.render(lambda show: slide.box(x=sw(360), y=sh(530), show=show))


@slides.slide()
def python_api(slide: Box):
    slide.update_style("code", TextStyle(size=sw(40)))

    header(slide, "Python API")

    b = slide.box()
    code = b.code(
        "python",
        """import hyperqueue as hq

client = hq.Client()

job = hq.Job()
job.program(args=["./my-computation"])

job_id = client.submit(job)
client.wait_for_jobs([job_id])
""",
    )
    code.line_box(0, show="2", z_level=-1, p_x=-5, p_y=-2).rect(bg_color="#80F080")
    code.line_box(2, show="3", z_level=-1, p_x=-5, p_y=-2).rect(bg_color="#80F080")
    code.line_box(4, show="4", z_level=-1, p_x=-5, p_y=-2).rect(bg_color="#80F080")
    code.line_box(5, show="4", z_level=-1, p_x=-5, p_y=-2).rect(bg_color="#80F080")
    code.line_box(7, show="5", z_level=-1, p_x=-5, p_y=-2).rect(bg_color="#80F080")
    code.line_box(8, show="5", z_level=-1, p_x=-5, p_y=-2).rect(bg_color="#80F080")


@slides.slide()
def python_api2(slide):
    slide.update_style("code", TextStyle(size=sw(34)))
    header(slide, "Python function tasks")

    b = slide.box()
    code = b.code(
        "python",
        """import hyperqueue as hq

def my_computation():
    import tensorflow as tf
    ...

client = hq.Client()

job = hq.Job()
resources = ResourceRequest(resources={"cpus": 32, "gpus/amd": 1})
job.function(my_computation, resources=resources)

job_id = client.submit(job)
client.wait_for_jobs([job_id])
""",
    )
    code.line_box(2, show="1", n_lines=3, z_level=-1, p_x=-5, p_y=-2).rect(
        bg_color="#80F080"
    )

    code.line_box(9, show="2", n_lines=2, z_level=-1, p_x=-5, p_y=-2).rect(
        bg_color="#80F080"
    )


@slides.slide()
def python_api3(slide: Box):
    slide.update_style("code", TextStyle(size=sw(34)))
    header(slide, "Task dependencies")

    cols = slide.box(horizontal=True)
    left = cols.box(p_right=sw(80))
    left.box(width=sw(500)).image("imgs/taskgraph.svg")

    right = cols.box()
    b = right.box(show="2", p_top=40)
    code = b.code(
        "python",
        """import hyperqueue as hq

client = hq.Client()

job = hq.Job()
p1 = job.program("preprocessing1")
p2 = job.program("preprocessing2")
main = job.function(my_function, deps=[p1, p2])
job.program("postprocessing", deps=[main])

job_id = client.submit(job)
client.wait_for_jobs([job_id])
""",
    )
    code.line_box(5, n_lines=4, show="2", z_level=-1, p_x=-5, p_y=-2).rect(
        bg_color="#80F080"
    )


@slides.slide()
def dashboard(slide: Box):
    header(slide, "Dashboard")
    slide.box(width=sw(1400), p_top=sh(40)).image("imgs/dashboard.png")


@slides.slide()
def local_usage(slide: Box):
    header(slide, "Local prototyping")
    slide.box(width=sw(600), p_top=sh(40)).image("imgs/local-usage.svg")


image(slides, "imgs/users.svg")
image(slides, "imgs/features.svg")


def generate_qr_code(content: str, scale=14) -> io.BytesIO:
    import segno
    qrcode = segno.make(content)
    buffer = io.BytesIO()
    qrcode.save(buffer, scale=scale, kind="png")
    buffer.seek(0)
    return buffer


def two_column_layout(parent: Box) -> Tuple[Box, Box]:
    row = parent.box(width="fill", horizontal=True)
    left = row.box(width=sw(1100), p_right=sh(40))
    line = row.box(width=sw(10), height=sh(800))
    line.fbox().rect(bg_color="black")
    right = row.box(p_left=sh(40))
    return (left, right)


@slides.slide()
def outro(slide: Box):
    link = "https://github.com/it4innovations/hyperqueue"

    left, right = two_column_layout(slide)
    left.box(width=sw(800)).image("imgs/hq.svg")
    left.box(p_top=sh(50)).text(
        f"~tt{{{link}}}", style=TextStyle(size=sw(36))
    )
    left.box(p_top=sh(80)).text("Thank you for your attention", style=TextStyle(size=sw(60)))

    qr_code = generate_qr_code(link)

    right.box().image(qr_code, image_type="png")
    right.box(width=sw(500), p_top=sh(40)).image("imgs/icons.svg")


image(slides, "imgs/bothsides.svg")

slides.render("slides.pdf")
