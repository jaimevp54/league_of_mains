from django.db import models


# Create your models here.
class SummonerData(models.Model):
    summoner_name = models.CharField(max_length=25, editable=False)
    champion_name = models.CharField(max_length=25, editable=False)
    wins = models.IntegerField()
    losses = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    penta_kills = models.IntegerField()
    quadra_kills = models.IntegerField()
    triple_kills = models.IntegerField()
    double_kills = models.IntegerField()
    largest_killing_spree = models.IntegerField()
    largest_cs_count = models.IntegerField()
    favorite_summ_spell_1 = models.CharField(max_length=25)
    favorite_summ_spell_2 = models.CharField(max_length=25)

    @property
    def kda(self):
        return round((self.kills + self.deaths + self.assists) / 3, 3)
