from dataclasses import dataclass

INF = float("inf")


@dataclass(frozen=True)
class CapitalGainsTaxRate:
    rate: float
    ceiling: float


# Updated for filing as single in 2024
CALIFORNIA_LONG_TERM_CAPITAL_GAINS_TAX = (
    CapitalGainsTaxRate(rate=0.01, ceiling=10_756.0),
    CapitalGainsTaxRate(rate=0.02, ceiling=25_499.0),
    CapitalGainsTaxRate(rate=0.04, ceiling=40_245.0),
    CapitalGainsTaxRate(rate=0.06, ceiling=55_866.0),
    CapitalGainsTaxRate(rate=0.08, ceiling=70_606.0),
    CapitalGainsTaxRate(rate=0.093, ceiling=360_659.0),
    CapitalGainsTaxRate(rate=0.103, ceiling=432_787.0),
    CapitalGainsTaxRate(rate=0.113, ceiling=721_314.0),
    CapitalGainsTaxRate(rate=0.123, ceiling=INF),
)

# Updated for filing as single in 2025
FEDERAL_LONG_TERM_CAPITAL_GAINS_TAX = (
    CapitalGainsTaxRate(rate=0.0, ceiling=48_350.0),
    CapitalGainsTaxRate(rate=0.15, ceiling=533_400.0),
    CapitalGainsTaxRate(rate=0.20, ceiling=INF),
)
