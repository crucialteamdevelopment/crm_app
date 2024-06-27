from django.db import models
from django.conf import settings
from users.models import CustomUser

# Create your models here.


class Team(models.Model):
    class Meta:
        db_table = 'teams'

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='leader_of_teams'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teams',
        through='TeamMembership'
    )

    def __str__(self):
        return self.name

class TeamMembership(models.Model):
    class Meta:
        db_table = 'team_membership'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"
