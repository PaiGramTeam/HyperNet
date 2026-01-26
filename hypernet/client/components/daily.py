"""Daily reward component."""

from typing import Optional

from hypernet.client.base import BaseClient
from hypernet.models.lab.daily import DailyReward, DailyRewardInfo, DailyRewardRecords
from hypernet.utils.enums import Game

__all__ = ("DailyRewardClient",)

from hypernet.utils.player import recognize_server


class DailyRewardClient(BaseClient):
    """A client for interacting with the daily reward system."""

    async def get_reward_info(
        self,
        cred: Optional[str] = None,
        player_id: Optional[int] = None,
        game: Optional[Game] = None,
    ) -> DailyRewardInfo:
        """Gets the daily reward info for the current user.

        Args:
            cred (str): The user's cred token. Defaults to self.cookies.cred if not provided.
            player_id (int): The player's ID. Defaults to None.
            game (Game): The game to request data for. Defaults to None.

        Returns:
            A DailyRewardInfo object containing information about the user's daily reward status.
        """
        game = game or self.game
        game_id = game.game_id
        player_id = player_id or self.player_id
        server_id = recognize_server(player_id, game)
        if game is Game.ENDFIELD:
            path = "game/endfield/attendance"
            headers = {"sk-game-role": f"{game_id}_{player_id}_{server_id}"}
        else:
            raise ValueError("Daily rewards are only supported for Endfield at this time.")
        data = await self.request_base_api(path, headers=headers, cred=cred)
        return DailyRewardInfo(**data)

    async def claimed_rewards(
        self,
        cred: Optional[str] = None,
        player_id: Optional[int] = None,
        game: Optional[Game] = None,
    ) -> DailyRewardRecords:
        """Gets all claimed rewards for the current user.

        Args:
            cred (str): The user's cred token. Defaults to self.cookies.cred if not provided.
            player_id (int): The player's ID. Defaults to None.
            game (Game): The game to request data for. Defaults to None.

        Returns:
            A list of ClaimedDailyReward objects representing the claimed rewards for the current user.
        """
        game = game or self.game
        game_id = game.game_id
        player_id = player_id or self.player_id
        server_id = recognize_server(player_id, game)
        if game is Game.ENDFIELD:
            path = "game/endfield/attendance/record"
            headers = {"sk-game-role": f"{game_id}_{player_id}_{server_id}"}
        else:
            raise ValueError("Daily rewards are only supported for Endfield at this time.")
        data = await self.request_base_api(path, headers=headers, cred=cred)
        return DailyRewardRecords(**data)

    async def claim_daily_reward(
        self,
        cred: Optional[str] = None,
        player_id: Optional[int] = None,
        game: Optional[Game] = None,
    ) -> DailyReward:
        """
        Signs into lab and claims the daily reward.

        Args:
            cred (str): The user's cred token. Defaults to self.cookies.cred if not provided.
            player_id (int): The player's ID. Defaults to None.
            game (Game): The game to claim the reward for. Defaults to None.
        """
        game = game or self.game
        game_id = game.game_id
        player_id = player_id or self.player_id
        server_id = recognize_server(player_id, game)
        if game is Game.ENDFIELD:
            path = "game/endfield/attendance"
            headers = {"sk-game-role": f"{game_id}_{player_id}_{server_id}"}
        else:
            raise ValueError("Daily rewards are only supported for Endfield at this time.")
        data = await self.request_base_api(path, method="POST", headers=headers, cred=cred)
        return DailyReward(**data)
