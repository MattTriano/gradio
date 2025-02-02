import re
from os.path import exists, getmtime, join

from jinja2 import BaseLoader, Environment, TemplateNotFound

README_TEMPLATE = "readme_template.md"
GETTING_STARTED_TEMPLATE = "guides/1)getting_started/1)quickstart.md"

with open(GETTING_STARTED_TEMPLATE, encoding="utf-8") as getting_started_file:
    getting_started = getting_started_file.read()

code_tags = re.findall(r'\$code_([^\s]+)', getting_started)
demo_tags = re.findall(r'\$demo_([^\s]+)', getting_started)
code, demos = {}, {}

for code_src in code_tags:
    with open(join("demo", code_src, "run.py")) as code_file:
        python_code = code_file.read()
        python_code = python_code.replace(
            'if __name__ == "__main__":\n    demo.launch()', "demo.launch()"
        )
        code[code_src] = "```python\n" + python_code + "\n```"

for demo_src in demo_tags:
    demos[demo_src] = (
        "![" + demo_src + " interface](demo/" + demo_src + "/screenshot.gif)"
    )

with open(README_TEMPLATE) as readme_template_md:
    readme = readme_template_md.read()
readme = readme.replace("$getting_started", getting_started)
readme = re.sub(
        r"\$code_([a-z _\-0-9]+)", 
        lambda x: code[x.group(1)], 
        readme
    )
readme = re.sub(
        r"\$demo_([a-z _\-0-9]+)", 
        lambda x: demos[x.group(1)], 
        readme
    )

readme = readme.replace("(/assets/", "(guides/assets/")

with open("README.md", "w", encoding="utf-8") as readme_md:
    readme = """<!-- DO NOT EDIT THIS FILE DIRECTLY. INSTEAD PLEASE EDIT: "readme_template.md" or 
    "guides/getting_started.md", AND THEN RUN: "python render_readme.py" --> """ + "\n" + readme
    readme_md.write(readme)
