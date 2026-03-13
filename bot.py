import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import random
from dotenv import load_dotenv
from collections import deque

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

SONGS_PATH = '/home/ubuntu/falloutbot/songs/'

# -- Song Data -----------------------------------------------------------------
#
# Each song has:
#   title:    display title
#   artist:   display artist
#   filename: exact filename in SONGS_PATH (including .mp3)
#
# Filename convention: {Title} - {Artist}.mp3

RADIO_DATA = {
    "Fallout 3": {
        "Galaxy News Radio": [
            {
                "title":    "I Don't Want to Set the World on Fire",
                "artist":   "The Ink Spots",
                "filename": "I Don't Want to Set the World on Fire - The Ink Spots.mp3",
            },
            {
                "title":    "Maybe",
                "artist":   "The Ink Spots",
                "filename": "Maybe - The Ink Spots.mp3",
            },
            {
                "title":    "Into Each Life Some Rain Must Fall",
                "artist":   "Ella Fitzgerald and The Ink Spots",
                "filename": "Into Each Life Some Rain Must Fall - Ella Fitzgerald and The Ink Spots.mp3",
            },
            {
                "title":    "Butcher Pete (Part 1)",
                "artist":   "Roy Brown",
                "filename": "Butcher Pete (Part 1) - Roy Brown.mp3",
            },
            {
                "title":    "Anything Goes",
                "artist":   "Vince Giordano and the Nighthawks",
                "filename": "Anything Goes - Vince Giordano and the Nighthawks.mp3",
            },
            {
                "title":    "Way Back Home",
                "artist":   "Bob Crosby and The Bob Cats",
                "filename": "Way Back Home - Bob Crosby and The Bob Cats.mp3",
            },
            {
                "title":    "Happy Times",
                "artist":   "Bob Crosby",
                "filename": "Happy Times - Bob Crosby.mp3",
            },
            {
                "title":    "Mighty Mighty Man",
                "artist":   "Roy Brown",
                "filename": "Mighty Mighty Man - Roy Brown.mp3",
            },
        ],
        "Enclave Radio": [
            {
                "title":    "The Stars and Stripes Forever",
                "artist":   "John Philip Sousa",
                "filename": "The Stars and Stripes Forever - John Philip Sousa.mp3",
            },
            {
                "title":    "The Washington Post",
                "artist":   "John Philip Sousa",
                "filename": "The Washington Post - John Philip Sousa.mp3",
            },
            {
                "title":    "America the Beautiful",
                "artist":   "Samuel A. Ward",
                "filename": "America the Beautiful - Samuel A. Ward.mp3",
            },
            {
                "title":    "Marines' Hymn",
                "artist":   "Traditional",
                "filename": "Marines' Hymn - Traditional.mp3",
            },
        ],
    },
    "Fallout: New Vegas": {
        "Radio New Vegas": [
            {
                "title":    "Ain't That a Kick in the Head",
                "artist":   "Dean Martin",
                "filename": "Ain't That a Kick in the Head - Dean Martin.mp3",
            },
            {
                "title":    "Big Iron",
                "artist":   "Marty Robbins",
                "filename": "Big Iron - Marty Robbins.mp3",
            },
            {
                "title":    "Blue Moon",
                "artist":   "Frank Sinatra",
                "filename": "Blue Moon - Frank Sinatra.mp3",
            },
            {
                "title":    "Jingle Jangle Jingle",
                "artist":   "The Kay Kyser Orchestra",
                "filename": "Jingle Jangle Jingle - The Kay Kyser Orchestra.mp3",
            },
            {
                "title":    "Johnny Guitar",
                "artist":   "Peggy Lee",
                "filename": "Johnny Guitar - Peggy Lee.mp3",
            },
            {
                "title":    "Heartaches by the Number",
                "artist":   "Guy Mitchell",
                "filename": "Heartaches by the Number - Guy Mitchell.mp3",
            },
            {
                "title":    "Something's Gotta Give",
                "artist":   "Bing Crosby",
                "filename": "Something's Gotta Give - Bing Crosby.mp3",
            },
            {
                "title":    "Why Don't You Do Right",
                "artist":   "Peggy Lee",
                "filename": "Why Don't You Do Right - Peggy Lee.mp3",
            },
            {
                "title":    "Manhattan",
                "artist":   "Gerhard Trede",
                "filename": "Manhattan - Gerhard Trede.mp3",
            },
        ],
        "Mojave Music Radio": [
            {
                "title":    "In the Shadow of the Valley",
                "artist":   "Lost Weekend Western Swing Band",
                "filename": "In the Shadow of the Valley - Lost Weekend Western Swing Band.mp3",
            },
            {
                "title":    "Lone Star",
                "artist":   "Lost Weekend Western Swing Band",
                "filename": "Lone Star - Lost Weekend Western Swing Band.mp3",
            },
            {
                "title":    "Stars of the Midnight Range",
                "artist":   "Johnny Bond",
                "filename": "Stars of the Midnight Range - Johnny Bond.mp3",
            },
            {
                "title":    "I'm So Blue",
                "artist":   "Katie Thompson",
                "filename": "I'm So Blue - Katie Thompson.mp3",
            },
            {
                "title":    "Let's Ride Into the Sunset Together",
                "artist":   "Lost Weekend Western Swing Band",
                "filename": "Let's Ride Into the Sunset Together - Lost Weekend Western Swing Band.mp3",
            },
            {
                "title":    "Lazy Day Blues",
                "artist":   "Bert Weedon",
                "filename": "Lazy Day Blues - Bert Weedon.mp3",
            },
            {
                "title":    "Happy Times",
                "artist":   "Bert Weedon",
                "filename": "Happy Times - Bert Weedon.mp3",
            },
        ],
    },
    "Fallout 4": {
        "Diamond City Radio": [
            {
                "title":    "Atom Bomb Baby",
                "artist":   "The Five Stars",
                "filename": "Atom Bomb Baby - The Five Stars.mp3",
            },
            {
                "title":    "Crawl Out Through the Fallout",
                "artist":   "Sheldon Allman",
                "filename": "Crawl Out Through the Fallout - Sheldon Allman.mp3",
            },
            {
                "title":    "The End of the World",
                "artist":   "Skeeter Davis",
                "filename": "The End of the World - Skeeter Davis.mp3",
            },
            {
                "title":    "Uranium Fever",
                "artist":   "Elton Britt",
                "filename": "Uranium Fever - Elton Britt.mp3",
            },
            {
                "title":    "Uranium Rock",
                "artist":   "Warren Smith",
                "filename": "Uranium Rock - Warren Smith.mp3",
            },
            {
                "title":    "Sixty Minute Man",
                "artist":   "Billy Ward and His Dominoes",
                "filename": "Sixty Minute Man - Billy Ward and His Dominoes.mp3",
            },
            {
                "title":    "Right Behind You Baby",
                "artist":   "Ray Smith",
                "filename": "Right Behind You Baby - Ray Smith.mp3",
            },
            {
                "title":    "Good Rocking Tonight",
                "artist":   "Roy Brown",
                "filename": "Good Rocking Tonight - Roy Brown.mp3",
            },
            {
                "title":    "Accentuate the Positive",
                "artist":   "Bing Crosby",
                "filename": "Accentuate the Positive - Bing Crosby.mp3",
            },
            {
                "title":    "Orange Colored Sky",
                "artist":   "Stan Kenton featuring Nat King Cole",
                "filename": "Orange Colored Sky - Stan Kenton featuring Nat King Cole.mp3",
            },
            {
                "title":    "Good Neighbor",
                "artist":   "Lynda Carter",
                "filename": "Good Neighbor - Lynda Carter.mp3",
            },
        ],
    },
    "Fallout 76": {
        "Appalachia Radio": [
            {
                "title":    "Sixteen Tons",
                "artist":   "Tennessee Ernie Ford",
                "filename": "Sixteen Tons - Tennessee Ernie Ford.mp3",
            },
            {
                "title":    "Shenandoah",
                "artist":   "Tennessee Ernie Ford",
                "filename": "Shenandoah - Tennessee Ernie Ford.mp3",
            },
            {
                "title":    "Dark as a Dungeon",
                "artist":   "Tennessee Ernie Ford",
                "filename": "Dark as a Dungeon - Tennessee Ernie Ford.mp3",
            },
            {
                "title":    "Ghost Riders in the Sky",
                "artist":   "Sons of the Pioneers",
                "filename": "Ghost Riders in the Sky - Sons of the Pioneers.mp3",
            },
            {
                "title":    "Mr. Sandman",
                "artist":   "The Chordettes",
                "filename": "Mr. Sandman - The Chordettes.mp3",
            },
            {
                "title":    "Wouldn't It Be Nice",
                "artist":   "The Beach Boys",
                "filename": "Wouldn't It Be Nice - The Beach Boys.mp3",
            },
            {
                "title":    "Ain't Misbehavin'",
                "artist":   "Fats Waller",
                "filename": "Ain't Misbehavin' - Fats Waller.mp3",
            },
            {
                "title":    "Don't Fence Me In",
                "artist":   "Bing Crosby and The Andrews Sisters",
                "filename": "Don't Fence Me In - Bing Crosby and The Andrews Sisters.mp3",
            },
            {
                "title":    "Steel Guitar Rag",
                "artist":   "Bob Wills and His Texas Cowboys",
                "filename": "Steel Guitar Rag - Bob Wills and His Texas Cowboys.mp3",
            },
            {
                "title":    "Take Me Home Country Roads",
                "artist":   "Spank Live",
                "filename": "Take Me Home Country Roads - Spank Live.mp3",
            },
            {
                "title":    "Ring of Fire",
                "artist":   "Spank Live",
                "filename": "Ring of Fire - Spank Live.mp3",
            },
        ],
    },
}

