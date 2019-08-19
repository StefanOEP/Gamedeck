
import npyscreen
import curses

from UI.CustomUI.CustomMultiLineAction import CustomMultiLineAction


class Sync(npyscreen.Form):
    def create(self):
        self.headline = self.add(
            npyscreen.Textfield, editable=False, max_height=3)
        self.headline.value = "Select Source:"
        #self.steam = self.add(npyscreen.Button, name = "STEAM", rely=4)

        #self.add(npyscreen.Button, name = "GoG", rely=6)
        self.choice = self.add(CustomMultiLineAction)

        self.add_handlers({
            "q": self.when_quit
        })

    def beforeEditing(self):
        self.choice.values = ['Steam', 'GoG']

    def afterEditing(self):
        self.parentApp.switchFormPrevious()

    def on_ok(self):
        self.exit_menu()

    def when_quit(self, *args, **keywords):
        self.exit_menu()

    def exit_menu(self):
        self.parentApp.switchFormPrevious()

    def run_sync_type(self, sync_type):
        if(sync_type.lower() == 'steam'):
            self.parentApp.getForm('SYNC_STEAM_OPTIONS')
            self.parentApp.switchForm('SYNC_STEAM_OPTIONS')
        elif (sync_type.lower() == 'gog'):
            self.parentApp.getForm('SYNC_GOG_OPTIONS')
            self.parentApp.switchForm('SYNC_GOG_OPTIONS')
