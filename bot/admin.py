from django.contrib import admin

from bot.models import TgUser, Category, Product, Cart

admin.site.register(TgUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
