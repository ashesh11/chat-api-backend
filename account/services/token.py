from account.models.token import BlacklistedToken

class BlacklistTokenServices:
    @staticmethod
    def add_to_blacklist(token):
        try:
            BlacklistedToken.objects.create(token=token)
            return True, None
        except Exception as e:
            return None, {"error": f"Add token to blacklist failed. {e}"}
        

    @staticmethod
    def check_if_blacklisted(token):
        try:
            token = BlacklistedToken.objects.filter(token=token)
            if token:
                return True, {"error": "Re-login required"}
            return False, None
        except Exception as e:
            return None, {"error": f"Exception raised while checking token in blacklist. {e}"}