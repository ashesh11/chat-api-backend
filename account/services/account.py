from account.models.account import UserAccount

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
            return None, {"error": f"User account creation failed. {e}"}
        
    @staticmethod
    def list_active_users():
    # Returns list f active users.
        try:
            user = UserAccount.objects.filter(is_active=True)
            if not user:
                return None, {"error": "No active user"}
            return user, None
        except Exception as e:
            return None, {"error": f"User listing failed. {e}"}
        
    @staticmethod
    def retrieve_active_user(user_id):
    # Takes user_id as input and returns that user if active.
        try:
            user = UserAccount.objects.get(id=user_id, is_active=True)
            if not user:
                return None, {"error": "User not found"}
            return user, None
        except Exception as e:
            return None, {"error": f"User retrieval failed. {e}"}
        

