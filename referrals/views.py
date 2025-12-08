from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# 【重要】Count と Q をインポート
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

from .models import Partner, Customer
from .forms import CustomerForm
import qrcode
from io import BytesIO

# 1. お客様登録画面
def customer_signup(request, referral_code):
    partner = get_object_or_404(Partner, referral_code=referral_code)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.referred_by = partner
            customer.save()
            return render(request, 'referrals/success.html', {'partner': partner})
    else:
        form = CustomerForm()

    context = {
        'partner': partner,
        'form': form
    }
    return render(request, 'referrals/signup.html', context)

# 2. QRコード生成
def partner_qrcode(request, referral_code):
    partner = get_object_or_404(Partner, referral_code=referral_code)
    
    signup_url = request.build_absolute_uri(f'/signup/{referral_code}/')
    
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
    )
    qr.add_data(signup_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    return HttpResponse(buffer.getvalue(), content_type="image/png")

# 3. 月次レポート（ダッシュボード）
@login_required
def dashboard_stats(request):
    # 月ごとにグループ化し、紹介数と来店数を集計
    summary_data = (
        Customer.objects
        .annotate(month=TruncMonth('joined_at'))
        .values('month', 'referred_by__name', 'referred_by__salon__name')
        .annotate(
            total_customers=Count('id'),
            # 来店済み（has_visited=True）のみカウント
            visited_customers=Count('id', filter=Q(has_visited=True))
        )
        .order_by('-month')
    )

    context = {
        'summary_data': summary_data
    }
    return render(request, 'referrals/dashboard.html', context)