from http import client
from re import I
from userbot import catub
from ..core.managers import edit_or_reply
from googletrans import Translator
import requests

plugin_category="fun"

@catub.cat_cmd(
    pattern="tarot ([\s\S]*)",
    command=("tarot", plugin_category),
    info={
        "header": "A command for getting random tarot names",
        "description": "get n tarot names",
        "usage": "{tr}tarot <number>",
        "examples": "{tr}tarot 4",
    },
)
async def tarot(event):
    translator = Translator()
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ")
    n = int(cat[0])

    await edit_or_reply(event,f"در حال گرفتن {n} تا تاروت هستم")

    res = requests.get(f"https://rws-cards-api.herokuapp.com/api/v1/cards/random?n={n}")

    res = res.json()
    
    cards = res["cards"]

    for card in cards:
        sname = card["name_short"]
        type = card["type"]
        name = card["name"]
        meaning_up = str(card['meaning_up']).split(",")[:4]
        meaning_rev = str(card['meaning_rev']).split(",")[:4]
        
        
        img = f'https://www.sacred-texts.com/tarot/pkt/img/{sname}.jpg'

        if type == "major":
            p_type = "کبیر"
        else:
            p_type = "صغیر"

        tname = translator.translate(str(name) , dest='fa').text

        fmeaning_up = []
        fmeaning_rev = []

        for i in meaning_up:
            fmeaning_up.append(translator.translate(str(i) , dest='fa').text)

        for i in meaning_rev:
            fmeaning_rev.append(translator.translate(str(i) , dest='fa').text)
        caption = f"نام : {name} | {tname} " + "\n" + f"نوع : {p_type}" + "\n \n" + "------------------------------"+"\n"+ "معنای معمولی :" + ','.join([str(elem) for elem in fmeaning_up]) + "\n" + "\n" + "معنای برعکس : "+','.join([str(elem) for elem in fmeaning_rev])

        await event.client.send_file(event.chat_id, img , caption=caption , parse_mode="HTML")



 