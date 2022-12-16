# ImageEditApplication
GUI上で画像を編集できるプログラムです。
USB機器の挿入をトリガーとして特定のフォルダ下にある画像ファイルを、事前に保存された設定に従って自動で編集してくれます。
## 自動編集のためのセットアップ
１．まずはUSB機器の'idVendor'と'idProduct'を取得します。
    取得するには認識させたいUSB機器を差したまま、プロンプトで'lsusb'と入力します。

２．次に'90-usbmem.rules'を編集します。
    ファイル中の
    ATTRS{idVendor}=="***",\
    ATTRS{idProduct}=="***",\
    の***の部分を先ほど取得したidVendorとidProductに置き換えます。

３．'90-usbmem.rules'に'App.sh'までの絶対パスを書き加えます。
    RUN+="/bin/bash ***"
    ***の部分を'App.sh'までの絶対パスに置き換えます。

４．'90-usbmem.rules'を移動させます。
    プロンプトで一番上の階層まで移動し、cdコマンドで'/etc/udev/rules.d/'まで移動します。
    移動した階層まで'90-usbmem.rules'ファイルを移動させます。

５．'App.sh'の編集をします。
    cd **pythonプログラムがあるこのフォルダまでのパス**と書かれているところに、
    'App.sh'までの絶対パスを入力します。

これでセットアップを完了です。

## GUIアプリケーションの使い方
main.pyを実行すると、GUIのアプリケーションが立ち上がります。
main.pyのみを利用するのであれば、基本的にセットアップはいりません。
編集したい画像ファイルと保存先を指定して保存を押すと編集が実行されます。

編集はsavedata.jsonに記録された設定に従って行われます。
編集設定ボタンを押すことで、GUIで編集の設定を行うことが出来ます。
仕様上、リサイズと切り抜きで入力した設定は、適用ボタンを押さない限り適用されません。
ただし、ON、OFFの設定は即座に反映されます。

編集設定のウィンドウはXボタンを押すことでも閉じることは出来ますが、保存ボタンを押して終了しないと設定はsavedata.jsonに保存されません。ご注意ください。

## 自動編集の使い方
自動編集はoriginalフォルダ下の画像ファイルに対して行われます。
また、編集内容はsavedata.jsonに保存されている設定に従って行われます。
自動編集を行うには、セットアップで事前に指定したUSB機器をraspberryPiに差し込みます。
自動編集のためのセットアップが上手くいっていれば、Editedフォルダ下に編集済みの画像ファイルが生成されます。