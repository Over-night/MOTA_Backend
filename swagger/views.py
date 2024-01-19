from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg import openapi

users_me_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 유저 정보 확인",
    "operation_description": 
        """
        ### 설명
        내 정보의 json을 반환한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`uid`                  |VARCHAR(255)   |Firebase UID                       |보통 28자                                      |
        |`nickname`             |VARCHAR(50)    |유저의 닉네임                      |                                               |
        |`gender`               |VARCHAR(20)    |유저의 성별                        |male: 남자 / female 여자 / private 비공개      |
        |`age`                  |VARCHAR(20)    |유저의 나이                        |10 단위                                        |
        |`picture`              |TEXT           |유저의 프로필 사진                 |db 내 사진의 링크                              |
        |`blocked_until`        |DATETIME       |유저의 블럭 여부 및 기한           |                                               |
        |`deleted_at`           |DATETIME       |유저의 계정 삭제 여부 및 일시      |                                               |
        ### 제공 형식 예제
        ```json
        {
            "uid": "cVLXxevNRhd6V5wAaGvZO72yc1I3",
            "nickname": "낙네임",
            "gender": "male",
            "age": "20대",
            "picture": "media/profile-picture/myUID",
            "blocked_until": null,
            "deleted_at": null
        }
        ```
        """,
    "responses" : {
        200 : "내 정보 반환",
        400 : "직렬화 실패",
        401 : "파이어베이스 인증 실패",
        404 : "유저 정보 조회 실패"
    },
    "tags" :
        ['/api/users/me']
}

users_me_put = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 유저 정보 수정",
    "operation_description": 
        """
        ### 설명
        json과 요청을 보내 정보를 수정한다
        
        ### 인자 목록
        |인자                   |요청 방식      |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`nickname`             |DATA           |유저의 닉네임                      |                                               |
        |`gender`               |DATA           |유저의 성별                        |male: 남자 / female 여자 / private 비공개      |
        |`age`                  |DATA           |유저의 나이                        |10 단위                                        |
        |`picture`              |FILES          |유저의 프로필 사진                 |db에선 s3 bucket 내 사진의 경로로 저장돰       |
        ### 수정 형식 예제
        ```json
        DATA : {
            "nickname": "새 닉네임",
            "gender": "private",
            "age": "30",
        }           
        ```
        ```
        FILES : {
            picture : ~~
        }
        ```
        """,
    "responses" : {
        200 : "내 정보 수정 성공",
        400 : "잘못된 요청값",
        401 : "파이어베이스 인증 실패",
        404 : "유저 정보 없음"
    },
    "tags" :
        ['/api/users/me']
}

users_me_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 유저 정보 삭제",
    "operation_description": 
        """
        ### 설명
        내 정보의 레코드 중 아래의 속성이 비고의 내용으로 변경됨
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`deleted_at`           |DATETIME       |유저의 계정 삭제 여부 및 일시      |now() 초기화                                   |
        |`is_active`            |BOOLEAN        |계정 활성화 여부                   |false → true                                   |
        
        ```
        """,
    "responses" : {
        204 : "내 정보 삭제 성공",
        401 : "파이어베이스 인증 실패",
        404 : "유저 정보 없음"
    },
    "tags" :
        ['/api/users/me']
}

users_me_driver_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 운전자 정보 확인",
    "operation_description": 
        """
        ### 설명
        내 운전자 정보의 json을 반환한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`user_id`              |VARCHAR(255)   |Firebase UID                       |PK, FK 1:1                                     |
        |`car_no`               |VARCHAR(20)    |차량 번호                          |                                               |
        |`car_type`             |VARCHAR(20)    |차량 종류                          |                                               |
        |`car_limit`            |INTEGER        |최대 탑승 가능 인원                |운전자를 제외한 인원                           |
        |`car_pictures`         |ARRAY(TEXT)    |차량 사진들                        |db 내 사진의 링크 리스트                       |
        |`license_path`         |TEXT           |면허증 경로                        |db 내 사진의 링크                              |
        |`license_at`           |DATETIME       |면허증 등록 일시                   |auto_now_add                                   |
        ### 제공 형식 예제
        ```json
        {
            "user": "ABCDE12345FGHIJ67890KLMNOPQR",
            "car_no": "1557",
            "car_type": "VOLVO",
            "car_limit": 3,
            "car_pictures": [
                "media/car-picture/myUID_01",
                "media/car-picture/myUID_02",
            ],
            "license_path": "",
            "license_at": null
        }      
        ```
        """,
    "responses" : {
        200 : "내 운전자 정보 반환",
        401 : "파이어베이스 인증 실패",
        404 : "운전자 정보 없음"
    },
    "tags" :
        ['users/me/driver']
}

users_me_driver_post = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 운전자 정보 등록",
    "operation_description": 
        """
        ### 설명
        내 운전자 정보를 등록한다
        모든 값 입력 필수
        ### 인자 목록
        |인자                   |요청 방식      |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`car_no`               |DATA           |차량 번호                          |                                               |
        |`car_type`             |DATA           |차량 종류                          |                                               |
        |`car_limit`            |DATA           |최대 탑승 가능 인원                |운전자를 제외한 인원                           |
        |`car_pictures`         |FILES          |차량 사진들                        |db 내 사진의 링크 리스트                       |
        |`license_path`         |FILES          |면허증 경로                        |db 내 사진의 링크                              |
        ### 입력 형식 예제
        ```json
        DATA : {
            "car_no": "1557",
            "car_type": "VOLVO",
            "car_limit": 3,
        }
        ```
        ```
        FILES : 
            "car_pictures": [
                ~~~
            ],
            "license_path": ~~~
        }      
        ```
        ### 참고사항
        license_path에 대한 등록 없음
        """,
    "responses" : {
        201 : "운전자 정보 등록됨",
        400 : "잘못된 요청 또는 요청값이 전송됨",
        401 : "파이어베이스 인증 실패"
    },
    "tags" :
        ['users/me/driver']
}

