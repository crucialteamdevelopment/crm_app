from django.db import models

class Bookmark(models.Model):
    bookmark_name = models.CharField(max_length=255)
    link = models.URLField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    code = models.CharField(max_length=4)

    def __str__(self):
        return self.bookmark_name
