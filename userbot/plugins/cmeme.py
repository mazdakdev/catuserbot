from http import client
from userbot import catub
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
import requests

plugin_category="fun"

@catub.cat_cmd(
    pattern="cmeme ([\s\S]*)",
    command=("cmeme", plugin_category),
    info={
        "header": "A command for creating meme's",
        "description": "create meme based on given details with imgflip",
        "usage": "{tr}cmeme <meme_id>;<text0>;<text1>",
        "examples": "{tr}cmeme 181913649;boys;girls",
    },
)
async def cmeme(event):
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    if ";" in input_str:
        idd , txt0 , txt1 = input_str.split(";")
    else :
        await edit_or_reply(event,"هیچی ندادی که برادر")
        



    await edit_or_reply(event," در حال ساخت میمت هستم میتونی صبر کنی برادر")

    res = requests.post("https://api.imgflip.com/caption_image" , data={
        "template_id" : idd,
        "username" : "MazdakPakaghideh",
        "password" : "m13851385",
        "text0" : txt0,
        "text1" : txt1,
        "font":"arial"
    })

    res = res.json()

    if res["success"] != True:
        await event.client.send_message(
            event.chat_id,
            "متاسفانه ساخت میمت با خطا مواجه شد برادر ",
            reply_to=reply_to_id,
        )
        await event.client.send_message(
            event.chat_id,
            res["error_message"],
            reply_to=reply_to_id,
        )

    pic = res["data"]["url"]

    await event.client.send_file(event.chat_id, pic)
