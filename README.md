

文書管理システム（warehouse）
programming by Norio.Goto

このプログラムは、MIT ライセンスのもとで公開されています。
このライセンスにより、誰でも自由にこの文書をコピー、改変、再配布できますが、
著作権表示（著者名）およびライセンス表示を保持する必要があります。

 --- MIT License ---

 Copyright (c) [2025] Norio.Goto

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 --- End MIT License ---


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
        - can add news (notice.add_news)
        - can view file
    - news_manager（ファイル管理以外のデータ管理）
        - can add news (notice.add_news)
        - can view file
    - sophiag（区分所有者）
        - can view file

