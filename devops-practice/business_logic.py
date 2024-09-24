from data_access import UserDataAccess


class UserService:

    @staticmethod
    def get_all_users():
        return UserDataAccess.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        return UserDataAccess.get_user_by_id(user_id)

    @staticmethod
    def create_user(name, email):
        return UserDataAccess.create_user(name, email)

    @staticmethod
    def update_user(user_id, name, email):
        return UserDataAccess.update_user(user_id, name, email)

    @staticmethod
    def delete_user(user_id):
        return UserDataAccess.delete_user(user_id)
