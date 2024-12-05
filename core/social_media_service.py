import requests
from datetime import datetime
from .models import *


class SocialMediaService:
    def __init__(self, user, platform):
        self.user = user
        self.platform = platform
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.get_credentials()

    def get_credentials(self):
        """
        Fetches the API credentials for a specific platform from the database.
        """
        try:
            account = Social_Media_Account.objects.get(user=self.user, platform=self.platform)
            self.access_token = account.access_token
            self.refresh_token = account.refresh_token
            self.expires_at = account.expires_at
        except Social_Media_Account.DoesNotExist:
            raise Exception(f"No user found for {self.platform}.")
        
    def is_token_expired(self):
        return self.expires_at and datetime.now()>self.expires_at

    def refresh_access_token(self):
        pass

    def make_request(self, url, params=None):

        if self.is_token_expired():
            self.refresh_access_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

class GithubService(SocialMediaService):
    def __init__(self, user):
        super().__init__(user, "Github")

    def get_user_data(self):
        url = 'https://api.github.com/user'
        return self.make_request(url)
    
    def get_repositories(self):
        url = 'https://api.github.com/user/repos'
        return self.make_request(url)
    
class TwitterService(SocialMediaService):
    def __init__(self, user):
        super().__init__(user, "Twitter")

    def get_user_profile(self):
        url = 'https://api.twitter.com/2/users/me'
        return self.make_request(url)

    def get_recent_tweets(self):
        url="https://api.twitter.com/2/tweets/"
        return self.make_request(url)    
    
class GoogleService(SocialMediaService):
    def __init__(self, user):
        super().__init__(user, "Google")

    def get_user_profile(self):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        return self.make_request(url)    
    