# ALL CREDIT GOES TO https://github.com/eddie3/gogrepo

import npyscreen
import threading
import time
import urllib.request
import json
import time
import socket
import contextlib
import html5lib
import codecs
import json
import http.cookiejar as cookiejar

from urllib.request import HTTPCookieProcessor, HTTPError, URLError, build_opener, Request
from urllib.parse import urlparse, urlencode, unquote
from http.client import BadStatusLine

from Model.Game import Game
from Business.GameData import GameData

from UI.CustomUI.CustomButton import CustomButton

try:
    input = raw_input
except NameError:
    pass
# HTTP request settings
HTTP_FETCH_DELAY = 1   # in seconds
HTTP_RETRY_DELAY = 5   # in seconds
HTTP_RETRY_COUNT = 3
HTTP_GAME_DOWNLOADER_THREADS = 4
HTTP_PERM_ERRORCODES = (404, 403, 503)

# GOG URLs
GOG_HOME_URL = r'https://www.gog.com'
GOG_ACCOUNT_URL = r'https://www.gog.com/account'
GOG_LOGIN_URL = r'https://login.gog.com/login_check'

GOG_MEDIA_TYPE_GAME = '1'

# UNxoTf3mt44Qd1zMtg3NWjih


class Sync_gog(npyscreen.FormBaseNew):
    def create(self):
        self.gog_username = None
        self.gog_password = None

        self.done = None
        self.gamedata = GameData()

        # bypass the hardcoded "Netscape HTTP Cookie File" check
        cookiejar.MozillaCookieJar.magic_re = r'.*'
        self.COOKIES_FILENAME = r'gog-cookies.dat'
        self.global_cookies = cookiejar.LWPCookieJar(self.COOKIES_FILENAME)
        self.cookieproc = HTTPCookieProcessor(self.global_cookies)
        self.opener = build_opener(self.cookieproc)

        self.loader = self.add(npyscreen.SliderPercent,
                               name="Loading", max_height=3)
        self.loader.editable = False

    def pre_edit_loop(self):
        if(not self.gog_username or not self.gog_password):
            npyscreen.notify_confirm(
                "Username and password is required to login..", "Error")
            self.parentApp.switchFormPrevious()
            return

        login_result = self.gog_login(self.gog_username, self.gog_password)
        if(login_result != 'success'):
            npyscreen.notify_confirm(login_result, "Error")
            self.parentApp.switchFormPrevious()
            return

        self.thread = None
        self.thread_run = True
        self.loader.set_value(0)
        # Daemonize thread
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()
        self.thread.join()
        self.done = self.add(CustomButton, name="Done", rely=10)

    def when_pressed(self):
        #TODO: CANCEL
        main = self.parentApp.getForm('MAIN')
        main.force_parent_update()
        self.parentApp.switchForm('MAIN')

    def run(self):
        platforms = self.gamedata.platforms
        store = ""
        for st in self.gamedata.stores:
            if(st.name.lower() == 'gog'):
                store = st.store_id

        games = self.gog_update(platforms, str(store))

        total_count = len(games)
        current_count = 0

        #npyscreen.notify_confirm("Found: " + str(total_count), "Error");

        while self.thread_run:
            for game in games:
                current_count = current_count + 1

                record = self.gamedata.gog_id_exists(game.gog_id)
                if(record):
                    game.record_id = record.record_id
                    #game.category = record.category;
                    game.set_category(record.category)
                    self.gamedata.update_game(game)
                else:
                    #npyscreen.notify_confirm(game.title + " " + game.description + " " + game.run_platforms + " " + game.genres + " " + game.store + " " + game.storepage + " " + game.gog_id, "Error");
                    self.gamedata.add_game(game)

                percentage = (current_count / total_count) * 100
                self.loader.set_value(percentage)
                self.loader.update()
                self.refresh()

            self.thread_run = False

    def gog_login(self, user, passwd):
        """Attempts to log into GOG and saves the resulting cookiejar to disk.
        """
        login_data = {'user': user,
                      'passwd': passwd,
                      'auth_url': None,
                      'login_token': None,
                      'two_step_url': None,
                      'two_step_token': None,
                      'two_step_security_code': None,
                      'login_success': False,
                      }

        self.global_cookies.clear()  # reset cookiejar

        # fetch the auth url
        with self.request(GOG_HOME_URL, delay=0) as page:
            etree = html5lib.parse(page, namespaceHTMLElements=False)
            for elm in etree.findall('.//script'):
                if elm.text is not None and 'GalaxyAccounts' in elm.text:
                    login_data['auth_url'] = elm.text.split("'")[3]
                    break

        # fetch the login token
        with self.request(login_data['auth_url'], delay=0) as page:
            etree = html5lib.parse(page, namespaceHTMLElements=False)
            # Bail if we find a request for a reCAPTCHA
            if len(etree.findall('.//div[@class="g-recaptcha form__recaptcha"]')) > 0:
                return "Recapchta enabled, try again later.."
            for elm in etree.findall('.//input'):
                if elm.attrib['id'] == 'login__token':
                    login_data['login_token'] = elm.attrib['value']
                    break

        # perform login and capture two-step token if required
        with self.request(GOG_LOGIN_URL, delay=0, args={'login[username]': login_data['user'],
                                                        'login[password]': login_data['passwd'],
                                                        'login[login]': '',
                                                        'login[_token]': login_data['login_token']}) as page:
            etree = html5lib.parse(page, namespaceHTMLElements=False)
            if 'two_step' in page.geturl():
                login_data['two_step_url'] = page.geturl()
                for elm in etree.findall('.//input'):
                    if elm.attrib['id'] == 'second_step_authentication__token':
                        login_data['two_step_token'] = elm.attrib['value']
                        break
            elif 'on_login_success' in page.geturl():
                login_data['login_success'] = True

        # perform two-step if needed
        if login_data['two_step_url'] is not None:
            #login_data['two_step_security_code'] = input("enter two-step security code: ")
            return "Two step enabled, not implemented yet..."

            # Send the security code back to GOG
            # with self.request(login_data['two_step_url'], delay=0,
            #             args={'second_step_authentication[token][letter_1]': login_data['two_step_security_code'][0],
            #                 'second_step_authentication[token][letter_2]': login_data['two_step_security_code'][1],
            #                 'second_step_authentication[token][letter_3]': login_data['two_step_security_code'][2],
            #                 'second_step_authentication[token][letter_4]': login_data['two_step_security_code'][3],
            #                 'second_step_authentication[send]': "",
            #                 'second_step_authentication[_token]': login_data['two_step_token']}) as page:
            #     if 'on_login_success' in page.geturl():
            #         login_data['login_success'] = True

        # save cookies on success
        if login_data['login_success']:
            self.global_cookies.save()
            return "success"
        else:
            return "Unable to login..."

    def gog_update(self, platforms, store_id):
        media_type = GOG_MEDIA_TYPE_GAME
        items = []
        i = 0

        self.load_cookies()

        api_url = GOG_ACCOUNT_URL
        api_url += "/getFilteredProducts"
        done = False
        while not done:
            i += 1
            url = api_url + "?" + urlencode({'mediaType': media_type,
                                             'sortBy': 'title',
                                             'page': str(i)})

            with self.request(url, delay=0) as data_request:
                reader = codecs.getreader("utf-8")

                try:
                    json_data = json.load(reader(data_request))
                except ValueError:
                    raise SystemExit(1)

                for item_json_data in json_data['products']:
                    if item_json_data.get('isHidden', False) is True:
                        continue

                    gog_id = str(item_json_data['id'])
                    title = item_json_data['title']
                    description = item_json_data['slug']
                    genre = item_json_data['category']
                    store_url = "https://www.gog.com" + item_json_data['url']

                    src_platforms = item_json_data['worksOn']

                    run_platforms = []
                    for platform in platforms:
                        key = platform.name.lower()
                        if('linux' in key):
                            key = 'linux'
                        if('mac' in key):
                            key = 'mac'

                        lower_src_platforms = dict(
                            (k.lower(), v) for k, v in src_platforms.items())

                        if(key in lower_src_platforms):
                            if lower_src_platforms[key]:
                                run_platforms.append(str(platform.platform_id))

                    run_platforms = ','.join(run_platforms)

                    game = Game(title, description, run_platforms,
                                genre, store_id, store_url, None, gog_id, None)
                    game.set_category(0)
                    items.append(game)

                    if i >= json_data['totalPages']:
                        done = True

        return items

    def request(self, url, args=None, byte_range=None, retries=HTTP_RETRY_COUNT, delay=HTTP_FETCH_DELAY):
        """Performs web request to url with optional retries, delay, and byte range.
        """
        _retry = False
        time.sleep(delay)

        try:
            if args is not None:
                enc_args = urlencode(args)
                enc_args = enc_args.encode('ascii')  # needed for Python 3
            else:
                enc_args = None
            req = Request(url, data=enc_args)
            if byte_range is not None:
                req.add_header('Range', 'bytes=%d-%d' % byte_range)
            page = self.opener.open(req)
        except (HTTPError, URLError, socket.error, BadStatusLine) as e:
            if isinstance(e, HTTPError):
                if e.code in HTTP_PERM_ERRORCODES:  # do not retry these HTTP codes
                    raise
            if retries > 0:
                _retry = True
            else:
                raise

            if _retry:
                return self.request(url=url, args=args, byte_range=byte_range, retries=retries-1, delay=HTTP_RETRY_DELAY)

        return contextlib.closing(page)

    def load_cookies(self):
        # try to load as default lwp format
        try:
            self.global_cookies.load()
            return
        except IOError:
            pass

        # try to import as mozilla 'cookies.txt' format
        try:
            tmp_jar = cookiejar.MozillaCookieJar(self.global_cookies.filename)
            tmp_jar.load()
            for c in tmp_jar:
                self.global_cookies.set_cookie(c)
            self.global_cookies.save()
            return
        except IOError:
            pass

        raise SystemExit(1)
