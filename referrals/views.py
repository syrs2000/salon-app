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
from .forms import PartnerLoginForm

# 1. お客様登録画面
def customer_signup(request, referral_code):
    partner = get_object_or_404(Partner, referral_code=referral_code)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.referred_by = partner
            customer.save()
            return render(request, 'referrals/success.html', {
                'partner': partner,
                'customer' : customer,})
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
    # 1. URLからソート順を取得（デフォルトは「日付の新しい順」）
    sort_param = request.GET.get('sort', '-month')

    # 2. 並び替えルールの定義
    # 左側がURLのパラメータ、右側がデータベースの項目名
    sort_options = {
        'month': 'month',                    # 対象月 (昇順 1月→12月)
        '-month': '-month',                  # 対象月 (降順 12月→1月)
        'salon': 'referred_by__salon__name', # 店舗名 (あいうえお順)
        'partner': 'referred_by__name',      # 紹介元名 (あいうえお順)
        'total': 'total_customers',          # 紹介人数 (少ない順)
        '-total': '-total_customers',        # 紹介人数 (多い順)
        'visited': 'visited_customers',      # 来店人数 (少ない順)
        '-visited': '-visited_customers',    # 来店人数 (多い順)
    }

    # 指定されたソートが無効なら、デフォルト(-month)に戻す安全策
    order_by_field = sort_options.get(sort_param, '-month')

    # 3. データの集計と取得
    summary_data = (
        Customer.objects
        # 入会日を「月」単位に丸める
        .annotate(month=TruncMonth('joined_at'))
        # 「月」「紹介元」「店舗」の組み合わせでグループ化する
        .values('month', 'referred_by__name', 'referred_by__salon__name')
        # 人数を数える
        .annotate(
            total_customers=Count('id'),                             # 紹介総数
            visited_customers=Count('id', filter=Q(has_visited=True)) # 来店済みのみ
        )
        # ここで並び替えを適用
        .order_by(order_by_field)
    )

    context = {
        'summary_data': summary_data,
        'current_sort': sort_param,  # 画面側で「今の並び順」を知るために渡す
    }
    return render(request, 'referrals/dashboard.html', context)


# 1. パートナーログイン
def partner_login(request):
    if request.method == 'POST':
        form = PartnerLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['referral_code']
            phone = form.cleaned_data['phone_number']
            
            # 紹介コードと電話番号が一致するパートナーを探す
            try:
                partner = Partner.objects.get(referral_code=code, phone_number=phone)
                # セッションにIDを保存（これでログイン状態にする）
                request.session['partner_id'] = partner.id
                return redirect('partner_dashboard')
            except Partner.DoesNotExist:
                form.add_error(None, "紹介コードまたは電話番号が間違っています")
    else:
        form = PartnerLoginForm()
    
    return render(request, 'referrals/partner_login.html', {'form': form})

# 2. パートナー専用ダッシュボード
def partner_dashboard(request):
    # ログインチェック（セッションにIDがあるか？）
    partner_id = request.session.get('partner_id')
    if not partner_id:
        return redirect('partner_login')
    
    partner = get_object_or_404(Partner, id=partner_id)
    
    # そのパートナーのデータだけを集計
    summary_data = (
        Customer.objects
        .filter(referred_by=partner)  # ★ここが重要：自分の店の客だけにする
        .annotate(month=TruncMonth('joined_at'))
        .values('month')
        .annotate(
            total_customers=Count('id'),
            visited_customers=Count('id', filter=Q(has_visited=True))
        )
        .order_by('-month')
    )
    
    context = {
        'partner': partner,
        'summary_data': summary_data
    }
    return render(request, 'referrals/partner_dashboard.html', context)

# 3. パートナーログアウト
def partner_logout(request):
    request.session.flush() # セッション削除
    return redirect('partner_login')