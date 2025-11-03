from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'phone', 'address', 'language')  # показываем язык
    search_fields = ('user__username', 'phone', 'address')             # поиск по этим полям
    list_filter = ('language',)                                        # фильтр по языку
