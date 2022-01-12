from bs4 import BeautifulSoup

from core.base_request import RjBaseRequest


class MP3(RjBaseRequest):

    def get_playlist(self):
        return self.get("https://r-j-app-desk.com/api2/playlists_dash", True)

    def info(self, mp3_id: int):
        return self.get(f"https://r-j-app-desk.com/api2/mp3?id={mp3_id}", True)

    def vote(self, mp3_id: int):
        res = self.get(f"https://r-j-app-desk.com/api2/mp3_vote?id={mp3_id}&type=mp3&vote=5", True)
        return res
