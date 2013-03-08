from django.contrib import admin
from player.models import Player


class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'phone', 'last_seen_at']})
    ]
    list_display = ('id', 'username', 'phone', 'created_at', 'last_seen_at')


admin.site.register(Player, PlayerAdmin)
