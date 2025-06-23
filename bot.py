import discord
from discord.ext import commands
from config import token
import re
import random  # Dedikodu için rastgele cümle

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

dedikodular = [
    "Zaten çok tuhaf davranıyordu...",
    "Kimse onu gerçekten sevmezdi zaten.",
    "Bence bu ban geç bile kaldı.",
    "Sürekli link atıyordu, cık cık...",
    "Sunucu huzur buldu be!",
    "Geçen gün de garip garip konuşuyordu...",
    "Artık rahat uyuyabiliriz.",
]

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanıcı {member.name} banlandı.")
            await ctx.send(random.choice(dedikodular))  # Dedikodu mesajı
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı etiketlemelidir. Örnek: `?ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    link_pattern = r"https?://\S+"
    if re.search(link_pattern, message.content):
        try:
            await message.author.ban(reason="Mesajda link paylaştığı için otomatik banlandı.")
            await message.channel.send(f"{message.author.mention} link paylaştığı için banlandı.")
            await message.channel.send(random.choice(dedikodular))  # Dedikodu burada da!
        except discord.Forbidden:
            await message.channel.send("Bu kullanıcıyı banlamak için yetkim yok.")
        return

    await bot.process_commands(message)

bot.run(token)