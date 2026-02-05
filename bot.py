import discord
from discord.ext import tasks
import feedparser
import os

# ====== CONFIG ======
DISCORD_TOKEN = "MTMwODQ1MzY5MTQzMDQwODIzMw.GVbpmF.7mnXiJIA1IlxdJgV5jfBW3w7d3vwoVUzZyzJeg"
CHANNEL_ID = 1419941517103075454 
RSS_URL = "https://rss.app/feeds/Rja0GFPWPIz5ZQNG.xml"
CHECK_INTERVAL = 60  # seconds
# ====================

intents = discord.Intents.default()
client = discord.Client(intents=intents)

posted_links = set()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    check_feed.start()

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_feed():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found. Check CHANNEL_ID.")
        return

    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries[:5]:
        link = entry.get("link")
        if not link or link in posted_links:
            continue

        title = entry.get("title", "New Facebook Post")
        description = entry.get("summary", "")

        embed = discord.Embed(
            title=title,
            url=link,
            description=description[:4000],
            color=0x1877F2  # Facebook blue
        )

        # Try grab image if RSS provides one
        if "media_content" in entry:
            try:
                embed.set_image(url=entry.media_content[0]["url"])
            except:
                pass
        elif "media_thumbnail" in entry:
            try:
                embed.set_image(url=entry.media_thumbnail[0]["url"])
            except:
                pass

        embed.set_footer(text="Facebook • Public Page")

        await channel.send(embed=embed)
        posted_links.add(link)

client.run(DISCORD_TOKEN)