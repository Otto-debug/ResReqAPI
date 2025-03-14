from src.api.base_api import BaseAPI

class LoginAPI(BaseAPI):
    """Класс для работы с эндпоинтом /api/login"""

    def login_user(self, email: str, password: str, headers: dict = None):
        """Логин пользователя"""
        data = {'email': email, 'password': password}
        return self.post('/api/login', json=data, headers=headers)
