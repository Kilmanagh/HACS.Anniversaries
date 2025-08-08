from dataclasses import dataclass, field
from datetime import date, datetime

from dateutil.relativedelta import relativedelta


def get_zodiac_sign(day, month):
    """Return the zodiac sign for a given date."""
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    if (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    if (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    if (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    if (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    if (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    if (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    if (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    if (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    if (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"


@dataclass
class AnniversaryData:
    """A class to hold anniversary data."""

    name: str
    date: date
    is_one_time: bool = False
    is_count_up: bool = False
    show_half_anniversary: bool = False
    unknown_year: bool = False
    config: dict = field(default_factory=dict)

    @property
    def zodiac_sign(self) -> str | None:
        """Return the zodiac sign of the anniversary."""
        return get_zodiac_sign(self.date.day, self.date.month)

    @property
    def named_anniversary(self) -> str | None:
        """Return the name of the anniversary if it's a known one."""
        named_anniversaries = {
            1: "Paper",
            5: "Wood",
            10: "Tin",
            15: "Crystal",
            20: "China",
            25: "Silver",
            30: "Pearl",
            40: "Ruby",
            50: "Golden",
            60: "Diamond",
        }
        return named_anniversaries.get(self.next_years)

    @property
    def is_milestone(self) -> bool:
        """Return true if the anniversary is a milestone."""
        milestone_years = [1, 5, 10, 18, 21, 25, 50, 75, 100]
        if self.next_years in milestone_years:
            return True
        if self.next_years is not None and self.next_years > 0 and self.next_years % 10 == 0:
            return True
        return False

    @property
    def days_remaining(self) -> int:
        """Calculate the number of days remaining until the next anniversary."""
        today = date.today()
        next_anniversary = self.next_anniversary_date
        if self.is_count_up:
            last_anniversary = self.last_anniversary_date
            return (today - last_anniversary).days
        return (next_anniversary - today).days

    @property
    def next_anniversary_date(self) -> date:
        """Calculate the date of the next anniversary."""
        today = date.today()
        anniversary_date = self.date
        if self.unknown_year:
            anniversary_date = anniversary_date.replace(year=today.year)

        if self.is_one_time and anniversary_date < today:
            return anniversary_date  # Past one-time event

        next_date = anniversary_date
        if today >= next_date:
            next_date = next_date.replace(year=today.year)
        if today > next_date:
            next_date = next_date.replace(year=today.year + 1)
        return next_date

    @property
    def last_anniversary_date(self) -> date:
        """Calculate the date of the last anniversary."""
        today = date.today()
        anniversary_date = self.date
        if self.unknown_year:
            anniversary_date = anniversary_date.replace(year=today.year)

        last_date = anniversary_date.replace(year=today.year)
        if today < last_date:
            last_date = last_date.replace(year=today.year - 1)
        return last_date

    @property
    def current_years(self) -> int | None:
        """Calculate the current number of years."""
        if self.unknown_year:
            return None
        return relativedelta(date.today(), self.date).years

    @property
    def next_years(self) -> int | None:
        """Calculate the number of years at the next anniversary."""
        if self.unknown_year:
            return None
        return relativedelta(self.next_anniversary_date, self.date).years

    @property
    def weeks_remaining(self) -> int:
        """Calculate the number of weeks remaining."""
        return self.days_remaining // 7

    @property
    def half_anniversary_date(self) -> date | None:
        """Calculate the half anniversary date."""
        if not self.show_half_anniversary:
            return None

        today = date.today()
        half_date = self.date + relativedelta(months=+6)

        next_half_date = half_date
        if today >= next_half_date:
            next_half_date = next_half_date.replace(year=today.year)
        if today > next_half_date:
            next_half_date = next_half_date.replace(year=today.year + 1)

        return next_half_date

    @property
    def days_until_half_anniversary(self) -> int | None:
        """Calculate the number of days until the half anniversary."""
        if not self.show_half_anniversary:
            return None

        half_date = self.half_anniversary_date
        if half_date:
            return (half_date - date.today()).days
        return None