users_me_driver_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 운전자 정보 삭제",
    "operation_description": 
        """
        ### 설명
        DB에서 내 운전자 정보를 삭제한다
        """,
    "responses" : {
        200 : "운전자 정보 삭제됨",
        400 : "운전자 정보 없음",
        401 : "파이어베이스 인증 실패"
    },
    "tags" :
        ['users/me/driver']
}

users_id_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 유저 정보 확인",
    "operation_description": 
        """
        ### `{userID}`
        - 자료형 : str
        - 유저의 UID
        ### 설명
        특정한 유저 정보의 json을 반환한다  
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`uid`                  |VARCHAR(255)   |Firebase UID                       |보통 28자                                      |
        |`nickname`             |VARCHAR(50)    |유저의 닉네임                      |                                               |
        |`gender`               |VARCHAR(20)    |유저의 성별                        |male: 남자 / female 여자 / private 비공개      |
        |`age`                  |VARCHAR(20)    |유저의 나이                        |10 단위                                        |
        |`picture`              |TEXT           |유저의 프로필 사진                 |db 내 사진의 링크                              |
        |`blocked_until`        |DATETIME       |유저의 블럭 여부 및 기한           |                                               |
        |`deleted_at`           |DATETIME       |유저의 계정 삭제 여부 및 일시      |                                               |
        ### 제공 형식 예제
        ```json
        {
            "uid": "cVLXxevNRhd6V5wAaGvZO72yc1I3",
            "nickname": "낙네임",
            "gender": "private",
            "age": "23대",
            "picture": "media/profile-picture/itsUID",
            "blocked_until": null,
            "deleted_at": null
        }
        ```   
        ```
        """,
    "responses" : {
        200 : "유저 정보 반환",
        400 : "직렬화 실패",
        404 : "유저 정보 조회 실패"
    },
    "tags" :
        ['/api/users/{userId}']
}

reviews_post = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 매칭에 대한 리뷰 작성",
    "operation_description": 
        """
        ### 설명
        리뷰를 작성한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`userto_id`            |VARCHAR(255)   |받는 유저의 UID                    |FK, users, 1:n                                 |
        |`room_id`              |INTEGER        |카풀 방의 ID                       |FK, rooms, 1:n                                 |
        |`review`               |VARCHAR(1000)  |리뷰 세부 내역                     |                                               |
        ### 제공 형식 예제
        ```json
        {
            "userto_id": "ABCDE12345FGHIJ67890KLMNOPQR",
            "room_id": 5
            "review": "살짝 늦게 오셨어요"
        }
        ```
        """,
    "responses" : {
        201 : "리뷰 작성 완료됨",
        400 : "직렬화 실패, 유효하지 않은 요청, 작성 조건 부족",
        401 : "파이어베이스 인증 실패, 작성 자격 없음"
    },
    "tags" :
        ['/api/reviews']
}

reviews_me_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내가 작성하거나 받은 리뷰 전부 조회",
    "operation_description": 
        """
        ### 설명
        내가 받은 리뷰들을 json 리스트를 반환한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |리뷰의 ID                          |PK                                             |
        |`userfrom_id`          |VARCHAR(255)   |작성한 유저의 UID                  |FK, users, 1:n                                 |
        |`userto_id`            |VARCHAR(255)   |받는 유저의 UID                    |FK, users, 1:n                                 |
        |`room_id`              |INTEGER        |카풀 방의 ID                       |FK, rooms, 1:n                                 |
        |`review`               |VARCHAR(1000)  |리뷰 세부 내역                     |                                               |
        |`created_at`           |DATETIME       |생성 일시                          |auto_now_add                                   |
        |`deleted_at`           |DATETIME       |삭제 일시                          |                                               |
        |`isWriteByMe`          |BOOLEAN        |내가 작성했는지의 여부             |True-내가작성 / False-남이작성                 |
        ### 제공 형식 예제
        ```json
        [
            {
                "id": 1,
                "review": "너무 좋았어요!",
                "created_at": null,
                "deleted_at": null,
                "userfrom": "ABCDE12345FGHIJ67890KLMNOPQR",
                "userto": "E7F8G9H0I1J2K3L4M5N6O7P8Q9R0",
                "room": 3,
                `isWriteByMe`: True
            },
            {
                "id": 2,
                "review": "살짝 느리셨어요..",
                "created_at": null,
                "deleted_at": null,
                "userfrom": "E7F8G9H0I1J2K3L4M5N6O7P8Q9R0",
                "userto": "ABCDE12345FGHIJ67890KLMNOPQR",
                "room": 3,
                `isWriteByMe`: False
            }
        ]
        ```
        """,
    "responses" : {
        200 : "내가 받은 리뷰 반환",
        401 : "파이어베이스 인증 실패",
    },
    "tags" :
        ['/api/reviews/me']
}

reviews_id_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내가 작성한 특정 리뷰 조회",
    "operation_description": 
        """
        ### `{reviewId}`
        - 자료형 : int
        - 리뷰의 ID
        ### 설명
        내가 작성한 특정 리뷰의 json을 반환한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |리뷰의 ID                          |PK                                             |
        |`userfrom_id`          |VARCHAR(255)   |작성한 유저의 UID                  |FK, users, 1:n                                 |
        |`userto_id`            |VARCHAR(255)   |받는 유저의 UID                    |FK, users, 1:n                                 |
        |`room_id`              |INTEGER        |카풀 방의 ID                       |FK, rooms, 1:n                                 |
        |`review`               |VARCHAR(1000)  |리뷰 세부 내역                     |                                               |
        |`created_at`           |DATETIME       |생성 일시                          |auto_now_add                                   |
        |`deleted_at`           |DATETIME       |삭제 일시                          |                                               |
        ### 제공 형식 예제
        ```json
        {
            "id": 1,
            "review": "ㅇㄴㅇㄴㅇㄴㅇㄴ",
            "created_at": null,
            "deleted_at": null,
            "userfrom": "ABCDE12345FGHIJ67890KLMNOPQR",
            "userto": "E7F8G9H0I1J2K3L4M5N6O7P8Q9R0",
            "room": 3
        }
        ```
        """,
    "responses" : {
        200 : "내가 장성한 리뷰 반환",
        400 : "직렬화 실패",
        401 : "파이어베이스 인증 실패",
        404 : "리뷰를 찾지 못함",
        410 : "이미 삭제된 리뷰"
    },
    "tags" :
        ['reviews/{reviewId}']
}

