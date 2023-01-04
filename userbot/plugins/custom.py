from telegraph import upload_file
from telethon.tl.functions.users import GetFullUserRequest
from urlextract import URLExtract
from validators.url import url

from userbot import BOTLOG_CHATID, catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "tools"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER

extractor = URLExtract()
vlist = [
    "ALIVE_PIC",
    "ALIVE_EMOJI",
    "ALIVE_TEMPLATE",
    "ALIVE_TEXT",
    "ALLOW_NSFW",
    "CHANGE_TIME",
    "DEFAULT_BIO",
    "DEFAULT_NAME",
    "DEFAULT_PIC",
    "DEFAULT_USER",
    "DIGITAL_PIC",
    "FIRST_NAME",
    "HELP_EMOJI",
    "HELP_TEXT",
    "IALIVE_PIC",
    "LAST_NAME",
    "PING_PIC",
    "PING_TEMPLATE",
    "PM_PIC",
    "PM_TEXT",
    "PM_BLOCK",
    "MAX_FLOOD_IN_PMS",
    "START_TEXT",
    "BOT_START_PIC",
    "NO_OF_ROWS_IN_HELP",
    "NO_OF_COLUMNS_IN_HELP",
    "CUSTOM_STICKER_PACKNAME",
]

oldvars = {
    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}


@catub.cat_cmd(
    pattern="(set|get|del)dv(?: |$)([\s\S]*)",
    command=("dv", plugin_category),
    info={
        "header": "Set vars in database or Check or Delete",
        "description": "Set , Fetch or Delete values or vars directly in database without restart or heroku vars.\n\nYou can set multiple pics by giving space after links in alive, ialive, pm permit.",
        "flags": {
            "set": "To set new var in database or modify the old var",
            "get": "To show the already existing var value.",
            "del": "To delete the existing value",
        },
        "var name": "**[list of vars]**(https://catuserbot.gitbook.io/catuserbot/data-vars-setup)",
        "usage": [
            "{tr}setdv <var name> <var value>",
            "{tr}getdv <var name>",
            "{tr}deldv <var name>",
        ],
        "examples": [
            "{tr}setdv ALIVE_PIC <pic link>",
            "{tr}setdv ALIVE_PIC <pic link 1> <pic link 2>",
            "{tr}getdv ALIVE_PIC",
            "{tr}deldv ALIVE_PIC",
        ],
    },
)
async def bad(event):  # sourcery no-metrics  # sourcery skip: low-code-quality
    "To manage vars in database"
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    if not vname:
        return await edit_delete(
            event, f"**📑 Give correct var name from the list :\n\n**{vnlist}", time=60
        )
    vinfo = None
    if " " in vname:
        vname, vinfo = vname.split(" ", 1)
    reply = await event.get_reply_message()
    if not vinfo and reply:
        vinfo = reply.text
    if vname in vlist:
        if vname in oldvars:
            vname = oldvars[vname]
        if cmd == "set":
            if vname == "DEFAULT_USER":
                if not vinfo or vinfo != "Me":
                    return await edit_delete(
                        event,
                        "**To save your Current Profile info Set the value:**\\n `.setdv DEFAULT_USER Me`",
                    )

                USERINFO = await catub.get_entity(catub.uid)
                FULL_USERINFO = (await catub(GetFullUserRequest(catub.uid))).full_user
                addgvar("FIRST_NAME", USERINFO.first_name)
                addgvar("DEFAULT_NAME", USERINFO.first_name)
                if USERINFO.last_name:
                    addgvar(
                        "DEFAULT_NAME",
                        f"{USERINFO.first_name}  {USERINFO.first_name}",
                    )
                    addgvar("LAST_NAME", USERINFO.last_name)
                elif gvarstatus("LAST_NAME"):
                    delgvar("LAST_NAME")
                if FULL_USERINFO.about:
                    addgvar("DEFAULT_BIO", FULL_USERINFO.about)
                elif gvarstatus("DEFAULT_BIO"):
                    delgvar("DEFAULT_BIO")
                try:
                    photos = await catub.get_profile_photos(catub.uid)
                    myphoto = await catub.download_media(photos[0])
                    myphoto_urls = upload_file(myphoto)
                    addgvar("DEFAULT_PIC", f"https://graph.org{myphoto_urls[0]}")
                except IndexError:
                    if gvarstatus("DEFAULT_PIC"):
                        delgvar("DEFAULT_PIC")
                usrln = gvarstatus("LAST_NAME") or None
                usrbio = gvarstatus("DEFAULT_BIO") or None
                usrphoto = gvarstatus("DEFAULT_PIC") or None
                vinfo = f'**Name:** `{gvarstatus("DEFAULT_NAME")}`\n**First Name:** `{gvarstatus("FIRST_NAME")}`\n**Last Name:** `{usrln}`\n**Bio:** `{usrbio}`\n**Photo:** `{usrphoto}`'
            else:
                if not vinfo and vname in ["ALIVE_TEMPLATE", "PING_TEMPLATE"]:
                    return await edit_delete(event, "Check @cat_alive")
                if not vinfo:
                    return await edit_delete(
                        event,
                        f"Give some values which you want to save for **{vname}**",
                    )
                check = vinfo.split(" ")
                for i in check:
                    if vname == "DEFAULT_PIC" and not url(i):
                        return await edit_delete(event, "**Give me a correct link...**")
                    elif vname == "DIGITAL_PIC" and not url(i):
                        return await edit_delete(event, "**Give me a correct link...**")
                    elif (("PIC" in vname) or ("pic" in vname)) and not url(i):
                        return await edit_delete(event, "**Give me a correct link...**")
                    elif vname in [
                        "DIGITAL_PIC",
                        "DEFAULT_PIC",
                        "BOT_START_PIC",
                    ] and url(i):
                        vinfo = i
                        break
                    elif "PIC" not in vname:
                        break
                if vname == "DEFAULT_BIO" and len(vinfo) > 70:
                    return await edit_or_reply(
                        event,
                        f"No of characters in your bio must not exceed 70 so compress it and set again\n`{vinfo}`",
                    )
                addgvar(vname, vinfo)
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#SET_DATAVAR\
                    \n**{vname}** is updated newly in database as below",
                )
                await event.client.send_message(BOTLOG_CHATID, vinfo, silent=True)
            await edit_delete(
                event, f"📑 Value of **{vname}** is changed to :- `{vinfo}`", time=20
            )
        if cmd == "get":
            var_data = gvarstatus(vname)
            await edit_delete(
                event, f"📑 Value of **{vname}** is  ```{var_data}```", time=20
            )
        elif cmd == "del":
            if vname == "DEFAULT_USER":
                delgvar("FIRST_NAME")
                delgvar("DEFAULT_NAME")
                if gvarstatus("LAST_NAME"):
                    delgvar("LAST_NAME")
                if gvarstatus("DEFAULT_BIO"):
                    delgvar("DEFAULT_BIO")
                if gvarstatus("DEFAULT_PIC"):
                    delgvar("DEFAULT_PIC")
            delgvar(vname)
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#DEL_DATAVAR\
                    \n**{vname}** is deleted from database",
                )
            await edit_delete(
                event,
                f"📑 Value of **{vname}** is now deleted & set to default.",
                time=20,
            )
    else:
        await edit_delete(
            event, f"**📑 Give correct var name from the list :\n\n**{vnlist}", time=60
        )