# -- Playback State ------------------------------------------------------------

queues:           dict[int, deque] = {}
now_playing:      dict[int, dict]  = {}
loop_modes:       dict[int, str]   = {}
volumes:          dict[int, float] = {}
disconnect_tasks: dict[int, asyncio.Task] = {}

FFMPEG_OPTIONS = {
    'options': '-vn',
}

# -- Playback ------------------------------------------------------------------

async def play_next(guild_id: int, voice_client: discord.VoiceClient, channel: discord.abc.Messageable):
    """Pop the next song from the queue and play it from local storage."""
    loop_mode = loop_modes.get(guild_id, 'off')
    current   = now_playing.get(guild_id)

    # If looping the whole queue, re-add the finished song to the end
    if loop_mode == 'queue' and current:
        queues[guild_id].append(current)

    if guild_id not in queues or not queues[guild_id]:
        now_playing.pop(guild_id, None)
        await channel.send("Queue finished - all songs have played!")
        return

    # If looping a single song, replay it without touching the queue
    if loop_mode == 'song' and current:
        song = current
    else:
        song = queues[guild_id].popleft()

    filepath = os.path.join(SONGS_PATH, song['filename'])

    if not os.path.isfile(filepath):
        await channel.send(f"Warning: could not find file for **{song['display_title']}**, skipping...")
        await play_next(guild_id, voice_client, channel)
        return

    now_playing[guild_id] = song

    volume     = volumes.get(guild_id, 1.0)
    raw_source = discord.FFmpegPCMAudio(filepath, **FFMPEG_OPTIONS)
    source     = discord.PCMVolumeTransformer(raw_source, volume=volume)

    def after_playing(error):
        if error:
            print(f"[Player Error] {error}")
        coro = play_next(guild_id, voice_client, channel)
        asyncio.run_coroutine_threadsafe(coro, bot.loop)

    voice_client.play(source, after=after_playing)

    loop_indicator = ''
    if loop_mode == 'song':
        loop_indicator = ' (loop: song)'
    elif loop_mode == 'queue':
        loop_indicator = ' (loop: queue)'

    await channel.send(f"Now Playing: **{song['display_title']}**{loop_indicator}")

