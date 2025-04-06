
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
users = {}

PRODUCT_NAME = "PayPal Personal Canada 🇨🇦 2015"
PRODUCT_PRICE = 10
PRODUCT_LINK = "https://drive.google.com/drive/folders/1SDTnt6BtB56T0QeKATFNir9pwvgG2XqV?usp=sharing"
USDT_ADDRESS = "TKXc6u3rG5CwpD4vPDNAVRqxLPLnqzZyvv"
ADMIN_USERNAME = "@cloudmaildarkweb"

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"purchased": False, "balance": 0}
    keyboard = [
        [InlineKeyboardButton("🛒 View Product", callback_data="view_product")],
        [InlineKeyboardButton("💰 Check Balance", callback_data="check_balance")],
        [InlineKeyboardButton("➕ Top Up Balance", callback_data="top_up")],
        [InlineKeyboardButton("👨‍💻 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME.strip('@')}")],
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Digital Shop Bot!", reply_markup=InlineKeyboardMarkup(keyboard))

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data == "view_product":
        if users[user_id]["purchased"]:
            query.edit_message_text("You have already purchased this product.")
        else:
            keyboard = [
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="confirm_purchase")],
            ]
            query.edit_message_text(
                f"🪪 {PRODUCT_NAME}\n\n"
                f"Includes:\n- Full documents\n- ID with selfie\n- Proof of address\n- 2FA available\n\n"
                f"💵 Price: ${PRODUCT_PRICE} (USDT - TRC20)\nOne-time purchase only.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    elif query.data == "check_balance":
        balance = users[user_id]["balance"]
        query.edit_message_text(f"Your current balance: ${balance}")

    elif query.data == "top_up":
        query.edit_message_text(
            f"To top up your balance (minimum $50), send USDT TRC20 to:\n\n"
            f"`{USDT_ADDRESS}`\n\n"
            "Then send the TXID or screenshot here and the admin will review and add your balance.",
            parse_mode="Markdown"
        )

    elif query.data == "confirm_purchase":
        if users[user_id]["balance"] >= PRODUCT_PRICE:
            users[user_id]["balance"] -= PRODUCT_PRICE
            users[user_id]["purchased"] = True
            query.edit_message_text("✅ Payment confirmed!\nHere is your product link:")
            context.bot.send_message(chat_id=query.message.chat_id, text=PRODUCT_LINK)
        else:
            query.edit_message_text("❌ Insufficient balance. Please top up your account first.")

def handle_message(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your message has been received. The admin will review it and update your balance if the payment is confirmed.")

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button_handler))
dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo, handle_message))

updater.start_polling()
updater.idle()
