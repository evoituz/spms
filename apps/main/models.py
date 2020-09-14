from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class GeneralSettings(SingletonModel):
    course_usd_to_uzs = models.DecimalField('Курс доллара в суммах', max_digits=12, decimal_places=0, null=True, blank=True)

    verbose_name = 'Настройка сайта'
    verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return '%s' % self.course_usd_to_uzs
