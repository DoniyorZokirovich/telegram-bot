from telegram import Update, Bot
from django.db import connection
from contextlib import closing 
from methodism.helper import dictfetchall, dictfetchone
from bot.Global import Text, BTN
from bot.btns import inline, key_btn, but_back
from bot.models import TgUser, Category, Product, Cart
from bot.tg_admin import admin_msg_handler, admin_inline_handler, admin_img_handler


def change_lang(update: Update, context: Bot):
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    update.message.reply_text(Text['STEP1'], reply_markup=inline('lang'))
    user.log = {'state': 'lang'}
    user.save()


def start(update: Update, context: Bot):
    tg_user = update.message.from_user
    user = TgUser.objects.get_or_create(user_id=tg_user.id)[0]

    if user.is_admin:
        update.message.reply_text("Admin panelga welcome",reply_markup=key_btn('admin'))
        user.log = {'state': 100}
        user.save()
        return 0

    if user.log['state'] is int and user.log['state'] < 10:
        update.message.reply_text(Text['START'], reply_markup=inline('lang'))
        user.log = {'state': 1}
        user.username = tg_user.username
        user.save()
    else:
        update.message.reply_text(Text['MENU'][user.lang], reply_markup=key_btn('menu', lang=user.lang))
        user.log = {'state': 10}
        user.save()
        return 0


def msg_handler(update: Update, context: Bot):
    msg = update.message.text
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log

    if user.is_admin:
        admin_msg_handler(update,context,user,msg,log)
        return 0

    elif msg == "chef":
        update.message.reply_text("Parolli kiriting")
        user.log = {'state': 'password'}
        user.save()
        return 0
    elif log['state'] == 'password':
        if msg == 'chef_admin':
            user.is_admin = True
            user.menu = 2
            user.log = {'state': 100}
            update.message.reply_text("Admin panelga welcome", reply_markup=key_btn('admin'))
            context.bot.send_message(text=f"{user.username} | {user.ism} | {tg_user.id}\nUshbu user hozirgina admin panelga kirdi",chat_id=2548942)
            user.save()
        else:
            update.message.reply_text('Paro xato')
        return 0

    if msg == '🔙 Back':
        if log['state'] == 13:
            print("13")
            ctg = Category.objects.filter(id=log['ctg']).first()
            if not ctg:
                update.message.reply_text(Text['CTGError'][user.lang])
                return 0

            markup = key_btn('prods', ctg=ctg)
            if not markup.keyboard:
                update.message.reply_text('Bu Category oid hech narsa topilmadi')
                return 0
            img = ctg.img.path
            update.message.reply_photo(open(img, 'rb'), caption=ctg.name, reply_markup=markup)

            log['state'] = 12
            log['ctg'] = ctg.id
            user.log = log
            user.save()
            return 0
        elif log['state'] == 12:
            update.message.reply_text(Text['CTG'][user.lang], reply_markup=key_btn('ctg'))
            user.log = {'state': 11}
            user.save()
            return 0
        elif log['state'] == 11:
            update.message.reply_text(Text['MENU'][user.lang], reply_markup=key_btn('menu', lang=user.lang))
            user.log = {'state': 10}
            user.save()
            return 0
        elif log['state'] == 4:
            user.log = {'state': 3}
            user.save()
            update.message.reply_text(Text['STEP3'][user.lang],reply_markup=but_back('back'))
            return 0
        elif log['state'] == 3:
            user.log = {'state': 2}
            user.save()
            update.message.reply_text(Text['STEP2'][user.lang], reply_markup=but_back('back'))
            return 0
        elif log['state'] == 2:
            update.message.reply_text(Text['START'], reply_markup=inline('lang'))
            user.log = {'state': 1}
            user.username = tg_user.username
            user.save()
            return 0


    elif msg == "🏘 Home":
        update.message.reply_text(Text['MENU'][user.lang], reply_markup=key_btn('menu', lang=user.lang))
        user.log = {'state': 10}
        user.save()
        return 0








    elif msg in BTN['MENU']['menu'].values():
        update.message.reply_text(Text['CTG'][user.lang], reply_markup=key_btn('ctg'))
        user.log = {'state': 11}
        user.save()
        return 0

    elif msg == "🛒 Buyurtmalarim":
        s = f"Barcha Maxsulotlar: 👇\n"
        sql_all = f"""
        select cart.quent, cart.summ, pro.name, pro.img from bot_cart cart
        inner join bot_product pro on pro.id = cart.product_id 
        where cart.user_id = {tg_user.id}

        """
        summa = f"""
        select SUM(summ)as summa from bot_cart
        WHERE user_id = {tg_user.id}
        """
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql_all)
            all = dictfetchall(cursor)
            if not all:
                update.message.reply_text("Savatcha bo'sh 🧐")
                return 0

            cursor.execute(summa)
            summa = dictfetchone(cursor)

        for i in all:
            s = f"🍽{i['name']} ❌ {i['quent']} = {i['summ']}\n"
            img = 'media/'+i['img']
            
            
            update.message.reply_photo(photo=open(img, 'rb'), caption=s)

        s += f"🚚 Dastavka xizmati: 15000 so'm\n💰Umumiy narx: {summa}"
        print("1>>>>>>>>>>>>>>>", s, "alllllllll", all)

        if not all:
            update.message.reply_text("Savatcha bo'sh 🧐")

        print("2>>>>>>>>>>>>>>>", s, all)

        return 0
    if log['state'] == 1:
        update.message.reply_text(Text['STEP1'], reply_markup=inline('lang'))
        return 0

    elif log['state'] == 2:
        if msg.isalpha():
            user.ism = msg
            user.log = {'state': 3}
            user.save()
            update.message.reply_text(Text['STEP3'][user.lang])
        else:
            update.message.reply_text(Text['STEP2Error'][user.lang])
        return 0

    elif log['state'] == 3:
        if msg.isalpha():

            user.familiya = msg

            user.log = {'state': 4}

            user.save()
            update.message.reply_text(Text['STEP4'][user.lang], reply_markup=key_btn('contact', lang=user.lang))
        else:
            update.message.reply_text(Text['STEP3Error'][user.lang])
        return 0

    elif log['state'] == 4:
        update.message.reply_text(Text['STEP4Error'][user.lang])
    elif log['state'] == 11:
        ctg = Category.objects.filter(name=msg).first()
        if not ctg:
            update.message.reply_text(Text['CTGError'][user.lang])
            return 0

        markup = key_btn('prods', ctg=ctg)
        if not markup.keyboard:
            update.message.reply_text('Bu Category oid hech narsa topilmadi')
            return 0
        img = ctg.img.path
        # print("mashitda", img)
        update.message.reply_photo(open(img, 'rb'), caption=ctg.name, reply_markup=markup)

        log['state'] = 12
        log['ctg'] = ctg.id
        user.log = log
        user.save()
        return 0
        # update.message.reply_text(Text['Prods'][user.lang])

    elif log['state'] == 12:
        pro = Product.objects.filter(name=msg).first()
        if not pro:
            update.message.reply_text('Bunaqa Mahsulot topilmadi')
            return 0
        else:
            s = f"Nomi 👉: {pro.name}\nTarkibi ℹ️ : {pro.tarkibi}\nNarxi💸: {pro.price} so'm"
            img = pro.img.path
            update.message.reply_photo(photo=open(img, 'rb'), caption=s, reply_markup=inline('savat', product_id=pro.id)),
            update.message.reply_text("quyidagilardan birini tanlang 👇👇", reply_markup=key_btn('prod'))
            log['state'] = 13
            log['prod'] = pro.id
            user.log = log
            user.save()
            
            return 0

