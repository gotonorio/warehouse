# 文書管理システム（warehouse）

## 1. デフォルト設定

1. ユーザ登録アプリ名は「register」に固定。  
1. 居住者の閲覧用ログイン名は「sophiag」に固定。  
1. データ管理者は「data_manager」グループに設定する。  
1. お知らせ管理者は「news_manager」グループに設定する。

## 2. 文書管理システムの権限

閲覧ユーザは下記の5グループに分類される。

1. chairmanグループ（プログラム管理者）

   - ユーザ管理。
   - 文書ファイルの登録・削除

1. data_managerグループ（データ管理者）

   - 文書ファイルの登録・削除

1. news_managerグループ（お知らせデータ管理者）

   - トップページのお知らせ編集権限

1. loginグループ（区分所有者）

   - 全ての文書ファイルの閲覧権限（総会議案書、理事会議事録等）

1. 第三者グループ（ログインなしで閲覧する）

    - マンション概要の閲覧
    - 管理規約、細則の閲覧
    - 管理組合資料の閲覧

## 3. admin管理画面

1. admin画面で以下のgroupを作成しておく。
    - chairman （プログラム管理者）
        - can add user (user.add_user)
        - can add file (library.add_file)
        - can add news (notice.add_news)
        - can view file
    - data_manager（データ管理）
        - can add file (library.add_file)
        - can add news (notis.add_news)
        - can view file
    - news_manager（ファイル管理以外のデータ管理）
        - can add news (notis.add_news)
        - can view file
    - sophiag（区分所有者）
        - can view file

dd