# -- Auto-disconnect -----------------------------------------------------------

async def auto_disconnect(guild_id: int, voice_client: discord.VoiceClient, channel: discord.abc.Messageable):
    """Wait 60 seconds alone in a channel then disconnect."""
    await asyncio.sleep(60)
    if voice_client.is_connected():
        queues.pop(guild_id, None)
        now_playing.pop(guild_id, None)
        loop_modes.pop(guild_id, None)
        volumes.pop(guild_id, None)
        await voice_client.disconnect()
        await channel.send("Left the voice channel - everyone left!")

# -- Shared Helpers ------------------------------------------------------------

def make_song_entry(s: dict) -> dict:
    return {
        'filename':      s['filename'],
        'display_title': f"{s['title']} - {s['artist']}",
    }


async def queue_and_play(interaction: discord.Interaction, song: dict):
    """Queue a single song and start playback if idle."""
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message(
            "You need to be in a voice channel first!", ephemeral=True
        )
        return

    voice_channel = interaction.user.voice.channel
    guild         = interaction.guild
    guild_id      = guild.id

    voice_client = guild.voice_client
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

    if guild_id not in queues:
        queues[guild_id] = deque()

    if voice_client.is_playing() or voice_client.is_paused():
        queues[guild_id].append(song)
        pos = len(queues[guild_id])
        await interaction.response.edit_message(
            content=f"Added **{song['display_title']}** to queue (position {pos})", view=None
        )
    else:
        queues[guild_id].append(song)
        await interaction.response.edit_message(content="Starting playback!", view=None)
        await play_next(guild_id, voice_client, interaction.channel)


