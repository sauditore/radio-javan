from typing import Dict

from .base_request import RjBaseRequest


class MP3(RjBaseRequest):
    """
    Class to operate on mp3 files
    """

    def get_playlist(self) -> Dict:
        """
        Get user active play lost

        :return:
        :rtype: Dict
        """

        return self.get("https://r-j-app-desk.com/api2/playlists_dash", True)

    def info(self, mp3_id: int):
        """

        :param mp3_id:
        :return:
        """

        return self.get(f"https://r-j-app-desk.com/api2/mp3?id={mp3_id}", True)

    def vote(self, mp3_id: int):
        res = self.get(f"https://r-j-app-desk.com/api2/mp3_vote?id={mp3_id}&type=mp3&vote=5", True)
        return res