reviews_id_put = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내가 작성한 특정 리뷰 수정",
    "operation_description": 
        """
        ### `{reviewId}`
        - 자료형 : int
        - 리뷰의 ID
        ### 설명
        일정 시간 이내 내가 작성한 특정 리뷰를 수정한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`review`               |VARCHAR(1000)  |리뷰 세부 내역                     |                                               |
        ### 제공 형식 예제
        ```json
        {
            "review": "수정한 리뷰"
        }
        ```
        """,
    "responses" : {
        200 : "내가 장성한 리뷰 반환",
        400 : "데이터에 이상이 있음, 수정가능 시간이 지남",
        401 : "파이어베이스 인증 실패, 리뷰에 대한 권한 없음",
    },
    "tags" :
        ['reviews/{reviewId}']
}

reviews_id_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내가 작성한 특정 리뷰 조회",
    "operation_description": 
        """
        ### `{reviewId}`
        - 자료형 : int
        - 리뷰의 ID
        ### 설명
        내가 작성한 특정 리뷰를 삭제한다
        """,
    "responses" : {
        200 : "내가 장성한 리뷰 반환",
        400 : "데이터에 이상이 있음, 수정가능 시간이 지남",
        401 : "파이어베이스 인증 실패, 리뷰에 대한 권한 없음",
        410 : "이미 삭제한 리뷰"
    },
    "tags" :
        ['reviews/{reviewId}']
}

rooms_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "이용 가능한 방 정보 확인",
    "operation_description": 
        """
        ### 설명
        조건에 맞는 방들을 시간 순(오름차순)으로 나열한 배열을 반환한다.
        조건은 다음과 같다.
        - room 테이블의 **user_id**가 자신의 **uid**와 다르며
        - 방 현재 정원이 방 정원 제한수보다 적고
        - 카풀이 종료되지 않았으며
        - 방 또는 일정 레코드가 삭제되지 않은 경우  
        
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |방의 ID                            |PK                                             |
        |`user`                 |JSON           |방장 유저의 정보                   |FK - users                                     |
        |`price`                |INTEGER        |카풀 당 이용 금액                  |단위 : 원                                      |
        |`party_limit`          |INTEGER        |방의 최대 정원                     |단위 : 명                                      |
        |`party_now`            |INTEGER        |방의 현재 정원                     |단위 : 명                                      |
        |`locate_start`         |VARCHAR(100)   |카풀의 출발지                      |                                               |
        |`locate_end`           |VARCHAR(100)   |카풀의 목적지                      |                                               |
        |`plan_at`              |DATETIME       |일정 시각                          |                                               |
        |`content`              |TEXT           |방 상세 설명                       |                                               |
        |`option`               |JSONB          |방 옵션                            |gender: male/female/anybody, age: xtoy/anybody |
        |`is_end`               |BOOLEAN        |카풀 종료 여부                     |True : 카풀이 종료됨                           |
        |`created_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`deleted_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`members`              |LIST           |맴버들의 user 정보                 |JSON 리스트 반환                               |
        ### 제공 형식 예제
        ```json
        [
            {
                "id": 34,
                "user": {
                    "uid": "4BagQwREOMZ17EL0U3ny47otLgd2",
                    "nickname": "서명원1",
                    "gender": "남성",
                    "age": "30대",
                    "picture": ""
                },
                "price": 3000,
                "party_limit": 4,
                "party_now": 0,
                "locate_start": "신림동",
                "locate_end": "선릉역",
                "plan_at": "2023-09-09T20:17:00",
                "content": "퇴근길에 같이 카풀 하실 분 구해요",
                "option": {
                    "age": "",
                    "gender": "상관없음"
                },
                "is_end": false,
                "created_at": "2023-09-08T20:18:23.320805",
                "deleted_at": null,
                "members": []
            },
            {
                "id": 37,
                "user": {
                    "uid": "4BagQwREOMZ17EL0U3ny47otLgd2",
                    "nickname": "서명원1",
                    "gender": "남성",
                    "age": "30대",
                    "picture": ""
                },
                "price": 2500,
                "party_limit": 3,
                "party_now": 0,
                "locate_start": "신림",
                "locate_end": "선릉",
                "plan_at": "2023-11-10T13:44:00",
                "content": "ㅁㅇㄴ리ㅜㅁ니울\nㅁㅇㄴㄹ\nㅁ\nㄴㅇㄹ\nㅁㄴㅇ",
                "option": {
                    "age": "",
                    "gender": "상관없음"
                },
                "is_end": false,
                "created_at": "2023-09-10T13:45:08.882045",
                "deleted_at": null,
                "members": []
            },
        ]
    }
]
        ```
        """,
    "responses" : {
        200 : "방 목록 조회 정보 반환",
        401 : "파이어베이스 인증 실패, 운전자 정보 없음",
        404 : "방 데이터가 없음"
    },
    "tags" :
        ['/api/rooms']
}

