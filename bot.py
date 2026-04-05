import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
from datetime import datetime, timedelta, timezone

TOKEN = "MTQ5MDE4MTU5NzY1MDA5MjE4Mw.GGzdXp.ZNgrp1kxC3FusNQGwX_fNcqZs8tLQoJmsmASic"
DATA_FILE = "daily_data.json"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

DAILY_REWARDS = {
    1: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Brasa"), (73, 80, "Runa Inferior da Nevada"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    2: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Faísca"), (73, 80, "Runa Inferior da Víbora"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    3: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Investigação"), (73, 80, "Runa Inferior da Sobrevivência"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    4: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Sobrenatural"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior do Estudioso"), (73, 80, "Runa Inferior do Historiador"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    5: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Persuasão"), (73, 80, "Runa Inferior da Mentira"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    6: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Autoridade"), (73, 80, "Runa Inferior do Disfarce"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    7: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Leitura de Pessoas"), (73, 80, "Runa Inferior da Brasa"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    8: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Sobrenatural"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Nevada"), (73, 80, "Runa Inferior da Faísca"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    9: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Víbora"), (73, 80, "Runa Inferior da Investigação"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    10: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Sobrevivência"), (73, 80, "Runa Inferior do Estudioso"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    11: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior do Historiador"), (73, 80, "Runa Inferior da Persuasão"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    12: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Sobrenatural"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Mentira"), (73, 80, "Runa Inferior da Autoridade"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    13: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior do Disfarce"), (73, 80, "Runa Inferior da Leitura de Pessoas"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    14: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Brasa"), (73, 80, "Runa Inferior da Nevada"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    15: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Faísca"), (73, 80, "Runa Inferior da Víbora"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    16: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Sobrenatural"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Investigação"), (73, 80, "Runa Inferior da Sobrevivência"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    17: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior do Estudioso"), (73, 80, "Runa Inferior do Historiador"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    18: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Persuasão"), (73, 80, "Runa Inferior da Mentira"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    19: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Autoridade"), (73, 80, "Runa Inferior do Disfarce"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    20: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Sobrenatural"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Leitura de Pessoas"), (73, 80, "Runa Inferior da Brasa"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    21: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Nevada"), (73, 80, "Runa Inferior da Faísca"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    22: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Víbora"), (73, 80, "Runa Inferior da Investigação"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    23: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Sobrevivência"), (73, 80, "Runa Inferior do Estudioso"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    24: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Sobrenatural"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior do Historiador"), (73, 80, "Runa Inferior da Persuasão"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    25: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Mentira"), (73, 80, "Runa Inferior da Autoridade"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    26: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior do Disfarce"), (73, 80, "Runa Inferior da Leitura de Pessoas"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    27: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Brasa"), (73, 80, "Runa Inferior da Nevada"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    28: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Sobrenatural"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Faísca"), (73, 80, "Runa Inferior da Víbora"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
    29: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Dragão"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Investigação"), (73, 80, "Runa Inferior da Sobrevivência"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior do Escudo"), (96, 100, "Runa Inferior da Recuperação")],
    30: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Sobrenatural"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior do Estudioso"), (73, 80, "Runa Inferior do Historiador"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior da Percepção"), (96, 100, "Runa Inferior do Líder")],
    31: [(1, 20, "35 GP"), (21, 30, "Runa Inferior do Caçador"), (31, 40, "Runa Inferior do Dragão"), (41, 50, "Runa Inferior do Desarme"), (51, 64, "Potion of Healing"), (65, 72, "Runa Inferior da Persuasão"), (73, 80, "Runa Inferior da Mentira"), (81, 90, "Corvo de Prata"), (91, 95, "Runa Inferior das Sombras"), (96, 100, "Runa Inferior das Estrelas")],
}