@catub.cat_cmd(
    pattern="custom (pmpermit|pmpic|pmblock|startmsg)$",
    command=("custom", plugin_category),
    info={
        "header": "To customize your CatUserbot.",
        "options": {
            "pmpermit": "To customize pmpermit text. ",
            "pmblock": "To customize pmpermit block message.",
            "startmsg": "To customize startmsg of bot when some one started it.",
            "pmpic": "To customize pmpermit pic. Reply to media url or text containing media.",
        },
        "custom": {
            "{mention}": "mention user",
            "{first}": "first name of user",
            "{last}": "last name of user",
            "{fullname}": "fullname of user",
            "{username}": "username of user",
            "{userid}": "userid of user",
            "{my_first}": "your first name",
            "{my_last}": "your last name ",
            "{my_fullname}": "your fullname",
            "{my_username}": "your username",
            "{my_mention}": "your mention",
            "{totalwarns}": "totalwarns",
            "{warns}": "warns",
            "{remwarns}": "remaining warns",
        },
        "usage": [
            "{tr}custom <option> reply",
        ],
        "NOTE": "You can set,fetch or delete these by `{tr}setdv` , `{tr}getdv` & `{tr}deldv` as well.",
    },
)
async def custom_catuserbot(event):
    "To customize your CatUserbot."
    reply = await event.get_reply_message()
    text = None
    if reply:
        text = reply.text
    if text is None:
        return await edit_delete(event, "__Reply to custom text or url__")
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        addgvar("pmpermit_txt", text)
    if input_str == "pmblock":
        addgvar("pmblock", text)
    if input_str == "startmsg":
        addgvar("START_TEXT", text)
    if input_str == "pmpic":
        urls = extractor.find_urls(reply.text)
        if not urls:
            return await edit_delete(event, "`the given link is not supported`", 5)
        text = " ".join(urls)
        addgvar("pmpermit_pic", text)
    await edit_or_reply(event, f"__Your custom {input_str} has been updated__")
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#SET_DATAVAR\
                    \n**{input_str}** is updated newly in database as below",
        )
        await event.client.send_message(BOTLOG_CHATID, text, silent=True)


@catub.cat_cmd(
    pattern="delcustom (pmpermit|pmpic|pmblock|startmsg)$",
    command=("delcustom", plugin_category),
    info={
        "header": "To delete costomization of your CatUserbot.",
        "options": {
            "pmpermit": "To delete custom pmpermit text",
            "pmblock": "To delete custom pmpermit block message",
            "pmpic": "To delete custom pmpermit pic.",
            "startmsg": "To delete custom start message of bot when some one started it.",
        },
        "usage": [
            "{tr}delcustom <option>",
        ],
        "NOTE": "You can set,fetch or delete these by `{tr}setdv` , `{tr}getdv` & `{tr}deldv` as well.",
    },
)
async def custom_catuserbot(event):
    "To delete costomization of your CatUserbot."
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        if gvarstatus("pmpermit_txt") is None:
            return await edit_delete(event, "__You haven't customzied your pmpermit.__")
        delgvar("pmpermit_txt")
    if input_str == "pmblock":
        if gvarstatus("pmblock") is None:
            return await edit_delete(event, "__You haven't customzied your pmblock.__")
        delgvar("pmblock")
    if input_str == "pmpic":
        if gvarstatus("pmpermit_pic") is None:
            return await edit_delete(event, "__You haven't customzied your pmpic.__")
        delgvar("pmpermit_pic")
    if input_str == "startmsg":
        if gvarstatus("START_TEXT") is None:
            return await edit_delete(
                event, "__You haven't customzied your start msg in bot.__"
            )
        delgvar("START_TEXT")
    await edit_or_reply(
        event, f"__successfully deleted your customization of {input_str}.__"
    )
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#DEL_DATAVAR\
                    \n**{input_str}** is deleted from database",
        )
