from src.api.base_api import BaseAPI

class UserAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /api/user"""

    def get_list_users(self, page):
        """Возвращает список пользователей"""
        return self.get(f'/api/users', params={"page": page})

    def get_single_user(self, user_id):
        """Возвращает одного пользователя"""
        return self.get(f'/api/users/{user_id}')

    def create_user(self, user_data, headers: dict = None):
        """Создание пользователя"""
        return self.post(f'/api/users', json=user_data, headers=headers)

    def update_user(self, user_id, user_data):
        """Обновление пользователя"""
        return self.put(f'/api/users/{user_id}', json=user_data)

    def delete_user(self, user_id):
        """Удаление пользователя"""
        return self.delete(f'/api/users/{user_id}')
