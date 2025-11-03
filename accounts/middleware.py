from django.utils import translation

class UserLanguageMiddleware:
    """
    Меняет язык интерфейса на язык пользователя, если он авторизован.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # если пользователь авторизован и есть профиль
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            lang = request.user.profile.language
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        translation.deactivate()
        return response
