from django.contrib import admin

from socialcomments import models

class SocialCommentsPreferencesAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.SocialCommentsPreferences, SocialCommentsPreferencesAdmin)
