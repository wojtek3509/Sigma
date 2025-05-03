
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

balances = {}

def get_balance(user_id):
    return balances.get(user_id, 1000)

def set_balance(user_id, amount):
    balances[user_id] = amount

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user.name}')

@bot.command()
async def saldo(ctx):
    balance = get_balance(ctx.author.id)
    await ctx.send(f'{ctx.author.mention}, masz {balance} monet.')

@bot.command()
async def graj(ctx, amount: int):
    balance = get_balance(ctx.author.id)
    if balance < amount:
        await ctx.send(f'{ctx.author.mention}, nie masz wystarczająco dużo monet!')
        return

    result = random.choices(['wygrana', 'przegrana'], weights=[0.4, 0.6])[0]
    if result == 'wygrana':
        new_balance = balance + amount
        set_balance(ctx.author.id, new_balance)
        await ctx.send(f'{ctx.author.mention}, wygrałeś {amount} monet! Masz teraz {new_balance} monet.')
    else:
        new_balance = balance - amount
        set_balance(ctx.author.id, new_balance)
        await ctx.send(f'{ctx.author.mention}, przegrałeś {amount} monet. Masz teraz {new_balance} monet.')

@bot.command()
async def daj(ctx, member: discord.Member, amount: int):
    balance = get_balance(ctx.author.id)
    if balance < amount:
        await ctx.send(f'{ctx.author.mention}, nie masz wystarczająco dużo monet!')
        return
    set_balance(ctx.author.id, balance - amount)
    set_balance(member.id, get_balance(member.id) + amount)
    await ctx.send(f'{ctx.author.mention} dał {amount} monet {member.mention}.')

@bot.command()
async def dodaj(ctx, member: discord.Member, amount: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(f'{ctx.author.mention}, nie masz uprawnień do tej komendy!')
        return
    set_balance(member.id, get_balance(member.id) + amount)
    await ctx.send(f'{ctx.author.mention} dodał {amount} monet do {member.mention}.')

@bot.command()
async def drop(ctx):
    result = random.choices(['hug', 'nic'], weights=[0.05, 0.95])[0]
    if result == 'hug':
        await ctx.send(f'{ctx.author.mention}, dostałeś/aś hug! 🤗')
    else:
        await ctx.send(f'{ctx.author.mention}, niestety nic nie wylosowałeś/aś.')

@bot.command()
async def pomoc(ctx):
    pomoc_text = """
Dostępne komendy:
!saldo - Sprawdź swoje saldo monet.
!graj <kwota> - Zagraj na określoną kwotę (40% szans na wygraną).
!daj @ktoś <kwota> - Daj monetę innemu użytkownikowi.
!dodaj @ktoś <kwota> - Dodaj monetę (admin only).
!drop - Losuj nagrodę (5% na hug).
!nitro - Oferta N!TR0 (admin only)
!roblox - Oferta ROBLOX (admin only)
"""
    await ctx.send(pomoc_text)

# ---------- WIDOKI ----------

class NitroView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(NitroSelect())

class NitroSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="N!TR0 G!FT", emoji="🎁", value="nitro"),
            discord.SelectOption(label="SERVER B00ST", emoji="🚀", value="boost"),
        ]
        super().__init__(placeholder="Wybierz ofertę...", options=options)

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]
        if value == "nitro":
            embed = discord.Embed(title="N!TR0 OFERTA", color=discord.Color.magenta())
            embed.description = """
N!TR0 G!FT
> aktywny przez : 1 miesiąc
Cena: 25 PLN

N!TR0 BASIC G!FT
> aktywny przez : 1 miesiąc
Cena: 15 PLN
"""
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif value == "boost":
            await interaction.response.send_message("SERVER BOOST - brak dostępnych ofert na ten moment.", ephemeral=True)

class RobloxView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RobloxSelect())

class RobloxSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="GEMY/RAP PS99", emoji="💎", value="gemy"),
            discord.SelectOption(label="ROBUXY", emoji="💰", value="robux"),
            discord.SelectOption(label="BGSI", emoji="🐾", value="bgsi"),
        ]
        super().__init__(placeholder="Wybierz kategorię...", options=options)

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]
        if value == "gemy":
            embed = discord.Embed(title="GEMY/RAP PS99", color=discord.Color.green())
            embed.description = """
**GEMY/RAP PS99**
> Ilość: 1B
> Cena: 15 PLN

**TITANIC PS99**
> Cena: 150 PLN
"""
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif value == "robux":
            embed = discord.Embed(title="ROBUXY", color=discord.Color.gold())
            embed.description = """
**ROBUXY GAMEPASSEM**
> Ilość: 1000
> Cena: 30 PLN
"""
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif value == "bgsi":
            embed = discord.Embed(title="BGSI PETS", color=discord.Color.blue())
            embed.description = """
**BGSI PETS**
> Diamond Hexarium - 0.40 PLN
> King Pufferfish - 4 PLN
> Rainbow shock - 1.5 PLN
> inne pety mogą być dostępne na ticket

**SHINY BGSI PETS**
> shiny King Pufferfish - 37 PLN
> shiny Diamond Hexarium - 4 PLN
> shiny Rainbow shock - 15 PLN

**BGSI PETS SECRETS**
> Overlord - 30 PLN
> inne secrety mogą być dostępne na ticket

można negocjować ceny przy większych zakupach
"""
            await interaction.response.send_message(embed=embed, ephemeral=True)

# ---------- KOMENDY ADMINA ----------

@bot.command()
async def nitro(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(f'{ctx.author.mention}, ta komenda jest tylko dla administratorów!')
        return
    embed = discord.Embed(title="PS99 SHOP × OFERTA N1TR0", color=discord.Color.purple())
    embed.description = "> N!TR0 G!FT
SERVER B00ST"
    await ctx.send(embed=embed, view=NitroView())

@bot.command()
async def roblox(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(f'{ctx.author.mention}, ta komenda jest tylko dla administratorów!')
        return
    embed = discord.Embed(title="🛒 Pet sim 99 shop × OFERTA ROBLOX", color=discord.Color.orange())
    embed.description = "** GEMY/RAP PS99**
** ROBUXY**
** BGSI**"
    await ctx.send(embed=embed, view=RobloxView())

bot.run("MTM2MjEwODEwMDE3NzQyODU3MA.GUma9W.wSAZP44_PG-ZF6FToSeDMSYAAEePd52LENNpj8")
