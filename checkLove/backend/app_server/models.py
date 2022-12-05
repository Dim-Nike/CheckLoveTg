from django.db import models


class AppResult(models.Model):
    lover = models.CharField(verbose_name='Любовник/Любовница', max_length=255, default=None)
    friend_best = models.CharField(verbose_name='Лучший друг', max_length=255, default=None)
    number_app = models.IntegerField(verbose_name='Номер заказа', max_length=10)


class ApplicationUser(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100)
    id_user = models.CharField(verbose_name='id пользователя', max_length=100)
    link_user = models.CharField(verbose_name='Ссылка жертвы', max_length=100)
    data_start = models.DateTimeField(verbose_name='Время начала заказа')
    data_end = models.DateTimeField(verbose_name='Дата конец заказа')
    result = models.ForeignKey(AppResult, verbose_name='Результат', on_delete=models.RESTRICT)




