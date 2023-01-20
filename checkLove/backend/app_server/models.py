from django.db import models


class AppResult(models.Model):
    lover = models.CharField(verbose_name='Любовник/Любовница', max_length=255, default=None)
    friend_best = models.CharField(verbose_name='Лучший друг', max_length=255, default=None)
    number_app = models.IntegerField(verbose_name='Номер заказа')

    def __str__(self):
        return self.number_app


class ApplicationUser(models.Model):

    name = models.CharField(verbose_name='Имя', max_length=100)
    id_user = models.CharField(verbose_name='id пользователя', max_length=100)
    link_user = models.CharField(verbose_name='Ссылка жертвы', max_length=100)
    data_start = models.DateTimeField(verbose_name='Время начала заказа')
    data_end = models.DateTimeField(verbose_name='Дата конец заказа')
    result = models.ForeignKey(AppResult, verbose_name='Результат', on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Rate(models.Model):
    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    name = models.CharField(verbose_name='Наименование', max_length=100)
    descriptions = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.name


class OrderUser(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    id_user = models.CharField(verbose_name='ID пользователя', max_length=100)
    id_tg = models.CharField(verbose_name='ID заказчика', max_length=100)
    rate = models.ForeignKey(Rate, verbose_name='Тариф', on_delete=models.RESTRICT)
    data_start = models.DateTimeField(verbose_name='Время начала заказа')
    data_end = models.DateTimeField(verbose_name='Дата конец заказа')



