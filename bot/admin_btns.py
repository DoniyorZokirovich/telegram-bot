from telegram import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton


def admin_btns(type):
    btn = []
    if type == "conf":
        btn = [
            [KeyboardButton('✅Xa'),KeyboardButton("❌Yo`q")]
        ]
    elif type =='menu':
        btn = [
            [KeyboardButton("🍑Categoriyalar"),KeyboardButton("Maxsulotlar")],
            [KeyboardButton("🔙 Back")]
        ]
    elif type == 'create_ctg':
        btn = [
            [KeyboardButton("🆕Yangi Categoriya qo'shish")]
        ]
    return ReplyKeyboardMarkup(btn,resize_keyboard=True)

def adbtn_inline(type=None,page=1,count=0,ctg=None):
    btn =[]
    if type == 'ctgs':
        btn = [
            [InlineKeyboardButton('⏮',callback_data=f"ctg_prev_{ctg.id}_{page}"),
            InlineKeyboardButton(f"{page}/{count}",callback_data=f"ctg_none"),
            InlineKeyboardButton("⏭",callback_data=f"ctg_next_{ctg.id}_{page}")],
            [InlineKeyboardButton("✏️Tahrirlash", callback_data=f"ctg_edit_{ctg.id}_{page}")],
            [InlineKeyboardButton("🗑O'chirib tashlash", callback_data=f"ctg_delete_{ctg.id}_{page}")],
        ]
    elif type == "ctg_delete_conf":
        btn = [
            [InlineKeyboardButton("🗑 O'chirish", callback_data=f'ctg_delete_conf_yes_{page}_{ctg.id}'),
             InlineKeyboardButton("🔙Ortga", callback_data=f'ctg_delete_conf_no_{page}_{ctg.id}')]
        ]
    return InlineKeyboardMarkup(btn)


