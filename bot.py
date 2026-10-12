import asyncio
import os
import discord
from discord.ext import commands
import httpx
from fastapi import FastAPI
import uvicorn
import threading

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Después de esas líneas continúas con tus imports habituales:
from interface import ModuleInterface, validate_amazonmusic_setup

# Importar el motor de OrpheusDL
from interface import ModuleInterface, validate_amazonmusic_setup

# Servidor web FastAPI para mantener el servicio activo en Render
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Amazon Music Discord Bot is active!"}

def run_web():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Configuración del Bot de Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user.name}")

async def upload_to_pixeldrain(file_path: str, filename: str) -> str:
    url = f"https://pixeldrain.com/api/file/{filename}"
    async with httpx.AsyncClient(timeout=180.0) as client:
        with open(file_path, "rb") as f:
            response = await client.put(url, content=f)
        if response.status_code == 201:
            data = response.json()
            return f"https://pixeldrain.com/u/{data.get('id')}"
        else:
            raise RuntimeError(f"Pixeldrain error: {response.text}")

def create_progress_embed(title: str, status_text: str, progress_bar: str, state: str = "processing"):
    # Color lateral personalizado (Azul/Índigo para proceso, Verde esmeralda para completado)
    color = discord.Color.from_rgb(99, 102, 241) if state == "processing" else discord.Color.from_rgb(34, 197, 94)
    embed = discord.Embed(
        title=f"🎧 {title}",
        description=f"{'🔄' if state == 'processing' else '✅'} **{status_text}**\n`{progress_bar}`",
        color=color
    )
    embed.set_footer(text="live updates • secure streaming")
    return embed

class QualitySelectView(discord.ui.View):
    def __init__(self, amazon_url: str):
        super().__init__(timeout=180)
        self.amazon_url = amazon_url

    @discord.ui.select(
        placeholder="Select Audio Quality & Format...",
        options=[
            discord.SelectOption(label="Ultra HD Lossless (UHD)", value="UHD"),
            discord.SelectOption(label="High Definition FLAC (HD)", value="HD"),
            discord.SelectOption(label="Dolby Atmos (Spatial)", value="SPATIAL_ATMOS"),
            discord.SelectOption(label="3D MPEG-H Audio (360RA)", value="SPATIAL_RA360"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        quality_choice = select.values[0]

        # 1. Estado inicial: Conectando (30%)
        initial_embed = create_progress_embed("Amazon Music Download", "Connecting to Amazon Music API...", "███▒▒▒▒▒▒▒ 30%", state="processing")
        await interaction.response.edit_message(embed=initial_embed, view=None)

        try:
            settings = {
                "wvd_path": "device.wvd",
                "country": os.environ.get("AMAZON_COUNTRY", "US"),
                "email": os.environ.get("AMAZON_EMAIL", ""),
                "password": os.environ.get("AMAZON_PASSWORD", ""),
            }
            validate_amazonmusic_setup(settings, "session_storage.bin", gui_mode=False)

            # 2. Estado intermedio: Descifrando DRM y procesando con FFmpeg (70%)
            await asyncio.sleep(1) # Simulación de progreso de paso
            mid_embed = create_progress_embed("Amazon Music Download", "Decrypting Widevine DRM & Remuxing...", "███████▒▒▒ 70%", state="processing")
            await interaction.edit_original_response(embed=mid_embed)

            # Aquí ejecutarías tu lógica de descarga real utilizando custom_url_parse y get_track_download de interface.py[cite: 6]
            # file_path = ...
            # pixeldrain_link = await upload_to_pixeldrain(file_path, "output.flac")
            
            pixeldrain_link = "https://pixeldrain.com/u/example" # Enlace de prueba

            # 3. Estado Final: Completado (100%)
            final_embed = create_progress_embed("Amazon Music Download", "Download Complete! Uploaded successfully 📦", "██████████ 100%", state="complete")
            
            # Botón interactivo con el enlace directo a Pixeldrain
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Download from Pixeldrain", url=pixeldrain_link, style=discord.ButtonStyle.link))

            await interaction.edit_original_response(embed=final_embed, view=view)

        except Exception as e:
            error_embed = discord.Embed(title="❌ Error", description=f"Failed to process download:\n`{str(e)}`", color=discord.Color.from_rgb(239, 68, 68))
            await interaction.edit_original_response(embed=error_embed, view=None)

@bot.command(name="amazon")
async def amazon_download(ctx, url: str):
    view = QualitySelectView(url)
    await ctx.send("🎵 **Amazon Music Web Downloader**\nSelect your desired audio format and quality below:", view=view)

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    bot.run(os.environ.get("DISCORD_TOKEN"))
