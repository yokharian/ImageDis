import random
import io
from PIL import Image
import requests
import sys
import patterns
import discord
from discord.ext import commands
from utils import permissions, default, http, dataIO

# Cog Beta-Release


class ImageDis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    def _downloadExternalImg(self, url: str) -> Image.Image:
        response: requests.Response = requests.get(url)
        im = Image.open(io.BytesIO(response.content))
        return im

    def _serve_pil_image(self, pil_img):
        img_io = io.BytesIO()
        pil_img.save(img_io, 'PNG')
        img_io.seek(0)
        # return img_io

    @commands.command()
    @commands.check(permissions.is_owner)
    # @commands.guild_only()
    async def discordMsgApi(self, ctx):
        conditionals = 'picture user message'.split(" ")

        hasAllConditionals = all(
            list(map(lambda x: x in request.json, conditionals)))

        if not request.json or not hasAllConditionals:
            abort(400)

        imageFile = _downloadExternalImg(request.json['picture'])

        task = {
            'picture': imageFile,
            'message': request.json.get('message', 'lorem ipsum dolor'),
            'user': request.json['user'],
            'color': request.json.get('color', "#8e9b9b")
        }
        patternAppliedImg = patterns.discordMsg(**task)

        # return _serve_pil_image(patternAppliedImg)
        # TODO Get a way to server pil images in discord chat
        await ctx.send("error 404")

    @commands.command()
    @commands.check(permissions.is_owner)
    @commands.guild_only()
    async def getrandomuser(self, ctx):
        await ctx.send("getting all users -->")


def setup(bot):
    bot.add_cog(ImageDis(bot))
