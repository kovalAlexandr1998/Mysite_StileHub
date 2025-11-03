from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"{self.name} — {self.email}"

    class Meta:
        verbose_name = "Сообщение с контактов"
        verbose_name_plural = "Сообщения с контактов"