rooms_post = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "방 등록",
    "operation_description": 
        """
        ### 설명
        방을 생성한다. 단 운전자 정보가 있을 경우에만 가능하다. 
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`price`                |INTEGER        |카풀 당 이용 금액                  |단위 : 원                                      |
        |`party_limit`          |INTEGER        |방의 최대 정원                     |단위 : 명                                      |
        |`locate_start`         |VARCHAR(100)   |카풀의 출발지                      |                                               |
        |`locate_end`           |VARCHAR(100)   |카풀의 목적지                      |                                               |
        |`plan_at`              |DATETIME       |일정 시각                          |                                               |
        |`content`              |TEXT           |방 상세 설명                       |                                               |
        |`option`               |JSONB          |방 옵션                            |gender: male/female/anybody, age: xtoy/anybody |
        ### 제공 형식 예제
        ```json
        {
            "price": 100000,
            "party_limit": 4,
            "locate_start": "신촌역",
            "locate_end": "종로역",
            "plan_at": "2023-08-17T18:10:00"
            "content": "테스트",
            "option": {
                "age": "anybody",
                "gender": "anybody"
            },
        }     
        ```
        """,
    "responses" : {
        201 : "생성 완료",
        400 : "잘못된 request",
        401 : "파이어베이스 인증 실패, 운전자 정보 없음"
    },
    "tags" :
        ['/api/rooms']
}

rooms_id_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 방 조회",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        특정 id의 방을 조회한다.
        조건은 다음과 같다.
        - room 테이블의 **id**가 입력된 값과 같고
        - 방 또는 일정 레코드가 삭제되지 않은 경우  
    

        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |방의 ID                            |PK                                             |
        |`user`                 |JSON           |방장 유저의 정보                   |FK - users                                     |
        |`price`                |INTEGER        |카풀 당 이용 금액                  |단위 : 원                                      |
        |`party_limit`          |INTEGER        |방의 최대 정원                     |단위 : 명                                      |
        |`party_now`            |INTEGER        |방의 현재 정원                     |단위 : 명                                      |
        |`locate_start`         |VARCHAR(100)   |카풀의 출발지                      |                                               |
        |`locate_end`           |VARCHAR(100)   |카풀의 목적지                      |                                               |
        |`plan_at`              |DATETIME       |일정 시각                          |                                               |
        |`content`              |TEXT           |방 상세 설명                       |                                               |
        |`option`               |JSONB          |방 옵션                            |gender: male/female/anybody, age: xtoy/anybody |
        |`is_end`               |BOOLEAN        |카풀 종료 여부                     |True : 카풀이 종료됨                           |
        |`created_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`deleted_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`members`              |LIST           |맴버들의 user 정보                 |JSON 리스트 반환                               |
        ### 제공 형식 예제
        ```json
        {
            "id": 34,
            "user": {
                "uid": "4BagQwREOMZ17EL0U3ny47otLgd2",
                "nickname": "서명원1",
                "gender": "남성",
                "age": "30대",
                "picture": ""
            },
            "price": 3000,
            "party_limit": 4,
            "party_now": 0,
            "locate_start": "신림동",
            "locate_end": "선릉역",
            "plan_at": "2023-09-09T20:17:00",
            "content": "퇴근길에 같이 카풀 하실 분 구해요",
            "option": {
                "age": "",
                "gender": "상관없음"
            },
            "is_end": false,
            "created_at": "2023-09-08T20:18:23.320805",
            "deleted_at": null,
            "members": []
        }
        ```
        """,
    "responses" : {
        200 : "방 조회 정보 반환",
        401 : "파이어베이스 인증 실패",
        404 : "방 데이터가 없음"
    },
    "tags" :
        ['api/rooms/{roomId}']
}

rooms_id_put = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "방 정보 수정",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        내가 방장인 방의 정보를 수정한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`price`                |INTEGER        |카풀 당 이용 금액                  |단위 : 원                                      |
        |`party_limit`          |INTEGER        |방의 최대 정원                     |단위 : 명                                      |
        |`locate_start`         |VARCHAR(100)   |카풀의 출발지                      |                                               |
        |`locate_end`           |VARCHAR(100)   |카풀의 목적지                      |                                               |
        |`plan_at`              |DATETIME       |일정 시각                          |                                               |
        |`content`              |TEXT           |방 상세 설명                       |                                               |
        |`option`               |JSONB          |방 옵션                            |gender: male/female/anybody, age: xtoy/anybody |
        ### 제공 형식 예제
        ```json
        {
            "price": 100000,
            "party_limit": 4,
            "locate_start": "신촌역",
            "locate_end": "종로역",
            "plan_at": "2023-08-17T18:10:00"
            "content": "테스트",
            "option": {
                "age": "anybody",
                "gender": "anybody"
            }
        }     
        ```
        """,
    "responses" : {
        204 : "수정 완료",
        400 : "잘못된 request, 필요 정보 없음, 수정하려는 일정이 과거임, 이미 진행된 일정",
        401 : "파이어베이스 인증 실패, 방장이 아님"
    },
    "tags" :
        ['api/rooms/{roomId}']
}

rooms_id_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "방 삭제",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        방을 삭제한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`deleted_at`           |DATETIME       |방 삭제 여부                       |rooms - now()                                  |  
        """,
    "responses" : {
        204 : "삭제 완료",
        400 : "잘못된 id 입력, 이미 삭제된 방",
        401 : "파이어베이스 인증 실패, 방장이 아님"
    },
    "tags" :
        ['api/rooms/{roomId}']
}

rooms_id_terminate_put = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "방 종료",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        해당 방의 운행을 종료한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`is_end`               |BOOLEAN        |방 종료 여부                       |is_end = True                                  |  
        """,
    "responses" : {
        204 : "삭제 완료",
        400 : "잘못된 id 입력, 이미 삭제된 방",
        401 : "파이어베이스 인증 실패, 방장이 아님"
    },
    "tags" :
        ['api/rooms/{roomId}/terminate']
}

