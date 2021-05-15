"""
digital URL Configuration
"""
# django imports
from django.contrib import admin
from django.urls import include, path
# REST imports
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls



urlpatterns = [
    # admin urls
    path("admin/", admin.site.urls),
    # dsrs app urls
    path('', include('dsrs.urls')),
    # API doc url
    path('api/', include_docs_urls(title='DSRS API', public=True)),
    # API schema url
    path('schema/', get_schema_view(title="DSRS API"), name="schema"),
]
