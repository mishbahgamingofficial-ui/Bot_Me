"""
Telegram Partner UID Verification Bot + Mini App Setup
Requires: pip install python-telegram-bot==21.6
"""

import os
from telegram import (
    Update,
    WebAppInfo,
    MenuButtonWebApp,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuration (Replace via environment variables or directly for local testing)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://your-hosted-miniapp.vercel.app")
PARTNER_REG_LINK = os.getenv("PARTNER_REG_LINK", "https://partner-platform.com/register?ref=VIP2026")
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "123456789"))


async def post_init(application: Application) -> None:
    """
    Sets the persistent 'Open' button on the left side of the Telegram message input bar.
    """
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Open",
            web_app=WebAppInfo(url=MINI_APP_URL),
        )
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends the official registration link first, and directs the user to submit their UID
    via the Mini App ('Open' button on the left side of the chat input bar).
    """
    user = update.effective_user
    is_admin = user and user.id == ADMIN_TELEGRAM_ID

    keyboard = [
        [InlineKeyboardButton("🔗 Step 1: Register on Official Link", url=PARTNER_REG_LINK)],
        [
            InlineKeyboardButton(
                "🚀 Step 2: Open Portal & Submit UID",
                web_app=WebAppInfo(url=MINI_APP_URL),
            )
        ],
    ]

    role_note = "\n\n🛡️ *Admin Mode Active:* Aap Mini App ke andar Admin Panel tab se sabhi UIDs approve/reject kar sakte hain." if is_admin else ""

    welcome_text = (
        "✨ *Welcome to the Official Partner Verification Portal*\n\n"
        "1️⃣ Sabse pehle niche diye gaye official link se apna account register karein:\n"
        f"`{PARTNER_REG_LINK}`\n\n"
        "2️⃣ Registration ke baad chat box ke left side me *Open* button dabayein (ya niche button par click karein) aur apna *Account UID* submit karein.\n\n"
        "3️⃣ Admin verify karega ki aapne sahi link se registration kiya hai ya nahi, aur aapka status update ho jayega."
        f"{role_note}"
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start_command))
    print("Bot is running with MenuButtonWebApp ('Open' button) enabled...")
    app.run_polling()


if __name__ == "__main__":
    main()
