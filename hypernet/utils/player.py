"""This module contains functions for recognizing servers associated with different player IDs."""

from collections.abc import Mapping, Sequence
from typing import Optional

from hypernet.utils.enums import Game, Region

UID_LENGTH: Mapping[Game, int] = {
    Game.ENDFIELD: 10,
}
UID_RANGE: Mapping[Game, Mapping[Region, Sequence[int]]] = {
    Game.ENDFIELD: {
        Region.OVERSEAS: (4, 6),
        Region.CHINESE: (1, 2, 3),
    },
}


def recognize_game_uid_first_digit(player_id: int, game: Game) -> int:
    """
    Recognizes the first digit of a game UID for a given game.

    Args:
        player_id (int): The player ID to recognize the first digit for.
        game (Game): The game the player ID belongs to.

    Returns:
        int: The first digit of the player ID.

    Raises:
        ValueError: If the specified uid is not right.
    """
    length = UID_LENGTH[game] - 1
    first = int(player_id / (10**length))
    if not first:
        raise ValueError(f"player id {player_id} is not right")
    return first


def recognize_endfield_server(player_id: int) -> str:
    """Recognize which server an Endfield UID is from.

    Args:
        player_id (int): The player ID to recognize the server for.

    Returns:
        str: The name of the server associated with the given player ID.

    Raises:
        ValueError: If the player ID is not associated with any server.
    """
    server = {
        1: "1",
        4: "2",
        6: "3",
    }.get(recognize_game_uid_first_digit(player_id, Game.ENDFIELD))

    if server:
        return server

    raise ValueError(f"Player id {player_id} isn't associated with any server")


def recognize_region(player_id: int, game: Game) -> Optional[Region]:
    """
    Recognizes the region of a player ID for a given game.

    Args:
        player_id (int): The player ID to recognize the region for.
        game (Game): The game the player ID belongs to.

    Returns:
        Optional[Region]: The region the player ID belongs to if it can be recognized, None otherwise.
    """
    for region, digits in UID_RANGE[game].items():
        first = recognize_game_uid_first_digit(player_id, game)
        if first in digits:
            return region

    return None


def recognize_server(player_id: int, game: Game) -> str:
    """
    Recognizes the server of a player ID for a given game.

    Args:
        player_id (int): The player ID to recognize the server for.
        game (Game): The game the player ID belongs to.

    Returns:
        str: The server the player ID belongs to.

    Raises:
        ValueError: If the specified game is not supported.
    """
    if game == Game.ENDFIELD:
        return recognize_endfield_server(player_id)
    raise ValueError(f"{game} is not a valid game")
