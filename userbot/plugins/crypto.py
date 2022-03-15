import requests

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "utils"


@catub.cat_cmd(
    pattern="fiat$",
    command=("fiat", plugin_category),
    info={
        "header": "fetch fiats price",
        "description": "fetch fiats price",
        "usage": "{tr}fiat",
        "examples": "{tr}fiat",
    },
)
async def fiat(event):
    res = requests.get("http://api.codebazan.ir/arz/?type=arz")
    res = res.json()

    for fiat in res:
        name = fiat["name"]
        price = fiat["price"]
        percent = fiat["percents"]

        if fiat["change"] == "+":
            changes = "➕"
        changes = "➖"

        caption = (
            f"نام : {name} "
            + "\n"
            + f"قیمت : {price} ریال"
            + "\n \n"
            + "------------------------------"
            + "\n"
            + f"تغییرات : {changes}"
            + "\n"
            + f"درصد : {percent} %"
        )

        await edit_or_reply(event, caption)


@catub.cat_cmd(
    pattern="gold$",
    command=("gold", plugin_category),
    info={
        "header": "fetch golds price",
        "description": "fetch golds price",
        "usage": "{tr}gold",
        "examples": "{tr}gold",
    },
)
async def gold(event):
    res = requests.get("http://api.codebazan.ir/arz/?type=tala")
    res = res.json()

    for gold in res:
        name = gold["name"]
        price = gold["price"]
        percent = gold["percents"]

        if gold["change"] == "+":
            changes = "➕"
        changes = "➖"

        caption = (
            f"نام : {name} "
            + "\n"
            + f"قیمت : {price} ریال"
            + "\n \n"
            + "------------------------------"
            + "\n"
            + f"تغییرات : {changes}"
            + "\n"
            + f"درصد : {percent} %"
        )

        await edit_or_reply(event, caption)


@catub.cat_cmd(
    pattern="crypto$",
    command=("crypto", plugin_category),
    info={
        "header": "fetch cryptos price",
        "description": "fetch cryptos price",
        "usage": "{tr}crypto",
        "examples": "{tr}crypto",
    },
)
async def gold(event):
    res = requests.get("http://api.codebazan.ir/arz/?type=tala")
    res = res.json()

    for gold in res:

        if fiat["change"] == "+":
            changes = "➕"
        changes = "➖"

        caption = (
            f'نام : {fiat["name"]} '
            + "\n"
            + f'قیمت : {fiat["price"]} ریال'
            + "\n \n"
            + "------------------------------"
            + "\n"
            + f"تغییرات : {changes}"
            + "\n"
            + f'درصد : {fiat["percent"]} %'
        )

        await edit_or_reply(event, caption)


@catub.cat_cmd(
    pattern="crypto ([\s\S]*)",
    command=("crypto", plugin_category),
    info={
        "header": "A command for fetching crypto's price",
        "description": "A command for fetching crypto's price",
        "usage": "{tr}crypto <id>;<id>;<id>",
        "examples": "{tr}crypto BTC;ETH;TRX",
    },
)
async def crypto(event):
    await reply_id(event)
    input_str = event.pattern_match.group(1)
    if ";" in input_str:
        ids = input_str.split(";").replace(",")
    else:
        await edit_or_reply(event, "هیچی ندادی که برادر")

    url = f"https://api.nomics.com/v1/currencies/ticker?key=9fb867492bcccdb687ef22fab2ef9a853b1792e5&ids={ids}&convert=USD&per-page=100"
    res = requests.get(url).json()

    for crypto in res:
        name = crypto["name"]
        price = crypto["price"]

        caption = f"Name : {name}" + "\n" + f"Price : {price}$"

        await edit_or_reply(event, caption)
