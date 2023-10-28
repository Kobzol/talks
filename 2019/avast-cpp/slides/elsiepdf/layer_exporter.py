import os
import subprocess
import tempfile

import lxml.etree as et
from elsie import sxml
from elsie.image import get_image_steps, create_image_data


def export_svg(filename, name=None, target_dir="."):
    if not name:
        name = os.path.splitext(os.path.basename(filename))[0]

    root = et.parse(filename).getroot()
    image_steps = get_image_steps(root)

    for step in range(1, image_steps + 1):
        xml = sxml.Xml()
        data = create_image_data(root, step)
        xml.raw_text(data)
        target_path = os.path.join(target_dir, "{}{}.svg").format(name, step)

        tmp_path = os.path.join(tempfile.gettempdir(), "elsie.svg")
        xml.write(tmp_path)

        target_path_pdf = os.path.join(target_dir, "{}{}.pdf").format(name, step)
        print(target_path_pdf)
        subprocess.run([
            "inkscape", "--file", tmp_path, "--export-area-drawing", "--without-gui", "--export-pdf", target_path_pdf
        ])


# intel = "/home/ber0134/projects/it4i/cpu_architecture_ptc_2019/day_2/04_Patterns_Intel"
intel = "../img"
export_svg(intel + "/false-sharing-array.svg", target_dir=intel)
