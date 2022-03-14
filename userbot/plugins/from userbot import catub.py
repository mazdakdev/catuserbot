import requests

from userbot import catub

from ..core.managers import edit_or_reply

plugin_category = "utils"


@catub.cat_cmd(
    pattern="pasgen ([\s\S]*)",
    command=("font", plugin_category),
    info={
        "header": "create password",
        "description": "create password",
        "usage": "{tr}pasgen <length>",
        "examples": "{tr}pasgen 8",
    },
)
async def psgen(event):
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ")
    n = int(cat[0])

    url = f"http://api.codebazan.ir/password/?length={n}"

    res = requests.get(url)

    await edit_or_reply(event, res.content)
