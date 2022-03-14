from userbot import catub
from ..core.managers import edit_or_reply
import requests

plugin_category="utils"

@catub.cat_cmd(
    pattern="tr$",
    command=("font", plugin_category),
    info={
        "header": "convert finglish to persian",
        "description": "convert fingilish to persian",
        "usage": "{tr}tr <txt>",
        "examples": "{tr}tr salam",
    },
)
async def tr(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message

        fa = requests.get(f"https://api.codebazan.ir/fintofa/?text={text}")

        fa = fa.json()
        
        if fa["ok"]:
            result = fa["result"]
            await edit_or_reply(event , result)
        else:
            await edit_or_reply(event , "متاسفانه تبدیل شکست خورد داداش🥲")

    else:
        await edit_or_reply(event , "باید رو پیام ریپلای بزنی برادر من")





 