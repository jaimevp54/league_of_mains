from django.db import models


from cassiopeia.type.api.exception import APIError


# Create your models here.
class Summoner(models.Model):
    name = models.CharField(max_length=25, editable=True)
    game_id = models.IntegerField(editable=True)
    profile_icon_id = models.IntegerField(editable=True)

    def __str__(self):
        return self.name


class ChampionData(models.Model):
    summoner = models.ForeignKey(Summoner)

    name = models.CharField(default='', max_length=25, editable=True)
    game_id = models.IntegerField(default=0, editable=True)
    mastery_level = models.IntegerField(default=0, editable=True)
    mastery_points = models.IntegerField(default=0, editable=True)
    highest_grade = models.CharField(default='0', max_length=2, editable=True)
    games = models.IntegerField(default=0, editable=True)
    wins = models.IntegerField(default=0, editable=True)
    losses = models.IntegerField(default=0, editable=True)
    kills = models.IntegerField(default=0, editable=True)
    deaths = models.IntegerField(default=0, editable=True)
    assists = models.IntegerField(default=0, editable=True)
    cs_count = models.IntegerField(default=0, editable=True)
    first_blood_count = models.IntegerField(default=0, editable=True)
    turret_kills = models.IntegerField(default=0, editable=True)
    inhibitor_kills = models.IntegerField(default=0, editable=True)
    wards_placed = models.IntegerField(default=0, editable=True)
    ward_kills = models.IntegerField(default=0, editable=True)
    penta_kills = models.IntegerField(default=0, editable=True)
    quadra_kills = models.IntegerField(default=0, editable=True)
    triple_kills = models.IntegerField(default=0, editable=True)
    double_kills = models.IntegerField(default=0, editable=True)
    largest_killing_spree = models.IntegerField(default=0, editable=True)
    largest_cs_count = models.IntegerField(default=0, editable=True)
    # time_played = models.DurationField(default=timedelta.min, editable=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def kda(self):
        return round((self.kills + self.assists) / (self.deaths if self.deaths else 1), 3)

    def update(self, summoner, champion, champion_mastery):

        match_list = summoner.match_list(champions=champion, begin_time=self.last_update)

        self.mastery_level = champion_mastery.level
        self.mastery_points = champion_mastery.points
        self.highest_grade = champion_mastery.highest_grade
        self.games += len(match_list)

        for match_reference in match_list:
            try:
                match = match_reference.match(include_timeline=False)
            except APIError as e:
                continue
            for p in match.participants:
                if p.summoner_name == summoner.name:
                    participant = p
                    break

            self.wins += 1 if participant.stats.win else 0
            self.kills += participant.stats.kills
            self.deaths += participant.stats.deaths
            self.assists += participant.stats.assists
            self.cs_count += participant.stats.cs
            self.first_blood_count += 1 if participant.stats.first_blood else 0
            self.turret_kills += participant.stats.turret_kills
            self.penta_kills += participant.stats.penta_kills
            self.quadra_kills += participant.stats.quadra_kills
            self.triple_kills += participant.stats.triple_kills
            self.double_kills += participant.stats.double_kills
            self.inhibitor_kills += participant.stats.inhibitor_kills
            self.wards_placed += participant.stats.wards_placed
            self.ward_kills += participant.stats.ward_kills
            # self.time_played += match.duration
            self.largest_killing_spree = max(self.largest_killing_spree, participant.stats.largest_killing_spree)
            self.largest_cs_count = max(self.largest_cs_count, participant.stats.cs)

        self.losses = self.games - self.wins

    @classmethod
    def create(cls, summoner, champion):
        champion_data = cls(
            summoner=summoner,
            name=champion.name,
            game_id=champion.id,
        )
        return champion_data

    def __str__(self):
        return self.summoner.name + " with " + self.name