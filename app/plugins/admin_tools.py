﻿import asyncio
from typing import Awaitable

from pyrogram.types import ChatPermissions, ChatPrivileges, User

from app import bot
from app.core import Message


def get_privileges(
    anon: bool = False, full: bool = False, demote: bool = False
) -> ChatPrivileges:
    if demote:
        return ChatPrivileges(
            can_manage_chat=False,
            can_manage_video_chats=False,
            can_pin_messages=False,
            can_delete_messages=False,
            can_change_info=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_promote_members=False,
            is_anonymous=False,
        )
    return ChatPrivileges(
        can_manage_chat=True,
        can_manage_video_chats=True,
        can_pin_messages=True,
        can_delete_messages=True,
        can_change_info=True,
        can_restrict_members=True,
        can_invite_users=True,
        can_promote_members=full,
        is_anonymous=anon,
    )


@bot.add_cmd(cmd=["promote", "demote"])
async def promote_or_demote(bot: bot, message: Message) -> None:
    user, title = await message.extract_user_n_reason()
    if not isinstance(user, User):
        await message.reply(user, del_in=10)
        return
    full: bool = "-f" in message.flags
    anon: bool = "-anon" in message.flags
    demote = message.cmd == "demote"
    privileges: ChatPrivileges = get_privileges(full=full, anon=anon, demote=demote)
    response = f"{message.cmd.capitalize()}d: {user.mention}"
    try:
        await bot.promote_chat_member(
            chat_id=message.chat.id, user_id=user.id, privileges=privileges
        )
        if not demote:
            # Let server promote admin before setting title
            # Bot is too fast moment 😂😂😂
            await asyncio.sleep(3)
            await bot.set_administrator_title(
                chat_id=message.chat.id, user_id=user.id, title=title or "Admin"
            )
            if title:
                response += f"\nTitle: {title}"
        await message.reply(text=response)
    except Exception as e:
        await message.reply(text=e, del_in=10, block=True)


@bot.add_cmd(cmd=["ban", "unban"])
async def ban_or_unban(bot: bot, message: Message) -> None:
    user, reason = await message.extract_user_n_reason()
    if not isinstance(user, User):
        await message.reply(user, del_in=10)
        return
    if message.cmd == "ban":
        action: Awaitable = bot.ban_chat_member(
            chat_id=message.chat.id, user_id=user.id
        )
    else:
        action: Awaitable = bot.unban_chat_member(
            chat_id=message.chat.id, user_id=user.id
        )
    try:
        await action
        await message.reply(
            text=f"{message.cmd.capitalize()}ed: {user.mention}\nReason: {reason}."
        )
    except Exception as e:
        await message.reply(text=e, del_in=10)


@bot.add_cmd(cmd=["mute", "unmute"])
async def mute_or_unmute(bot: bot, message: Message):
    user, reason = await message.extract_user_n_reason()
    if not isinstance(user, User):
        await message.reply(user, del_in=10)
        return
    perms = message.chat.permissions
    word = "Unmuted"
    if message.cmd == "mute":
        perms = ChatPermissions(
            can_send_messages=False,
            can_pin_messages=False,
            can_invite_users=False,
            can_change_info=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
        )
        word = "Muted"
    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id, user_id=user.id, permissions=perms
        )
        await message.reply(text=f"{word}: {user.mention}\nReason: {reason}.")
    except Exception as e:
        await message.reply(text=e, del_in=10)
