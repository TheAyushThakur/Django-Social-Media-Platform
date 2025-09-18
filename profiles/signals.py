from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def populate_profile(request, user, **kwargs):
    image = request.FILES.get("image")
    if image:
        user.profile.image = image
        user.profile.save()