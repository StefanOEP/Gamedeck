
import npyscreen
from UI.GameList import GameList
from UI.ActionControllerSearch import ActionControllerSearch


class GameListDisplay(npyscreen.FormMuttActiveTraditional):
    MAIN_WIDGET_CLASS = GameList
    ACTION_CONTROLLER = ActionControllerSearch

    def __init__(self, *args, **keywords):
        super(GameListDisplay, self).__init__(*args, **keywords)
        self.set_value(self.DATA_CONTROLER())
        self.sort = 1
        self.cat = None
        self.title = "ALL"
        self.parentApp.gamelist = self.parentApp.gamedata.games

    def force_parent_update(self):
        self.parentApp.reset()

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        # self.wMain.value.get();
        games = self.parentApp.gamedata.games
        gameList = self.parentApp.gamelist

        if(self.sort > 4):
            self.sort = 0

        if(self.sort == 0):
            self.title = "ALL"
            gameList = games

        elif(self.sort == 1):
            self.title = "TO PLAY"
            gameList = [game for game in games if game.category == 0]

        elif(self.sort == 2):
            self.title = "Completed"
            gameList = [game for game in games if game.category == 1]

        elif(self.sort == 3):
            self.title = "Skip"
            gameList = [game for game in games if game.category == 2]

        elif(self.sort == 4):
            self.title = "Multiplayer"
            gameList = [game for game in games if game.category == 3]

        self.parentApp.gamelist = gameList
        self.update_view(gameList)

    def update_view(self, gamelist):
        count = len(gamelist)
        #npyscreen.notify_confirm("COUNT: " + str(count), "Error")
        self.wStatus1.value = self.title + " (" + str(count) + ") "
        self.wStatus2.value = "q: Quit\t^a: Add\t^Enter: Edit\t^d: Delete\tt: Toggle Category\tF8: Sync "
        self.wStatus1.display()
        #self.wMain.values = gamelist
        self.value.set_values(gamelist)
        self.wMain.values = self.value.get()
        self.wMain.display()

    def toggle_sort(self):
        self.sort = self.sort + 1
        self.update_list()
