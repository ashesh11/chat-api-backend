from account.models import UserAccount

class UserAccountServices:
    @staticmethod
    def create(data):
    # Create a new account with email and password. Password is encrypted and saved to database.
        try:
            account = UserAccount.objects.create(**data)
            account.set_password(account.password)
            account.save()
            return account, None
        except Exception as e:
            return None, {"errors": f"User account creation failed. {e}"}