from django.db import models
from django.contrib.comments.models import Comment as BaseComment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, Moderator
from django.contrib.comments import signals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from panya.models import ModelBase
from secretballot.models import Vote
from preferences.models import Preferences
from preferences import preferences

from cadbury.models import Recipe

class SocialCommentsPreferences(Preferences):
    __module__ = 'preferences.models'

    likes_enabled = models.BooleanField(default=True)
    notification_recipients = models.TextField(blank=True, help_text=_("One email address per line"))

    class Meta:
        verbose_name_plural = 'Social Comments Preferences'

    def __unicode__(self):
        return u"Social Comments Preferences"

class SocialComment(BaseComment):
    """Custom comment class"""
    parent = models.ForeignKey('self', null=True, blank=True)

    @property
    def nested_comments(self):
        return SocialComment.objects.filter(parent=self).order_by('id')

    def can_vote(self, request):
        """Play along with Panya API"""
        return True, 'can_vote'

    def likes_enabled(self):
        """Play along with Panya API"""
        return True

    @property
    def vote_total(self):
        """Return number of votes"""
        content_type = ContentType.objects.get(app_label='socialcomments', model__iexact='socialcomment')
        q = Vote.objects.filter(content_type=content_type, object_id=self.id)
        return q.filter(vote=+1).count() - q.filter(vote=-1).count()

    @property
    def as_leaf_class(self):
        """Play along with Panya API"""
        return {'content_type':'socialcomment'}

    @property
    def creator(self):
        return User.objects.get(id=self.user_id)

class SocialCommentModerator(CommentModerator):
    email_notification = True

    def email(self, *args, **kwargs):
        """Lame trick to avoid copy-and-paste of large method"""
        old_managers = settings.MANAGERS
        settings.MANAGERS = [('', n) for n in preferences.SocialCommentsPreferences.notification_recipients.split()]
        try:
            super(SocialCommentModerator, self).email(*args, **kwargs)
        finally:
            settings.MANAGERS = old_managers

class SocialModerator(Moderator):
    """Subclass and override connect method since the moderation framework 
    does not make provision for custom comment app."""

    def connect(self):
        signals.comment_will_be_posted.connect(self.pre_save_moderation, sender=SocialComment)
        signals.comment_was_posted.connect(self.post_save_moderation, sender=SocialComment)

moderator = SocialModerator()
moderator.register(ModelBase, SocialCommentModerator)
