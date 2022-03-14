from http import client
from userbot import catub
from ..core.managers import edit_or_reply
import requests

plugin_category="utils"

@catub.cat_cmd(
    pattern="font ([\s\S]*)",
    command=("font", plugin_category),
    info={
        "header": "A command for getting fonts ",
        "description": "get fonts",
        "usage": "{tr}tarot <text>",
        "examples": "{tr}font mazdak",
    },
)
async def font(event):
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ")
    txt = str(cat[0])
    await edit_or_reply(event , "حله داش")
    res = requests.get(f"https://api.codebazan.ir/font/?type=en&text={txt}")

    res = res.json()
    
    if res['ok'] != True:
        await edit_or_reply(event , "خطایی رخ داد داشم")

    fonts = str(res["result"]).replace("," , "\n")
    
    await event.client.send_message(
        event.chat_id,
        fonts,
        parse_mode="HTML"
    )







 