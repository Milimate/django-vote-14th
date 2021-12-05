# django-vote-14th
ceos 15th executive voting application of Millimate-back 

## 1차 모델링

### 1. User 모델
> Abstractbaseuser 이용

|이름|열|태그|자료형|
|---|---|---|---|
|id| |pk|int|
|username|아이디|unique|char|
|password|비밀번호| |char|
|email|이메일|unique|str|


### 2. Candidate 모델

|이름|열|태그|자료형|
|---|---|---|---|
|id| |pk|int|
|name|이름| |char|
|picture|카톡 프로필 사진| |str|
|position|포지션-프론트/백| |char|
|vote_count|투표수| |int|




## 1차 api 명세서

### 1.메인화면   
> Request

|태그|url|설명|열|
|---|---|---|---|
|GET|/ceos-15th-partzzang|메인 화면||





### 2. 회원가입 화면   
> Request   

   
|태그|url|설명|열|
|---|---|---|---|
|GET|/ceos-15th-partzzang/signup|회원가입 페이지||
|POST|/ceos-15th-partzzang/signup|||
 


> Request 형식

|Name|Tags|Column|
|---|---|---|
|username|메인 화면|사용자 아이디|
|password|메인 화면|사용자 비밀번호|
|email|메인 화면|사용자 이메일|




### 3. 로그인 화면
>Request

|태그|url|설명|열|
|---|---|---|---|
|GET|/ceos-15th-partzzang/login|로그인 화면||
|GET|/ceos-15th-partzzang/login|||


> Request 형식

|Name|Tags|Column|
|---|---|---|
|username|메인 화면|사용자 아이디|
|password|메인 화면|사용자 비밀번호|




### 4. 투표 화면
> Request

|태그|url|설명|열|
|---|---|---|---|
|GET|/ceos-15th-partzzang/vote|투표 화면||
|POST|/ceos-15th-partzzang/vote/<int:pk >|||


> Response Body

|Name|Type|Description|
|---|---|---|
|id|int|후보자 id|
|name|char|후보자 이름|
|picture|string||
|position|char||
|vote_count|int||

