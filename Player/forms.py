from django import forms
from Player.models import Media


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('uname', 'f_name', 'up_date', 'file',)