async def queue_all_songs(interaction: discord.Interaction, game: str, station: str, shuffle: bool = False):
    """Queue every song from a station, playing immediately if idle."""
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message(
            "You need to be in a voice channel first!", ephemeral=True
        )
        return

    voice_channel = interaction.user.voice.channel
    guild         = interaction.guild
    guild_id      = guild.id

    entries = [make_song_entry(s) for s in RADIO_DATA[game][station]]

    if shuffle:
        random.shuffle(entries)

    voice_client = guild.voice_client
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

    already_playing = voice_client.is_playing() or voice_client.is_paused()

    if guild_id not in queues:
        queues[guild_id] = deque()

    for s in entries:
        queues[guild_id].append(s)

    shuffle_note = " (shuffled)" if shuffle else ""
    await interaction.response.edit_message(
        content=f"Queued all **{len(entries)}** songs from **{station}**{shuffle_note}!", view=None
    )

    if not already_playing:
        await play_next(guild_id, voice_client, interaction.channel)

# -- UI Views ------------------------------------------------------------------

class GameSelectView(discord.ui.View):
    """Step 1: Pick a Fallout game."""

    def __init__(self):
        super().__init__(timeout=120)
        options = [
            discord.SelectOption(label=game, value=game, emoji="🎮")
            for game in RADIO_DATA.keys()
        ]
        select          = discord.ui.Select(placeholder="Choose a Fallout game...", options=options)
        select.callback = self.game_selected
        self.add_item(select)

    async def game_selected(self, interaction: discord.Interaction):
        game = interaction.data['values'][0]
        await interaction.response.edit_message(
            content=f"**{game}** - Choose a radio station:",
            view=StationSelectView(game),
        )


class StationSelectView(discord.ui.View):
    """Step 2: Pick a radio station."""

    def __init__(self, game: str):
        super().__init__(timeout=120)
        self.game = game

        options = [
            discord.SelectOption(label=station, value=station, emoji="📡")
            for station in RADIO_DATA[game].keys()
        ]
        select          = discord.ui.Select(placeholder="Choose a station...", options=options)
        select.callback = self.station_selected
        self.add_item(select)

        back          = discord.ui.Button(label="Back", style=discord.ButtonStyle.secondary)
        back.callback = self.go_back
        self.add_item(back)

    async def station_selected(self, interaction: discord.Interaction):
        station = interaction.data['values'][0]
        await interaction.response.edit_message(
            content=f"**{self.game} - {station}** - Choose a song:",
            view=SongSelectView(self.game, station),
        )

    async def go_back(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content="Fallout Radio - Choose a game:",
            view=GameSelectView(),
        )