rooms_me_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내가 생성하거나 참여중인 방 목록 확인",
    "operation_description": 
        """
        ### 설명
        내가 생성하거나 참여중인 방의 목록을 시간 순(오름차순)으로 나열한 배열한 후 반환한다.
        조건은 다음과 같다.
        - (room 테이블의 **user_id**가 자신의 **uid**와 같은 방) 또는 (users_rooms 테이블의 **user_id**가 자신의 **uid**와 같은 모든 레코드들의 **room_id** 에 해당하는 방) 이며
        - 방이 종료되지 않았으며 
        - 방 또는 일정 레코드가 삭제되지 않은 경우  
        
        # request : type
        - all : 전부
        - host : 내가 방장인 방
        - member : 내가 참가자인 방
        
        
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |방의 ID                            |PK                                             |
        |`user`                 |JSON           |방장 유저의 정보                   |FK - users                                     |
        |`price`                |INTEGER        |카풀 당 이용 금액                  |단위 : 원                                      |
        |`party_limit`          |INTEGER        |방의 최대 정원                     |단위 : 명                                      |
        |`party_now`            |INTEGER        |방의 현재 정원                     |단위 : 명                                      |
        |`locate_start`         |VARCHAR(100)   |카풀의 출발지                      |                                               |
        |`locate_end`           |VARCHAR(100)   |카풀의 목적지                      |                                               |
        |`plan_at`              |DATETIME       |일정 시각                          |                                               |
        |`content`              |TEXT           |방 상세 설명                       |                                               |
        |`option`               |JSONB          |방 옵션                            |gender: male/female/anybody, age: xtoy/anybody |
        |`is_end`               |BOOLEAN        |카풀 종료 여부                     |True : 카풀이 종료됨                           |
        |`created_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`deleted_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`type`                 |VARCHAR        |방 타입                            |host-내가 방장 / member-내가 구성원            |
        |`members`              |LIST           |맴버들의 user 정보                 |JSON 리스트 반환                               |
        ### 제공 형식 예제
        ```json 
        [
            {
                "id": 34,
                "user": {
                    "uid": "4BagQwREOMZ17EL0U3ny47otLgd2",
                    "nickname": "서명원1",
                    "gender": "남성",
                    "age": "30대",
                    "picture": ""
                },
                "price": 3000,
                "party_limit": 4,
                "party_now": 0,
                "locate_start": "신림동",
                "locate_end": "선릉역",
                "plan_at": "2023-09-09T20:17:00",
                "content": "퇴근길에 같이 카풀 하실 분 구해요",
                "option": {
                    "age": "",
                    "gender": "상관없음"
                },
                "is_end": false,
                "created_at": "2023-09-08T20:18:23.320805",
                "deleted_at": null,
                "type" : "host",
                "members": []
            },
            {
                "id": 37,
                "user": {
                    "uid": "4BagQwREOMZ17EL0U3ny47otLgd2",
                    "nickname": "서명원1",
                    "gender": "남성",
                    "age": "30대",
                    "picture": ""
                },
                "price": 2500,
                "party_limit": 3,
                "party_now": 0,
                "locate_start": "신림",
                "locate_end": "선릉",
                "plan_at": "2023-11-10T13:44:00",
                "content": "ㅁㅇㄴ리ㅜㅁ니울\nㅁㅇㄴㄹ\nㅁ\nㄴㅇㄹ\nㅁㄴㅇ",
                "option": {
                    "age": "",
                    "gender": "상관없음"
                },
                "is_end": false,
                "created_at": "2023-09-10T13:45:08.882045",
                "deleted_at": null,
                "type" : "host",
                "members": []
            },
        ]
        ```
        """,
    "responses" : {
        200 : "방 목록 조회 정보 반환",
        401 : "파이어베이스 인증 실패, 운전자 정보 없음",
        404 : "방 데이터가 없음"
    },
    "tags" :
        ['api/rooms/me']
}

rooms_me_all_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "종료와 상관없이 내가 생성하거나 참여중인 방 목록 확인",
    "operation_description": 
        """
        ### 설명
        내가 생성하거나 참여중인 방의 목록을 시간 순(오름차순)으로 나열한 배열한 후 반환한다.
        조건은 다음과 같다.
        - (room 테이블의 **user_id**가 자신의 **uid**와 같은 방) 또는 (users_rooms 테이블의 **user_id**가 자신의 **uid**와 같은 모든 레코드들의 **room_id** 에 해당하는 방) 이며
        - 방 또는 일정 레코드가 삭제되지 않은 경우  
        
        # request : type
        - all : 전부
        - host : 내가 방장인 방
        - member : 내가 참가자인 방
        
        
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |방의 ID                            |PK                                             |
        |`user`                 |JSON           |방장 유저의 정보                   |FK - users                                     |
        |`price`                |INTEGER        |카풀 당 이용 금액                  |단위 : 원                                      |
        |`party_limit`          |INTEGER        |방의 최대 정원                     |단위 : 명                                      |
        |`party_now`            |INTEGER        |방의 현재 정원                     |단위 : 명                                      |
        |`locate_start`         |VARCHAR(100)   |카풀의 출발지                      |                                               |
        |`locate_end`           |VARCHAR(100)   |카풀의 목적지                      |                                               |
        |`plan_at`              |DATETIME       |일정 시각                          |                                               |
        |`content`              |TEXT           |방 상세 설명                       |                                               |
        |`option`               |JSONB          |방 옵션                            |gender: male/female/anybody, age: xtoy/anybody |
        |`is_end`               |BOOLEAN        |카풀 종료 여부                     |True : 카풀이 종료됨                           |
        |`created_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`deleted_at`           |DATETIME       |방 생성 일시                       |                                               |
        |`type`                 |VARCHAR        |방 타입                            |host-내가 방장 / member-내가 구성원            |
        |`members`              |LIST           |맴버들의 user 정보                 |JSON 리스트 반환                               |
        ### 제공 형식 예제
        ```json 
        [
            {
                "id": 34,
                "user": {
                    "uid": "4BagQwREOMZ17EL0U3ny47otLgd2",
                    "nickname": "서명원1",
                    "gender": "남성",
                    "age": "30대",
                    "picture": ""
                },
                "price": 3000,
                "party_limit": 4,
                "party_now": 0,
                "locate_start": "신림동",
                "locate_end": "선릉역",
                "plan_at": "2023-09-09T20:17:00",
                "content": "퇴근길에 같이 카풀 하실 분 구해요",
                "option": {
                    "age": "",
                    "gender": "상관없음"
                },
                "is_end": false,
                "created_at": "2023-09-08T20:18:23.320805",
                "deleted_at": null,
                "type" : "host",
                "members": []
            },
            {
                "id": 37,
                "user": {
                    "uid": "4BagQwREOMZ17EL0U3ny47otLgd2",
                    "nickname": "서명원1",
                    "gender": "남성",
                    "age": "30대",
                    "picture": ""
                },
                "price": 2500,
                "party_limit": 3,
                "party_now": 0,
                "locate_start": "신림",
                "locate_end": "선릉",
                "plan_at": "2023-11-10T13:44:00",
                "content": "ㅁㅇㄴ리ㅜㅁ니울\nㅁㅇㄴㄹ\nㅁ\nㄴㅇㄹ\nㅁㄴㅇ",
                "option": {
                    "age": "",
                    "gender": "상관없음"
                },
                "is_end": false,
                "created_at": "2023-09-10T13:45:08.882045",
                "deleted_at": null,
                "type" : "host",
                "members": []
            },
        ]
        ```
        """,
    "responses" : {
        200 : "방 목록 조회 정보 반환",
        401 : "파이어베이스 인증 실패, 운전자 정보 없음",
        404 : "방 데이터가 없음"
    },
    "tags" :
        ['api/rooms/me']
}

