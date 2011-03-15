from django import forms
from django.contrib.comments.forms import CommentForm as BaseCommentForm

from socialcomments.models import SocialComment

class CommentForm(BaseCommentForm):
    parent = forms.ModelChoiceField(queryset=SocialComment.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['rows'] = 3
        self.fields['comment'].initial = 'Add your comment...'

    def get_comment_model(self):
        return SocialComment

    def get_comment_create_data(self):
        data = super(CommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        return data
