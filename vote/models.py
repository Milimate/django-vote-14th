from django.db import models

# Create your models here.


# 후보자 모델
class Candidate(models.Model):
    POSITION_CHOICES = (
        ('Front_end', 'Front_end'),
        ('Back_end', 'Back_end'),
    )
    name = models.CharField(max_length=20) # 이름
    picture = models.ImageField(upload_to="", blank=True, null=True) # 프로필 사진 # 루트 media에 저장되도록 경로설정
    position = models.CharField(choices=POSITION_CHOICES, max_length=20) # 프론트/백 포지션
    vote_count = models.PositiveIntegerField(default=0) # 투표 수

    def __str__(self):
        return self.name # 후보자 이름을 대표로 함