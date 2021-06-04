import logging
import requests
from telegram.ext import *
from telegram import *
import connect

bot = Bot(<token>)


def start(update, context):
    update.message.reply_text("Welcome to Covid India Vaccine bot\n"
                              "Please enter keyword <b>vaccine</b> to check your nearest vaccination center and slots availability\n"
                              "or you can also enter your area <b>pincode</b> to check details",parse_mode="HTML"
                              )


def echo(update, context):
    message = update.message.text
    message=message.lower()
    if message == "hello":
        update.message.reply_text("hello")
    elif message == "vaccine":
        button(update, context)
    elif message.isdigit() and len(message) == 6:
        msg = connect.pincode(message)
        if len(msg) == 0:
            update.message.reply_text("No vaccines stock is available in your area\n"
                                      "please visit https://www.cowin.gov.in/ for more details")
        else:
            update.message.reply_text(msg)
    else:
        update.message.reply_text("Please enter correct input")


def button(update, context):
    keyboard = [[
        InlineKeyboardButton('Andaman And Nicobar Islands', callback_data="1"),
        InlineKeyboardButton('Andhra Pradesh', callback_data="2"),
        InlineKeyboardButton('Arunachal Pradesh', callback_data="3")
    ],
        [InlineKeyboardButton('Assam', callback_data="4"),
         InlineKeyboardButton('Bihar', callback_data="5"),
         InlineKeyboardButton('Chandigarh', callback_data="6"),
         ],
        [InlineKeyboardButton('Chhattisgarh', callback_data="7"),
         InlineKeyboardButton('Dadra And Nagar Haveli', callback_data="8"),
         InlineKeyboardButton('Daman And Diu', callback_data="37"),
         ],
        [InlineKeyboardButton('Delhi', callback_data="9"),
         InlineKeyboardButton('Goa', callback_data="10"),
         InlineKeyboardButton('Gujarat', callback_data="11"),
         ],
        [InlineKeyboardButton('Haryana', callback_data="12"),
         InlineKeyboardButton('Himachal Pradesh', callback_data="13"),
         InlineKeyboardButton('Jammu And Kashmir', callback_data="14"),
         ],
        [InlineKeyboardButton('Jharkhand', callback_data="15"),
         InlineKeyboardButton('Karnataka', callback_data="16"),
         InlineKeyboardButton('Kerala', callback_data="17"),
         ],
        [InlineKeyboardButton('Ladakh', callback_data="18"),
         InlineKeyboardButton('Lakshadweep', callback_data="19"),
         InlineKeyboardButton('Madhya Pradesh', callback_data="20"),
         ],
        [InlineKeyboardButton('Maharashtra', callback_data="21"),
         InlineKeyboardButton('Manipur', callback_data="22"),
         InlineKeyboardButton('Meghalaya', callback_data="23"),
         ],
        [InlineKeyboardButton('Mizoram', callback_data="24"),
         InlineKeyboardButton('Nagaland', callback_data="25"),
         InlineKeyboardButton('Odisha', callback_data="26"),
         ],
        [InlineKeyboardButton('Puducherry', callback_data="27"),
         InlineKeyboardButton('Punjab', callback_data="28"),
         InlineKeyboardButton('Rajasthan', callback_data="29"),
         ],
        [InlineKeyboardButton('Sikkim', callback_data="30"),
         InlineKeyboardButton('Tamil Nadu', callback_data="31"),
         InlineKeyboardButton('Telangana', callback_data="32"),
         ],
        [InlineKeyboardButton('Tripura', callback_data="33"),
         InlineKeyboardButton('Uttar Pradesh', callback_data="34"),
         InlineKeyboardButton('Uttarakhand', callback_data="35"),
         ],
        [InlineKeyboardButton('West Bengal', callback_data="36")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please select the state", reply_markup=reply)


def handler(update, context):
    query = update.callback_query
    if int(query.data) < 38:
        districts(update, context, query.data)
    else:
        if len(connect.showcenter(query.data)) == 0:
            bot.send_message(
                chat_id=update.effective_chat.id,
                text="No vaccines stock is available in your area\n"
                     "please visit https://www.cowin.gov.in/ for more details"
            )
        else:
            bot.send_message(
                chat_id=update.effective_chat.id,
                text=connect.showcenter(query.data)
            )


def districts(update, context, link):
    lists = connect.get_states(link)
    buttons = []
    q = len(lists[0]) // 3
    j = 0
    for i in range(q):
        l = []
        l.append(InlineKeyboardButton(lists[0][j], callback_data=1000+lists[1][j]))
        l.append(InlineKeyboardButton(lists[0][j + 1], callback_data=1000+lists[1][j + 1]))
        l.append(InlineKeyboardButton(lists[0][j + 2], callback_data=1000+lists[1][j + 2]))
        j = j + 3
        buttons.append(l)
    l = []
    for i in range(len(lists[0]) % 3):
        l.append(InlineKeyboardButton(lists[0][j + i], callback_data=1000+lists[1][j + i]))
    buttons.append(l)
    reply = InlineKeyboardMarkup(buttons)
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please select the district",
        reply_markup=reply
    )


def error(update, context):
    print(context.error)


def main():
    updater = Updater(<token>, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CallbackQueryHandler(handler))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
