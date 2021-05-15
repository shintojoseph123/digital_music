"""
digital model Registration
"""
from django.contrib import admin
from dsrs.models import Territory, Currency, DSR, Resource

admin.site.register(DSR)
admin.site.register(Currency)
admin.site.register(Territory)
admin.site.register(Resource)
