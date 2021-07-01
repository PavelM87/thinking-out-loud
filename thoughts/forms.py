from django import forms
from django.conf import settings

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > settings.MAX_POST_LENGTH:
            raise forms.ValidationError("Короче, пожалста!")
        return content