rooms_id_member_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "현재 방의 모든 유저 조회",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        특정 id값을 가진 방의 멤버를 모두 조회한다

        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`uid`                  |VARCHAR(255)   |Firebase UID                       |보통 28자                                      |
        |`nickname`             |VARCHAR(50)    |유저의 닉네임                      |                                               |
        |`gender`               |VARCHAR(20)    |유저의 성별                        |male: 남자 / female 여자 / private 비공개      |
        |`age`                  |VARCHAR(20)    |유저의 나이                        |10 단위                                        |
        |`picture`              |TEXT           |유저의 프로필 사진                 |db 내 사진의 링크                              |
        |`blocked_until`        |DATETIME       |유저의 블럭 여부 및 기한           |                                               |
        |`deleted_at`           |DATETIME       |유저의 계정 삭제 여부 및 일시      |                                               |
        ### 제공 형식 예제
        ```json
        [
            {
                "uid": "GvcGux76HiMPdVVtzjbQ91xUYkI3",
                "nickname": "서명원2",
                "gender": "남성",
                "age": "20대 이하",
                "picture": "",
                "blocked_until": null,
                "deleted_at": null
            }
        ]
        ```
        """,
    "responses" : {
        200 : "멤버 리스트 조회 정보 반환",
        400 : "잘못된 요청",
        401 : "파이어베이스 인증 실패, 열람조건 없음"
    },
    "tags" :
        ['/api/rooms/{roomId}/member']
}

rooms_id_member_me_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "지정한 방에 탈퇴절차 진행",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        특정 방에 탈퇴을 진행한다
        """,
    "responses" : {
        200 : "탈퇴 완료",
        400 : "해당 방이 존재하지 않음, 잘못된 요청, 이미 탈퇴한 방임",
        401 : "파이어베이스 인증 실패, 열람조건 없음",
        500 : "DB 이상"
    },
    "tags" :
        ['/api/rooms/{roomId}/member/me']
}

rooms_id_member_id_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "지정한 방의 특정 유저에 대한 강퇴절차 진행",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### `{memberID}`
        - 자료형 : str
        - 유저의 uid
        ### 설명
        특정 방의 특정 유저를 강퇴한다
        """,
    "responses" : {
        200 : "탈퇴 완료",
        400 : "권한 없음, 이미 탈퇴한 멤버, 유저 정보 없음",
        401 : "파이어베이스 인증 실패, 열람조건 없음",
        500 : "DB 이상"
    },
    "tags" :
        ['/api/rooms/{roomId}/member/{memberId}']
}

rooms_id_approval_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 방의 신청 목록 전부 조회",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        특정 방에서 상태가 wait인 모든 신청 대기 목록을 조회한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |일련번호                           |PK                                             |
        |`user_id`              |VARCHAR(255)   |방장 유저의 Firebase UID           |FK - users                                     |
        |`room_id`              |INTEGER        |방의 ID                            |FK - rooms                                     |
        |`prove`                |VARCHAR        |수락 여부                          |wait 대기 / proved 승인 / disproved 거절       |
        |`updated_at`           |DATETIME       |업데이트 일시                      |auto_now                                       |
        ### 제공 형식 예제
        ```json
        [
            {
                "id": 1,
                "prove": "wait",
                "updated_at": "2023-08-15T17:09:53.183071",
                "user": "G5H6I7J8K9L0M1N2O3P4Q5R6S7T8",
                "room": 5
            }
        ]
        ```
        """,
    "responses" : {
        200 : "신청 정보 목록 반환",
        400 : "방 정보 없음, 직렬화 실패",
        401 : "파이어베이스 인증 실패",
        404 : "신청 정보 없음"
    },
    "tags" :
        ['/api/rooms/{roomId}/approval']
}

