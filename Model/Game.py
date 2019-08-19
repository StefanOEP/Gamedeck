import json
import uuid


class Game():
  def __init__(self, title, description, run_platforms, genres, store, storepage, steam_appid, gog_id, record_id):
    self.record_id = record_id;
    self.title = title;
    self.description = description;
    self.run_platforms = run_platforms;
    self.genres = genres;
    self.store = store;
    self.storepage = storepage;
    self.steam_appid = steam_appid;
    self.gog_id = gog_id;
    self.category = 0;
    self.updated_at = '';
    self.created_at ='';
  
  def set_category(self, category):
    self.category = int(category);

  def set_created(self, date):
    self.created_at = date;

  def set_updated(self, date):
    self.updated_at = date;
  
