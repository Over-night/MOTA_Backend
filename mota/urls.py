from django.urls import path, include
from rest_framework import routers
import mota.views.login as login
import mota.views.user as user
import mota.views.reviews as reviews
import mota.views.rooms as rooms
import mota.views.driver as driver
import mota.views.chat_list as chat_list

import mota.views.term as term
import mota.views.approved as approved
import mota.views.members as members

import mota.views.notices as notices
import mota.views.test as test

# from .views import UserViewSet

# router =routers.DefaultRouter()
# router.register(r'users', UserViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
     # * api
     path('login', login.LoginAPI.as_view()),
     # path('api/terms', term.TermsViewSet.as_view({'get':'list', 'post':'create', 'delete': 'destroy',})),

     # * users
     # path('users/', user.user_list),
     path('users/me', user.UserMeAPI.as_view()),
     path('users/me/driver', driver.DriverAPI.as_view()),
     path('users/<str:userId>', user.UserOtherView.as_view()),

     # * terms
     path('terms', term.terms_list),

     # # * rooms
     path('rooms', rooms.RoomsAPI.as_view(), name="rooms"),
     path('rooms/me', rooms.RoomsByMeAPI.as_view()),
     path('rooms/me/all', rooms.RoomsByMeAllAPI.as_view()),
     path('rooms/<int:roomId>', rooms.RoomByIdAPI.as_view()),
     path('rooms/<int:roomId>/terminate', rooms.RoomByIdTerminateAPI.as_view()),
     
     # * users_approved
     path('rooms/<int:roomId>/approval', approved.ApproveAPI.as_view()),
     path('rooms/<int:roomId>/approval/<int:approvalId>', approved.ApproveByIdAPI.as_view()),
     path('rooms/me/approval', approved.ApprovesByMeAPI.as_view()),
     path('rooms/me/approval/<int:approvalId>', approved.ApproveByMeAPI.as_view()),
     
     
     # * users_member
     path('rooms/<int:roomId>/member', members.MembersAPI.as_view()),
     path('rooms/<int:roomId>/member/me', members.MemberByMeAPI.as_view()),
     path('rooms/<int:roomId>/member/<str:memberId>', members.MemberByIdAPI.as_view()),
     # path('users_approved/', users_approved.users_approved_list),
     # path('users_approved/<int:pk>', users_approved.users_approved_detail),

     # # * users_reviews
     path('reviews', reviews.ReviewsFromMeAPI.as_view()),
     path('reviews/me', reviews.ReviewsToMeAPI.as_view()),
     path('reviews/<int:reviewId>', reviews.ReviewIdFromMeAPI.as_view()),

     # # # * users_rooms
     # path('users_rooms/', users_rooms.users_rooms_list),
     # path('users_rooms/<int:pk>', users_rooms.users_rooms_detail),

     # * chat
     path('chats', chat_list.ChatListApi.as_view()),
     path('chats/fcm', chat_list.ChatFcmApi.as_view()),
     path('chats/<str:chatId>', chat_list.ChatApi.as_view()),
     
     # * notice
     path('notices', notices.NoticeAPI.as_view()),
     path('notices/<int:noticeId>', notices.NoticeByIdAPI.as_view()),
     
     # TEST
     path('test/room-terminate/<int:termId>', test.TestRoomsTerminateAPI.as_view()),
     path('test/upload-picture', driver.PictureTestApi.as_view())
]
