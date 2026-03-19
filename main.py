import asyncio
from config import BOT_TOKEN, CHANNELS

from aiogram import Bot, Dispatcher, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.enums import ChatMemberStatus


router = Router()


# 🔍 Проверка подписки
async def is_subscribed(user_id, bot: Bot):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR
            ]:
                return False
        except:
            return False  # если бот не может проверить канал
    return True


# 📌 Кнопки
def sub_keyboard():
    buttons = []
    for ch in CHANNELS:
        buttons.append(
            [InlineKeyboardButton(text=f"Подписаться {ch}", url=f"https://t.me/{ch[1:]}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)



@router.message()
async def check(message: Message):
    if message.from_user.is_bot:
        return

    ok = await is_subscribed(message.from_user.id, message.bot)

    if not ok:
        try:
            await message.delete()
        except:
            pass

        try:
            user = message.from_user
            username = f"@{user.username}" if user.username else ""
            await message.answer(
                f"❌ {user.first_name} {username}, подпишитесь на каналы чтобы писать в чат!",
                reply_markup=sub_keyboard()
            )
        except:
            pass

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    print("Бот запущен!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")