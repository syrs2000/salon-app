from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse  # ← 追加
from .models import Partner
from .forms import CustomerForm
import qrcode  # ← 追加
from io import BytesIO  # ← 追加

def customer_signup(request, referral_code):
    # 1. URLに含まれる紹介コード(例: RAMEN001)から、パートナー情報を取得する
    # もしコードが間違っていたら「ページが見つかりません(404)」を出す安全設計です
    partner = get_object_or_404(Partner, referral_code=referral_code)

    if request.method == 'POST':
        # 登録ボタンが押された時の処理
        form = CustomerForm(request.POST)
        if form.is_valid():
            # まだデータベースには保存せず、インスタンスだけ作る
            customer = form.save(commit=False)
            # ここで紹介元（パートナー）を自動的にセット！
            customer.referred_by = partner
            # 保存
            customer.save()
            # 完了画面へ（まだ作っていないので仮の完了ページへ）
            return render(request, 'referrals/success.html', {'partner': partner})
    else:
        # 最初に画面を開いた時の処理（空のフォームを表示）
        form = CustomerForm()

    # 画面（HTML）にデータを渡して表示
    context = {
        'partner': partner,
        'form': form
    }
    return render(request, 'referrals/signup.html', context)

def partner_qrcode(request, referral_code):
    # 1. パートナーが存在するか確認
    partner = get_object_or_404(Partner, referral_code=referral_code)
    
    # 2. QRコードにするURLを作成
    # build_absolute_uriを使うと 'http://ドメイン/...' という完全なURLを自動で作ってくれます
    # ユーザーが登録する画面のURLを指定します
    signup_url = request.build_absolute_uri(f'/signup/{referral_code}/')
    
    # 3. QRコードを生成
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
    )
    qr.add_data(signup_url)
    qr.make(fit=True)
    
    # 4. 画像データとしてメモリ上に書き出す
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # 5. ブラウザに「これは画像ですよ」と伝えるレスポンスを返す
    return HttpResponse(buffer.getvalue(), content_type="image/png")