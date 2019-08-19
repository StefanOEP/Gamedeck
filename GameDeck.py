#!/usr/bin/env python
# https://npyscreen.readthedocs.io/index.html

import npyscreen
import os
import Settings
from Business.GameData import GameData

from UI.GameListDisplay import GameListDisplay
from UI.GameList import GameList
from UI.EditGame import EditGame
from UI.SyncUI.Sync import Sync
from UI.SyncUI.Sync_steam_options import Sync_steam_options
from UI.SyncUI.Sync_steam import Sync_steam
from UI.SyncUI.Sync_gog_options import Sync_gog_options
from UI.SyncUI.Sync_gog import Sync_gog

from Model.Game import Game


class GameDeck(npyscreen.NPSAppManaged):
    def onStart(self):
        self.gamedata = GameData()
        
        
        self.addForm('MAIN', GameListDisplay)
        self.addForm('EDITGAME', EditGame)
        self.addForm('SYNC', Sync)
        self.addForm('SYNC_STEAM_OPTIONS', Sync_steam_options)
        self.addForm('SYNC_STEAM', Sync_steam)
        self.addForm('SYNC_GOG_OPTIONS', Sync_gog_options)
        self.addForm('SYNC_GOG', Sync_gog)

    def reset(self):
        self.gamedata = GameData()


if __name__ == '__main__':
    app = GameDeck()
    app.run()
