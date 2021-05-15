from import_export import resources
from dsrs.models import Resource, DSR
from import_export.widgets import ForeignKeyWidget
from import_export import fields

class ResourceResource(resources.ModelResource):
    class Meta:
        model = Resource
