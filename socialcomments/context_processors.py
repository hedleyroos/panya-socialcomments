from django.conf import settings

def main(request):
    return {'SOCIALCOMMENTS_HAS_LIKES': getattr(settings, 'SOCIALCOMMENTS_HAS_LIKES', True)}
