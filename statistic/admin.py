from django.contrib import admin
from .models import Miner, HashRate, TimeStart, Balance


def make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)


make_visible.short_description = "Mark selected miners as visible"


def make_invisible(modeladmin, request, queryset):
    queryset.update(visible=False)


make_invisible.short_description = "Mark selected miners as invisible"


@admin.register(Miner)
class MinerAdmin(admin.ModelAdmin):
    list_display = ['name', 'worker', 'is_online', 'visible']
    actions = [make_visible, make_invisible]


@admin.register(HashRate)
class HRAdmin(admin.ModelAdmin):
    list_display = ['miner', 'time', 'hr']
    list_filter = ['time']


@admin.register(TimeStart)
class TimeStartAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', ]
    list_filter = ['time']


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['value', 'description', 'updated', ]
    list_filter = ['updated']
