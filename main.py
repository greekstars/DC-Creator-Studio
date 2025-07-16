from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Full bundle codes with proper spacing and real commands
bundles = {
    "moderation": {
        "code": '''
# ========== Moderation Commands ==========

@tree.command(name="kick", description="Kick a user")
async def kick_command(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("You lack kick permissions.", ephemeral=True)
        return
    await user.kick(reason=reason)
    await interaction.response.send_message(f"Kicked {user} for: {reason}")


@tree.command(name="ban", description="Ban a user")
async def ban_command(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("You lack ban permissions.", ephemeral=True)
        return
    await user.ban(reason=reason)
    await interaction.response.send_message(f"Banned {user} for: {reason}")


@tree.command(name="mute", description="Mute a user for 10 minutes")
async def mute_command(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("You lack mute permissions.", ephemeral=True)
        return
    from datetime import datetime, timedelta
    until = datetime.utcnow() + timedelta(minutes=10)
    await user.edit(timed_out_until=until)
    await interaction.response.send_message(f"Muted {user} for 10 minutes.")


@tree.command(name="unmute", description="Unmute a user")
async def unmute_command(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("You lack mute permissions.", ephemeral=True)
        return
    await user.edit(timed_out_until=None)
    await interaction.response.send_message(f"Unmuted {user}.")


@tree.command(name="unban", description="Unban a user by ID")
async def unban_command(interaction: discord.Interaction, user_id: int):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("You lack ban permissions.", ephemeral=True)
        return
    user = await client.fetch_user(user_id)
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"Unbanned {user}.")


@tree.command(name="warn", description="Warn a user")
async def warn_command(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("You lack permissions to warn.", ephemeral=True)
        return
    await interaction.response.send_message(f"Warned {user}: {reason}")


@tree.command(name="purge", description="Purge specified amount of messages")
async def purge_command(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("You lack manage messages permissions.", ephemeral=True)
        return
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"Purged {amount} messages.", ephemeral=True)
''',
        "requirements": ["discord.py>=2.0.0"]
    },

    "basic": {
        "code": '''
# ========== Basic Utility Commands ==========

import psutil
import time

start_time = time.time()

@tree.command(name="uptime", description="Shows bot uptime")
async def uptime_command(interaction: discord.Interaction):
    uptime = time.time() - start_time
    await interaction.response.send_message(f"Uptime: {uptime:.2f} seconds")


@tree.command(name="ram", description="Shows RAM usage")
async def ram_command(interaction: discord.Interaction):
    mem = psutil.virtual_memory()
    await interaction.response.send_message(f"RAM Usage: {mem.percent}%")


@tree.command(name="guilds", description="Shows total guilds")
async def guilds_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Total guilds: {len(client.guilds)}")


@tree.command(name="members", description="Shows total members in each guild")
async def members_command(interaction: discord.Interaction):
    counts = [f"{g.name}: {g.member_count}" for g in client.guilds]
    await interaction.response.send_message("\\n".join(counts))


@tree.command(name="avatar", description="Get someone's avatar")
async def avatar_command(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(user.avatar.url if user.avatar else "No avatar.")


@tree.command(name="banner", description="Get someone's banner")
async def banner_command(interaction: discord.Interaction, user: discord.User):
    u = await client.fetch_user(user.id)
    await interaction.response.send_message(u.banner.url if u.banner else "No banner.")


@tree.command(name="hello", description="Hello world test command")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, world!")


@tree.command(name="botinfo", description="Shows bot info")
async def botinfo_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"I am {client.user}. Latency: {round(client.latency * 1000)}ms")
''',
        "requirements": ["discord.py>=2.0.0", "psutil"]
    },

    "advanced1": {
        "code": '''
# ========== Advanced Bundle 1 ==========

@tree.command(name="purgeall", description="Purges ALL messages in the channel (Admin only)")
async def purgeall_command(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You lack administrator permissions.", ephemeral=True)
        return
    await interaction.channel.purge()
    await interaction.response.send_message("Purged all messages.", ephemeral=True)


@tree.command(name="quarantine", description="Quarantine a user to only one channel")
async def quarantine_command(interaction: discord.Interaction, user: discord.Member, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You lack administrator permissions.", ephemeral=True)
        return
    overwrite = discord.PermissionOverwrite()
    overwrite.read_messages = False
    for c in interaction.guild.channels:
        await c.set_permissions(user, overwrite=overwrite)
    overwrite.read_messages = True
    await channel.set_permissions(user, overwrite=overwrite)
    await interaction.response.send_message(f"Quarantined {user} to {channel}.")
''',
        "requirements": ["discord.py>=2.0.0"]
    },

    "developer": {
        "code": '''
# ========== Developer Bundle ==========

@tree.command(name="debug", description="Runs debug test")
async def debug_command(interaction: discord.Interaction):
    await interaction.response.send_message("Debug successful.")


# Editable commands and webhook tools would require persistent storage and are not implemented in this demo.
''',
        "requirements": ["discord.py>=2.0.0"]
    },

    "advanced2": {
        "code": '''
# ========== Advanced Bundle 2 ==========

@tree.command(name="logtest", description="Test logging functionality")
async def logtest_command(interaction: discord.Interaction):
    await interaction.response.send_message("Logging is active (stub).")
''',
        "requirements": ["discord.py>=2.0.0"]
    }
}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    token = request.form.get("token", "").strip()
    selected = request.form.getlist("bundles")

    if not token:
        return "<h3>Error: Token is required.</h3><a href='/'>Back</a>"

    bot_code = '''import discord
from discord import app_commands

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

'''

    requirements = set(["discord.py>=2.0.0"])

    # Add selected bundles with two new lines spacing
    for b in selected:
        bundle = bundles.get(b)
        if bundle:
            bot_code += bundle["code"].strip() + "\n\n"
            requirements.update(bundle["requirements"])

    # Add on_ready event and run
    bot_code += f'''
@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {{client.user}} (ID: {{client.user.id}})")

client.run("{token}")
'''

    # Save generated files in 'static' folder
    os.makedirs("static", exist_ok=True)
    bot_path = os.path.join("static", "generated_bot.py")
    req_path = os.path.join("static", "requirements.txt")

    with open(bot_path, "w", encoding="utf-8") as f:
        f.write(bot_code)

    with open(req_path, "w") as f:
        f.write("\n".join(sorted(requirements)))

    return f'''
    <h2>Files Generated:</h2>
    <a href="/static/generated_bot.py" download>Download generated_bot.py</a><br>
    <a href="/static/requirements.txt" download>Download requirements.txt</a><br><br>
    <a href="/">Go back</a>
    '''


if __name__ == "__main__":
    # Listen on all interfaces on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