class SongSelectView(discord.ui.View):
    """Step 3: Pick a song, queue all, or queue all shuffled."""

    def __init__(self, game: str, station: str):
        super().__init__(timeout=120)
        self.game    = game
        self.station = station

        songs   = RADIO_DATA[game][station]
        options = [
            discord.SelectOption(
                label=s['title'][:100],
                description=s['artist'][:100],
                value=s['filename'][:100],
            )
            for s in songs
        ]
        select          = discord.ui.Select(placeholder="Choose a song...", options=options)
        select.callback = self.song_selected
        self.add_item(select)

        queue_all_btn          = discord.ui.Button(label="Queue All", style=discord.ButtonStyle.success)
        queue_all_btn.callback = self.queue_all
        self.add_item(queue_all_btn)

        shuffle_btn          = discord.ui.Button(label="Shuffle All", style=discord.ButtonStyle.primary)
        shuffle_btn.callback = self.queue_all_shuffled
        self.add_item(shuffle_btn)

        back          = discord.ui.Button(label="Back", style=discord.ButtonStyle.secondary)
        back.callback = self.go_back
        self.add_item(back)

    async def song_selected(self, interaction: discord.Interaction):
        filename = interaction.data['values'][0]
        songs    = RADIO_DATA[self.game][self.station]
        match    = next((s for s in songs if s['filename'] == filename), None)
        if not match:
            await interaction.response.send_message("Could not find that song.", ephemeral=True)
            return
        song = make_song_entry(match)
        await queue_and_play(interaction, song)

    async def queue_all(self, interaction: discord.Interaction):
        await queue_all_songs(interaction, self.game, self.station, shuffle=False)

    async def queue_all_shuffled(self, interaction: discord.Interaction):
        await queue_all_songs(interaction, self.game, self.station, shuffle=True)

    async def go_back(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content=f"**{self.game}** - Choose a radio station:",
            view=StationSelectView(self.game),
        )

# -- Bot Setup -----------------------------------------------------------------

intents              = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# -- Auto-disconnect on empty channel ------------------------------------------

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member.bot:
        return

    guild    = member.guild
    guild_id = guild.id
    vc       = guild.voice_client

    if vc is None or vc.channel is None:
        return

    human_members = [m for m in vc.channel.members if not m.bot]

    if len(human_members) == 0:
        if guild_id in disconnect_tasks:
            disconnect_tasks[guild_id].cancel()

        text_channel = None
        for ch in guild.text_channels:
            if ch.permissions_for(guild.me).send_messages:
                text_channel = ch
                break

        task = asyncio.create_task(auto_disconnect(guild_id, vc, text_channel))
        disconnect_tasks[guild_id] = task
    else:
        if guild_id in disconnect_tasks:
            disconnect_tasks[guild_id].cancel()
            disconnect_tasks.pop(guild_id, None)

# -- /foradio command group ----------------------------------------------------

foradio_group = app_commands.Group(name="foradio", description="Fallout Radio controls")


@foradio_group.command(name="play", description="Browse and play Fallout radio music")
async def foradio_play(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Fallout Radio - Choose a game:",
        view=GameSelectView(),
        ephemeral=True,
    )


@foradio_group.command(name="skip", description="Skip the current song")
async def foradio_skip(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and (vc.is_playing() or vc.is_paused()):
        vc.stop()
        await interaction.response.send_message("Skipped!")
    else:
        await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)


@foradio_group.command(name="pause", description="Pause the current song")
async def foradio_pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await interaction.response.send_message("Paused.")
    elif vc and vc.is_paused():
        await interaction.response.send_message("Already paused. Use /foradio resume to resume.", ephemeral=True)
    else:
        await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)


@foradio_group.command(name="resume", description="Resume the paused song")
async def foradio_resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("Resumed!")
    elif vc and vc.is_playing():
        await interaction.response.send_message("Already playing!", ephemeral=True)
    else:
        await interaction.response.send_message("Nothing is paused right now.", ephemeral=True)


@foradio_group.command(name="stop", description="Stop music, clear the queue, and disconnect")
async def foradio_stop(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    vc       = interaction.guild.voice_client
    if vc:
        queues.pop(guild_id, None)
        now_playing.pop(guild_id, None)
        loop_modes.pop(guild_id, None)
        if guild_id in disconnect_tasks:
            disconnect_tasks[guild_id].cancel()
            disconnect_tasks.pop(guild_id, None)
        vc.stop()
        await vc.disconnect()
        await interaction.response.send_message("Stopped and disconnected.")
    else:
        await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)


