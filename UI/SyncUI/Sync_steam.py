import npyscreen
import threading
import time
import urllib.request
import json

from Model.Game import Game
from Business.GameData import GameData

from UI.CustomUI.CustomButton import CustomButton

class Sync_steam(npyscreen.FormBaseNew):
    def create(self):

        self.steamid = None
        self.steamAPIKey = None
        self.loader = self.add(npyscreen.SliderPercent,
                               name="Loading", max_height=3)
        self.loader.editable = False
        self.done = None
        self.gamedata = GameData()

    def pre_edit_loop(self):

        if(not self.steamid or not self.steamAPIKey):
            npyscreen.notify_confirm(
                "steamid and steam api key is required to fetch steam data..", "Error")
            self.parentApp.switchFormPrevious()
        else:
            self.thread = None
            self.thread_run = True
            self.loader.set_value(0)
            self.thread = threading.Thread(target=self.run, args=())
            self.thread.start()
            self.thread.join()
            self.done = self.add(CustomButton, name="Done", rely=10)

    def post_edit_loop(self):
        pass

    def when_pressed(self):
        #TODO: CANCEL
        main = self.parentApp.getForm('MAIN')
        main.force_parent_update()
        self.parentApp.switchForm('MAIN')

    def run(self):
        while self.thread_run:

            content = self.get_games()
            total_count = content["total_count"]
            games = content["games"]
            current_count = 0

            for meta_game in games:
                current_count = current_count + 1

                temp_game = self.get_game(meta_game["appid"])
                if(not temp_game):
                    continue

                title = temp_game['name']
                description = temp_game['short_description']

                src_platforms = temp_game['platforms']
                platforms = self.gamedata.platforms

                run_platforms = []
                for platform in platforms:
                    key = platform.name.lower()
                    if('linux' in key):
                        key = 'linux'
                    if('mac' in key):
                        key = 'mac'

                    if(key in src_platforms):
                        if src_platforms[key]:
                            run_platforms.append(str(platform.platform_id))

                run_platforms = ','.join(run_platforms)

                genres = []
                if('genres' in temp_game):
                    src_genres = temp_game['genres']
                    for genre in src_genres:
                        if ('description' in genre):
                            genres.append(genre['description'])

                    if('categories' in temp_game):
                        src_categories = temp_game['categories']
                        for category in src_categories:
                            genres.append(category['description'])

                genres = '\n'.join(genres)

                # Get steam
                store = ""
                for st in self.gamedata.stores:
                    if(st.name.lower() == 'steam'):
                        store = st.store_id

                # create steampage:
                storepage = 'https://store.steampowered.com/app/' + \
                    str(meta_game["appid"])

                steam_appid = str(meta_game["appid"])

                game = Game(title, description, run_platforms, genres,
                            store, storepage, steam_appid, None, None)
                game.set_category(0)

                record = self.gamedata.steam_appid_exists(steam_appid)
                if(record):
                    game.record_id = record.record_id
                    game.set_category(record.category);

                    self.gamedata.update_game(game)
                else:
                    self.gamedata.add_game(game)

                percentage = (current_count / total_count) * 100
                self.loader.set_value(percentage)
                self.loader.update()
                self.refresh()

            self.thread_run = False

    def get_games(self):
        url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
        url = url + self.steamAPIKey
        url = url + '&steamid=' + self.steamid + \
            '&format=json&include_played_free_games=false'

        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        cont = json.loads(r.decode('utf-8'))
        total_count = cont['response']['game_count']
        games = cont['response']['games']
        return {"total_count": total_count, "games": games}

    def get_game(self, appid):
        try:
            url = 'https://store.steampowered.com/api/appdetails?appids=' + \
                str(appid)
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req).read()
            game = json.loads(r.decode('utf-8'))
            return game[str(appid)]["data"]
        except:
            return None
