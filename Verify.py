import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ยืนยันตัวตน", style=discord.ButtonStyle.success, emoji="✅", custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_name = "Verified"
        role = discord.utils.get(interaction.guild.roles, name=role_name)

        if not role:
            await interaction.response.send_message("ไม่พบ role ที่ชื่อว่า Verified", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.response.send_message("คุณได้รับ role นี้แล้ว", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("ยืนยันตัวตนเรียบร้อยแล้ว!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"บอทออนไลน์ในชื่อ {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"ซิงค์ {len(synced)} คำสั่ง")
    except Exception as e:
        print(f"ซิงค์คำสั่งไม่สำเร็จ: {e}")

@bot.command()
async def sendverify(ctx):
    view = VerifyButton()
    await ctx.send("กดปุ่มด้านล่างเพื่อยืนยันตัวตน:", view=view)

bot.run("TOKEN")
