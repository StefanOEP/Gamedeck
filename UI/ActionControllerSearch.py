#!/usr/bin/env python
import npyscreen
import curses


class ActionControllerSearch(npyscreen.ActionControllerSimple):
    def create(self):
        #self.add_action('^:[pP]{1}[0-9]{1,2}$', self.set_command, False)
        #self.add_action('^:[pP]riority[0-9]{1,2}$', self.set_command, False)
        self.add_action('^/.*', self.set_search, True)

    # def set_command(self, command_line, widget_proxy, live):
    #     priorityPhrase = command_line[2:]
    #     priorityInt = int(priorityPhrase)

    def set_search(self, command_line, widget_proxy, live):

        searchPhrase = command_line[1:]
        games = self.search_games(searchPhrase, self.parent.parentApp.gamelist)

        self.parent.update_view(games)

    def search_games(self, searchPhrase, gameList):
        result = []
        searchPhrase = searchPhrase.lower()

        if(searchPhrase.startswith("title:")):
            searchPhrase = searchPhrase[6:]
            for g in gameList:
                if(searchPhrase in g.title.lower()):
                    result.append(g)

        elif (searchPhrase.startswith("description:")):
            searchPhrase = searchPhrase[12:]
            searchList = searchPhrase.split(',')

            for g in gameList:
                exist_in = True
                for i in searchList:
                    if(i not in g.description.lower()):
                        exist_in = False

                if(exist_in):
                    result.append(g)

        elif (searchPhrase.startswith("tags:")):
            searchPhrase = searchPhrase[5:]
            searchList = searchPhrase.split(',')
            for g in gameList:
                exist_in = True
                for i in searchList:
                    if(i not in g.genres.lower()):
                        exist_in = False
                if(exist_in):
                    result.append(g)

        elif(searchPhrase.startswith("platform:")):
            platforms = self.parent.parentApp.gamedata.platforms
            searchPhrase = searchPhrase[10:]
            searchList = searchPhrase.split(',')

            searched_platforms = []
            for searchedItem in searchList:
                for p in platforms:
                    if(searchedItem in p.name):
                        searched_platforms.append(p)

            for g in gameList:
                add_game = False
                for p in searched_platforms:
                    if (str(p.platform_id) in g.run_platforms):
                        add_game = True

                if(add_game):
                    result.append(g)

        elif(searchPhrase.startswith("store:")):
            stores = self.parent.parentApp.gamedata.stores
            searchPhrase = searchPhrase[7:]
            searchList = searchPhrase.split(',')

            searched_stores = []
            for searchedItem in searchList:
                for s in stores:
                    if(searchedItem.lower() in s.name.lower()):
                        searched_stores.append(s)

            for g in gameList:
                add_game = False
                for s in searched_stores:
                    if(str(s.store_id) in g.store):
                        add_game = True

                if(add_game):
                    result.append(g)

        else:
            for g in gameList:
                if(searchPhrase in g.title.lower() or searchPhrase in g.description.lower()):
                    result.append(g)

        return result
