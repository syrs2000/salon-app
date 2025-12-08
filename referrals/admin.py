from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Partner, Customer, Salon

# 1. 店舗（Salon）の管理画面
@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name',)

# 2. 飲食店（Partner）の管理画面
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    # 一覧に表示する項目
    # 店舗、紹介コード、ページ確認ボタン、QRボタン、登録日時
    list_display = ('name', 'salon', 'referral_code', 'view_page_link', 'get_qrcode_link', 'created_at')
    
    search_fields = ('name', 'referral_code')
    list_filter = ('salon',) # 店舗で絞り込み

    # 【ボタン1】QRコードを表示するボタン
    def get_qrcode_link(self, obj):
        try:
            url = reverse('partner_qrcode', args=[obj.referral_code])
            return format_html('<a class="button" href="{}" target="_blank" style="background:#6c757d; color:white; padding:3px 8px; border-radius:3px; text-decoration:none;">QR画像</a>', url)
        except Exception:
            return "-"
    get_qrcode_link.short_description = "QR"
    get_qrcode_link.allow_tags = True

    # 【ボタン2】その店の登録ページ（HTML）を開くボタン
    def view_page_link(self, obj):
        try:
            # そのパートナーの登録画面URLを取得
            url = reverse('customer_signup', args=[obj.referral_code])
            # 青いボタンで表示
            return format_html('<a href="{}" target="_blank" style="background:#007bff; color:white; padding:3px 8px; border-radius:3px; text-decoration:none;">📄 ページを開く</a>', url)
        except Exception:
            return "-"
    view_page_link.short_description = "登録画面"
    view_page_link.allow_tags = True

# 3. お客様（Customer）の管理画面
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # 一覧画面で見たい項目（ID、名前、電話、紹介元、来店有無、入会日、支払有無）
    list_display = ('id', 'name', 'phone_number', 'referred_by', 'has_visited', 'joined_at', 'is_paid')
    
    # 一覧画面で直接チェックを入れられるようにする（便利！）
    list_editable = ('has_visited', 'is_paid')
    
    # 絞り込みフィルター
    list_filter = ('referred_by', 'has_visited', 'is_paid', 'joined_at')
    
    # 検索ボックス（名前と電話番号で検索可能）
    search_fields = ('name', 'phone_number')