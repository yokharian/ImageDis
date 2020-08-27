# __init__.py configs
from patterns import *
from PIL import Image, ImageDraw
from PIL.ImageFont import FreeTypeFont
import datetime

DARKBG = (54, 57, 63, 255)
WHITEBG = (255, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

PROFILEPICSIZE = 128
THUMBNAILSIZE = 48

MINWIDTH = 384

FONTSIZE = 25
DEFAULTFONT = FreeTypeFont("fonts/whitneybook.otf", size=FONTSIZE-5)


def _addProfilePic(og: Image.Image, profilePic: Image.Image) -> Image.Image:
    mask = Image.new("RGBA", [PROFILEPICSIZE, PROFILEPICSIZE], (0, 0, 0, 0))
    d = ImageDraw.Draw(mask)
    d.ellipse([0, 0, PROFILEPICSIZE-1, PROFILEPICSIZE-1], fill=(0, 0, 0, 255))

    empty = Image.new("RGBA", [PROFILEPICSIZE,
                               PROFILEPICSIZE], (0, 0, 0, 0))
    empty.paste(profilePic, mask=mask)

    ORIGINDELTA = 0
    profilePic = empty.resize((THUMBNAILSIZE, THUMBNAILSIZE))

    og.paste(profilePic, box=[ORIGINDELTA, ORIGINDELTA,
                              ORIGINDELTA+THUMBNAILSIZE, ORIGINDELTA+THUMBNAILSIZE])
    return og


def _addUsername(og: Image.Image, username: str, color: str) -> Image.Image:
    d = ImageDraw.Draw(og)
    d.text((THUMBNAILSIZE+15, 0), username,
           font=DEFAULTFONT, fill=color)
    return og


def _addMsg(og: Image.Image, text: str) -> Image.Image:
    d = ImageDraw.Draw(og)
    d.multiline_text((THUMBNAILSIZE+15, THUMBNAILSIZE//2), text,
                     font=DEFAULTFONT, fill=(220, 221, 222))
    return og


def _addDate(og: Image.Image, username: str) -> Image.Image:
    d = ImageDraw.Draw(og)
    x = datetime.datetime.now()
    actualDate = "{wknd} at {hour}:{min} {ampm}".format(wknd=x.strftime(
        "%A"), min=x.strftime("%M"), hour=x.strftime("%I"), ampm=x.strftime("%p"))

    usernamePixels = (len(username)*9)
    d.text((THUMBNAILSIZE+15+usernamePixels, 7),
           actualDate, font=DEFAULTFONT.font_variant(size=12), fill=(106, 109, 113))
    return og


def _calculateCanvasSize(text: str) -> tuple():
    # TODO can be optimized with DEFAULTFONT properties
    deltaWidth = THUMBNAILSIZE+15
    width = MINWIDTH

    for paragraph in text.splitlines():
        paragraphs = (len(paragraph)*9)
        if paragraphs > width:
            width = paragraphs

    deltaHeight = THUMBNAILSIZE//2
    height = len(text.splitlines())*FONTSIZE

    return (deltaWidth+width, deltaHeight+height)


def discordMsg(picture: Image.Image, message: str, user: str, color: str = "#8e9b9b") -> Image.Image:
    """pattern for fake discord user screenshot"""
    CANVASSIZE = _calculateCanvasSize(message)
    final = Image.new("RGBA", CANVASSIZE, TRANSPARENT)
    final = _addProfilePic(final, picture)
    final = _addUsername(final, user, color)
    final = _addDate(final, user)
    final = _addMsg(final, message)

    return final


if __name__ == "__main__":
    pass
