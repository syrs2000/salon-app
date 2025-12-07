from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Partner, Customer

# 飲食店（パートナー）の管理画面設定
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    # 【ここが重要】リストの中に 'get_qrcode_link' が含まれているか確認してください
    list_display = ('name', 'referral_code', 'reward_per_customer', 'get_qrcode_link', 'created_at')
    
    search_fields = ('name', 'referral_code')

    # ボタンを作る関数
    def get_qrcode_link(self, obj):
        try:
            url = reverse('partner_qrcode', args=[obj.referral_code])
            return format_html('<a class="button" href="{}" target="_blank" style="background:#447e9b; color:white; padding:3px 8px; border-radius:3px; text-decoration:none;">QR表示</a>', url)
        except Exception:
            return "-"
    
    get_qrcode_link.short_description = "QRコード"
    get_qrcode_link.allow_tags = True

# お客様の管理画面設定
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'referred_by', 'joined_at', 'is_paid')
    list_filter = ('referred_by', 'is_paid', 'joined_at')
    search_fields = ('name',)