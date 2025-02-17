from django import forms
from .models import Comment


class SharePostForm(forms.Form):
    name = forms.CharField(max_length=25)
    from_email = forms.EmailField(label='Email')
    to_email = forms.EmailField(label='To')
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Comment here!',
        'rows': 2,
        'cols': 50
        }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        

class SearchForm(forms.Form):
    query = forms.CharField()