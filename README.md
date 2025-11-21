# Church Song App

A Python application to manage church songs, with both a GUI (Tkinter) and optional CLI interface.

## Project Description

The Church Song App helps users organize, add, edit, search, and save church songs in a structured format (`songs.json`). It is designed for easy access and management of songs for church services or personal use.

## Features

**GUI (Tkinter):**
- View all songs in a list
- Real-time search and filter
- Add new songs (title and optional number)
- Edit existing songs
- Delete songs
- Import multiple songs from text
- Save changes to `songs.json` (manual or automatic)

**CLI (Command-Line Interface):**
- List all songs
- Add songs quickly from the command line
- Remove songs by index

**Data Storage:**
- Songs are stored in `songs.json`
- Auto-creates `songs.json` if it doesn't exist

## Installation

1. Make sure you have Python 3 installed.
2. Clone this repository:
```bash
git clone https://github.com/yourusername/church-song-app.git
```
3. Navigate to the project directory:
```bash
cd church-song-app
```
4. Run the application:
```bash
python church_song_app.py
```

To run in CLI mode:
```bash
python church_song_app.py --cli
```

## Dependencies

- Python 3
- Tkinter (usually included with Python)

## Usage

**GUI Mode:**
- Double-click a song to edit
- Use the Add/Edit/Delete buttons to manage songs
- Use the search bar to filter songs in real-time
- Save your changes using the Save button

**CLI Mode:**
- List songs: `python church_song_app.py --cli --list`
- Add song: `python church_song_app.py --cli --add "Song Title" "Number"`
- Remove song: `python church_song_app.py --cli --remove INDEX`

## License

MIT License


