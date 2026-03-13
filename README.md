# 📻 Fallout Radio Bot

A Discord music bot that plays radio stations from across the Fallout series - Fallout 3, Fallout: New Vegas, Fallout 4, and Fallout 76. Songs are served from local MP3 files for reliable, lag-free playback.

## Features

- Browse radio stations by game using Discord's dropdown menus
- Queue individual songs or an entire station at once
- Shuffle a station's playlist
- Full queue management (view, remove by position)
- Loop modes: off, single song, or entire queue
- Per-server volume control
- Auto-disconnect after 60 seconds alone in a voice channel

## Stations

| Game | Station |
|------|---------|
| Fallout 3 | Galaxy News Radio |
| Fallout 3 | Enclave Radio |
| Fallout: New Vegas | Radio New Vegas |
| Fallout: New Vegas | Mojave Music Radio |
| Fallout 4 | Diamond City Radio |
| Fallout 76 | Appalachia Radio |

## Commands

All commands are available under `/foradio` or as standalone shortcuts.

| Command | Description |
|---------|-------------|
| `/foradio play` | Open the radio station browser |
| `/foradio skip` | Skip the current song |
| `/foradio pause` | Pause playback |
| `/foradio resume` | Resume playback |
| `/foradio stop` | Stop playback and disconnect |
| `/foradio queue` | Show the current queue |
| `/foradio remove <position>` | Remove a song from the queue |
| `/foradio loop <off/song/queue>` | Set loop mode |
| `/foradio volume <0-100>` | Set the volume |
| `/foradio nowplaying` | Show what's currently playing |
| `/foradio help` | Show all commands |

## Setup

### Requirements

- Python 3.10+
- [discord.py](https://github.com/Rapptz/discord.py) 2.x
- [FFmpeg](https://ffmpeg.org/) installed and in PATH
- A Discord bot token

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fallout-radio-bot
   cd fallout-radio-bot
   ```

2. Install dependencies:
   ```bash
   pip install discord.py python-dotenv
   ```

3. Create a `.env` file in the project root:
   ```
   DISCORD_TOKEN=your_token_here
   ```

4. Add your MP3 files to the songs directory (see below).

5. Run the bot:
   ```bash
   python3 bot.py
   ```

### Songs

The bot plays local MP3 files from `/home/ubuntu/falloutbot/songs/` (configurable via `SONGS_PATH` in `bot.py`). Files must match the exact filenames defined in `RADIO_DATA` inside `bot.py`, following the convention:

```
Title - Artist.mp3
```

Songs are not included in this repository.

NOTE - All of this is only relevant if you're trying to build the bot yourself. If you simply want to use the bot, you should be able to find it on various Discord Bot websites such as discord.bots.gg or top.gg.

### Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and add a bot
3. Under **OAuth2 -> URL Generator**, select the `bot` and `applications.commands` scopes
4. Under bot permissions, select: `Connect`, `Speak`, `Send Messages`, `Use Slash Commands`, `View Channels`, `Embed Links`
5. Use the generated URL to invite the bot to your server

## Hosting

This bot is designed to run on a Linux VPS. To keep it running after closing your SSH session, use `screen`:

```bash
screen -S bot
python3 bot.py
# Detach with Ctrl+A then D
# Reattach with: screen -r bot
```

## Built With

- [discord.py](https://github.com/Rapptz/discord.py)
- [FFmpeg](https://ffmpeg.org/)
- Python 3.10+
- Hosted on Oracle Cloud Free Tier (Ubuntu 22.04)
