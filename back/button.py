from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup


button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="My vocabluary"),KeyboardButton(text="Game with words")],
        [KeyboardButton(text="Guess word by Audio"),KeyboardButton(text="Add new words")],
        [KeyboardButton(text="Improve Reading skill"),KeyboardButton(text="Improve Listening skill with audiobooks")]

    ],resize_keyboard=True
)
delete_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Delete word",callback_data="Delete")]
    ]
)
agree = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🟩Yes"),KeyboardButton(text = "🟥No")]
    ]
)
mylevel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Beginner")],
        [KeyboardButton(text="Elementary")],
        [KeyboardButton(text="Intermediate")],
        [KeyboardButton(text="Advanced")],
        [KeyboardButton(text="Expert")]

    ]
)

