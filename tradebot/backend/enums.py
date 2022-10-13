from enum import Enum


class CandleFrequencyType(Enum):
    MINUTE = "minute"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class CandlePeriodType(Enum):
    DAY = "day"
    MONTH = "month"
    YEAR = "year"
    YTD = "ytd"