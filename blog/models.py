from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое статьи')
    photo = models.ImageField(upload_to='blog/', verbose_name='изображение', blank=True, null=True)
    views_count = models.IntegerField(verbose_name='количество просмотров')
    published_date = models.DateTimeField(verbose_name='дата публикации')
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
