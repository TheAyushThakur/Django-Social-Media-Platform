from django import forms
from .models import Profile

class CustomSignupForm(forms.Form):
    image= forms.ImageField(required=False)

    def signup(self, request, user):
        """
        Called by allauth after the user is created.
        Attach extra signup data (profile image) here.
        """
        image = self.cleaned_data.get("image")
        if image:
            user.profile.image = image
            user.profile.save()
        return user
