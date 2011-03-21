from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin

from socialcomments import models

class SocialCommentsPreferencesAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.SocialCommentsPreferences, SocialCommentsPreferencesAdmin)
admin.site.register(models.SocialComment, CommentsAdmin)
