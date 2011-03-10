from django.core.management.base import BaseCommand, CommandError
from django.contrib.comments.models import Comment
from django.conf import settings

from socialcomments.models import SocialComment

class Command(BaseCommand):
    help = "Migrate django comments so they appear as social comments"

    def handle(self, *args, **options):
        for comment in Comment.objects.all():
            result = SocialComment.objects.filter(id=comment.id)
            if not result:
                obj = SocialComment(comment=comment, parent=None)
                for field in comment._meta.fields:                    
                    if field.name != 'id':
                        setattr(obj, field.name, getattr(comment, field.name))
                obj.save()
                comment.delete()
        self.stdout.write('Done')
