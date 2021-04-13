---
title: Building Commandline Applications
description: In this session we'll go through how to build and test commandline applications, these will provide another way for users to interact with program.
prev_know: None
skills:
  - Commandline Applications
date: 13/04/2021
mentors: 
  - TimSando
  - ghandic
links:
  - '[Coursera follow along course](https://www.coursera.org/learn/python-data?specialization=python#syllabus){target=_blank}'

---

{{ course_summary(title, date, description=description, prev_know=prev_know, skills=skills, mentors=mentors, links=links) }}

## What is a commandline application?

A command-line interface (CLI) is a simple text based interface to your program that will usually rely on using a shell prompt. If you have used basic commands on a terminal window before such as `ls` then you probably have interacted with a CLI before. In the case of `ls` it is a tool to list the files in a given directory, you can give additional options to the `ls` utility such as `ls -l` which will list the files/directories one item per line, you could also add the `-a` option to show all files/directories such as the hidden files like `.git` if you are in a git repository.

## How to make your program have a CLI

### Argparse - Standard Library

The first option we will look at is the built in library called `argparse` which parses arguments that you afix to your entrypoint script, for example `python list_files.py -l` would have the entrypoint script of `list_files.py` and the argument `-l` would be parsed, presumably in this case `-l`  would be a boolean flag dictating if you wanted to list with each item on its own line.

```python
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser(prog="python file lister")
parser.add_argument("-p", default=".", help="Directory to look into")
parser.add_argument("-l", action="store_true", default=False, help="Whether to print out each item on one line")
args = parser.parse_args()


def list_files(dir: str, pretty: bool = False) -> str:
    sep = "\n" if pretty else "\t"
    return sep.join([path.name for path in Path(dir).glob("*")])


print(list_files(args.p, args.l))
```

This could then be used as follows

Example 1 - Default current working directory and tab (\t) separated output

```bash
python list_files.py
```

Example 2 - Default current working directory and newline (\n) separated output

```bash
python list_files.py -l
```

Example 3 - Given directory (/usr) and newline (\n) separated output

```bash
python list_files.py -l -p /usr
```

### Typer

Now lets move onto some more advanced tooling that does a lot of the job for us, namely using [`Typer`](https://typer.tiangolo.com/), with  this library it is intended that you should write minimal argument parsing and instead concentrate on your own functionality, this reduces what is known as "boilerplate code". Lets try using Typer to upgrade our last example.

!!! note
    Remember to install this package using `pip install typer` from your terminal

```python
from pathlib import Path
from typing import Optional
import typer

app = typer.Typer()


@app.command()
def list_files(p: Optional[Path] = Path("."), l: Optional[bool] = False) -> str:
    sep = "\n" if l else "\t"
    print(sep.join([path.name for path in p.glob("*")]))


if __name__ == "__main__":
    app()
```

To use this it is a slight modification `-l` becomes `--l` and `-p` becomes `--p`, as follows:

```bash
python list_files.py --l --p /usr
```

Note we can very easily write a unit test for our function by simply importing the `app` variable that typer generates.

```python
from typer.testing import CliRunner

from .list_files import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--l", "--p", "/usr"])
    assert result.exit_code == 0
    assert "bin" in result.stdout
    assert "\n" in result.stdout
```

You can find out more about Typer  and how to integrate it in with your capsone by checking out there documentation [here](https://typer.tiangolo.com/)

### Pick

Finally we will look at taking your user interactions on the cli to a extra level by giving the user a kind of "menu bar" of options, this will be using the [pick](https://github.com/wong2/pick) package

!!! note
    Remember to install this package using `pip install pick` from your terminal

Following on from our last example, lets add an option the user can pick from, either to print pretty using new lines or compressed using tabs (replacing our `--l` option from using typer)

```python
from pathlib import Path
from typing import Optional

import typer
from pick import pick

app = typer.Typer()


@app.command()
def list_files(p: Optional[Path] = Path(".")) -> str:
    option, _ = pick(["Pretty", "Compressed"], "How would you like to view your files?")
    sep = "\n" if option == "Pretty" else "\t"
    print(sep.join([path.name for path in p.glob("*")]))


if __name__ == "__main__":
    app()

```

Notice this does make it harder to unit test the functionality so it would be better to split this into smaller  functions that have separated concerns (one for functionality and the other for user input), for further details on `pick`, check out the documentation [here](https://github.com/wong2/pick)
