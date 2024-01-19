from mota.models.users import Users
from mota.models.notices import Notices
from mota.models.rooms import Rooms
from mota.models.terms import Terms
from mota.models.users_approved import UsersApproved
from mota.models.users_driver import UsersDriver
from mota.models.users_reviews import UsersReviews
from mota.models.users_rooms import UsersRooms

from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter

class UsersAdmin(admin.ModelAdmin):
    list_display = ['uid', 'nickname', 'gender', 'age', 'picture', 'blocked_until', 'deleted_at']
    list_filter = (
        'gender',
        'age',
        ('blocked_until', DateTimeRangeFilter),
        ('deleted_at', DateTimeRangeFilter),
    )
    search_fields = ['uid', 'nickname']

admin.site.register(Users, UsersAdmin)


class UsersDriverAdmin(admin.ModelAdmin):
    list_display = ['user', 'car_no', 'car_type', 'car_limit', 'car_pictures', 'license_path', 'license_at']
    list_filter = (
        'car_type',
        'car_limit',
        ('license_at', DateTimeRangeFilter),
    )
    search_fields = ['user', 'car_no']

admin.site.register(UsersDriver, UsersDriverAdmin)


class RoomsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'price', 'party_limit', 'party_now', 'locate_start', 'locate_end', 'plan_at', 'content', 'option', 'is_end', 'created_at', 'deleted_at']
    list_filter = (
        'price',
        'party_now',
        'locate_start',
        'locate_end',
        ('plan_at', DateTimeRangeFilter),
        'is_end',
    )
    search_fields = ['id', 'user', 'locate_start', 'locate_end', 'plan_at']

admin.site.register(Rooms, RoomsAdmin)


class UsersRoomsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'created_at', 'deleted_at']
    list_filter = (
        ('created_at', DateTimeRangeFilter),
    )
    search_fields = ['id', 'user', 'room']

admin.site.register(UsersRooms, UsersRoomsAdmin)


class UsersApprovedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'prove', 'updated_at']
    list_filter = (
        'prove',
        ('updated_at', DateTimeRangeFilter),
    )
    search_fields = ['id', 'user', 'room']

admin.site.register(UsersApproved, UsersApprovedAdmin)

class UsersReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'userfrom', 'userto', 'room', 'review', 'created_at', 'deleted_at']
    list_filter = (
        ('created_at', DateTimeRangeFilter),
        ('deleted_at', DateTimeRangeFilter),
    )
    search_fields = ['id', 'userfrom', 'room']
    
admin.site.register(UsersReviews, UsersReviewsAdmin)


class NoticesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'created_at', 'read_at']
    list_filter = (
        ('created_at', DateTimeRangeFilter),
        ('read_at', DateTimeRangeFilter),
    )
    search_fields = ['id', 'user']
    
admin.site.register(Notices, NoticesAdmin)


class TermsAdmin(admin.ModelAdmin):
    list_display = ['name', 'isEssential', 'content', 'created_at', 'updated_at', 'deleted_at']
    list_filter = (
        'isEssential',
        ('created_at', DateTimeRangeFilter),
        ('updated_at', DateTimeRangeFilter),
        ('deleted_at', DateTimeRangeFilter),
    )
    search_fields = ['name']
    
admin.site.register(Terms, TermsAdmin)
