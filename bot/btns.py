from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup
from .Global import BTN
from .models import Category, Product


def but_back(type):
    btn = []
    if type == "back":
        btn = [
            [KeyboardButton("🔙 Back")]
        ]
    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def key_btn(type, lang='uz', ctg: Category = None):
    btn = []
    if type == 'contact':
        btn = [
            [KeyboardButton(f"{BTN['CONTACT'][lang]}", request_contact=True)],
            [KeyboardButton("🔙 Back")]
        ]
    elif type == "menu":
        btn = [
            [KeyboardButton(f"{BTN['MENU']['menu'][lang]}")],
            [KeyboardButton("🛒 Buyurtmalarim")],
            [KeyboardButton("💬 Fikringiz"), KeyboardButton("⚙️ Sozlamalar")]
        ]

    elif type == 'ctg':
        category = Category.objects.all()
        btn = []
        for i in range(1, len(category), 2):
            btn.append([
                KeyboardButton(category[i - 1].name),
                KeyboardButton(category[i].name),

            ])
        if len(category) % 2:
            btn.append([KeyboardButton(category[len(category) - 1].name)])
        btn.append([KeyboardButton("🔙 Back"), KeyboardButton("🏘 Home")])

    elif type == 'prods':
        roots = Product.objects.filter(ctg=ctg)
        for i in range(1, len(roots), 2):
            btn.append([
                KeyboardButton(roots[i - 1].name),
                KeyboardButton(roots[i].name),
            ])
        if len(roots) % 2:
            btn.append([KeyboardButton(roots[len(roots) - 1].name)])
        btn.append([KeyboardButton("🔙 Back"), KeyboardButton("🏘 Home")])

    elif type == 'prod':
        btn = [
            [KeyboardButton("🔙 Back"), KeyboardButton("🏘 Home")]
        ]

    elif type == 'admin':
        btn = [
            [KeyboardButton("🛂Boshqaruv"),KeyboardButton('👥Foydalanuvchila ro`yhati')],
            [KeyboardButton("🏘Logout")]
        ]
    return ReplyKeyboardMarkup(btn, resize_keyboard=True)




def inline(type, product_id=None, count=1):
    btn = []
    if type == 'lang':
        btn = [
            [
                InlineKeyboardButton('🇺🇿 Uz', callback_data='uz'),
                InlineKeyboardButton('🇷🇺 Ru', callback_data='ru'),
                InlineKeyboardButton('🇺🇸 En', callback_data='en')
            ]
        ]
    elif type == 'savat':
        btn = [
            [
                InlineKeyboardButton('-', callback_data=f'minus_{product_id}_{count}'),
                InlineKeyboardButton(f'{count}', callback_data='nothing'),
                InlineKeyboardButton('+', callback_data=f'plus_{product_id}_{count}')
            ],
            [
                InlineKeyboardButton("🛒 Savatga qo'shish", callback_data=f'cart_{product_id}_{count}')
            ]
        ]

    return InlineKeyboardMarkup(btn)
