from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mota.models.users import Users
from mota.models.notices import Notices
from mota.models.chats import Chats
from mota.serializers.chat import *

from mota.utils import send_fcm_notification, load_user

from firebase_admin import firestore
from google.cloud.firestore import ArrayUnion

from drf_yasg.utils import swagger_auto_schema
from swagger.views import chats_get, chats_post, chats_chatId_get, chats_chatId_post

from django.utils import timezone
import uuid

# TODO 채팅방 알림 작업 

db = firestore.client()

class ChatListApi(APIView):   
    # * GET /api/chats
    # * 채팅방 리스트 조회
    @swagger_auto_schema(**chats_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
            
        chats = Chats.objects.filter(user=user.uid)
        serializer = ChatsGetSerializer(chats, many=True)
        
        chatsData = []
        for data in serializer.data:
            chat = dict(data)
            db_ref = db.collection('chat_info').document(chat["chat_uuid"])
            try:
                db_data = db_ref.get()
            except:
                return Response(data={"ERROR" : "채팅방 정보가 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)   
            if not db_data.exists:
                return Response(data={"ERROR" : "채팅방 정보가 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)
                
            info = db_data.to_dict()
            chat["info"] = info
            chatsData.append(chat)

        return Response(data=chatsData, 
                        status=status.HTTP_200_OK)
    
    # * POST /api/chats
    # * 개인 별 채팅 신청
    @swagger_auto_schema(**chats_post)
    def post(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        if not "uid" in request.data:
            return Response(data={"ERROR" : "대상 UID 없음"}, 
                            status = status.HTTP_400_BAD_REQUEST)
        try:
            target = Users.objects.get(uid=request.data["uid"])
        except:
            return Response(data={"ERROR" : "유저 정보가 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)
         
        chats_me = Chats.objects.filter(user=user.uid).values_list('chat_uuid', flat=True)
        chat_with = Chats.objects.filter(chat_uuid__in=chats_me, user=target.uid)
        if chat_with.count() > 0:
            return Response(data={"ERROR" : "이미 방이 존재함"}, 
                            status = status.HTTP_400_BAD_REQUEST)
        
        myChat = Chats.objects.create(chat_name=f"{target.nickname}님과의 개인 대화", user=user)
        yourChat = Chats.objects.create(chat_uuid=myChat.chat_uuid, chat_name=f"{user.nickname}님과의 개인 대화", user=target)
        
        dbInfo_ref = db.collection('chat_info').document(str(myChat.chat_uuid))
        dbInfo_obj = {
            "room_id": None,
            "members" : [str(user.uid), str(target.uid)],
            "chat_count": 0,
            "last_message": "",
            "is_end": False,
            "created_at": timezone.now(),
            "updated_at": timezone.now(),
        }
        dbInfo_ref.set(dbInfo_obj)
        
        dbData_ref = db.collection('chat_data').document(str(myChat.chat_uuid))
        dbData_obj = {
            "messages": []
        }
        dbData_ref.set(dbData_obj)
        
        return Response(data=myChat.chat_uuid,
                        status=status.HTTP_200_OK)
        
class ChatApi(APIView):
    # * GET /api/chats/{chatId}
    # * 특정 채팅방 리스트 조회
    @swagger_auto_schema(**chats_chatId_get)
    def get(self, request, chatId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        # 채팅방 검색
        try:
            myChat = Chats.objects.get(chat_uuid=chatId, user=user.uid)
        except:
            return Response(data={"ERROR" : "채팅방 정보가 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        # 저장소 탐색
        dbInfo_ref = db.collection('chat_info').document(chatId)
        dbData_ref = db.collection('chat_data').document(chatId)
        try:
            dbInfo_obj = dbInfo_ref.get()
            dbData_obj = dbData_ref.get()
        except:
            return Response(data={"ERROR" : "채팅방 정보가 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)   
        if not dbInfo_obj.exists or not dbData_obj.exists:
            return Response(data={"ERROR" : "채팅방 정보가 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        # 문서 to 딕셔너리
        infoDict = dbInfo_obj.to_dict()
        dataDict = dbData_obj.to_dict()
        
        # 메시지 슬라이싱
        dataDict["messages"] = dataDict["messages"][myChat.load_since:] if myChat.load_until is None else dataDict["messages"][myChat.load_since:myChat.load_until]
        
        # 읽음 정보 반영
        myChat.read_until = infoDict["chat_count"] if myChat.load_until is None else myChat.load_until
        myChat.save()
        
        return Response(data=dataDict, 
                        status=status.HTTP_200_OK)
    
    # * POST /api/chats/{chatId}
    # * 채팅 업로드
    @swagger_auto_schema(**chats_chatId_post)
    def post(self, request, chatId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        if not "text" in request.data:
            return Response(data={"ERROR" : "채팅 정보를 전송하지 않음"}, 
                            status = status.HTTP_400_BAD_REQUEST)
         
        # 채팅방 검색
        try:
            myChat = Chats.objects.get(chat_uuid=chatId, user=user.uid)
        except:
            return Response(data={"ERROR" : "채팅방 정보가 없음1"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        # 저장소 탐색
        dbInfo_ref = db.collection('chat_info').document(str(myChat.chat_uuid))
        dbData_ref = db.collection('chat_data').document(str(myChat.chat_uuid))
        try:
            dbInfo_obj = dbInfo_ref.get()
            dbData_obj = dbData_ref.get()
        except:
            return Response(data={"ERROR" : "채팅방 정보가 없음2"}, 
                            status=status.HTTP_404_NOT_FOUND)   
        if not dbInfo_obj.exists or dbData_obj:
            return Response(data={"ERROR" : "채팅방 정보가 없음3"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        # 문서 to 딕셔너리
        infoDict = dbInfo_obj.to_dict()
        dataDict = dbData_obj.to_dict()
        if infoDict["is_end"] == True:
            return Response(data={"ERROR" : "종료된 채팅입니다"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        # 추가하려는 메시지 
        message = {
            "id": infoDict["chat_count"],
            "timestamp": timezone.now(),
            "sender": str(user.uid),
            "text": request.data["text"],
            "file": ""
        }
        
        dbInfo_ref.update({
            "chat_count": infoDict["chat_count"] + 1,
            "last_chat": message["text"],
            "updated_at": timezone.now()
        })
        dbData_ref.update({
            "messages": ArrayUnion([message]),
        })
        
        members = dbInfo_ref["members"]
        
        for member in members:
            if member == str(user.uid):
                continue
            send_fcm_notification(
                user=Users.objects.get(uuid=member),
                title=f"{user.nickname} 님의 채팅",
                body=f"{request.data['text']}"
            ) 
        
        return Response(status=status.HTTP_200_OK)
    
    
class ChatFcmApi(APIView):
    # * GET /api/chats/fcm
    # * 특정 채팅방 리스트 조회
    
    def post(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
    
        members = request.data["members"]
        for member in members:
            userTo = Users.objects.get(uid=member)
            send_fcm_notification(
                user=userTo,
                title=f"{user.nickname} 님의 채팅",
                body=f"{request.data['text']}"
            )
        
        return Response(status=status.HTTP_200_OK)