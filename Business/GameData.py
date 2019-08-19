from appdirs import AppDirs
import os
import json
import sqlite3
from datetime import date, datetime
import os
#from tinydb import TinyDB, Query

from Model.Game import Game
from Model.Platform import Platform
from Model.Store import Store
from Model.Category import Category

class GameData:

    games = None
    platforms = None
    stores = None
    categories = None


    db = None

    def __init__(self):
        dbdir = os.getenv("dbdir")
        if(dbdir and os.path.isdir(dbdir)):
            self.dataFile = dbdir + 'gamedata.db'
        else:
            dirs = AppDirs("GameDeck", "GameDeck")
            self.dataFile = dirs.user_data_dir + '/gamedata.db'

        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS games\
            ( game_internal_id INTEGER PRIMARY KEY, \
              title     TEXT  NOT NULL, \
              description   TEXT, \
              run_platforms   TEXT, \
              genres TEXT, \
              store TEXT, \
              storepage TEXT, \
              steam_appid TEXT, \
              gog_id TEXT, \
              category_id INTEGER, \
              created_at DATE, \
              updated_at DATE \
              )"
        )
        db.commit()
        c.close()

        c = db.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS run_platforms\
            ( platform_internal_id INTEGER PRIMARY KEY, \
              name     TEXT \
              )"
        )
        db.commit()
        c.close()

        c = db.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS stores\
            ( store_internal_id INTEGER PRIMARY KEY, \
              name     TEXT \
              )"
        )
        db.commit()
        c.close()

        c = db.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS categories\
            ( category_id INTEGER PRIMARY KEY, \
              name     TEXT \
              )"
        )
        db.commit()
        c.close()

        self.load_games()

        self.load_platforms()
        if(len(self.platforms) < 1):
            self.add_basic_platforms();
            self.load_platforms()
        

        self.load_stores()
        if(len(self.stores) < 1):
            self.add_basic_stores();
            self.load_stores()
        
        self.load_categories()
        if(len(self.categories) < 1):
            self.add_basic_categories();
            self.load_categories();


    def add_game(self, game):
        now = datetime.now()
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('INSERT INTO games(title, description, run_platforms, genres, store, storepage, steam_appid, gog_id, category_id, created_at, updated_at) \
                    VALUES(?,?,?,?,?,?,?,?,?,?,?)', (game.title, game.description, game.run_platforms, game.genres, game.store, game.storepage, game.steam_appid, game.gog_id, game.category, now, now))
        db.commit()
        c.close()

    def update_game(self, game):
        now = datetime.now()
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('UPDATE games set title=?, description=?, run_platforms=?, genres=?, store=?, storepage=?, gog_id=?, category_id=?, updated_at=? \
                    WHERE game_internal_id=?', (game.title, game.description, game.run_platforms, game.genres, game.store, game.storepage, game.gog_id, game.category, now, game.record_id))
        db.commit()
        c.close()    

    def delete_game(self, game):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('DELETE FROM games where game_internal_id=?', (game.record_id,))
        db.commit()
        c.close()    
    
    def load_games(self, ):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('SELECT title, description, run_platforms, genres, store, storepage, steam_appid, gog_id, game_internal_id, category_id, created_at, updated_at from games ORDER BY title ASC')
        games_raw = c.fetchall()
        c.close()
        games_new = [];

        for g in games_raw:
            new_game = Game(g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8]);
            new_game.set_category(g[9]);
            new_game.set_created(g[10]);
            new_game.set_updated(g[11]);
            games_new.append(new_game);
        
        self.games = games_new;
    
    def steam_appid_exists(self, appid):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('SELECT title, description, run_platforms, genres, store, storepage, steam_appid, gog_id, game_internal_id, category_id from games where steam_appid = ?', (appid,));
        games_raw = c.fetchall()
        c.close()
        if(games_raw and len(games_raw) > 0):
            g = games_raw[0];
            game = Game(g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8]);
            game.set_category(g[9]);
            return game;

        else:
            return None;
        
    
    def gog_id_exists(self, gog_id):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('SELECT title, description, run_platforms, genres, store, storepage, steam_appid, gog_id, game_internal_id, category_id from games where gog_id = ?', (gog_id,));
        games_raw = c.fetchall()
        c.close()
        if(games_raw and len(games_raw) > 0):
            g = games_raw[0];
            game = Game(g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8]);
            game.set_category(g[9]);
            return game;

        else:
            return None;


    def load_platforms(self):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('SELECT platform_internal_id, name from run_platforms')
        platforms_raw = c.fetchall()
        c.close()
        platforms_new = [];

        for g in platforms_raw:
            platforms_new.append(Platform(g[0], g[1]));
        
        self.platforms = platforms_new;
        
    
    def add_platform(self, p):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('INSERT INTO run_platforms(name) VALUES(?)', (p,))
        db.commit()
        c.close()

    def add_basic_platforms(self):
        bplatforms = ['Windows', 'Linux/GNU', 'MacOS'];
        for p in bplatforms:
            self.add_platform(p)


    def load_stores(self):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('SELECT store_internal_id, name from stores')
        stores_raw = c.fetchall()
        c.close()
        stores_new = [];

        for s in stores_raw:
            stores_new.append(Store(s[0], s[1]));

        self.stores = stores_new;

    def add_store(self, s):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('INSERT INTO stores(name) VALUES(?)', (s,))
        db.commit()
        c.close()
    
    def add_basic_stores(self):
        bstores = ['Steam', 'GoG', 'EpicStore', 'Uplay', 'HumbleBundle', 'Battle.Net', 'Origin', 'WindowsStore', 'Other']
        for s in bstores:
            self.add_store(s);


    def load_categories(self):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('SELECT category_id, name from categories')
        categories_raw = c.fetchall()
        c.close()
        categories_new = [];

        for s in categories_raw:
            categories_new.append(Category(s[0], s[1]));

        self.categories = categories_new;
    
    def add_category(self, cat):
        db = sqlite3.connect(self.dataFile)
        c = db.cursor()
        c.execute('INSERT INTO categories(name) VALUES(?)', (cat,))
        db.commit()
        c.close()
    
    def add_basic_categories(self):
        bcategories = ['To-Play', 'Completed', 'Skipped', 'Multiplayer']
        for c in bcategories:
            self.add_category(c);
