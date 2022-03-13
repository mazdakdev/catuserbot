from userbot import catub
from ..helpers.utils import reply_id

plugin_category="fun"

@catub.cat_cmd(
    pattern="soraya$",
    command=("soraya", plugin_category),
    info={
        "header": "I'll sing a song soraya",
        "description": "to sing a soraya song",
        "usage": "{tr}soraya",
        "examples": "{tr}soraya",
    },
)
async def soraya(event):
    reply_to_id = await reply_id(event)

    await event.client.send_message(
        event.chat_id,
        "میگن اسمش ثریاست",
        reply_to=reply_to_id,
    )

    await event.client.send_message(
        event.chat_id,
        "چشماش همرنگ دریاست",
        reply_to=reply_to_id,
    )
    
    await event.client.send_message(
        event.chat_id,
        "آره اسمش ثریاست تنش برگ گل یاس",
        reply_to=reply_to_id,
    )

    await event.client.send_message(
        event.chat_id,
        "وقتی صدای پاش میاد",
        reply_to=reply_to_id,
    )


    await event.client.send_message(
        event.chat_id,
        "صدای خنده هاش میاد",
        reply_to=reply_to_id,
    )

    

    await event.client.send_message(
        event.chat_id,
        "نسیم سبزه زار میاد",
        reply_to=reply_to_id,
    )


    await event.client.send_message(
        event.chat_id,
        "بوی گل بهار میاد",
        reply_to=reply_to_id,
    )
    await event.client.send_message(
        event.chat_id,
        "وقتی که از سفر میاد",
        reply_to=reply_to_id,
    )
    await event.client.send_message(
        event.chat_id,
        "صدای زنگ در میاد",
        reply_to=reply_to_id,
    )
    await event.client.send_message(
        event.chat_id,
        "تو شب تار دل من",
        reply_to=reply_to_id,
    )
    await event.client.send_message(
        event.chat_id,
        "اون مژده ی سحر میاد",
        reply_to=reply_to_id,
    )
    