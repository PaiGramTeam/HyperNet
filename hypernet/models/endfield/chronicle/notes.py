import datetime
from typing import Optional

from hypernet.models.base import APIModel, DateTimeField


class EndfieldNoteSkportBp(APIModel):
    """
    表示 Endfield Note 中的战斗通行证（Battle Pass）系统。

    Attributes:
        curLevel (int): 当前的通行证等级。
        maxLevel (int): 通行证的最大等级。
    """

    curLevel: int
    maxLevel: int


class EndfieldNoteSkportDailyMission(APIModel):
    """
    表示 Endfield Note 中的每日任务系统。

    Attributes:
        dailyActivation (int): 当前每日活跃度。
        maxDailyActivation (int): 每日活跃度的最大值。
    """

    dailyActivation: int
    maxDailyActivation: int


class EndfieldNoteSkportDungeon(APIModel):
    """
    表示 Endfield Note 中的体力系统。

    Attributes:
        curStamina (int): 当前可用的体力值。
        maxStamina (int): 体力值的最大容量。
        maxTs (DateTimeField): 体力完全恢复的时间戳。
    """

    curStamina: int
    maxStamina: int
    maxTs: DateTimeField


class EndfieldNoteSkport(APIModel):
    """Represents a Endfield Note Skport."""

    player_id: int

    bpSystem: EndfieldNoteSkportBp
    dailyMission: EndfieldNoteSkportDailyMission
    dungeon: EndfieldNoteSkportDungeon


class EndfieldNoteData(APIModel):
    """
    A model representing data for an Endfield Note.

    Attributes:
        current (int): The current value of the note data.
        total (int): The total value of the note data.
        maxTs (Optional[DateTimeField]): The maximum timestamp associated with the note data, if available.
    """

    current: int
    total: int
    maxTs: Optional[DateTimeField] = None


class EndfieldNote(APIModel):
    """Represents a Endfield Note."""

    player_id: int

    bp: EndfieldNoteData
    dailyMission: EndfieldNoteData
    dungeon: EndfieldNoteData
    signIn: bool

    @property
    def current_stamina(self) -> int:
        return self.dungeon.current

    @property
    def max_stamina(self) -> int:
        return self.dungeon.total

    @property
    def stamina_recover_time(self) -> datetime.datetime:
        """A property that returns the time when resin will be fully recovered."""
        return self.dungeon.maxTs

    @property
    def current_train_score(self) -> int:
        return self.dailyMission.current

    @property
    def max_train_score(self) -> int:
        return self.dailyMission.total

    @classmethod
    def from_skport(cls, skport: EndfieldNoteSkport) -> "EndfieldNote":
        return cls(
            player_id=skport.player_id,
            bp=EndfieldNoteData(
                current=skport.bpSystem.curLevel,
                total=skport.bpSystem.maxLevel,
            ),
            dailyMission=EndfieldNoteData(
                current=skport.dailyMission.dailyActivation,
                total=skport.dailyMission.maxDailyActivation,
            ),
            dungeon=EndfieldNoteData(
                current=skport.dungeon.curStamina,
                total=skport.dungeon.maxStamina,
                maxTs=skport.dungeon.maxTs,
            ),
            signIn=False,
        )
