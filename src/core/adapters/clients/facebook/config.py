from pydantic_settings import BaseSettings


class FacebookConfig(BaseSettings):
    # Find your credentials on the [Facebook App page](https://developers.facebook.com/apps).
    FACEBOOK_CLIENT_ID: str = "<client-id>"
    FACEBOOK_CLIENT_SECRET: str = "<client-secret>"
