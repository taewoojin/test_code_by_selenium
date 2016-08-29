from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    pass

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    list = models.ForeignKey(List, default=None)
    text = models.TextField(default='')
