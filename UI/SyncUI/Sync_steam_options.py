
import npyscreen
import curses
import os

from UI.CustomUI.CustomTextFieldBox import CustomTextFieldBox


class Sync_steam_options(npyscreen.ActionFormV2):
    def create(self):
        self.steamId = self.add(
            CustomTextFieldBox, name="SteamID:", max_height=3)
        self.steamAPIKey = self.add(
            CustomTextFieldBox, name="SteamAPI:", max_height=3)

    def beforeEditing(self):
        steamid = os.getenv("steamid")
        self.steamId.value = steamid

        steamapi = os.getenv("steamAPIKey")
        self.steamAPIKey.value = steamapi

    def on_cancel(self):
        self.go_back()

    def on_ok(self):
        sync = self.parentApp.getForm('SYNC_STEAM')
        sync.steamAPIKey = self.steamAPIKey.value
        sync.steamid = self.steamId.value
        self.parentApp.switchForm('SYNC_STEAM')

    def go_back(self):
        self.parentApp.switchFormPrevious()
