
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Yudai-Saito/DINE)
[![GitHub stars](https://img.shields.io/github/stars/Yudai-Saito/DINE)](https://github.com/Yudai-Saito/DINE/stargazers)
![GitHub all releases](https://img.shields.io/github/downloads/Yudai-Saito/DINE/total)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Yudai-Saito/DINE)

<div align="center">
<img src="https://user-images.githubusercontent.com/42965816/124094931-31c5e580-da94-11eb-8f68-02f286168c05.png" alt="属性" title="タイトル">
</div>

# ☁DINE 
DINEは、あなたのLINEとDiscordをスマートにお繋げします。 

**DINEを使用される方は、公式Discordサーバーへの参加をお願いしております : [Discordサーバー参加はこちら](https://discord.gg/cRaQ3XnzNb)**  
**フィードバック, 更新情報, 導入方法, FAQなど、オトクな情報いっぱいです。**
# 💻デモ
<video width="512px" height="288px" src="https://user-images.githubusercontent.com/42965816/124354801-d1c47000-dc48-11eb-85aa-8a42e9869348.mp4" controls></video>
</div>

# 🔍使い方
## 導入方法
* herokuデプロイ用ブランチ作成時に追記予定。

## Discord編
1. Discord Delelopver PortalからDiscordBOTを作りましょう。
1. DiscordBOTをサーバーに追加しましょう。
1. LINEを受信するチャンネルを設定しましょう。
1. LINEとDiscordからメッセージを送受信できることを確認しましょう。

## LINE編
1. LINE DevelopersからLINEBOTを作りましょう。
1. Discordサーバーと連携するために、メニューから"サーバーと連携"をタップしましょう。
1. Discordサーバーに連携用パスワードを入力して連携を完了させましょう。
1. LINEとDiscordからメッセージを送受信できることを確認しましょう。

# 🔨開発内容と今後の方針
## 使用したライブラリ・技術
* Python  
	* [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
	* [responder](https://github.com/taoufik07/responder)
	* [discord.py](https://github.com/Rapptz/discord.py)
	* [line-bot-sdk](https://github.com/line/line-bot-sdk-python)
* PostgreSQL
* ngrok  
## プロジェクトの反省
>今回のプロジェクトでは、並列処理, 非同期処理を使用したため、学習コストは高めだった。両者の理解により、ブロッキングせず, 高パフォーマンスなシステムを作るにはどうしたら良いのかという考えが身につき,今後のプロジェクトでも活かそうと思う。  
>webフレームワークの使用、ORMでのCRUD操作などを通し、バックエンドの楽しさと興味深さがより一層深まった。次回は、これらの機能が詰まったWebアプリを作ろうと思う。  
>また、LINE Messaging APIの仕様上、プッシュメッセージの最大送信料が1000件なため、私自身でのDINE公開運用を行うことは難しいものとなってしまったのは残念な結果だ。

## 今後の開発目標
>今後は、LINEBOTの完全非同期化, Discordからのスケジュール機能の追加などを予定している。  
>リファクタリングも時間を見つけて進めていきたい。
# 📖ライセンス
```
Copyright 2021 YudaiSaito

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
# 💬作成者情報
* 齋藤 悠大 - Yudai Saito
* yudai.saito.dev@gmail.com