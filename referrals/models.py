# referrals/models.py

from django.db import models

class Salon(models.Model):
    name = models.CharField("店舗名", max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name = "店舗"; verbose_name_plural = "店舗一覧"

class Partner(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="紐付け店舗")
    name = models.CharField("飲食店名", max_length=100)
    phone_number = models.CharField("電話番号", max_length=20)
    referral_code = models.CharField("紹介コード", max_length=20, unique=True)
    reward_per_customer = models.IntegerField("1人あたりの報酬額", default=1000)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    def __str__(self):
        salon_name = self.salon.name if self.salon else "店舗未定"
        return f"{self.name} ({salon_name})"
    class Meta: verbose_name = "パートナー"; verbose_name_plural = "パートナー一覧"

class Customer(models.Model):
    name = models.CharField("お名前（ニックネーム可）", max_length=100)
    phone_number = models.CharField("電話番号", max_length=20, blank=True, null=True)

    referred_by = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, verbose_name="紹介元", related_name="customers")
    joined_at = models.DateTimeField("入会日時", auto_now_add=True)
    
    # ▼▼▼【追加】来店済みフラグ ▼▼▼
    has_visited = models.BooleanField("来店済み", default=False)
    
    is_paid = models.BooleanField("報酬支払い済み", default=False)

    def __str__(self):
        return f"{self.name} (紹介: {self.referred_by.name if self.referred_by else '削除済み'})"
    class Meta: verbose_name = "お客様"; verbose_name_plural = "お客様一覧"