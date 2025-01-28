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
ASK_PAYMENT_METHOD, ASK_COUNTRY, ASK_AMOUNT, ASK_PRICE, ADMIN_DECISION, \
GRE_USERNAME, GRE_PASSWORD, GRE_EXAM_TYPE, GRE_EXAM_DATE, GRE_CENTER, \
GRE_TIME, GRE_FINALIZE, GRE_DISCOUNT_CODE, GRE_DISCOUNT_RESPONSE, GRE_NOTES, GRE_TEST_TYPE,\
APPLICANT_INFO, APPLICANT_NAME, \
APPLICANT_LAST_NAME, APPLICATION_LOOP, APPLICATION_DETAILS, APPLICATION_COUNT, \
APPLICATION_RESTART, SOS_OPTIONS, TOEFL_FAQS, TOEFL_DETAILS, CONFIRM_FEE, \
GRE_DETAILS, GRE_FAQS, \
TOEFL_USERNAME, TOEFL_PASSWORD, TOEFL_EXAM_TYPE, TOEFL_EXAM_DATE, TOEFL_CENTER, \
TOEFL_TIME, TOEFL_FINALIZE, TOEFL_DISCOUNT_CODE, TOEFL_DISCOUNT_RESPONSE = range(44)


# بازگشت به منوی اصلی
async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["شروع معامله 💱", "پرداخت آزمون های زبان 📑", "اپلیکیشن فی دانشگاه 🏫"], ["تنظیمات ⚙️", "راهنما 🆘", "لغو ❌"]]
    await update.message.reply_text(
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return SHOW_OPTIONS

# بازگشت به منوی اصلی TOEFL
async def return_to_toefl_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ["تافل چیست؟", "بخش های آزمون تافل"],
        ["نحوه ثبت نام تافل", "سوالات متداول درباره ثبت نام تافل"],
        ["بازگشت 🔙"]
    ]
    await update.message.reply_text(
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return TOEFL_DETAILS

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
        reply_keyboard = [["جی آر ای", "تافل"], ["بازگشت 🔙"]]
        await update.message.reply_text(
            "لطفاً آزمون مورد نظر خود را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return GRE_USERNAME
    elif user_choice == "اپلیکیشن فی دانشگاه 🏫":
        await handle_application_fee(update, context)  # Call the university fee handler
        return APPLICANT_INFO
    elif user_choice == "تنظیمات ⚙️":
        await update.message.reply_text("به بخش تنظیمات خوش آمدید.")
        return SHOW_OPTIONS
    elif user_choice == "راهنما 🆘":
        reply_keyboard = [["جی آر ای", "تافل", "تبادل ارز"], ["بازگشت 🔙"]]
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return SOS_OPTIONS
    elif user_choice == "لغو ❌":
        await update.message.reply_text("مکالمه لغو شد.")
        return ConversationHandler.END
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

# پردازش راهنما
async def handle_sos_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text

    if user_choice == "جی آر ای":
        reply_keyboard = [
            ["؟آزمون جی آر ای از چه بخش هایی تشکیل شده", "بخش های آزمون GRE General"],
            ["آزمون GRE Subject", "سوالات متداول درباره ثبت نام جی آر ای"],
            ["بازگشت 🔙"]
        ]
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return GRE_DETAILS

    elif user_choice == "تافل":
        reply_keyboard = [
            ["تافل چیست؟", "بخش های آزمون تافل"],
            ["نحوه ثبت نام تافل", "سوالات متداول درباره ثبت نام تافل"],
            ["بازگشت 🔙"]
        ]
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return TOEFL_DETAILS

    elif user_choice == "تبادل ارز":
        await update.message.reply_text(
            "در حال حاضر خدمات تبادل ارز ارائه می‌شود. لطفاً با پشتیبانی تماس بگیرید."
        )
        return SOS_OPTIONS

    elif user_choice == "بازگشت 🔙":
        # Return to the main SOS menu
        reply_keyboard = [["جی آر ای", "تافل", "تبادل ارز"], ["بازگشت به منوی اصلی"]]
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return SOS_OPTIONS

    elif user_choice == "بازگشت به منوی اصلی":
        # Return to the main menu
        await return_to_main_menu(update, context)
        return SHOW_OPTIONS

    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
        return SOS_OPTIONS



# پردازش راهنمای آزمون تافل
async def handle_toefl_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "تافل چیست؟":
        await update.message.reply_text(
            """
            می توان آزمون تافل را در کنار آیلتس معتبرترین آزمون زبان بین المللی دانست. ثبت نام تافل توسط ets  و آیلتس توسط British Council انجام می شود. البته برای دانشگاه‌های غیر آمریکایی معمولاً آیلتس ترجیح داده می شود. ولی بی شک در دانشگاه های آمریکا اولویت با ثبت نام در آزمون تافل خواهد بود. نام نویسی برای آزمون تافل در سراسر دنیا انجام می شود. در بیش از 120 کشور دنیا آزمون تافل برگزار می گردد. تافل اینترنتی رایج ترین شکل برگزاری آزمون است. البته هنوز تافل کاغذی در بعضی از نقاط جهان برگزار می شود. در ایران فقط تافل اینترنتی TOEFL iBT برگزار می شود. هزینه آزمون تافل اینترنتی در ایران 265 دلار است. بنابراین قیمت ارز بر روی هزینه ریالی امتحان تافل اینترنتی تاثیر مستقیم دارد.
"""
        )
    elif user_choice == "بخش های آزمون تافل":
        await update.message.reply_text(
            """
آزمون تافل به طور معمول با بخش Reading شروع می شود که حدود 35 تا 55 سوال است و 60 الی 90 دقیقه فرصت برای پاسخگویی دارید.

بخش Listening آزمون از 35 تا 50 سوال تشکیل شده و 60 الی 80 دقیقه زمان برای پاسخگویی دارید.

بخش Writing دو قسمت است . در قسمت اول که حدود 20 دقیقه است به سوالات مطرح شده پاسخ می دهید و در بخش دوم که حدود 30 دقیقه است باید یک متن یا انشا در رابطه با مطلب خواسته شده بنویسید.

بخش Speaking باید به سوالاتی که برای شما مطرح می شود پاسخ دهید.
"""
        )
    elif user_choice == "نحوه ثبت نام تافل":
        await update.message.reply_text(
            """
            برای ثبت نام TOEFL ابتدا با ثبت نام در بخش تافل سایت ETS  یک پروفایل برای خود ایجاد کنید. نام کاربری و گذرواژه شما برای ثبت سفارش در ربات لازم است. پس از مشخص کردن تاریخ امتحان و حوزه مورد نظر، پرداخت هزینه امتحان تافل باید توسط پرداخت آنلاین با کارت اعتباری بین المللی مثل Visa Card ،Master Card  و غیره صورت گیرد. شما با پر کردن فرم ثبت سفارش در همین صفحه می توانید سفارش پرداخت هزینه ثبت نام امتحان تافل اینترنتی را برای ما ثبت کنید. بعد از واریز مبلغ ریالی آزمون از درگاه آنلاین بانکی، ثبت نام آزمون تافل شما انجام شده و تایید آن برای شما ارسال می گردد.

شما می توانید برای شرکت در آزمون تافل، در آزمون آزمایشی تافل شرکت کنید. برای ثبت نام در امتحان تافل آزمایشی واقعی می توانید از اینجا سفارش خود را ثبت کنید.
"""
        )
    elif user_choice == "سوالات متداول درباره ثبت نام تافل":
        reply_keyboard = [
            ["هزینه آزمون تافل اینترنتی Toefl iBT چقدر است؟"],
            ["خرید ووچر تافل با ثبت نام توسط بات تبادل ارز چه تفاوتی دارد؟"],
            ["مراکز مجاز تافل در ایران چه سنترهایی است؟"],
            ["ثبت نام تافل اینترنتی توسط بات تبادل ارز چقدر زمان می برد؟"],
            ["مراحل ثبت نام آزمون تافل چیست؟"],
            ["آیا محدودیتی برای تعداد ثبت نام تافل وجود دارد؟"],
            ["بازگشت 🔙"]
        ]
        await update.message.reply_text(
            "سوالات متداول درباره ثبت نام تافل را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return TOEFL_FAQS
    elif user_choice == "بازگشت 🔙":
        # Return to the SOS menu for TOEFL
        reply_keyboard =      ["تافل چیست؟", "بخش های آزمون تافل"], \
            ["نحوه ثبت نام تافل", "سوالات متداول درباره ثبت نام تافل"], \
            ["بازگشت 🔙"]
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return SOS_OPTIONS
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
    return TOEFL_DETAILS

# پردازش گزینه های راهنمای آزمون تافل
async def handle_toefl_faqs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "هزینه آزمون تافل اینترنتی Toefl iBT چقدر است؟":
        await update.message.reply_text("هزینه دلاری ثبت نام آزمون تافل 265 دلار است. البته اگر به تاریخ امتحان، کمتر از یک هفته مانده باشد، این هزینه 40 دلار افزایش پیدا می کند.")
    elif user_choice == "خرید ووچر تافل با ثبت نام بات تبادل ارز چه تفاوتی دارد؟":
        await update.message.reply_text(
            "در صورتی که شما از کد ووچر برای ثبت نام استفاده کنید، معمولا امکان کنسلی و بازگشت هزینه شما وجود ندارد. در صورتی که پس از ثبت نام با بات تبادل ارز، در صورت تغییر تصمیم مبنی بر کنسلی آزمون، می توانید به راحتی آزمون را کنسل کرده و نصف هزینه را استرداد کنید."
        )
    elif user_choice == "مراکز مجاز تافل در ایران چه سنترهایی است؟":
        await update.message.reply_text(
            "از معروف ترین سنترهای برگزاری تافل در تهران می توان دانشگاه خاتم، سازمان سنجش، موسسه امیربهادر و زبان نگار را نام برد. البته سنترهای دیگری چون علامه سخن، مرکز زبان ایران، معرفت و دانشگاه شهید بهشتی نیز، این آزمون را در ایران به طور رسمی برگزار می کنند."
        )
    elif user_choice == "ثبت نام تافل اینترنتی توسط بات تبادل ارز چقدر زمان می برد؟":
        await update.message.reply_text(
            " از ساعت 9 صبح تا 11 شب طبق جدول انجام سفارشات ، ثبت نام شما در کمتر از 150 دقیقه انجام می شود. پیام و اطلاعات ثبت سفارش برای شما در ربات ارسال خواهد شد."
        )
    elif user_choice == "مراحل ثبت نام آزمون تافل اینترنتی چیست؟":
        await update.message.reply_text(
            "ابتدا در سایت ets.org و در بخش تافل یک اکانت می سازید. سپس در قسمت آزمون تافل در ربات را انتخاب و سفارش را تکمیل می کنید. تاریخ و مرکز برگزاری آزمون را انتخاب کرده و هزینه ریالی را پس از ارتباط با ادمین، پرداخت میکنید."
        )
    elif user_choice == "آیا محدودیتی برای تعداد ثبت نام تافل وجود دارد؟":
        await update.message.reply_text(
            "بله، باید حداقل 14 روز بین دو آزمون شما فاصله باشد. به عبارتی هر دو هفته یک بار می توانید در آزمون تافل شرکت نمایید."
        )
    elif user_choice == "بازگشت 🔙":
        return await handle_toefl_details(update, context)
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
    return TOEFL_FAQS


#  GRE پردازش گزینه های راهنمای آزمون
async def handle_gre_faqs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "هزینه آزمون جی آر ای چقدر است؟":
        await update.message.reply_text("هزینه دلاری ثبت نام آزمون جی آر ای 220 دلار است.")
    elif user_choice == "خرید ووچر جی آر ای با ثبت نام بات تبادل ارز چه تفاوتی دارد؟":
        await update.message.reply_text(
            "در صورتی که شما از کد ووچر برای ثبت نام استفاده کنید، معمولا امکان کنسلی و بازگشت هزینه شما وجود ندارد. در صورتی که پس از ثبت نام با بات تبادل ارز، در صورت تغییر تصمیم مبنی بر کنسلی آزمون، می توانید به راحتی تا پیش از 5 روز به تاریخ آزمون، آن را کنسل کرده و نصف هزینه را استرداد کنید."
        )
    elif user_choice == "مراکز مجاز جی آر ای در ایران چه سنترهایی است؟":
        await update.message.reply_text(
            "از معروف ترین سنترهای برگزاری تافل در تهران می توان دانشگاه خاتم، سازمان سنجش، موسسه امیربهادر و زبان نگار را نام برد. البته سنترهای دیگری چون علامه سخن، مرکز زبان ایران، معرفت و دانشگاه شهید بهشتی نیز، این آزمون را در ایران به طور رسمی برگزار می کنند."
        )
    elif user_choice == "ثبت نام جی آر ای توسط بات تبادل ارز چقدر زمان می برد؟":
        await update.message.reply_text(
            " از ساعت 9 صبح تا 11 شب طبق جدول انجام سفارشات ، ثبت نام شما در کمتر از 150 دقیقه انجام می شود. پیام و اطلاعات ثبت سفارش برای شما در ربات ارسال خواهد شد."
        )
    elif user_choice == "مراحل ثبت نام آزمون جی آر ای چیست؟":
        await update.message.reply_text(
            "ابتدا در سایت ets.org و در بخش تافل یک اکانت می سازید. سپس در قسمت آزمون تافل در ربات را انتخاب و سفارش را تکمیل می کنید. تاریخ و مرکز برگزاری آزمون را انتخاب کرده و هزینه ریالی را پس از ارتباط با ادمین، پرداخت میکنید."
        )
    elif user_choice == "آیا می توان آزمون جی آر ای را جابجا کرد؟":
        await update.message.reply_text(
            "بله، شما میتوانید تا 4 روز قبل از روز آزمون خود، با پرداخت 50 دلار اقدام به تغییر زمان و مرکز آزمون نمایید."
        )
    elif user_choice == "بازگشت 🔙":
        return await handle_gre_details(update, context)
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
    return GRE_FAQS

# پردازش راهنمای آزمون GRE
async def handle_gre_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "؟آزمون جی آر ای از چه بخش هایی تشکیل شده":
        await update.message.reply_text(
            """
            آزمون GRE خود به دو نوع Subject و General تقسیم می‌شود.
"""
        )
    elif user_choice == "بخش های آزمون GRE General":
        await update.message.reply_text(
            """
            آزمون GRE General کتبی شامل سه بخش می‌باشد:

1 . Quantitative ( استدلال کمی و ریاضیات )
2 . Verbal ( استدلال کیفی و درک زبانی )
3 . Analytical Writing ( بخش نوشتاری تحلیلی )
            """
        )
    elif user_choice == "آزمون GRE Subject":
        await update.message.reply_text(
            """
            آزمون GRE Subject از دروس تخصصی رشته‌هایی خاص مانند زیست شناسی، شیمی، ادبیات انگلیسی، ریاضی، فیزیک و روان شناسی تشکیل شده و به داوطلبان همین رشته‌ها کمک می‌کند تا بیش از پیش خود را متمایز کنند. اگر در این رشته‌ها تحصیل می‌کنید باید وب‌سایت دانشکده مورد نظر را بررسی کنید تا از لزوم شرکت در این آزمون با خبر شوید. در حال حاضر این آزمون سه مرتبه و توسط سازمان سنجش ایران برگزار می شود.

نکته قبل توجه اینکه این آزمون تنها به صورت کتبی برگزار شده و خبری از سوالات اینترنتی در آن نخواهد بود؛ 100 سوال 5 گزینه ای که برخلاف آزمون GRE General، دارای نمره منفی نیز می باشند. این آزمون معمولا برای متقاضیان دانشگاه های بسیار مطرح که رقابتی سنگین برای ورود به آنها وجود دارد توصیه می شود. افرادی نیز  که نمرات چندان قابل قبولی در مقاطع گذشته خود کسب نکرده و قصد دارند تا با جبران آن نمرات توانایی هایی خود را اثبات نمایند، معمولا به نمره GRE Subject نیاز خواهند داشت.
"""
        )
    elif user_choice == "سوالات متداول درباره ثبت نام جی آر ای":
        reply_keyboard = [
            ["هزینه آزمون جی آر ای چقدر است؟"],
            ["خرید ووچر جی آر ای با ثبت نام بات تبادل ارز چه تفاوتی دارد؟"],
            ["مراکز مجاز جی آر ای در ایران چه سنترهایی است؟"],
            ["ثبت نام جی آر ای توسط بات تبادل ارز چقدر زمان می برد؟"],
            ["مراحل ثبت نام آزمون جی آر ای چیست؟"],
            ["آیا می توان آزمون جی آر ای را جابجا کرد؟"],
            ["بازگشت 🔙"]
        ]
        await update.message.reply_text(
            "سوالات متداول درباره ثبت نام جی آر ای را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return GRE_FAQS
    elif user_choice == "بازگشت 🔙":
        # Return to the SOS menu for GRE
        reply_keyboard =      ["؟آزمون جی آر ای از چه بخش هایی تشکیل شده", "بخش های آزمون GRE General"], \
            ["آزمون GRE Subject", "سوالات متداول درباره ثبت نام جی آر ای"], \
            ["بازگشت 🔙"]
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
        )
        return SOS_OPTIONS
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
    return GRE_DETAILS

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

        # Keep track of request count
        if 'request_count' not in context.bot_data:
            context.bot_data['request_count'] = 1
        else:
            context.bot_data['request_count'] += 1

        request_number = context.bot_data['request_count']


        # ارسال به مدیر
        message_admin = (f"معامله جدید شماره {request_number}:\n"

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

  # ارسال به مدیر
        message_admin = (f"معامله جدید شماره {request_number}:\n"
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
        message_channel = (f"معامله جدید شماره {request_number}:\n"
                           f"نوع معامله: {trade_type}\n"
                           f"مقدار: {amount} یورو\n"
                           f"قیمت: {price} تومان\n"
                           f"روش پرداخت: {payment_method}\n"
                           f"کشور: {country}\n"
                           f"[تماس با ادمین](https://t.me/alirezashra)")
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
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=message_channel, parse_mode="Markdown")
        await update.message.reply_text("درخواست با موفقیت به کانال ارسال شد.")
    elif decision in ["بازگشت 🔙", "لغو ❌"]:
        await update.message.reply_text("به منوی اصلی بازگشتید.")
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر را انتخاب کنید.")
        return ADMIN_DECISION

    # Return to the main menu
    return await return_to_main_menu(update, context)

# لغو مکالمه
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await return_to_main_menu(update, context)
    return ConversationHandler.END


# ثبت اطلاعات آزمون GRE
async def handle_gre_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle the "بازگشت 🔙" button
    if update.message.text == "بازگشت 🔙":
        current_step = context.user_data.get('gre_step', GRE_TEST_TYPE)
        if current_step > GRE_TEST_TYPE:
            context.user_data['gre_step'] -= 1  # Go back one step
            return await handle_gre_registration(update, context)  # Restart the previous step
        else:
            await return_to_main_menu(update, context)
            return SHOW_OPTIONS

    # Determine the current step
    current_step = context.user_data.get('gre_step', GRE_TEST_TYPE)

    # Step: Select GRE test type
    if current_step == GRE_TEST_TYPE:
        await update.message.reply_text(
            "لطفاً نوع آزمون GRE خود را مشخص کنید:",
            reply_markup=ReplyKeyboardMarkup([["Subject", "General"], ["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['gre_step'] = GRE_USERNAME
        return GRE_USERNAME

    # Step: Collect ETS username
    elif current_step == GRE_USERNAME:
        context.user_data['test_type'] = update.message.text
        await update.message.reply_text(
            "لطفاً نام کاربری ETS خود را وارد کنید:",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['gre_step'] = GRE_PASSWORD
        return GRE_PASSWORD

    # Step: Collect ETS password
    elif current_step == GRE_PASSWORD:
        context.user_data['username'] = update.message.text
        await update.message.reply_text(
            "لطفاً رمز عبور ETS خود را وارد کنید:",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['gre_step'] = GRE_EXAM_TYPE
        return GRE_EXAM_TYPE

    # Step: Select exam type
    elif current_step == GRE_EXAM_TYPE:
        context.user_data['password'] = update.message.text
        await update.message.reply_text(
            "لطفاً نوع آزمون خود را مشخص کنید (حضوری یا Home Edition):",
            reply_markup=ReplyKeyboardMarkup([["حضوری", "Home Edition"], ["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['gre_step'] = GRE_EXAM_DATE
        return GRE_EXAM_DATE

    # Step: Collect exam date
    elif current_step == GRE_EXAM_DATE:
        context.user_data['exam_type'] = update.message.text
        await update.message.reply_text(
            "لطفاً تاریخ آزمون را وارد کنید (به‌صورت YYYY-MM-DD):",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        # Skip GRE_CENTER if exam type is "Home Edition"
        if context.user_data['exam_type'] == "Home Edition":
            context.user_data['gre_step'] = GRE_TIME
            return await handle_gre_registration(update, context)
        else:
            context.user_data['gre_step'] = GRE_CENTER
            return GRE_CENTER

    # Step: Collect exam center (only for حضوری)
    elif current_step == GRE_CENTER:
        context.user_data['exam_date'] = update.message.text
        await update.message.reply_text(
            "لطفاً مرکز آزمون خود را وارد کنید:",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['gre_step'] = GRE_TIME
        return GRE_TIME

    # Step: Select exam time
    elif current_step == GRE_TIME:
        if 'exam_date' not in context.user_data:  # For "Home Edition," exam_date is set earlier
            context.user_data['exam_date'] = update.message.text
        await update.message.reply_text(
            "لطفاً زمان آزمون خود را مشخص کنید (صبح یا عصر):",
            reply_markup=ReplyKeyboardMarkup([["صبح", "عصر"], ["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['gre_step'] = GRE_DISCOUNT_CODE
        return GRE_DISCOUNT_CODE

    # Step: Ask for discount code availability
    elif current_step == GRE_DISCOUNT_CODE:
        await update.message.reply_text(
            "آیا کد تخفیف ETS دارید؟",
            reply_markup=ReplyKeyboardMarkup([["دارم", "ندارم"], ["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['gre_step'] = GRE_DISCOUNT_RESPONSE
        return GRE_DISCOUNT_RESPONSE

    # Step: Handle discount code response
    elif current_step == GRE_DISCOUNT_RESPONSE:
        if update.message.text == "دارم":
            await update.message.reply_text(
                "لطفاً کد تخفیف ETS خود را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
            )
        else:
            context.user_data['discount_code'] = "ندارم"
            await update.message.reply_text(
                "اگر یادداشتی دارید وارد کنید، در غیر این صورت تایپ کنید 'ندارم':",
                reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
            )
        context.user_data['gre_step'] = GRE_FINALIZE
        return GRE_FINALIZE

    # Step: Finalize the process
    elif current_step == GRE_FINALIZE:
        context.user_data['note'] = update.message.text
        await update.message.reply_text(
            "فرآیند ثبت‌نام با موفقیت تکمیل شد! به منوی اصلی بازگشتید.",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data.clear()
        return SHOW_OPTIONS

    # Handle unexpected input
    else:
        await update.message.reply_text("خطایی رخ داده است. لطفاً دوباره تلاش کنید.")
        return SHOW_OPTIONS

# ثبات اطلاعات آزمون تاقل
async def handle_toefl_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle the "بازگشت 🔙" button
    if update.message.text == "بازگشت 🔙":
        current_step = context.user_data.get('toefl_step', TOEFL_USERNAME)
        if current_step > TOEFL_USERNAME:
            context.user_data['toefl_step'] -= 1  # Go back one step
            return await handle_toefl_registration(update, context)  # Restart the previous step
        else:
            await return_to_main_menu(update, context)
            return SHOW_OPTIONS

    # Determine the current step
    current_step = context.user_data.get('toefl_step', TOEFL_USERNAME)

    # Step: Collect ETS username
    if current_step == TOEFL_USERNAME:
        await update.message.reply_text(
            "لطفاً نام کاربری ETS خود را وارد کنید:",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['toefl_step'] = TOEFL_PASSWORD
        return TOEFL_PASSWORD

    # Step: Collect ETS password
    elif current_step == TOEFL_PASSWORD:
        context.user_data['username'] = update.message.text
        await update.message.reply_text(
            "لطفاً رمز عبور ETS خود را وارد کنید:",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['toefl_step'] = TOEFL_EXAM_TYPE
        return TOEFL_EXAM_TYPE

    # Step: Select exam type
    elif current_step == TOEFL_EXAM_TYPE:
        context.user_data['password'] = update.message.text
        await update.message.reply_text(
            "لطفاً نوع آزمون خود را مشخص کنید (حضوری یا Home Edition):",
            reply_markup=ReplyKeyboardMarkup([["حضوری", "Home Edition"], ["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['toefl_step'] = TOEFL_EXAM_DATE
        return TOEFL_EXAM_DATE

    # Step: Collect exam date
    elif current_step == TOEFL_EXAM_DATE:
        context.user_data['exam_type'] = update.message.text
        await update.message.reply_text(
            "لطفاً تاریخ آزمون را وارد کنید (به‌صورت YYYY-MM-DD):",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        # Skip TOEFL_CENTER if exam type is "Home Edition"
        if context.user_data['exam_type'] == "Home Edition":
            context.user_data['toefl_step'] = TOEFL_TIME
            return await handle_toefl_registration(update, context)
        else:
            context.user_data['toefl_step'] = TOEFL_CENTER
            return TOEFL_CENTER

    # Step: Collect exam center (only for حضوری)
    elif current_step == TOEFL_CENTER:
        context.user_data['exam_date'] = update.message.text
        await update.message.reply_text(
            "لطفاً مرکز آزمون خود را وارد کنید:",
            reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['toefl_step'] = TOEFL_TIME
        return TOEFL_TIME

    # Step: Select exam time
    elif current_step == TOEFL_TIME:
        if 'exam_date' not in context.user_data:  # For "Home Edition," exam_date is set earlier
            context.user_data['exam_date'] = update.message.text
        await update.message.reply_text(
            "لطفاً زمان آزمون خود را مشخص کنید (صبح یا عصر):",
            reply_markup=ReplyKeyboardMarkup([["صبح", "عصر"], ["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['toefl_step'] = TOEFL_DISCOUNT_CODE
        return TOEFL_DISCOUNT_CODE

    # Step: Ask for discount code availability
    elif current_step == TOEFL_DISCOUNT_CODE:
        await update.message.reply_text(
            "آیا کد تخفیف ETS دارید؟",
            reply_markup=ReplyKeyboardMarkup([["دارم", "ندارم"], ["بازگشت 🔙"]], resize_keyboard=True),
        )
        context.user_data['toefl_step'] = TOEFL_DISCOUNT_RESPONSE
        return TOEFL_DISCOUNT_RESPONSE

    # Step: Handle discount code response
    elif current_step == TOEFL_DISCOUNT_RESPONSE:
        if update.message.text == "دارم":
            await update.message.reply_text(
                "لطفاً کد تخفیف ETS خود را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
            )
        else:
            context.user_data['discount_code'] = "ندارم"
            await update.message.reply_text(
                "اگر یادداشتی دارید وارد کنید، در غیر این صورت تایپ کنید 'ندارم':",
                reply_markup=ReplyKeyboardMarkup([["بازگشت 🔙"]], resize_keyboard=True),
            )
        context.user_data['toefl_step'] = TOEFL_FINALIZE
        return TOEFL_FINALIZE

    # Step: Finalize the process
    elif current_step == TOEFL_FINALIZE:
        context.user_data['note'] = update.message.text
        await update.message.reply_text(
            "فرآیند ثبت‌نام با موفقیت تکمیل شد! به منوی اصلی بازگشتید.",
            reply_markup=ReplyKeyboardMarkup([["بازگشت به منوی اصلی"]], resize_keyboard=True),
        )
        context.user_data.clear()
        return SHOW_OPTIONS

    # Handle unexpected input
    else:
        await update.message.reply_text("خطایی رخ داده است. لطفاً دوباره تلاش کنید.")
        return SHOW_OPTIONS


# ثبت اطلاعات برای پرداخت اپلیکیشن فی دانشگاه ها
async def handle_application_fee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle the "بازگشت 🔙" button to return to the main menu and stop the process
    if update.message.text == "بازگشت 🔙":
        await return_to_main_menu(update, context)
        # Clear all user data related to this process
        context.user_data.clear()
        return SHOW_OPTIONS

    # Determine the current step
    current_step = context.user_data.get('application_step', APPLICANT_INFO)

    # Step: Determine who the application is for
    if current_step == APPLICANT_INFO:
        await update.message.reply_text(
            "سفارش را برای چه کسی ثبت می کنید؟",
            reply_markup=ReplyKeyboardMarkup([["خودم", "فرد دیگری"], ["بازگشت 🔙"]], resize_keyboard=True)
        )
        context.user_data['application_step'] = APPLICANT_NAME
        return APPLICANT_NAME

    # Step: Collect the applicant's name
    elif current_step == APPLICANT_NAME:
        context.user_data['applicant_for'] = update.message.text
        await update.message.reply_text("لطفا نام پاسپورتی متقاضی به انگلیسی وارد کنید:")
        context.user_data['application_step'] = APPLICANT_LAST_NAME
        return APPLICANT_LAST_NAME

    # Step: Collect the applicant's last name
    elif current_step == APPLICANT_LAST_NAME:
        context.user_data['applicant_name'] = update.message.text
        await update.message.reply_text("لطفا نام خانوادگی پاسپورتی متقاضی به انگلیسی وارد کنید:")
        context.user_data['application_step'] = APPLICATION_LOOP
        return APPLICATION_LOOP

    # Step: Collect the number of applications
    elif current_step == APPLICATION_LOOP:
        context.user_data['applicant_last_name'] = update.message.text
        await update.message.reply_text("لطفا تعداد ارسال اپلیکیشن را بین 1 تا 5 وارد کنید:")
        context.user_data['application_step'] = APPLICATION_COUNT
        return APPLICATION_COUNT

    # Step: Validate and store the application count
    elif current_step == APPLICATION_COUNT:
        try:
            application_count = int(update.message.text)
            if 1 <= application_count <= 5:
                context.user_data['application_count'] = application_count
                context.user_data['application_data'] = [{} for _ in range(application_count)]
                context.user_data['current_index'] = 0

                await update.message.reply_text("اطلاعات مرحله 1:\nلینک ورود به صفحه اپلیکیشن دانشگاه:")
                context.user_data['application_step'] = APPLICATION_DETAILS
                return APPLICATION_DETAILS
            else:
                await update.message.reply_text("عدد وارد شده باید بین 1 تا 5 باشد.")
                return APPLICATION_LOOP
        except ValueError:
            await update.message.reply_text("لطفا یک عدد معتبر وارد کنید.")
            return APPLICATION_LOOP

    # Step: Collect details for each application
    elif current_step == APPLICATION_DETAILS:
        application_data = context.user_data['application_data']
        current_index = context.user_data['current_index']

        if 'link' not in application_data[current_index]:
            application_data[current_index]['link'] = update.message.text
            await update.message.reply_text("مبلغ اپلیکیشن فی به یورو:")
            return APPLICATION_DETAILS

        elif 'fee' not in application_data[current_index]:
            try:
                application_data[current_index]['fee'] = float(update.message.text)
                await update.message.reply_text("نام کاربری:")
                return APPLICATION_DETAILS
            except ValueError:
                await update.message.reply_text("لطفا مبلغ معتبر وارد کنید.")
                return APPLICATION_DETAILS

        elif 'username' not in application_data[current_index]:
            application_data[current_index]['username'] = update.message.text
            await update.message.reply_text("رمز عبور:")
            return APPLICATION_DETAILS

        elif 'password' not in application_data[current_index]:
            application_data[current_index]['password'] = update.message.text
            context.user_data['application_data'][current_index] = application_data[current_index]

            if current_index + 1 < context.user_data['application_count']:
                context.user_data['current_index'] += 1
                await update.message.reply_text(
                    f"اطلاعات مرحله {context.user_data['current_index'] + 1}:\nلینک ورود به صفحه اپلیکیشن دانشگاه:"
                )
                return APPLICATION_DETAILS
            else:
                await update.message.reply_text(
                    "تمام اطلاعات اپلیکیشن‌ها با موفقیت ثبت شد! آیا می‌خواهید اطلاعات جدیدی برای فرد دیگری ثبت کنید؟",
                    reply_markup=ReplyKeyboardMarkup([["بله", "خیر"], ["بازگشت 🔙"]], resize_keyboard=True)
                )
                context.user_data['application_step'] = APPLICATION_RESTART
                return APPLICATION_RESTART

    # Step: Restart for another applicant
    elif current_step == APPLICATION_RESTART:
        if update.message.text == "بله":
            await update.message.reply_text("سفارش را برای چه کسی ثبت می کنید؟")
            context.user_data['application_step'] = APPLICANT_NAME
            context.user_data.pop('application_data', None)  # Reset application data
            context.user_data.pop('current_index', None)
            context.user_data.pop('application_count', None)
            return APPLICANT_NAME
        elif update.message.text == "خیر":
            await return_to_main_menu(update, context)
            context.user_data.clear()  # Clear all data to prevent unintended behavior
            return SHOW_OPTIONS
        else:
            await update.message.reply_text("لطفاً یکی از گزینه‌های معتبر را انتخاب کنید.")
            return APPLICATION_RESTART

# تابع اصلی
async def main():
    application = Application.builder().token("7418611705:AAFZx5wqrHisM0vFup9zq56bvlpQmFYsLls").build()

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

            # GRE Registration Steps
            GRE_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_EXAM_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_TEST_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_EXAM_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_CENTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_DISCOUNT_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_DISCOUNT_RESPONSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_FINALIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],
            GRE_NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_registration)],

            # TOEFL Registration Steps
            TOEFL_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_EXAM_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_EXAM_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_CENTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_DISCOUNT_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_DISCOUNT_RESPONSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],
            TOEFL_FINALIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_registration)],

            # Application Fee Registration Steps
            APPLICANT_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_fee)],
            APPLICANT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_fee)],
            APPLICANT_LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_fee)],
            APPLICATION_LOOP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_fee)],
            APPLICATION_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_fee)],
            APPLICATION_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_fee)],
            APPLICATION_RESTART: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_fee)],

            # SOS options
            SOS_OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sos_options)],

            # TOEFL details and FAQs
            TOEFL_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_details)],
            TOEFL_FAQS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_toefl_faqs)],

            # GRE details and FAQs
            GRE_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_details)],
            GRE_FAQS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gre_faqs)],



        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Start bot
    print("Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

    
