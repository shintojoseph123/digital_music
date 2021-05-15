# Django imports
from django.urls import include, path
# rest_framework imports
from rest_framework import routers
# file imports
from dsrs import views

# select the router
router = routers.DefaultRouter()
# register the urls and viewset
router.register('dsrs', views.DSRViewSet)
router.register('resources', views.ResourceViewSet)


urlpatterns = [
    # include router urls
    path('', include(router.urls)),
    # resource percentile url
    path('resources/percentile/<int:number>/', views.ResourceViewSet.as_view({"get": "percentile"})),
    # ingest data to database
    path('ingest/', views.ingest, name="ingest"),
]
