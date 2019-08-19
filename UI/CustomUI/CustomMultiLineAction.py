
import npyscreen
import curses


class CustomMultiLineAction(npyscreen.MultiLineAction):
    def create(self):
        pass

    def actionHighlighted(self, act_on_this, key_press):
        self.parent.run_sync_type(act_on_this)