@foradio_group.command(name="queue", description="Show the current song queue")
async def foradio_queue(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    current  = now_playing.get(guild_id)
    q        = queues.get(guild_id, deque())

    if not current and not q:
        await interaction.response.send_message("The queue is empty.", ephemeral=True)
        return

    loop_mode = loop_modes.get(guild_id, 'off')
    loop_str  = {'off': '', 'song': ' (loop: song)', 'queue': ' (loop: queue)'}[loop_mode]

    lines = []
    if current:
        lines.append(f"Now Playing: **{current['display_title']}**{loop_str}")
    if q:
        lines.append("\n**Up Next:**")
        for i, song in enumerate(list(q), 1):
            lines.append(f"  {i}. {song['display_title']}")

    await interaction.response.send_message('\n'.join(lines), ephemeral=True)


@foradio_group.command(name="remove", description="Remove a song from the queue by its position")
@app_commands.describe(position="Position number to remove (use /foradio queue to see positions)")
async def foradio_remove(interaction: discord.Interaction, position: int):
    guild_id = interaction.guild.id
    q        = queues.get(guild_id, deque())

    if not q:
        await interaction.response.send_message("The queue is empty.", ephemeral=True)
        return

    if position < 1 or position > len(q):
        await interaction.response.send_message(
            f"Invalid position. Queue has {len(q)} song(s).", ephemeral=True
        )
        return

    q_list  = list(q)
    removed = q_list.pop(position - 1)
    queues[guild_id] = deque(q_list)
    await interaction.response.send_message(f"Removed **{removed['display_title']}** from the queue.")


@foradio_group.command(name="loop", description="Set loop mode: off, song, or queue")
@app_commands.describe(mode="off = no loop | song = repeat current song | queue = loop entire queue")
@app_commands.choices(mode=[
    app_commands.Choice(name="off",   value="off"),
    app_commands.Choice(name="song",  value="song"),
    app_commands.Choice(name="queue", value="queue"),
])
async def foradio_loop(interaction: discord.Interaction, mode: app_commands.Choice[str]):
    guild_id             = interaction.guild.id
    loop_modes[guild_id] = mode.value
    messages = {
        'off':   "Loop disabled.",
        'song':  "Now looping the current song.",
        'queue': "Now looping the entire queue.",
    }
    await interaction.response.send_message(messages[mode.value])


@foradio_group.command(name="volume", description="Set the playback volume (0-100)")
@app_commands.describe(level="Volume level from 0 to 100")
async def foradio_volume(interaction: discord.Interaction, level: int):
    if level < 0 or level > 100:
        await interaction.response.send_message("Volume must be between 0 and 100.", ephemeral=True)
        return

    guild_id          = interaction.guild.id
    volumes[guild_id] = level / 100.0

    vc = interaction.guild.voice_client
    if vc and vc.source and isinstance(vc.source, discord.PCMVolumeTransformer):
        vc.source.volume = level / 100.0

    await interaction.response.send_message(f"Volume set to **{level}%**.")


@foradio_group.command(name="nowplaying", description="Show what's currently playing")
async def foradio_nowplaying(interaction: discord.Interaction):
    guild_id  = interaction.guild.id
    current   = now_playing.get(guild_id)
    loop_mode = loop_modes.get(guild_id, 'off')
    volume    = int(volumes.get(guild_id, 1.0) * 100)

    if current:
        loop_str = {'off': '', 'song': ' | loop: song', 'queue': ' | loop: queue'}[loop_mode]
        msg = f"Now Playing: **{current['display_title']}**\nVolume: {volume}%{loop_str}"
        await interaction.response.send_message(msg, ephemeral=True)
    else:
        await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)


