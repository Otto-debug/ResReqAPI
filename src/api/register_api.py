from src.api.base_api import BaseAPI

class RegisterAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /api/register"""

    def register_user(self, email: str, password: str, headers: dict = None):
        """Регистрируем нового пользователя"""
        data = {'email': email, 'password': password}
        return self.post('/api/register', json=data, headers=headers)