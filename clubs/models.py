from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class ClubMember(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
