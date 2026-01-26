from hypernet.models.base import APIModel, DateTimeField


class DailyRewardItem(APIModel):
    awardId: str
    available: bool
    done: bool


class DailyRewardAttendance(APIModel):
    id: str
    count: int
    name: str
    icon: str


class DailyRewardInfo(APIModel):
    currentTs: str
    calendar: list[DailyRewardItem]
    first: list[DailyRewardItem]
    resourceInfoMap: dict[str, DailyRewardAttendance]
    hasToday: bool


class DailyRewardRecord(APIModel):
    ts: DateTimeField
    awardId: str


class DailyRewardRecords(APIModel):
    records: list[DailyRewardRecord]
    resourceInfoMap: dict[str, DailyRewardAttendance]


class DailyRewardAward(APIModel):
    id: str
    type: int


class DailyReward(APIModel):
    ts: DateTimeField
    awardIds: list[DailyRewardAward]
    resourceInfoMap: dict[str, DailyRewardAttendance]
    tomorrowAwardIds: list[DailyRewardAward]