@foradio_group.command(name="help", description="Show all available Fallout Radio commands")
async def foradio_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Fallout Radio - Commands",
        description="All commands are available as /foradio <command>.",
        color=0xf5a623,
    )
    embed.add_field(name="Playback", value=(
        "`play` - Open the radio browser\n"
        "`skip` - Skip the current song\n"
        "`pause` - Pause playback\n"
        "`resume` - Resume playback\n"
        "`stop` - Stop and disconnect\n"
        "`volume <0-100>` - Set the volume"
    ), inline=False)
    embed.add_field(name="Queue", value=(
        "`queue` - Show the queue\n"
        "`remove <position>` - Remove a song by position\n"
        "`loop <off|song|queue>` - Set loop mode"
    ), inline=False)
    embed.add_field(name="Info", value=(
        "`nowplaying` - Show the current song\n"
        "`help` - Show this message"
    ), inline=False)
    embed.add_field(name="Tips", value=(
        "In the song browser, use **Queue All** to add a whole station,\n"
        "or **Shuffle All** to add it in random order."
    ), inline=False)
    embed.set_footer(text="War never changes. But the music is timeless.")
    await interaction.response.send_message(embed=embed, ephemeral=True)


# -- Standalone shortcut commands ----------------------------------------------

@bot.tree.command(name="falloutradio", description="Browse and play Fallout radio music")
async def falloutradio(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Fallout Radio - Choose a game:",
        view=GameSelectView(),
        ephemeral=True,
    )


@bot.tree.command(name="skip", description="Skip the current song")
async def skip(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and (vc.is_playing() or vc.is_paused()):
        vc.stop()
        await interaction.response.send_message("Skipped!")
    else:
        await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)


@bot.tree.command(name="pause", description="Pause the current song")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await interaction.response.send_message("Paused.")
    elif vc and vc.is_paused():
        await interaction.response.send_message("Already paused. Use /resume to resume.", ephemeral=True)
    else:
        await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)


@bot.tree.command(name="resume", description="Resume the paused song")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("Resumed!")
    elif vc and vc.is_playing():
        await interaction.response.send_message("Already playing!", ephemeral=True)
    else:
        await interaction.response.send_message("Nothing is paused right now.", ephemeral=True)


@bot.tree.command(name="stop", description="Stop music, clear the queue, and disconnect")
async def stop(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    vc       = interaction.guild.voice_client
    if vc:
        queues.pop(guild_id, None)
        now_playing.pop(guild_id, None)
        loop_modes.pop(guild_id, None)
        if guild_id in disconnect_tasks:
            disconnect_tasks[guild_id].cancel()
            disconnect_tasks.pop(guild_id, None)
        vc.stop()
        await vc.disconnect()
        await interaction.response.send_message("Stopped and disconnected.")
    else:
        await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)


@bot.tree.command(name="queue", description="Show the current song queue")
async def show_queue(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    current  = now_playing.get(guild_id)
    q        = queues.get(guild_id, deque())

    if not current and not q:
        await interaction.response.send_message("The queue is empty.", ephemeral=True)
        return

    loop_mode = loop_modes.get(guild_id, 'off')
    loop_str  = {'off': '', 'song': ' (loop: song)', 'queue': ' (loop: queue)'}[loop_mode]

    lines = []
    if current:
        lines.append(f"Now Playing: **{current['display_title']}**{loop_str}")
    if q:
        lines.append("\n**Up Next:**")
        for i, song in enumerate(list(q), 1):
            lines.append(f"  {i}. {song['display_title']}")

    await interaction.response.send_message('\n'.join(lines), ephemeral=True)


@bot.tree.command(name="nowplaying", description="Show what's currently playing")
async def nowplaying(interaction: discord.Interaction):
    guild_id  = interaction.guild.id
    current   = now_playing.get(guild_id)
    loop_mode = loop_modes.get(guild_id, 'off')
    volume    = int(volumes.get(guild_id, 1.0) * 100)

    if current:
        loop_str = {'off': '', 'song': ' | loop: song', 'queue': ' | loop: queue'}[loop_mode]
        msg = f"Now Playing: **{current['display_title']}**\nVolume: {volume}%{loop_str}"
        await interaction.response.send_message(msg, ephemeral=True)
    else:
        await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)


# -- on_ready ------------------------------------------------------------------

MY_GUILD = discord.Object(id=1296546881886752900)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print("Slash commands synced.")
    print("/falloutradio  |  /foradio play|pause|resume|skip|stop|queue|remove|loop|volume|nowplaying|help")


bot.tree.add_command(foradio_group)
bot.run(TOKEN)
