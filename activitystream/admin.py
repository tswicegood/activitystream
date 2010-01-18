from django.contrib import admin
from activitystream.models import Avatar, ActivityType, ActivityItem


admin.site.register(Avatar)
admin.site.register(ActivityType)
admin.site.register(ActivityItem)

