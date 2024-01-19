from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import patch

from django.contrib.auth.models import User as AuthUser
from mota.models.users import Users
from mota.models.rooms import Rooms

from mota.views.rooms import RoomsAPI


class RoomTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rooms_url = reverse('rooms') 

    def test_rooms_get_unauthorized(self):
        response = self.client.get(self.rooms_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('firebase.authentication.FirebaseAuthentication.authenticate')
    def test_rooms_get_success(self, mock_get_user_from_token):
        mock_get_user_from_token.return_value = {'username': 'cVLXxevNRhd6V5wAaGvZO72yc1I3'}

        # 인증된 유저로 요청을 보내는 코드를 작성해야 합니다. 
        # 예를 들면, Firebase 토큰을 설정하는 방식 등.
        response = self.client.get(self.rooms_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
