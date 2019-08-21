# GameDeck

A small python build program for the command-line (TUI) which display and organize gamecollections from multiple sources such as Steam and GOG.

>I wanted to try out working with command line interfaces, and ended up using Python with Npyscreen. I am not usually a Python developer, so i consider this an early prototype that require some cleanup.

![][/Screenshots/example.gif?raw=true]

## Features
- Add and edit game meta-data
- Sort games by **To-play**, **Multiplayer**, **Skipped** or **Completed**
- Search games by title, tags, genre etc.
- Automatically synchronize game-data from **Steam** or **GoG**

## Settings

GameDeck will look for a **.env** file in the program root directory, which can be used to store a few settings and login data for synchronization.

Currently the file can have the following fields:
```
#location for the database (without filename)
dbdir= 

#Steam id and apikey (can be found in the steam profile)
steamid=
steamAPIKey=

#gog login credentials
gog-username=
gog-password=
```
Login and API credentials can also be typed directly into the application when running the syncronization process. 

## Usage
### Commands
Commands are shown in the buttom of the screen.
```
Ctrl+a          Add game
Ctrl+d          Remove game
Enter/Space     Edit game
t               Toggle list category
F8              Open synchronize menu
/               Start search typing
q               Quit
```
### Searching
To start search type "/" 

By default everything typed will search in game title or description, but to make more detailed searched you can type the following keywords:

```
/title:
/description:
/tags:
/platforms:
/store:
```


## Requirements

- Python 3 (Developed using 3.7.3)
- npyscreen
- dotenv 




