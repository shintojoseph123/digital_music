# lib mports
from import_export import resources
from import_export.widgets import ForeignKeyWidget
from import_export import fields
# file imports
from dsrs.models import Resource, DSR

class ResourceResource(resources.ModelResource):
    class Meta:
        model = Resource
