from userbot import catub
from ..helpers.utils import reply_id
import random

plugin_category = "fun"

@catub.cat_cmd(
    pattern="fal$",
    command=("fal", plugin_category),
    info={
        "header": "get a fall",
        "description": "get a fall",
        "usage": "{tr}fal",
        "examples": "{tr}fal",
    },
)
async def fal(event):
    reply_to_id = await reply_id(event)

    fal_number = random.randrange(1,150)
    url = f"http://api.codebazan.ir/fal/hafez/{fal_number}.gif"

    await event.client.send_file(
        event.chat_id,
        url,
        caption="بیا اینم فالت داداش 🔥"
    )
