import os, discord, logging, sys
from discord import app_commands
from discord.ext import commands

import api
import dataTypes

globals()['GrindSpots'] = []

class Garmoth(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cached_data = False
        self.logger = logging.getLogger('root')

    async def sync_tree(self):
        self.logger.info("Attempting to sync command(s).")
        try:
            cmds = await self.bot.tree.sync()
            self.logger.info("Sycned " + str(len(cmds)) + " command(s).")
        except Exception as e:
            self.logger.critical("Failed to sync command(s): "+e)

    async def load_grindspots(self):
        r = api.ApiRequest("/grind-tracker/getGrindSpots")
        await r.execute()
        data = r.response

        # error checking
        if data == "": return False

        # serialize JSON data to GrindSpot object
        mod = 0
        self.logger.info("Beginning caching Garmoth grindspots data.")
        for x in range(1, len(data)-2):
            while(True):
                try:
                    spot = data[str(x+mod)]
                    break
                except KeyError:
                    self.logger.debug("Skipping " + str(x) + "th index.")
                    x =- 1
                    mod += 1
                    continue

            gs = dataTypes.GrindSpot()
            try:
                gs.name = spot['name']
                gs.ap = spot['ap']
                gs.dp = spot['dp']
                gs.specials = spot['specials']
                gs.players = spot['players']
                gs.zone = spot['zone']
                gs.mob_type = spot['mob_type']
                globals()['GrindSpots'].append(gs)
            except KeyError:
                self.logger.warning("Failed to serialize JSON object.")
                continue

        self.cached_data = True
        self.logger.info("Finished caching Garmoth grindspots data.")

    def search_for_spot(self, spot: str):
        for s in globals()['GrindSpots']:
            if spot in s.name:
                return s
        return None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.sync_tree()
        await self.load_grindspots()

    @app_commands.command(name="list", description="list something from garmoth!")
    @app_commands.describe(search="keyword to search")
    async def spotsearch(self, interaction: discord.Interaction, search: str = ""):
        """list the available grindspots"""
        res = ""
        if (search == ""):
            for spot in globals()['GrindSpots']:
                res += spot.name + "\n"
        else:
            for spot in globals()['GrindSpots']:
                if search in spot.name:
                    res += spot.name + "\n"
        await interaction.response.send_message(res, ephemeral=True)
        return True

    @app_commands.command(name="spotinfo", description="Grindspot information lookup")
    @app_commands.describe(spot="Which grindspot?")
    async def spotinfo(self, interaction: discord.Interaction, spot: str):
        s = self.search_for_spot(spot)
        if not self.cached_data:
            await interaction.response.send_message("Please wait until Garmoth database has been cached.", ephemeral=True)
            return False
        if not s:
            await interaction.response.send_message("Spot not found!", ephemeral=True)
            return False
        embed = discord.Embed(
            title=s.name,
            description=s.desc
        )
        embed.add_field(name="Mob Type", value=s.mob_type.capitalize())
        embed.add_field(name="Zone", value=s.zone.capitalize())
        embed.add_field(name="AP", value=s.ap)
        embed.add_field(name="DP", value=s.dp)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        

async def setup(bot):
    await bot.add_cog(Garmoth(bot))