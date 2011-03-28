from django.db import models
from django.contrib.comments.models import Comment as BaseComment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, Moderator
from django.contrib.comments import signals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, loader
from django.contrib.sites.models import Site

from panya.models import ModelBase
from secretballot.models import Vote
from preferences.models import Preferences
from preferences import preferences

from cadbury.models import Recipe

class SocialCommentsPreferences(Preferences):
    __module__ = 'preferences.models'

    moderation_enabled = models.BooleanField(default=False)
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

    def moderate(self, *args, **kwargs):
        return preferences.SocialCommentsPreferences.moderation_enabled

    def email(self, comment, content_object, request):
        if isinstance(content_object, ModelBase):
            content_url = content_object.as_leaf_class().get_absolute_url()
        else:
            content_url = content_object.get_absolute_url()
        if not self.email_notification:
            return
        recipient_list = preferences.SocialCommentsPreferences.notification_recipients.split()
        t = loader.get_template('comments/comment_notification_email.txt')
        c = Context({ 'comment': comment,
                      'content_object': content_object ,
                      'content_url': content_url,
                      'site': Site.objects.get_current(),
                      'moderation_required':preferences.SocialCommentsPreferences.moderation_enabled})
        subject = '[%s] New comment posted on "%s"' % (Site.objects.get_current().name,
                                                          content_object)
        message = t.render(c)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

class SocialModerator(Moderator):
    """Subclass and override connect method since the moderation framework 
    does not make provision for custom comment app."""

    def connect(self):
        signals.comment_will_be_posted.connect(self.pre_save_moderation, sender=SocialComment)
        signals.comment_was_posted.connect(self.post_save_moderation, sender=SocialComment)

moderator = SocialModerator()
moderator.register(ModelBase, SocialCommentModerator)
