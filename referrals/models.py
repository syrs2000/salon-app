from django.db import models
from django.contrib.auth.models import User

# 1. 紹介元（飲食店などのパートナー）
class Partner(models.Model):
    name = models.CharField("飲食店名", max_length=100)
    phone_number = models.CharField("電話番号", max_length=20)
    
    # 紹介コード（例: RAMEN001）
    referral_code = models.CharField("紹介コード", max_length=20, unique=True)
    
    # 報酬額設定（店ごとに変えられるように）
    reward_per_customer = models.IntegerField("1人あたりの報酬額", default=1000)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.referral_code})"

    class Meta:
        verbose_name = "パートナー（飲食店）"
        verbose_name_plural = "パートナー一覧"

# 2. お客様（紹介された人）
class Customer(models.Model):
    # 名前や連絡先（Userモデルを使わずシンプルに管理する場合の例）
    name = models.CharField("お名前（ニックネーム可）", max_length=100)
        
    # どのパートナーからの紹介か
    referred_by = models.ForeignKey(
        Partner, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="紹介元",
        related_name="customers"
    )
    
    joined_at = models.DateTimeField("入会日時", auto_now_add=True)
    
    # まだ報酬を支払っていないかどうかの管理
    is_paid = models.BooleanField("報酬支払い済み", default=False)

    def __str__(self):
        return f"{self.name} (紹介: {self.referred_by.name if self.referred_by else 'なし'})"

    class Meta:
        verbose_name = "お客様"
        verbose_name_plural = "お客様一覧"