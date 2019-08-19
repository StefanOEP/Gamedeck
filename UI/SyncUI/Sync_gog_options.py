
import npyscreen
import curses
import os

from UI.CustomUI.CustomTextFieldBox import CustomTextFieldBox


class Sync_gog_options(npyscreen.ActionFormV2):
    def create(self):
        self.username = self.add(
            npyscreen.TitleText, name="Username:", max_height=3)
        self.password = self.add(
            npyscreen.TitlePassword, name="Password:", max_height=3)

    def beforeEditing(self):
        username = os.getenv("gog-username")
        self.username.value = username

        password = os.getenv("gog-password")
        self.password.value = password

    def on_cancel(self):
        self.go_back()

    def on_ok(self):
        sync = self.parentApp.getForm('SYNC_GOG')
        sync.gog_username = self.username.value
        sync.gog_password = self.password.value
        self.parentApp.switchForm('SYNC_GOG')

    def go_back(self):
        self.parentApp.switchFormPrevious()
