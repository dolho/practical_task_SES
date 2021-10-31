from model import UserModel


class UserAuthRegistrationHandler:
    #TODO Продолжить выполнение задания
    def __init__(self, user_model: UserModel):
        self.__user_model = user_model
        self.__router = {"create": self.create_user, "login": self.login_user, "confirm_email": self.confirm_email}

    def route(self, data):
        return self.__router[data["request"]](data)

    def create_user(self, data: dict):
        email = data.get("email")
        password = data.get("password")
        email_confirmation_url = data.get("email_confirmation_url")
        if not (email and password and email_confirmation_url):
            return {"status": 400, "message": "Incorrect email or password"}
        try:
            self.__user_model.create_user(email, password, email_confirmation_url)
            return {"status": 200, "message": "Ok"}
        except ValueError:
            return {"status": 400, "message": "User already exists"}

    def login_user(self, data: dict):
        email = data.get("email")
        password = data.get("password")
        if not (email and password):
            return {"status": 400, "message": "Incorrect email or password"}
        try:
            return self.__user_model.login_user(email, password)
        except (ValueError, FileNotFoundError):
            return {"status": 400, "message": "Incorrect email or password"}

    def confirm_email(self, data: dict):
        token = data.get("token")
        return self.__user_model.activate_account(token)