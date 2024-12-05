from pydantic import Field
from pydantic_settings import BaseSettings
import typing


class FacebookConfig(BaseSettings):
    # Find your credentials on the [Facebook App page](https://developers.facebook.com/apps).
    FACEBOOK_CLIENT_ID: str = "UNDEFINED"
    FACEBOOK_CLIENT_SECRET: str = "UNDEFINED"
    FACEBOOK_WEBHOOK_VERIFICATION_TOKEN: typing.Optional[str] = Field(default='UNDEFINED')

    PROXY_URL: typing.Optional[str] = Field(default=None)
