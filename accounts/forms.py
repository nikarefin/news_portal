from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="Common users")
        user.groups.add(common_users)

        send_mail(
            subject='Добро пожаловать на News Portal!',
            message=f'Привет,{user.username}! Вы успешно зарегистрировались на нашем замечательном сайте.',
            from_email=None,
            recipient_list=[user.email]
        )
        return user
