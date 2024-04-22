##### admin管理画面

1. admin画面で以下のgroupを作成しておく。
    - guest（permission無し）  
    - data_manager  
        - information|Can add information  
        - library| Can add file  
        - notice|Can add news  
    - news_manager  
        - notice|Can add news  
1. admin画面で居住者用として「sophiag」ユーザを作成する。  
    - 「group」をguestとする。  

##### デフォルト設定

1. ユーザ登録アプリ名は「register」に固定。  
1. 居住者の閲覧用ログイン名は「sophiag」に固定。  
1. データ管理者は「data_manager」グループに設定する。  
1. お知らせ管理者は「news_manager」グループに設定する。


##### 文書管理システムの権限

###### guestグループ（第三者）
- 管理費等の閲覧
- マンション概要の閲覧
- 管理規約、細則の閲覧
- 管理組合資料の閲覧

###### sophiagグループ（区分所有者）
- guestグループの全て。
- 全ての文書ファイル（総会議案書、理事会議事録等）。

###### directorグループ（理事）
- sophiagグループの全て。
- 氏名を除く各住戸の管理費等の一覧。

###### chairmanグループ（理事長）
- directorグループの全て。
- 各住戸の管理費等の一覧。

###### news_managerグループ
- sofiagグループの全て。
- トップページのお知らせ編集権限。

###### data_managerグループ
- news_managerの全て。
- 文書ファイルの登録・削除

##### ファイル保存について
- FileField()を利用する。
- upload_toで保存パスを動的に設定する。
- django_cleanupパッケージでファイル削除を行う。（同じファイル名で保存した場合の処理）