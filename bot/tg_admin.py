from contextlib import closing

import requests
from PIL import Image
from django.core.files.images import ImageFile

from django.db import connection
from methodism import dictfetchall, dictfetchone
from telegram import Update,PhotoSize, TelegramObject

from bot.Global import Text
from bot.admin_btns import adbtn_inline, admin_btns
from bot.btns import key_btn
from bot.models import Category


def admin_msg_handler(update:Update,context,user,msg,log):
    if msg == '👥Foydalanuvchila ro`yhati':
        user = "select user_id,ism ,familiya ,username  from bot_tguser limit 10"
        cnt = 'select COUNT(*) as cnt from bot_tguser bt'
        with closing(connection.cursor()) as cursor:
            cursor.execute(user)
            all = dictfetchall(cursor)

            cursor.execute(cnt)
            cnt = dictfetchone(cursor)
        s = f"Umumiy {cnt['cnt']} ta odam bor\n\n"
        for i in all:
            s+= f"ID: {i['user_id']} \nName: {i['ism']} {i['familiya']}\n\n"
        update.message.reply_text(s)

    elif msg == "🏘Logout":
        update.message.reply_text("😡Rostan ham chiqmoqchimisiz",reply_markup=admin_btns('conf'))
        user.log = {'state':101}
        user.save()
        return 0
    elif msg == "🛂Boshqaruv":
        update.message.reply_text("Bazada quyidagi ro`yhatlar bor", reply_markup=admin_btns('menu'))
        user.log = {'state': 105}
        user.save()
        return 0
    elif msg == "🍑Categoriyalar":
        ctg = Category.objects.all()
        update.message.reply_text(".",reply_markup=admin_btns("create_ctg"))
        update.message.reply_photo(open(ctg[0].img.path,'rb'),
                                   caption=ctg[0].name,reply_markup=adbtn_inline('ctgs',count=len(ctg), ctg=ctg[0]))


    elif msg == '🆕Yangi Categoriya qo\'shish':
        update.message.reply_text("Categoriya uchun Nom kiriting👇👇")
        user.log = {'state': 110}
        user.save()
        return 0

    if log['state'] == 101:
        if msg == "✅Xa":
            update.message.reply_text(Text["MENU"][user.lang],reply_markup=key_btn('menu',lang=user.lang))
            user.log = {'state':10}
            user.is_admin = False
            user.menu = 1
            user.save()
            return 0
        else:
            update.message.reply_text("Fikringizni xurmat qilamiz",reply_markup=key_btn('admin'))
            user.log = {'state':100}
            user.save()
            return 0


    elif log['state'] == 105:
        if msg == "🔙 Back":
            update.message.reply_text("Glavniy panelga qaytiz", reply_markup=key_btn('admin'))
            user.log = {'state': 100}
            user.save()
            return 0
    elif log['state'] == 110:
        update.message.reply_text("Endi Shu ctg ga mos Rasm Yuboring")
        log['new_ctg'] = msg
        log['state'] = 111
        user.log = log
        user.save()
        return 0
    elif log['state'] == 111:
        update.message.reply_text("Rasm Yubor Mazgi")
        return 0
    elif log['state'] == 112:
        if msg == "✅Xa":
            tgimg = context.bot.get_file(file_id=log['ctg_file_id'])
            print('xa ichi')

            img_url = tgimg.file_path
            img = Image.open(requests.get(img_url, stream=True).raw)
            img.save(f'media/{tgimg.file_unique_id}.png')
            category = Category.objects.create(name=log['new_ctg'])
            category.img.save(f'media/{tgimg.file_unique_id}.png',
                              ImageFile(open(f'media/{tgimg.file_unique_id}.png', 'rb')))

            ctg = Category.objects.all()
            update.message.reply_text("Yangi Categoriya qo'shildi", reply_markup=admin_btns('create_ctg'))
            update.message.reply_photo(open(ctg[0].img.path, 'rb'),
                                       caption=ctg[0].name,
                                       reply_markup=adbtn_inline('ctgs', count=len(ctg), ctg=ctg[0]))

        else:
            ctg = Category.objects.all()
            update.message.reply_text("Categoriya Qo'shilmadi", reply_markup=admin_btns('create_ctg'))
            update.message.reply_photo(open(ctg[0].img.path, 'rb'),
                                       caption=ctg[0].name,
                                       reply_markup=adbtn_inline('ctgs', count=len(ctg), ctg=ctg[0]))
        return 0



def admin_img_handler(update: Update, context, user, photo: [PhotoSize], log):
    if log['state'] == 111:
        update.message.reply_photo(photo[0], caption=log['new_ctg'])
        update.message.reply_text("Yuqoridagi ma'lumotlarni Saqlaymizmi?", reply_markup=admin_btns('conf'))
        log['state'] = 112
        log['ctg_file_id'] = photo[2].file_id
        log['ctg_file_unique_id'] = photo[2].file_unique_id
        log['ctg_file_width'] = photo[2].width
        log['ctg_file_height'] = photo[2].height

        user.log = log
        user.save()
        return 0

def admin_inline_handler(query:Update, context, user, data, log,data_sp):
    print("\nuser==",user, "\ndata==",data, "\nlog==",log, "\ndata_sp==",data_sp)

    if data_sp[0] == 'ctg':
        ctgs = Category.objects.all()
        if data_sp[1] == 'prev':
            if int(data_sp[-1]) <= 1:
                query.answer("Boshqa yo`q")
                return 0
            else:
                page = int(data_sp[-1])-2
                ctg = ctgs[page]
                query.message.delete()
                query.message.reply_photo(open(ctg.img.path, 'rb'),
                                          caption=ctg.name,
                                          reply_markup=adbtn_inline('ctgs', count=len(ctgs),
                                                                    ctg=ctg,
                                                                    page=page+1
                                                                    ))
        elif data_sp[1] == 'next':
            if int(data_sp[-1]) >= len(ctgs):
                query.answer("Yetib kelding")
                return 0
            else:
                query.message.delete()
                query.message.reply_photo(open(ctgs[int(data_sp[-1])].img.path, 'rb'),
                                          caption=ctgs[int(data_sp[-1])].name,
                                           reply_markup=adbtn_inline('ctgs', count=len(ctgs),
                                                                     ctg=ctgs[int(data_sp[-1])] ,
                                                                     page=int(data_sp[-1])+1
                                                                     ))
                return 0

        elif data_sp[1] == 'delete':
            if data_sp[2] == 'conf':
                ctg = Category.objects.filter(id=int(data_sp[-1])).first()
                if data_sp[3] == 'no':
                    markup = adbtn_inline(
                            "ctgs",
                            count=len(ctgs),
                            ctg=ctg,
                            page=int(data_sp[-2])
                        )
                    query.message.edit_reply_markup(reply_markup=markup)
                    return 0
                elif data_sp[3] == 'yes':
                    ctg.delete()
                    query.answer(f"{ctg.name} o'chirib yuborildi")
                    query.message.reply_photo(open(ctgs[0].img.path, 'rb'),
                                                  caption=ctgs[0].name,
                                                  reply_markup=adbtn_inline('ctgs', count=len(ctgs), ctg=ctgs[0]))
                    return 0

            else:
                ctg = Category.objects.filter(id=int(data_sp[2])).first()
                if not ctg:
                    query.answer("Bunaqa Categoriya yo'q yoki qandaydir xatolik")
                    return 0
                query.message.edit_reply_markup(reply_markup=adbtn_inline('ctg_delete_conf', page=int(data_sp[-1]),
                                                                              ctg=ctg))
                return 0



