import nest_asyncio
import asyncio
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler,
)

nest_asyncio.apply()

# Constants
ADMIN_CHAT_ID = 685549695  # Admin's Telegram ID
CHANNEL_USERNAME = "@PM_tabadol"  # Channel username

# Conversation states
(
    ASK_NAME, ASK_SURNAME, ASK_PHONE, ASK_CITY, SHOW_OPTIONS, TRADE_TYPE,
    ASK_PAYMENT_METHOD, ASK_COUNTRY, ASK_AMOUNT, ASK_PRICE, CONFIRM_FEE,
    ADMIN_DECISION, GRE_USERNAME, GRE_PASSWORD, GRE_EXAM_TYPE, GRE_EXAM_DATE,
    GRE_CENTER, GRE_TIME, GRE_DISCOUNT_CODE, GRE_NOTES, APPLICANT_INFO,
    APPLICANT_NAME, APPLICANT_LAST_NAME, APPLICATION_LOOP, APPLICATION_DETAILS,
    SOS_OPTIONS, TOEFL_FAQS, TOEFL_DETAILS, GRE_DETAILS, NEGOTIATION
) = range(30)

# Trade statuses
TRADE_STATUS_PENDING = "در انتظار خریدار"
TRADE_STATUS_NEGOTIATING = "در حال مذاکره"
TRADE_STATUS_ACCEPTED = "پذیرفته شد ✅"
TRADE_STATUS_DECLINED = "رد شد ❌"

