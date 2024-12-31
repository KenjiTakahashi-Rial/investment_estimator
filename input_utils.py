from typing import Callable, Optional, Union


def parse_float(input_str: str) -> float:
    if input_str.endswith("%"):
        input_str = input_str[:-1]
        return float(input_str) / 100

    as_float = float(input_str)
    return as_float if as_float < 1 else as_float / 100


def parse_int(input_str: str) -> int:
    digit_str = "".join([c for c in input_str if c.isdigit()])
    return int(digit_str)


def parse_bool(input_str: str) -> bool:
    lower_str = input_str.lower()

    if lower_str.startswith("y"):
        return True

    if lower_str.startswith("n"):
        return False

    raise ValueError("invalid yes/no string")


def _input(
    prompt: str,
    error_prompt: str,
    convert_fn: Union[Callable[[str], int], Callable[[str], float], Callable[[str], bool]],
    default: Optional[Union[int, float, bool]] = None,
    enforce_non_negative: bool = True,
) -> Union[int, float, bool]:
    def convert_input(input_str: str) -> Optional[Union[int, float, bool]]:
        if default is not None and input_str == "":
            return default
        try:
            return convert_fn(input_str)
        except ValueError:
            return None

    value = convert_input(input(prompt))
    while value is None or (enforce_non_negative and value < 0):
        value = convert_input(input(error_prompt))

    return value


def float_input(prompt: str, default: Optional[float] = None, enforce_non_negative: bool = True) -> float:
    error_prompt = "Please enter a non-negative number with a percent symbol or decimal number (e.g. 10.5% or 0.105): "
    val = float(_input(prompt, error_prompt, parse_float, default=default, enforce_non_negative=enforce_non_negative))
    assert isinstance(val, float)
    return val


def int_input(prompt: str, default: Optional[int] = None, enforce_non_negative: bool = True) -> int:
    error_prompt = "Please enter a non-negative integer: "
    return int(_input(prompt, error_prompt, parse_int, default=default, enforce_non_negative=enforce_non_negative))


def bool_input(prompt: str, default: Optional[bool] = None) -> bool:
    error_prompt = 'Please enter "yes" or "no": '
    return bool(_input(prompt, error_prompt, parse_bool, default=default))
