
import npyscreen

from Model.Game import Game
from datetime import datetime

#from UI.multiContainedBox import multiContainedBox
from UI.CustomUI.CustomBoxTitle import CustomBoxTitle
from UI.CustomUI.CustomInputBox import CustomInputBox
from UI.CustomUI.CustomTextFieldBox import CustomTextFieldBox
from UI.CustomUI.CustomBoxTitleSingleSelect import CustomBoxTitleSingleSelect


class EditGame(npyscreen.ActionFormV2):
    def create(self):

        self.add_handlers({
            "q": self.when_quit
        })
        #self.value = None;
        self.gametitle = self.add(
            CustomTextFieldBox, name="Title:", max_height=3)
        self.gamedescription = self.add(
            npyscreen.MultiLineEditableBoxed, name="Description:", editable=True, max_height=5)
        self.gamedescription.scroll_exit = True
        self.gameplatforms = self.add(CustomBoxTitle, name="Platforms:", max_height=6,
                                      contained_widget_arguments={
                                          'widgets_inherit_color': True, }, )
        self.gameplatforms.values = self.parentApp.gamedata.platforms
        self.gameplatforms.scroll_exit = True

        self.gamestores = self.add(CustomBoxTitle, name="Stores:", max_height=11,
                                   contained_widget_arguments={
                                       'widgets_inherit_color': True, }, )
        self.gamestores.values = self.parentApp.gamedata.stores
        self.gamestores.scroll_exit = True

        self.gamestorepage = self.add(
            CustomTextFieldBox, name="Store page:", max_height=3)

        self.gamegenre = self.add(
            npyscreen.MultiLineEditableBoxed, name="Genres/Tags:", editable=True, max_height=15)
        self.gamegenre.scroll_exit = True

        self.gamecategory = self.add(
            CustomBoxTitleSingleSelect, name="Category", max_height=7)
        self.gamecategory.values = self.parentApp.gamedata.categories
        self.gamecategory.scroll_exit = True

        self.gameupdated = self.add(npyscreen.Textfield, editable=False)

    def beforeEditing(self):
        self.gameplatforms.value = []
        self.gamestores.value = []
        self.gamegenre.value = []
        self.gamegenre.values = []
        self.gametitle.value = ''
        self.gamedescription.value = ''
        self.gamedescription.values = ''
        self.gamestorepage.value = ''
        self.gameupdated.value = ''
        self.gamecategory.value = 0

        if(self.value):
            #game = self.parentApp.gamedata.get_game(self.value)
            game = self.value
            self.gametitle.value = game.title
            self.gamedescription.values = game.description.split('\n')
            self.gamedescription.entry_widget.start_display_at = 0
            self.gamedescription.entry_widget.cursor_line = 0

            self.gameplatforms.value = self.get_platform_selection()
            self.gamestores.value = self.get_store_selection()
            self.gamestorepage.value = game.storepage

            self.gamegenre.values = game.genres.split('\n')
            self.gamegenre.entry_widget.start_display_at = 0
            self.gamegenre.entry_widget.cursor_line = 0

            cat = 0
            if(game.category):
                cat = game.category
            self.gamecategory.value = int(cat)

            #self.gameupdated.value = game.updated_at
            up = datetime.strptime(game.updated_at, '%Y-%m-%d %H:%M:%S.%f')
            up_str = up.strftime("%m/%d/%Y, %H:%M:%S")
            self.gameupdated.value = up_str

    def on_ok(self):
        #platforms = self.gameplatforms._contained_widget.get_selected_objects(self.gameplatforms);
        if not self.gametitle.value:
            npyscreen.notify_confirm("Title is required", "Error")
        else:

            platformString = ""
            #all_platforms = self.parentApp.gamedata.platforms;
            platform_selections = self.gameplatforms._contained_widget.get_selected_objects(
                self.gameplatforms)
            if(platform_selections and len(platform_selections) > 0):
                for pselection in platform_selections:
                    platformString += str(pselection.platform_id) + ","

            storesString = ""
            stores_selections = self.gamestores._contained_widget.get_selected_objects(
                self.gamestores)
            if(stores_selections and len(stores_selections) > 0):
                for sselection in stores_selections:
                    storesString += str(sselection.store_id) + ","

            description = '\n'.join(self.gamedescription.values)
            storepage = self.gamestorepage.value

            genres = self.unique(self.gamegenre.values)
            genres = '\n'.join(genres)
            category = self.gamecategory._contained_widget.get_selected_objects(
                self.gamecategory)[0].category_id

            if(not self.value):
                game = Game(self.gametitle.value, description, platformString,
                            genres, storesString, storepage, None, None, None)
                game.set_category(category - 1)
                self.parentApp.gamedata.add_game(game)

            else:
                game_old = self.value
                game_new = Game(self.gametitle.value, description, platformString,  genres,
                                storesString, storepage, game_old.steam_appid, game_old.gog_id, game_old.record_id)
                game_new.set_category(category - 1)

                self.parentApp.gamedata.update_game(game_new)

            self.parentApp.gamedata.load_games()
            self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def when_quit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def get_platform_selection(self):
        platform_selected_index = []
        all_platforms = self.parentApp.gamedata.platforms
        selection_platforms = [x.strip()
                               for x in self.value.run_platforms.split(',')]
        for select_platform in selection_platforms:
            for all_platform in all_platforms:
                if select_platform and (all_platform.platform_id == int(select_platform)):
                    platform_selected_index.append(
                        all_platforms.index(all_platform))
        return platform_selected_index

    def get_store_selection(self):
        store_selected_index = []
        all_stores = self.parentApp.gamedata.stores
        selection_stores = [x.strip() for x in self.value.store.split(',')]
        for selection_store in selection_stores:
            for all_store in all_stores:
                if selection_store and (all_store.store_id == int(selection_store)):
                    store_selected_index.append(all_stores.index(all_store))
        return store_selected_index

    def unique(self, slist):

        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in slist:
            x = x.replace('.', '').replace(',', '')
            x = x.lower()
            x = x.capitalize()
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)

        return unique_list
