from django.contrib import admin

from .models import Summoner, ChampionData


# Register your models here.
class ChampionDataInline(admin.TabularInline):
    model = ChampionData


class ChampionDataAdmin(admin.ModelAdmin):
    readonly_fields = (
        'summoner',
        'name',
        'game_id',
        'mastery_level',
        'mastery_points',
        'highest_grade',
        'games',
        'wins',
        'losses',
        'kills',
        'deaths',
        'assists',
        'cs_count',
        'first_blood_count',
        'turret_kills',
        'inhibitor_kills',
        'wards_placed',
        'ward_kills',
        'penta_kills',
        'quadra_kills',
        'triple_kills',
        'double_kills',
        'largest_killing_spree',
        'largest_cs_count',
        'last_update',
    )


class SummonerAdmin(admin.ModelAdmin):
    readonly_fields = (
        'name',
        'game_id',
        'profile_icon_id',
    )
    inlines = [
        ChampionDataInline,
    ]


admin.site.register(ChampionData, ChampionDataAdmin)
admin.site.register(Summoner, SummonerAdmin)
