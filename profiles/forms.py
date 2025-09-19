from django import forms
from .models import Profile
from django.contrib.auth.models import User


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
class EditProfileForm(forms.ModelForm):
    username = forms.CharField(required=True, min_length=3)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ["image"]  # Profile-specific fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["username"].initial = user.username
            self.fields["email"].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile.save()
        return profile