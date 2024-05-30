#### 【デフォルト設定】

1. ユーザ登録アプリ名は「register」に固定。  
1. 居住者の閲覧用ログイン名は「sophiag」に固定。  
1. データ管理者は「data_manager」グループに設定する。  
1. お知らせ管理者は「news_manager」グループに設定する。


#### 【文書管理システムの権限】
###### chairmanグループ（理事長）
- ユーザ管理。
- 文書ファイルの登録・削除

###### data_managerグループ
- 文書ファイルの登録・削除

###### news_managerグループ
- トップページのお知らせ編集権限。

###### 区分所有者
- 全ての文書ファイル（総会議案書、理事会議事録等）。

###### 第三者
- マンション概要の閲覧
- 管理規約、細則の閲覧
- 管理組合資料の閲覧

#### admin管理画面

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
