from typing import Any
from django import forms
from django.forms import ModelForm , RadioSelect
from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    image=forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpeg','pdf'])])

    class Meta:
        model = Post
        fields = [
            'id','title','content','image','tag','user'
        ]
        widgets = {
            "user": RadioSelect(),
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        if image.size > int(settings.MAX_UPLOAD_SIZE):
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)))
        return image 