TOTAL_DAYS = 31


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def can_claim(last_claim_str):
    if not last_claim_str:
        return True, None
    last_claim = datetime.fromisoformat(last_claim_str)
    now = datetime.now(timezone.utc)
    next_claim_time = last_claim + timedelta(days=1)
    if now >= next_claim_time:
        return True, None
    return False, next_claim_time - now


def get_current_day(user_data):
    total_claims = user_data.get("total_claims", 0)
    return (total_claims % TOTAL_DAYS) + 1


def roll_reward(day_number):
    roll = random.randint(1, 100)
    for start, end, reward in DAILY_REWARDS[day_number]:
        if start <= roll <= end:
            return roll, reward
    return roll, "Recompensa Desconhecida"


def format_remaining_time(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


@bot.event
async def on_ready():
    synced = await tree.sync()
    print(f"Bot ligado como {bot.user}")
    print(f"Comandos sincronizados: {len(synced)}")


@tree.command(name="daily", description="Recebe a tua recompensa diária.")
async def daily(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_data()
    user_data = data.get(user_id, {})

    allowed, remaining = can_claim(user_data.get("last_claim"))
    if not allowed:
        await interaction.response.send_message(
            f"⏳ Já resgataste a tua recompensa diária.\nPodes tentar novamente em **{format_remaining_time(remaining)}**.",
            ephemeral=True
        )
        return

    current_day = get_current_day(user_data)
    roll, reward = roll_reward(current_day)

    user_data["last_claim"] = datetime.now(timezone.utc).isoformat()
    user_data["total_claims"] = user_data.get("total_claims", 0) + 1
    user_data["last_reward"] = reward
    user_data["last_roll"] = roll
    user_data["last_day"] = current_day

    data[user_id] = user_data
    save_data(data)

    next_day = (current_day % TOTAL_DAYS) + 1

    embed = discord.Embed(title="🎁 Recompensa Diária", color=discord.Color.gold())
    embed.add_field(name="Jogador", value=interaction.user.mention, inline=False)
    embed.add_field(name="Dia do ciclo", value=f"Dia **{current_day}** / {TOTAL_DAYS}", inline=True)
    embed.add_field(name="Rolagem", value=f"**{roll}**", inline=True)
    embed.add_field(name="Recompensa", value=f"**{reward}**", inline=False)
    embed.add_field(name="Próximo dia", value=f"Dia **{next_day}**", inline=True)
    embed.set_footer(text="Falhar um dia não remove o teu progresso.")

    await interaction.response.send_message(embed=embed)


@tree.command(name="dailyinfo", description="Mostra o teu progresso do daily.")
async def dailyinfo(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_data()
    user_data = data.get(user_id)

    if not user_data:
        await interaction.response.send_message(
            "Ainda não resgataste nenhuma recompensa diária.",
            ephemeral=True
        )
        return

    current_day = get_current_day(user_data)

    embed = discord.Embed(title="📦 Informação do Daily", color=discord.Color.blue())
    embed.add_field(name="Total de resgates", value=str(user_data.get("total_claims", 0)), inline=False)
    embed.add_field(name="Último dia resgatado", value=str(user_data.get("last_day", "-")), inline=True)
    embed.add_field(name="Próximo dia", value=str(current_day), inline=True)
    embed.add_field(name="Última rolagem", value=str(user_data.get("last_roll", "-")), inline=True)
    embed.add_field(name="Última recompensa", value=user_data.get("last_reward", "Nenhuma"), inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="dailytable", description="Mostra a tabela de um dia específico.")
@app_commands.describe(day="Dia que queres consultar (1 a 31)")
async def dailytable(interaction: discord.Interaction, day: int):
    if day < 1 or day > TOTAL_DAYS:
        await interaction.response.send_message("Escolhe um dia entre 1 e 31.", ephemeral=True)
        return

    lines = [f"**{start:02d}-{end:02d}** → {reward}" for start, end, reward in DAILY_REWARDS[day]]
    embed = discord.Embed(
        title=f"📜 Tabela do Dia {day}",
        description="\n".join(lines),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


bot.run(TOKEN)