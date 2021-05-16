# Django imports
from django.urls import include, path
# rest_framework imports
from rest_framework import routers
# file imports
from dsrs import views

# select the router
router = routers.DefaultRouter()
# register the DSRViewSet and urls
router.register('dsrs', views.DSRViewSet)
# register the ResourceViewSet and urls
router.register('resources', views.ResourceViewSet)

urlpatterns = [
    # include router urls
    path('', include(router.urls)),
    # ingest data to database
    path('ingest/', views.ingest, name="ingest"),
    # GET: resource percentile url
    path('resources/percentile/<int:number>/', views.ResourceViewSet.as_view({"get": "percentile"})),
]