rooms_id_approval_post = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 방에 카풀 가입 신청",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### 설명
        특정 방에 가입 신청을 진행한다 
        """,
    "responses" : {
        201 : "생성 완료",
        400 : "해당 방의 방장 또는 일원임, 신청한지 얼마 안됨",
        401 : "파이어베이스 인증 실패",
        404 : "방 정보를 찾을 수 없음"
    },
    "tags" :
        ['/api/rooms/{roomId}/approval']
}

rooms_id_approval_id_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 방의 특정 신청 정보 조회",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### `{approvalId}`
        - 자료형 : int
        - 신청 정보의 ID
        ### 설명
        특정 방에서 상태가 wait인 신청 목록 중 하나를 조회한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |일련번호                           |PK                                             |
        |`user_id`              |VARCHAR(255)   |방장 유저의 Firebase UID           |FK - users                                     |
        |`room_id`              |INTEGER        |방의 ID                            |FK - rooms                                     |
        |`prove`                |VARCHAR        |수락 여부                          |wait 대기 / proved 승인 / disproved 거절       |
        |`updated_at`           |DATETIME       |업데이트 일시                      |auto_now                                       |
        ### 제공 형식 예제
        ```json
        {
            "id": 1,
            "prove": "wait",
            "updated_at": "2023-08-15T17:09:53.183071",
            "user": "G5H6I7J8K9L0M1N2O3P4Q5R6S7T8",
            "room": 5
        }
        ```
        """,
    "responses" : {
        200 : "신청 정보 반환",
        400 : "가입 요청 정보 없음, 직렬화 실패",
        401 : "파이어베이스 인증 실패, 조회 권한 없음"
    },
    "tags" :
        ['/api/rooms/{roomId}/approval/{approvalId}']
}

