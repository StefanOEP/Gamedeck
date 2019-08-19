#!/usr/bin/env python

import npyscreen
import curses

#from UI.GameListWidget import GameListWidget


class GameList(npyscreen.MultiLineAction):

    #_contained_widgets    = GameListWidget;
    _contained_widget_height = 1
    
    def __init__(self, *args, **keywords):        
        super(GameList, self).__init__(*args, **keywords)
        self.add_handlers({
            "q": self.when_quit,
            "^A": self.when_add_game,
            "^D": self.when_delete_record,
            "t": self.toggle_category,
            curses.KEY_F8: self.when_sync
        })

    def display_value(self, game):
        return "      %s" % (game.title)
        # return game;

    def actionHighlighted(self, act_on_this, keypress):        
        self.parent.parentApp.getForm('EDITGAME').value = act_on_this
        self.parent.parentApp.switchForm('EDITGAME')
    
    def afterEditing(self):
        self.parent.parentApp.setNextForm(None)

    def when_quit(self, *args, **keywords):
        #self._last_value
        self.parent.parentApp.switchForm(None)

    def when_add_game(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITGAME').value = None
        self.parent.parentApp.switchForm('EDITGAME')

    def when_delete_record(self, *args, **keywords):
        ok = npyscreen.notify_ok_cancel(
            "Sure you want to delete entry?", title="Confirm")
        if(ok):
            self.parent.parentApp.gamedata.delete_game(
                self.values[self.cursor_line])
            self.parent.parentApp.gamedata.load_games()
            self.parent.parentApp.switchFormPrevious()

    def when_sync(self, *args, **keywords):
        #npyscreen.notify_confirm("Title is required", "Error");
        self.parent.parentApp.switchForm('SYNC')

    def toggle_category(self, *args, **keywords):
        self.parent.toggle_sort()

