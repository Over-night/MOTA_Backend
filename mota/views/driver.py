import boto3
from mota.serializers.driver import *
from mota.models.users_driver import UsersDriver

from mota.utils import load_user

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from swagger.views import users_me_driver_get, users_me_driver_post, users_me_driver_delete
from moyeobayo.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_CUSTOM_DOMAIN

from datetime import datetime

# @ /api/users/me/driver : GET POST
# @ 운전자 정보 
class DriverAPI(APIView):
    post_key = ["car_no", "car_type", "car_limit"]
    
    # * GET /api/users/me/driver
    # * 내 운전자 정보 조회
    @swagger_auto_schema(**users_me_driver_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 유저의 운전자 정보 확인
        try:
            driver = UsersDriver.objects.get(user_id=user.uid)
        except:
            return Response(data={"ERROR" : "운전자 정보 없음"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        serializer = DriverGetSerializer(driver)
        
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
    
    # * POST /api/users/me/driver
    # * 내 운전자 정보 등록 
    @swagger_auto_schema(**users_me_driver_post)
    def post(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        driverInfo = UsersDriver.objects.filter(user_id=user.uid)
        
        if driverInfo.count() > 0:
            driver = driverInfo[0]
            if "car_no" in request.data: 
                if not isinstance(request.data["car_no"], str):
                    return Response(data={"ERROR" : f"car_no : 잘못된 자료형의 요청값 - {type(request.data['car_no'],)}"},
                                status=status.HTTP_400_BAD_REQUEST)
                driver.car_no = request.data["car_no"]
            
            if "car_type" in request.data:
                if not isinstance(request.data["car_type"], str):
                    return Response(data={"ERROR" : f"car_type : 잘못된 자료형의 요청값 - {type(request.data['car_type'],)}"},
                                status=status.HTTP_400_BAD_REQUEST)
                driver.car_type = request.data["car_type"]
            
            if "car_limit" in request.data:
                limit = request.data["car_limit"]
                if not isinstance(limit, int):
                    try:
                        limit = int(limit)
                    except ValueError:
                        return Response(data={"ERROR" : f"car_limit : 잘못된 자료형의 요청값 - {type(request.data['car_limit'],)}"},
                                        status=status.HTTP_400_BAD_REQUEST)
                driver.car_limit = limit

            if "car_pictures" in request.FILES:                              
                images = request.FILES.getlist('car_pictures')  # 'files'는 프론트엔드에서 설정한 파일 필드 이름이어야 합니다.
                s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

                # 기존 배열의 길이
                baseLen = len(driverInfo[0].car_pictures)
                urls = []
                cnt = 1
                for image in images:
                    imageName = str(user.uid) + (f'_0{cnt}' if cnt < 10 else f"_{cnt}")
                    unique_names =  str(datetime.now().month) + '_' + str(datetime.now().day) + '_' + str(datetime.now().hour) + '_' + str(datetime.now().minute) + '_' + str(datetime.now().second) + '_'
                    imagePath = f"media/car-picture/{imageName + unique_names}"
           
                    s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, imagePath)
        
                    imageUrl = f"https://{AWS_S3_CUSTOM_DOMAIN}/{imagePath}"
                    urls.append(imageUrl)
                    cnt += 1
                
                # # 이전 파일 삭제
                # s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                # response = s3.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix="media/car-picture/")
                # carImages = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].split('/')[-1].startswith(f"{user.uid}")]
                # for carImage in carImages:
                #     if int(carImage[-2]) > baseLen:
                #         s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=carImage)
                        
            
            driver.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
    
        else:
            # 모든 필요 값이 request.data에 없을 경우 
            if not all(key in request.data for key in self.post_key):
                return Response(data={
                                        "ERROR" : "잘못된 자료 요청 형식", 
                                        "data" : request.data
                                    },
                                      status=status.HTTP_400_BAD_REQUEST)

            driver = UsersDriver.objects.create(user_id=user.uid, 
                                                car_no=request.data["car_no"],
                                                car_type=request.data["car_type"],
                                                car_limit=request.data["car_limit"],
                                                license_path=" ",
                                                car_pictures=[" "])

            images = request.FILES.getlist('car_pictures')  # 'files'는 프론트엔드에서 설정한 파일 필드 이름이어야 합니다.

            urls = []
            cnt = 1
            for image in images:
                imageName = str(user.uid) + (f"_0{cnt}" if cnt < 10 else f"_{cnt}")
                unique_names =  str(datetime.now().month) + '_' + str(datetime.now().day) + '_' + str(datetime.now().hour) + '_' + str(datetime.now().minute) + '_' + str(datetime.now().second) + '_'
                imagePath = f"media/car-picture/{imageName + unique_names}"
           
                s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, imagePath, ExtraArgs={'ACL': 'public-read'})
        
                imageUrl = f"https://{AWS_S3_CUSTOM_DOMAIN}/{imagePath}"
                urls.append(imageUrl)
                cnt += 1
            
            driver.car_pictures = urls

            driver.save()

            return Response(status=status.HTTP_201_CREATED)
    
    # * DELETE /api/users/me/driver
    # * 내 운전자 정보 삭제
    @swagger_auto_schema(**users_me_driver_delete)
    def delete(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
    
        # 유저의 운전자 정보 확인
        try:
            driver = UsersDriver.objects.get(user_id=user.uid)
        except:
            return Response(data={"ERROR" : "운전자 정보 없음"}, 
                            status = status.HTTP_400_BAD_REQUEST)
        
        driver.delete()
        
        return Response(status = status.HTTP_200_OK)
    
class PictureTestApi(APIView):
    def post(self, request):
        images = request.FILES.getlist('images')  # 'files'는 프론트엔드에서 설정한 파일 필드 이름이어야 합니다.
        urls = []
        unique_names =  str(datetime.now().month) + '_' + str(datetime.now().day) + '_' + str(datetime.now().hour) + '_' + str(datetime.now().minute) + '_' + str(datetime.now().second) + '_'
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        
        cnt = 1
        for image in images:
            try:
                imageName = f"media/test/{unique_names + (f'_0{cnt}' if cnt < 10 else f'_{cnt}')}"
            
                s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, imageName)
            
                imageUrl = f"https://{AWS_S3_CUSTOM_DOMAIN}/{imageName}"
                urls.append(imageUrl)
            
                cnt += 1
            except:
                 return Response(data=urls, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=urls, status=status.HTTP_200_OK)