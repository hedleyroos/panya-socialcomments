from django.conf import settings
from preferences import preferences

def main(request):
    return {'SOCIALCOMMENTS_LIKES_ENABLED': preferences.SocialCommentsPreferences.likes_enabled}
