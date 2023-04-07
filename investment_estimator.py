import sys
from typing import Callable, Optional, Union

LARGE_NUM_ABBREVIATIONS = {
    10**3: "K",
    10**6: "M",
    10**9: "B",
    10**12: "T",
    10**15: "Qa",
    10**18: "Qi",
    10**21: "Sx",
    10**24: "Sp",
}

LARGEST_NUM = list(LARGE_NUM_ABBREVIATIONS.keys())[-1]
LARGEST_NUM_ABBREVIATION = list(LARGE_NUM_ABBREVIATIONS.values())[-1]


class InvestmentEstimator:
    _DEFAULT_ANNUAL_RETURN_RATE = 0.1
    _DEFAULT_CAP_GAINS_RATE = 0.15
    _DEFAULT_YEARS_TO_INVEST = 20
    _LEFT_DIGITS_TO_ROUND_TO = 3
    _YEAR_CHECKPOINT_STEP = 5

    def __init__(
        self,
        cap_gains_rate: Optional[float] = None,
        annual_return_rate: Optional[float] = None,
        monthly_contribution: Optional[int] = None,
        years_to_invest: Optional[int] = None,
        age: Optional[int] = None,
    ):
        self._cap_gains_rate = self._DEFAULT_CAP_GAINS_RATE
        self._annual_return_rate = self._DEFAULT_ANNUAL_RETURN_RATE
        self._monthly_contribution: int
        self._years_to_invest: int
        self._age: int

        self._year_checkpoints: tuple[int, ...]

        if cap_gains_rate is not None:
            self._cap_gains_rate = cap_gains_rate
        if annual_return_rate is not None:
            self._annual_return_rate = annual_return_rate
        if monthly_contribution is not None:
            self._monthly_contribution = monthly_contribution
        if years_to_invest is not None:
            self._years_to_invest = years_to_invest
        if age is not None:
            self._age = age

    @staticmethod
    def _get_input(
        prompt: str,
        error_prompt: str,
        convert_fn: Callable[[str], float],
        default: Optional[Union[int, float]] = None,
        enforce_positive: bool = True,
    ) -> Union[int, float]:
        def convert_input(input_str: str) -> Optional[Union[int, float]]:
            if default is not None and input_str == "":
                return default
            try:
                return convert_fn(input_str)
            except ValueError:
                return None

        value = convert_input(input(prompt))
        while value is None or (enforce_positive and value <= 0):
            value = convert_input(input(error_prompt))

        return value

    @staticmethod
    def _get_percent_input(prompt: str, default: Optional[float] = None, enforce_positive: bool = True) -> float:
        error_prompt = (
            "Please enter a positive number with a percent symbol or a positive decimal number (e.g. 10.5% or 0.105): "
        )

        def convert_fn(input_str: str) -> float:
            if input_str.endswith("%"):
                input_str = input_str[:-1]
                return float(input_str) / 100

            as_float = float(input_str)
            return as_float if as_float < 1 else as_float / 100

        return int(
            InvestmentEstimator._get_input(
                prompt, error_prompt, convert_fn, default=default, enforce_positive=enforce_positive
            )
        )

    @staticmethod
    def _get_int_input(prompt: str, default: Optional[int] = None, enforce_positive: bool = True) -> int:
        error_prompt = "Please enter a positive integer: "

        def convert_fn(input_str: str) -> int:
            return int(input_str)

        return int(
            InvestmentEstimator._get_input(
                prompt, error_prompt, convert_fn, default=default, enforce_positive=enforce_positive
            )
        )

    def _get_inputs(self) -> None:
        self._cap_gains_rate = self._get_percent_input(
            f"Long-term capital gains tax rate (default {self._DEFAULT_CAP_GAINS_RATE * 100:.0f}%): ",
            self._DEFAULT_CAP_GAINS_RATE,
        )
        self._annual_return_rate = self._get_percent_input(
            f"Average annual rate of return of your investment (default {self._DEFAULT_ANNUAL_RETURN_RATE * 100:.0f}%): ",
            self._DEFAULT_ANNUAL_RETURN_RATE,
        )
        self._monthly_contribution = self._get_int_input(f"Monthly contribution: ")
        self._years_to_invest = self._get_int_input(
            f"Years to invest (default {self._DEFAULT_YEARS_TO_INVEST}): ", self._DEFAULT_YEARS_TO_INVEST
        )
        age = self._get_int_input(f"Age (Enter to skip): ", sys.maxsize)
        self._age = 0 if age == sys.maxsize else age

    def _calculate_year_checkpoints(self) -> None:
        year_checkpoints = []

        for i in range(self._YEAR_CHECKPOINT_STEP, self._years_to_invest, self._YEAR_CHECKPOINT_STEP):
            year_checkpoints.append(i)
        year_checkpoints.append(self._years_to_invest)

        self._year_checkpoints = tuple(year_checkpoints)

    def _invest_monthly(self, months: int) -> float:
        total = 0.0

        for i in range(months):
            total += self._monthly_contribution
            total *= 1 + (self._annual_return_rate / 12)

        return total

    @staticmethod
    def _format_num(num: Union[int, float]) -> str:
        num = int(num)
        rounded = round(num, InvestmentEstimator._LEFT_DIGITS_TO_ROUND_TO - len(str(int(num))))
        prev_amount = 1
        prev_abbreviation = ""

        for amount, abbreviation in LARGE_NUM_ABBREVIATIONS.items():
            if rounded < amount:
                return f"~${rounded / prev_amount:g}{prev_abbreviation}"
            prev_amount = amount
            prev_abbreviation = abbreviation

        return f"~${rounded * 1_000 / LARGEST_NUM:g}{LARGEST_NUM_ABBREVIATION}"

    def run(self, get_inputs: bool = True) -> None:
        if get_inputs:
            self._get_inputs()

        self._calculate_year_checkpoints()

        for years in self._year_checkpoints:
            age_str = f" (age {self._age + years})" if self._age > 0 else ""
            months = years * 12
            total = self._invest_monthly(months)

            if total == float("inf"):
                print(
                    f"You earned so much money that you broke the program! We're not sure exactly how much you earned, but it's at least {self._format_num(sys.float_info.max)[1:]}. Wow!"
                )
                return

            principal = self._monthly_contribution * months
            profit = total - principal
            annual_return = total * self._annual_return_rate
            annual_return_after_tax = annual_return * (1 - self._cap_gains_rate)
            print(
                f"After {years} years{age_str} you would have {self._format_num(total)}.\n"
                f"\tYour total principal investment is {self._format_num(principal)}.\n"
                f"\tYour profit is {self._format_num(profit)}.\n"
                f"\tYour annual return is {self._format_num(annual_return)} ({self._format_num(annual_return_after_tax)} after tax)."
            )


def main() -> None:
    InvestmentEstimator().run()


if __name__ == "__main__":
    main()