# Helper function to return to the main menu
async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["شروع معامله 💱", "پرداخت آزمون های زبان 📑", "اپلیکیشن فی دانشگاه 🏫"], ["تنظیمات ⚙️", "راهنما 🆘", "لغو ❌"]]
    await update.message.reply_text(
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return SHOW_OPTIONS

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً نام خود را وارد کنید:")
    return ASK_NAME

# Ask for name
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("نام خانوادگی خود را وارد کنید:")
    return ASK_SURNAME

# Ask for surname
async def ask_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['surname'] = update.message.text
    await update.message.reply_text("لطفاً شماره تلفن خود را وارد کنید:")
    return ASK_PHONE

# Ask for phone
async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("لطفاً شهر خود را وارد کنید:")
    return ASK_CITY

# Ask for city
async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    name = context.user_data['name']
    surname = context.user_data['surname']
    city = context.user_data['city']
    await update.message.reply_text(f"ممنون {name} {surname} از {city}!")
    return await return_to_main_menu(update, context)

# Handle main menu options
async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "شروع معامله 💱":
        reply_keyboard = [["خرید 📈", "فروش 📉"], ["بازگشت 🔙"]]
        await update.message.reply_text("آیا می‌خواهید خرید کنید یا فروش؟", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return TRADE_TYPE
    elif user_choice == "لغو ❌":
        await update.message.reply_text("مکالمه لغو شد.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
        return SHOW_OPTIONS

# Handle trade type (buy/sell)
async def handle_trade_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trade_choice = update.message.text
    if trade_choice == "بازگشت 🔙":
        return await return_to_main_menu(update, context)

    context.user_data['trade_type'] = "خرید" if trade_choice == "خرید 📈" else "فروش"
    reply_keyboard = [["انتقال بانکی", "پی‌پال", "نقدی"], ["بازگشت 🔙"]]
    await update.message.reply_text(
        "چگونه می‌خواهید پول خود را دریافت یا پرداخت کنید؟",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return ASK_PAYMENT_METHOD

# Handle payment method
async def handle_payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment_method = update.message.text
    if payment_method == "بازگشت 🔙":
        return await return_to_main_menu(update, context)

    context.user_data['payment_method'] = payment_method
    await update.message.reply_text("لطفاً مقدار یورو را وارد کنید:")
    return ASK_AMOUNT

# Handle amount
async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['amount'] = float(update.message.text)
        await update.message.reply_text("لطفاً قیمت مورد نظر خود را برای هر یورو وارد کنید (به تومان):")
        return ASK_PRICE
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد معتبر وارد کنید.")
        return ASK_AMOUNT

# Handle price
async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['price'] = float(update.message.text)
        amount = context.user_data['amount']
        trade_fee = amount * 0.005
        context.user_data['trade_fee'] = trade_fee
        total_with_fee = amount + trade_fee if context.user_data['trade_type'] == "خرید" else amount - trade_fee

        await update.message.reply_text(
            f"هزینه معامله شما 0.5 درصد یا {trade_fee:.2f} یورو است. مقدار کل: {total_with_fee:.2f} یورو. آیا مایل به ادامه هستید؟",
            reply_markup=ReplyKeyboardMarkup([["بله", "بازگشت 🔙"]], resize_keyboard=True),
        )
        return CONFIRM_FEE
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد معتبر وارد کنید.")
        return ASK_PRICE

# Confirm fee
async def confirm_fee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    decision = update.message.text
    if decision == "بله":
        # Send trade details to admin
        trade_details = (
            f"معامله جدید:\n"
            f"نام: {context.user_data['name']}\n"
            f"نام خانوادگی: {context.user_data['surname']}\n"
            f"شماره تلفن: {context.user_data['phone']}\n"
            f"شهر: {context.user_data['city']}\n"
            f"نوع معامله: {context.user_data['trade_type']}\n"
            f"روش پرداخت: {context.user_data['payment_method']}\n"
            f"مقدار: {context.user_data['amount']} یورو\n"
            f"قیمت: {context.user_data['price']} تومان\n"
            f"هزینه معامله: {context.user_data['trade_fee']:.2f} یورو"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=trade_details)

        # Ask admin for decision
        reply_keyboard = [["تایید ✅", "رد ❌"]]
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="آیا این معامله را تایید می‌کنید؟",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return ADMIN_DECISION
    elif decision == "بازگشت 🔙":
        return await return_to_main_menu(update, context)
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر انتخاب کنید.")
        return CONFIRM_FEE

# Handle admin decision
async def handle_admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    decision = update.message.text
    if decision == "تایید ✅":
        # Generate a unique trade ID
        trade_id = context.bot_data.get("trade_counter", 1)
        context.bot_data["trade_counter"] = trade_id + 1

        # Store trade details
        context.bot_data[f"trade_{trade_id}"] = {
            "seller_id": update.message.chat_id,
            "status": TRADE_STATUS_PENDING,
            "details": context.user_data
        }

        # Post trade to channel
        trade_message = (
            f"📢 **معامله جدید شماره {trade_id}**\n"
            f"🔄 نوع معامله: {context.user_data['trade_type']}\n"
            f"💰 مقدار: {context.user_data['amount']} یورو\n"
            f"💲 قیمت: {context.user_data['price']} تومان\n"
            f"💳 روش پرداخت: {context.user_data['payment_method']}\n"
            f"📌 **وضعیت:** {TRADE_STATUS_PENDING}"
        )
        keyboard = [[InlineKeyboardButton("💬 تماس با فروشنده", callback_data=f"contact_seller_{trade_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=trade_message, reply_markup=reply_markup, parse_mode="Markdown")

        # Store the message ID for later updates
        context.bot_data[f"trade_message_{trade_id}"] = message.message_id

        await update.message.reply_text("معامله با موفقیت به کانال ارسال شد.")
        return await return_to_main_menu(update, context)
    elif decision == "رد ❌":
        await update.message.reply_text("معامله رد شد.")
        return await return_to_main_menu(update, context)
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر انتخاب کنید.")
        return ADMIN_DECISION

# Handle contact button
async def handle_contact_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query to stop the loading spinner

    # Extract trade ID from the callback data
    trade_id = int(query.data.split("_")[-1])
    trade_info = context.bot_data.get(f"trade_{trade_id}")
    if not trade_info:
        await query.edit_message_text("⚠️ این معامله دیگر معتبر نیست.")
        return

    # Check if the buyer is registered
    if "name" not in context.user_data:
        await query.edit_message_text("⚠️ شما باید در ربات ثبت‌نام کنید.")
        return

    # Notify the seller
    seller_id = trade_info["seller_id"]
    await context.bot.send_message(
        chat_id=seller_id,
        text=f"👤 یک خریدار برای معامله شماره {trade_id} علاقه‌مند است.\n"
             f"🔄 لطفاً به معامله بپیوندید و شرایط را بررسی کنید."
    )

    # Update trade status
    trade_info["status"] = TRADE_STATUS_NEGOTIATING
    trade_info["buyer_id"] = query.from_user.id

    # Update the message in the channel
    trade_message_id = context.bot_data.get(f"trade_message_{trade_id}")
    updated_trade_message = (
        f"📢 **معامله جدید شماره {trade_id}**\n"
        f"🔄 نوع معامله: {trade_info['details']['trade_type']}\n"
        f"💰 مقدار: {trade_info['details']['amount']} یورو\n"
        f"💲 قیمت: {trade_info['details']['price']} تومان\n"
        f"💳 روش پرداخت: {trade_info['details']['payment_method']}\n"
        f"📌 **وضعیت:** {TRADE_STATUS_NEGOTIATING}"
    )
    await context.bot.edit_message_text(
        chat_id=CHANNEL_USERNAME,
        message_id=trade_message_id,
        text=updated_trade_message,
        parse_mode="Markdown"
    )

    # Notify the buyer
    await query.edit_message_text(
        text=f"📌 **وضعیت:** {TRADE_STATUS_NEGOTIATING}\n"
             f"✅ فروشنده مطلع شد. منتظر پاسخ باشید.",
        parse_mode="Markdown"
    )

    return NEGOTIATION

# Main function
async def main():
    application = Application.builder().token("7823324333:AAG6QRPbZ4mVmsEtvITEfCWY6katXTIMqTQ").build()

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_surname)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_city)],
            SHOW_OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_options)],
            TRADE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_trade_type)],
            ASK_PAYMENT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment_method)],
            ASK_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount)],
            ASK_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price)],
            CONFIRM_FEE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_fee)],
            ADMIN_DECISION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_decision)],
            NEGOTIATION: [CallbackQueryHandler(handle_contact_seller, pattern=r"contact_seller_\d+")]
        },
        fallbacks=[CommandHandler('cancel', return_to_main_menu)],
    )

    application.add_handler(conv_handler)
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
