from knox.models import AuthToken

def custom_token_creator(token_model, user, serializer):
    instance, token = AuthToken.objects.create(user)
    return token