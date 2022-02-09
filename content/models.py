from django.db import models  # type: ignore


class News(models.Model):
    """
    Class model for containing all the news parsed for 5 years
    """

    newsId = models.IntegerField()
    tmb = models.ImageField(upload_to="tmbs")
    title = models.CharField(max_length=255)
    excerpt = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    count = models.CharField(max_length=255)
    rcm = models.CharField(max_length=255)

    def __str__(self):
        return self.title
