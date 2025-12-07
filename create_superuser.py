import os
import django
from django.contrib.auth import get_user_model

# 1. Djangoの設定を読み込む
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 2. ユーザーモデルを取得
User = get_user_model()

# 3. 環境変数からIDとパスワードを取得（なければデフォルト値を使用）
username = os.environ.get('SUPERUSER_NAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('SUPERUSER_PASSWORD', 'admin1234')

# 4. 管理者が存在しなければ作成
if not User.objects.filter(username=username).exists():
    print(f"管理ユーザー '{username}' を作成します...")
    User.objects.create_superuser(username, email, password)
    print("作成完了！")
else:
    print(f"管理ユーザー '{username}' は既に存在します。スキップします。")