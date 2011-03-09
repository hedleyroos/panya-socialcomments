from socialcomments.models import SocialComment
from socialcomments.forms import CommentForm

def get_model():
    return SocialComment

def get_form():
    return CommentForm
