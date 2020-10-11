# from django.contrib import admin

# from .models import *
# Register your models here.

# class NetworkMembershipPlanFeaturesInline(admin.TabularInline):
#     model = NetworkMembershipPlanFeatures
#     extra = 1

# @admin.register(NetworkMembershipPlan)
# class NetworkMembershipPlanAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'price_per_day', 'created']
#     inlines = [NetworkMembershipPlanFeaturesInline]


# @admin.register(NetworkMembershipRelation)
# class NetworkMembershipRelationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'network', 'plan']
#     list_filter = ['plan']


# @admin.register(NetworkMembershipActivity)
# class NetworkMembershipActivityAdmin(admin.ModelAdmin):
#     list_display = ['id', 'relation', 'payment', 'created', 'active_till', 'active']

 
from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('premium')

for model_name, model in app.models.items():
    admin.site.register(model)