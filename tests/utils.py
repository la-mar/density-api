import contextlib
import os
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, Union


def unpack_fixture(fixture: Any, *args, **kwargs) -> Any:
    """ Unpack a fixture for use in interactive debugging """

    if hasattr(fixture, "_pytestfixturefunction"):
        return next(fixture.__wrapped__(*args, **kwargs))  # type: ignore
    else:
        return fixture


def get_open_port():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def rand(length: int = None, min: int = None, max: int = None, choices=None):
    n = 8

    if length:
        n = length
    else:
        if not length and min and max:
            n = random.choice(range(min, max + 1))

    return "".join(random.choice(choices) for _ in range(n))


def rand_str(
    length: int = None, min: int = None, max: int = None, choices=string.ascii_letters
):
    return rand(length, min, max, choices)


def rand_int(
    length: int = None, min: int = None, max: int = None, choices=string.digits
):
    return int(rand(length, min, max, choices))


def rand_float(min: float = 0, max: float = 100, step: float = 0.01):
    return random.uniform(min, max)


def rand_lon(min: float = -98.7, max: float = -95, step: float = 0.0000000001):
    return rand_float(min, max, step)


def rand_lat(min: float = 31.9, max: float = 33.6, step: float = 0.0000000001):
    return rand_float(min, max, step)


def rand_email(min: int, max: int):
    return f"{rand_str(min=3, max=25)}@hoaxmail.com"


def rand_datetime(min_year=1900, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def rand_bool():
    return random.choice([True, False])


def generator_map():
    return {
        datetime: rand_datetime(),
        int: rand_int(min=1, max=9),
        str: rand_str(min=4, max=10),
        float: rand_float(),
        bool: rand_bool(),
        bytes: rand_str(min=300, max=10000).encode(),
        dict: {rand_str(length=4): rand_str(length=4) for x in range(0, 5)},
        list: [rand_str(length=4) for x in range(0, 5)],
    }


def to_bool(value: Optional[str]) -> bool:
    valid = {
        "true": True,
        "t": True,
        "1": True,
        "yes": True,
        "no": False,
        "false": False,
        "f": False,
        "0": False,
    }

    if value is None:
        return False

    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        raise ValueError("invalid literal for boolean. Not a string.")

    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('invalid literal for boolean: "%s"' % value)


@contextlib.contextmanager
def working_directory(p: Union[Path, str]):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(p)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
