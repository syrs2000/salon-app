from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
# ↓【重要】ここに 'Salon' を追加しました
from .models import Partner, Customer, Salon 

# 1. 店舗（Salon）の管理画面
@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name',)

# 2. 飲食店（Partner）の管理画面
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    # 一覧に 'salon' (店舗) を追加して表示
    list_display = ('name', 'salon', 'referral_code', 'reward_per_customer', 'get_qrcode_link', 'created_at')
    
    search_fields = ('name', 'referral_code')
    list_filter = ('salon',) # 店舗で絞り込みできるように追加

    # ボタンを作る関数
    def get_qrcode_link(self, obj):
        try:
            url = reverse('partner_qrcode', args=[obj.referral_code])
            return format_html('<a class="button" href="{}" target="_blank" style="background:#447e9b; color:white; padding:3px 8px; border-radius:3px; text-decoration:none;">QR表示</a>', url)
        except Exception:
            return "-"
    
    get_qrcode_link.short_description = "QRコード"
    get_qrcode_link.allow_tags = True

# 3. お客様（Customer）の管理画面
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # 'has_visited' を表示に追加
    list_display = ('name', 'referred_by', 'has_visited', 'joined_at', 'is_paid')
    
    # これを入れると、一覧画面でそのままチェックボックスをON/OFFできます（便利！）
    list_editable = ('has_visited', 'is_paid')
    
    list_filter = ('referred_by', 'has_visited', 'is_paid', 'joined_at')
    search_fields = ('name',)