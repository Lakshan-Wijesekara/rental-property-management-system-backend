import bcrypt

class AuthenticationService:
    def authenticate_user(entered_password, database_password):
        try:
            check_pwd = bcrypt.checkpw(entered_password.encode('utf-8'), database_password.encode('utf-8'))

            return check_pwd

        except:
            raise