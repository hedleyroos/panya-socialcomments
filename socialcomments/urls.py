from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^comments/', include('django.contrib.comments.urls')),

)
