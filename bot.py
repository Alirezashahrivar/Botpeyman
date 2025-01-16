import nest_asyncio
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

nest_asyncio.apply()

# شناسه مدیر
ADMIN_CHAT_ID = 685549695  # شناسه تلگرام شما
CHANNEL_USERNAME = "@Tabadole_test"  # نام کاربری کانال تلگرام

# وضعیت‌ها برای مکالمه
ASK_NAME, ASK_SURNAME, ASK_PHONE, ASK_CITY, SHOW_OPTIONS, TRADE_TYPE, \
ASK_PAYMENT_METHOD, ASK_COUNTRY, ASK_AMOUNT, ASK_PRICE, CONFIRM_FEE, ADMIN_DECISION, \
GRE_USERNAME, GRE_PASSWORD, GRE_EXAM_TYPE, GRE_EXAM_DATE, GRE_CENTER, \
GRE_TIME, GRE_DISCOUNT_CODE, GRE_NOTES, APPLICANT_INFO, APPLICANT_NAME, \
APPLICANT_LAST_NAME, APPLICATION_LOOP, APPLICATION_DETAILS = range(25)


# بازگشت به منوی اصلی
async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["شروع معامله 💱", "پرداخت آزمون های زبان 📑", "اپلیکیشن فی دانشگاه 🏫"], ["تنظیمات ⚙️", "راهنما 🆘", "لغو ❌"]]
    await update.message.reply_text(
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return SHOW_OPTIONS

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً نام خود را وارد کنید:")
    return ASK_NAME

# دریافت نام
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("نام خانوادگی خود را وارد کنید:")
    return ASK_SURNAME

# دریافت نام خانوادگی
async def ask_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['surname'] = update.message.text
    await update.message.reply_text("لطفاً شماره تلفن خود را وارد کنید:")
    return ASK_PHONE

# دریافت شماره تلفن
async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("لطفاً شهر خود را وارد کنید:")
    return ASK_CITY

# دریافت شهر و نمایش گزینه‌ها
async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    name = context.user_data['name']
    surname = context.user_data['surname']
    city = context.user_data['city']

    await update.message.reply_text(f"ممنون {name} {surname} از {city}!")
    return await return_to_main_menu(update, context)

# پردازش گزینه‌های اصلی
async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "شروع معامله 💱":
        reply_keyboard = [["خرید 📈", "فروش 📉"], ["بازگشت 🔙"]]
        await update.message.reply_text("آیا می‌خواهید خرید کنید یا فروش؟", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return TRADE_TYPE
    elif user_choice == "پرداخت آزمون های زبان 📑":
        reply_keyboard = [["GRE", "TOEFL"], ["بازگشت 🔙"]]
        await update.message.reply_text(
            "لطفاً آزمون مورد نظر خود را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return GRE_USERNAME
    elif user_choice == "اپلیکیشن فی دانشگاه 🏫":
        await handle_application_fee(update, context)
        return APPLICANT_INFO
    elif user_choice in ["تنظیمات ⚙️", "راهنما 🆘"]:
        await update.message.reply_text("در حال حاضر این گزینه موجود نیست.")
        return await return_to_main_menu(update, context)
    elif user_choice in ["لغو ❌", "بازگشت 🔙"]:
        return await return_to_main_menu(update, context)
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
        return SHOW_OPTIONS

# پردازش انتخاب خرید یا فروش
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

# پردازش روش پرداخت
async def handle_payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment_method = update.message.text
    if payment_method == "بازگشت 🔙":
        return await return_to_main_menu(update, context)

    if payment_method == "انتقال بانکی":
        context.user_data['payment_method'] = payment_method
        reply_keyboard = [["آلمان", "فرانسه", "ایتالیا", "هلند"], ["اسپانیا", "اتریش", "سوئیس", "انگلستان"], ["سایر موارد", "بازگشت 🔙"]]
        await update.message.reply_text(
            "لطفاً کشوری که حساب بانکی دارید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return ASK_COUNTRY
    elif payment_method in ["پی‌پال", "نقدی"]:
        context.user_data['payment_method'] = payment_method
        await update.message.reply_text("لطفاً مقدار یورو را وارد کنید:")
        return ASK_AMOUNT
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
        return ASK_PAYMENT_METHOD

# پردازش کشور
async def handle_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = update.message.text
    if country == "بازگشت 🔙":
        return await return_to_main_menu(update, context)

    if country == "سایر موارد":
        await update.message.reply_text("لطفاً نام کشور را وارد کنید:")
        return ASK_COUNTRY

    context.user_data['country'] = country
    await update.message.reply_text("لطفاً مقدار یورو را وارد کنید:")
    return ASK_AMOUNT

# دریافت مقدار
async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['amount'] = float(update.message.text)
        await update.message.reply_text("لطفاً قیمت مورد نظر خود را برای هر یورو وارد کنید (به تومان):")
        return ASK_PRICE
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد معتبر وارد کنید.")
        return ASK_AMOUNT

# دریافت قیمت
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

# تأیید هزینه
async def confirm_fee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    decision = update.message.text
    if decision == "بله":
        name = context.user_data['name']
        surname = context.user_data['surname']
        phone = context.user_data['phone']
        city = context.user_data['city']
        trade_type = context.user_data['trade_type']
        payment_method = context.user_data['payment_method']
        country = context.user_data.get('country', "نامشخص")
        amount = context.user_data['amount']
        price = context.user_data['price']
        trade_fee = context.user_data['trade_fee']

        # ارسال به مدیر
        message_admin = (f"معامله جدید شماره {request_number}:
        
                         f"نام: {name}\n"
                         f"نام خانوادگی: {surname}\n"
                         f"شماره تلفن: {phone}\n"
                         f"شهر: {city}\n"
                         f"نوع معامله: {trade_type}\n"
                         f"روش پرداخت: {payment_method}\n"
                         f"کشور: {country}\n"
                         f"مقدار: {amount} یورو\n"
                         f"قیمت: {price} تومان\n"
                         f"هزینه معامله: {trade_fee:.2f} یورو")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message_admin)

        # ارسال به کانال
        message_channel = (f"معامله جدید شماره {request_number}:
                           f"نوع معامله: {trade_type}\n"
                           f"مقدار: {amount} یورو\n"
                           f"قیمت: {price} تومان\n"
                           f"روش پرداخت: {payment_method}\n"
                           f"کشور: {country}")
                           f"[تماس با مدیر](https://t.me/{ADMIN_CHAT_ID})")

        reply_keyboard = [["ارسال به کانال 📢", "بازگشت 🔙"]]
        await update.message.reply_text("آیا می‌خواهید این درخواست را به کانال ارسال کنید؟", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        context.user_data['message_channel'] = message_channel
        return ADMIN_DECISION
    else:
        await return_to_main_menu(update, context)
        return ConversationHandler.END

# تصمیم مدیر
async def handle_admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    decision = update.message.text
    if decision == "ارسال به کانال 📢":
        message_channel = context.user_data['message_channel']
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=message_channel)
        await update.message.reply_text("درخواست با موفقیت به کانال ارسال شد.")
    elif decision in ["بازگشت 🔙", "لغو ❌"]:
        await return_to_main_menu(update, context)
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
        return ADMIN_DECISION

    return ConversationHandler.END

# لغو مکالمه
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await return_to_main_menu(update, context)
    return ConversationHandler.END

# تابع اصلی
async def main():
    application = Application.builder().token("7823324333:AAG6QRPbZ4mVmsEtvITEfCWY6katXTIMqTQ").build()

    # تنظیم ConversationHandler
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
            ASK_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_country)],
            ASK_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount)],
            ASK_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price)],
            CONFIRM_FEE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_fee)],
            ADMIN_DECISION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_decision)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Start bot
    print("Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