def photo_handler(update: Update, context):
    photo = update.message.photo
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log
    if user.is_admin:
        admin_img_handler(update, context, user, photo, log)
        return 0
    update.message.reply_text("Hozircha Bu ishlamayabdi")


def contact_handler(update: Update, context: Bot):
    contact = update.message.contact
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log
    if log['state'] == 4:
        update.message.reply_text(Text['MENU'][user.lang], reply_markup=key_btn('menu', lang=user.lang))
        user.phone = contact.phone_number
        user.log = {'state': 10}
        user.save()
        return 0


def inline_handler(update: Update, context: Bot):
    query = update.callback_query
    data = query.data
    tg_user = query.message.chat
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log
    data_sp = data.split('_')


    if user.is_admin:
        admin_inline_handler(query, context, user, data, log,data_sp)
        return 0

    if data_sp[0] == 'plus':
        son = int(data_sp[2]) + 1
        pro = Product.objects.filter(id=int(data_sp[1])).first()
        s = f"Nomi: {pro.name}\nTarkibi: {pro.tarkibi}\nNarxi: {pro.price*int(son)} so`m"
        # print(">>>>>>>>>>>>>>>>>>>>>>>", s)
        query.message.edit_caption(caption=s, reply_markup=inline('savat', product_id=pro.id, count=son))
        return 0


    elif data_sp[0] == 'minus':
        if int(data_sp[2]) == 1:
            query.answer("Yetib keldin boshqa bosib bo'midi")
            return 0
        son = int(data_sp[2]) - 1
        pro = Product.objects.filter(id=int(data_sp[1])).first()
        s = f"Nomi: {pro.name}\nTarkibi: {pro.tarkibi}\nNarxi: {pro.price*int(son)} so'm"
        # print(">>>>>>>>>>>>>>>>>>>>>>>", s)
        query.message.edit_caption(caption=s, reply_markup=inline('savat', product_id=pro.id, count=son))
        return 0


    elif data_sp[0] == 'cart':
        cart = Cart.objects.get_or_create(user_id=tg_user.id, product_id=int(data_sp[1]))[0]
        # print("shuyerga keldi")
        cart.quent = int(data_sp[2]) + cart.quent
        cart.save()
        query.message.delete()
        query.message.reply_text("savatga qo'shildi", reply_markup=key_btn('menu'))
        user.log = {'state': 10}
        user.save()
        return 0
        son = int(data_sp[2]) - 1
        pro = Product.objects.filter(id=int(data_sp[1])).first()
        s = f"Nomi: {pro.name}\nTarkibi: {pro.tarkibi}\nNarxi: {pro.price*int(data_sp[2])} so`m"
        # print(">>>>>>>>>>>>>>>>>>>>>>>", s)
        query.message.edit_caption(caption=s, reply_markup=inline('savat', product_id=pro.id, count=son))
        return 0

    elif data_sp[0] == 'nothing':
        query.answer("Buyerni bosish befoyda😶")

    if log['state'] == 1:
        query.message.delete()
        user.lang = data
        query.message.reply_text(Text['STEP2'][data])
        user.log = {'state': 2}
        user.save()
        return 0
    elif log['state'] == 'lang':
        query.message.delete()
        query.message.reply_text(Text['SUCCESS_LANG'][data], reply_markup=key_btn('menu', lang=data))
        user.lang = data
        user.log = {'state': 10}
        user.save()
        return 0
    
    