rooms_id_approval_id_put = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 방의 특정 신청 정보 수정 및 가입절차 진행",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### `{approvalId}`
        - 자료형 : int
        - 신청 정보의 ID
        ### 설명
        특정 방에서 상태가 wait인 신청 목록의 상태를 업데이트 한다
        (신청 수락 / 거절)
        신청 수락 시 가입 절차를 진행한다
        ### 수정 형식 예제
        ```json
        {
            "prove": "proved"
        }
        또는
        {
            "prove": "disproved"
        }
        ```
        """,
    "responses" : {
        204 : "수정 완료",
        400 : "가입 요청 정보 없음, 잘못된 요청",
        401 : "파이어베이스 인증 실패, 조회 권한 없음"
    },
    "tags" :
        ['/api/rooms/{roomId}/approval/{approvalId}']
}

rooms_id_approval_id_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 방의 특정 신청 정보 삭제",
    "operation_description": 
        """
        ### `{roomID}`
        - 자료형 : int
        - 방의 ID
        ### `{approvalId}`
        - 자료형 : int
        - 신청 정보의 ID
        ### 설명
        특정 방에 대한 자신의 신청 요청을 삭제한다
        DB의 레코드 삭제 방식
        """,
    "responses" : {
        200 : "삭제 완료",
        400 : "가입 요청 정보 없음",
        401 : "파이어베이스 인증 실패, 삭제 권한 없음"
    },
    "tags" :
        ['/api/rooms/{roomId}/approval/{approvalId}']
}

rooms_me_approval_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "나의 신청 목록 전부 조회",
    "operation_description": 
        """
        ### 설명
        내가 수행한 모든 신청 정보를 확인한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |일련번호                           |PK                                             |
        |`user_id`              |VARCHAR(255)   |방장 유저의 Firebase UID           |FK - users                                     |
        |`room_id`              |INTEGER        |방의 ID                            |FK - rooms                                     |
        |`prove`                |VARCHAR        |수락 여부                          |wait 대기 / proved 승인 / disproved 거절       |
        |`updated_at`           |DATETIME       |업데이트 일시                      |auto_now                                       |
        ### 제공 형식 예제
        ```json
        [
            {
                "id": 1,
                "prove": "wait",
                "updated_at": "2023-08-15T17:09:53.183071",
                "user": "G5H6I7J8K9L0M1N2O3P4Q5R6S7T8",
                "room": 5
            }
        ]
        ```
        """,
    "responses" : {
        200 : "신청 정보 목록 반환",
        400 : "방 정보 없음, 직렬화 실패",
        401 : "파이어베이스 인증 실패",
    },
    "tags" :
        ['/api/rooms/me/approval']
}

rooms_me_approval_id_delete = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "나의 특정 신청에 대한 취소 절차 진행",
    "operation_description": 
        """
        ### `{approvalId}`
        - 자료형 : int
        - 신청 정보의 ID
        ### 설명
        특정 신청을 취소한다,
        """,
    "responses" : {
        200 : "신청 정보 목록 반환",
        400 : "방 정보 없음, 직렬화 실패",
        401 : "파이어베이스 인증 실패",
        404 : "신청 정보 없음"
    },
    "tags" :
        ['/api/rooms/me/approval']
}

notice_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "나의 notice 조회",
    "operation_description": 
        """
        ### 설명
        확인하지 않은 notices들을 전부 조회한다
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |일련번호                           |PK                                             |
        |`user_id`              |VARCHAR(255)   |유저의 Firebase UID                |FK - users                                     |
        |`message`              |JSONB          |방의 ID                            |                                               |
        |`created_at`           |DATETIME       |수락 여부                          |auto_now_add                                   |
        |`read_at`              |DATETIME       |읽은 일시                          |                                               |
        """,
    "responses" : {
        200 : "안내 정보 반환",
        400 : "가입 요청 정보 없음, 직렬화 실패",
        401 : "파이어베이스 인증 실패, 조회 권한 없음"
    },
    "tags" :
        ['/api/notices']
}

notice_put = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "나의 알림을 전부 읽음 처리",
    "operation_description": 
        """
        ### 설명
        내 notices들을 전부 읽음 처리
        """,
    "responses" : {
        200 : "안내 정보 반환",
        401 : "파이어베이스 인증 실패"
    },
    "tags" :
        ['/api/notices']
}

notice_id_put = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "특정 알림을 읽음 처리",
    "operation_description": 
        """
        ### 설명
        내 특정 알림을 읽음처리 진행
        pk : 알림의 id 값
        """,
    "responses" : {
        200 : "안내 정보 반환",
        401 : "파이어베이스 인증 실패",
        404 : "알림을 찾을 수 없음"
    },
    "tags" :
        ['/api/notices']
}

chats_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 채팅을 전체 조회",
    "operation_description": 
        """
        ### 설명
        내 채팅 목록을 전부 조회함
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`id`                   |SERIAL         |일련번호                           |PK                                             |
        |`chat_uuid`            |UUID           |유저의 식별 UID                    |                                               |
        |`chat_name`            |VARCHAR(100)   |채팅방명                           |                                               |
        |`user`                 |UUID           |해당 유저                          |FK                                             |
        |`read_until`           |INTEGER        |읽은 일시                          |default=0                                      |
        |`load_since`           |INTEGER        |열람 가능한 메시지 시작 범위       |default=0                                      |
        |`load_until`           |INTEGER        |열람 가능한 메시지 끝 범위         |defalut=None, None일 경우 끝까지               |
        |`will_notify`          |BOOLEAN        |알림 여부                          |default=True                                   |
        """,
    "responses" : {
        200 : "채팅 생성 성공",
        401 : "파이어베이스 인증 실패"
    },
    "tags" :
        ['/api/chats']
}
chats_post = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "1:1 대화 생성",
    "operation_description": 
        """
        ### 설명
        1:1 대화를 생성한다
        카풀 대화 생성은 방 생성시 자동 생성됨
        ### 제공 형식 예제
        ```json
        {
            "uid": "대상의 uid"
        }
        ### firestore 데이터 생성 예시
        ```json
        {
            "room_id": number,
            "members" : [myUID, targetUID]
            "chat_count": n,
            "is_end": T/F,
            "created_at": 시간,
            "updated_at": 시간,
            "messages": [
                {
                    "id": serial
                    "timestamp": 시간,
                    "sender": 사용자 UUID,
                    "text": 메시지,
                    "file": url
                },
            ]
        }
        """,
    "responses" : {
        200 : "채팅방의 uid 정보 반환",
        400 : "채팅방이 이미 존재함",
        401 : "파이어베이스 인증 실패"
    },
    "tags" :
        ['/api/chats']
}

chats_chatId_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "내 특정 채팅방 정보 조회",
    "operation_description": 
        """
        ### `{chatId}`
        - 자료형 : str
        - 채팅 방의 uid
        ### 설명
        내 특정 채팅방의 채팅 정보 조회
        ### 인자 목록
        |인자                   |자료형         |설명                               |비고
        |:---------------------:|:-------------:|:----------------------------------|:----------------------------------------------|
        |`room_id`              |INTEGER        |방 번호                            |개인 간 대화일 경우 Null값 가짐                |
        |`members`              |UUID           |유저 목록                          |배열 형태                                      |
        |`chat_count`           |INTEGER        |채팅 개수                          |                                               |
        |`is_end`               |BOOLEAN        |채팅 종료 여부                     |                                               |
        |`created_at`           |DATETIME       |방 생성 시각                       |                                               |
        |`updated_at`           |DATETIME       |채팅 업데이트 시각                 |                                               |
        |`messages`             |INTEGER        |메시지 내역                        |배열 형태                                      |
        |messages - `id`        |SERIAL         |대화의 id                          |순차적 증가                                    |
        |messages - `timestamp` |DATETIME       |대화 보낸 시각                     |                                               |
        |messages - `sender`    |STRING         |대화 전송자                        |                                               |
        |messages - `text`      |STRING         |대화 내용                          |                                               |
        |messages - `file`      |STRING         |파일 링크                          |아직 미사용                                    |
        ### 제공 형식
        ```json
        {
            "room_id": number,
            "members" : [myUID, targetUID]
            "chat_count": n,
            "is_end": T/F,
            "created_at": 시간,
            "updated_at": 시간,
            "messages": [
                {
                    "id": serial
                    "timestamp": 시간,
                    "sender": 사용자 UUID,
                    "text": 메시지,
                    "file": url
                },
            ]
        }
        """,
    "responses" : {
        200 : "채팅 생성 성공",
        401 : "파이어베이스 인증 실패",
        404 : "채팅방 정보 없음"
    },
    "tags" :
        ['/api/chats/{chatId}']
}
chats_chatId_post = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "채팅 등록",
    "operation_description": 
        """
        ### `{chatId}`
        - 자료형 : str
        - 채팅 방의 uid
        ### 설명
        내 특정 채팅방에서 채팅 등록
        ### 입력 형식
        ```json
        {
            "text" : "채팅 내역"
        }
        """,
    "responses" : {
        200 : "채팅 생성 성공",
        400 : "채팅 정보 미전송",
        401 : "파이어베이스 인증 실패",
        404 : "채팅방 정보 없음"
    },
    "tags" :
        ['/api/chats/{chatId}']
}

test_carpool_terminate = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "(테스트) 방 운행 종료",
    "operation_description": 
        """
        ### 설명
        강제로 운행종료 진행
        """,
    "responses" : {
        200 : "방 종료 완료",
        404 : "방을 찾을 수 없음"
    },
    "tags" :
        ['test']
}

login_get = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "Firebase Auth 기반 OAuth 로그인",
    "operation_description": 
        """
        ### 설명
        로그인을 수행한다. 서버에 계정 정보가 없을 경우 post를 진행한다.
        ### 제공 값
        - Firebase Token
        - idToken : 사용자 uid
        - isRegister : 가입 여부 (Boolean)
        """,
    "responses" : {
        200 : "로그인 완료",
        400 : "회원 생성 실패",
        404 : "토큰 조회 실패"
    },
    "tags" :
        ['login']
}

login_post = {
    "auto_schema": 
        SwaggerAutoSchema,
    "operation_summary": 
        "Firebase Auth 기반 OAuth 회원가입",
    "operation_description": 
        """
        ### 설명
        회원가입을 수행한다.
        users 테이블에 레코드 추가, auth_user 테이블에 레코드 수정
        """,
    "responses" : {
        201 : "회원가입 완료",
        400 : "이미 회원가입을 완료함",
        401 : "파이어베이스 인증 실패"
    },
    "tags" :
        ['login']
}
