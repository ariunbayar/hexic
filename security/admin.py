# coding: utf-8
from security.models import Account
from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Утасны дугаар', {'fields': ['phone_number']}),
        ('Нууц дугаар',   {'fields': ['pin_code']}),
        ('Credit',   {'fields': ['credit']})
    ]

    list_display = ('phone_number', 'credit')

admin.site.register(Account, AccountAdmin)
