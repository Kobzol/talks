import inspect
from functools import wraps
from pathlib import Path


def into_path(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        sig = inspect.getfullargspec(f)
        args = [annotation(arg) for (arg, (name, annotation)) in zip(args, sig.annotations.items())]

        return f(*args, **kwargs)
    return wrapper


@into_path
def write_config(dir: Path | str):
    file = dir / "config.txt"
    with open(file, "w") as f:
        f.write("foo")


config = write_config("configs")
