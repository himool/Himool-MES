from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from extensions.exceptions import NotAuthenticated
from apps.system.models import User
from django.conf import settings


class JWTScheme(SimpleJWTScheme):
    target_class = 'extensions.authentications.BaseAuthentication'


class BaseAuthentication(JWTAuthentication):

    def authenticate(self, request):
        if settings.DEBUG:
            return User.objects.all().first(), {}

        if (header := self.get_header(request)) is None:
            return None

        if (raw_token := self.get_raw_token(header)) is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = User.objects.get(id=validated_token['user_id'])
        except KeyError as e:
            raise NotAuthenticated('令牌不包含用户标识') from e
        except User.DoesNotExist as e:
            raise NotAuthenticated('用户不存在') from e
        except InvalidToken as e:
            raise NotAuthenticated('令牌无效') from e

        return user, validated_token


__all__ = [
    'BaseAuthentication',
]
