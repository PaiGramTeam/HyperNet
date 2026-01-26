import enum as _enum

__all__ = ("AppCode", "Region", "Game")


class AppCode(str, _enum.Enum):
    SKLAND = "4ca99fa6b56cc2ba"
    SKPORT = "6eb76d4e13aa36e6"


class Region(str, _enum.Enum):
    """
    Represents a region where a game is being played.

    Attributes:
        OVERSEAS (Region): Represents an overseas region where a game is being played.
        CHINESE (Region): Represents a Chinese region where a game is being played.
    """

    OVERSEAS = "os"
    CHINESE = "cn"


class Game(str, _enum.Enum):
    """
    Represents a game that can be played in different regions.

    Attributes:
        ARKNIGHTS (Game): Represents the game "Arknights".
        ENDFIELD (Game): Represents the game "Endfield".
    """

    ARKNIGHTS = "arknights"
    ENDFIELD = "endfield"

    @property
    def game_id(self) -> int:
        """
        Returns the game ID associated with the game.

        Returns:
            int: The game ID.
        """
        game_ids = {
            Game.ARKNIGHTS: 1,
            Game.ENDFIELD: 3,
        }
        return game_ids[self]
