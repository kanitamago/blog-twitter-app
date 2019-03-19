#__init__で作成されるアプリケーションを読み込む
from blog import app

if __name__ == "__main__":
    app.run(port=9999)
