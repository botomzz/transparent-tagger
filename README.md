
forked from [https://github.com/corkborg/wd14-tagger-standalone](https://github.com/corkborg/wd14-tagger-standalone)

The feature of this program is that it generates a transparent window using TKinter, captures everything below the window on the screen, keywords it using tagger, and saves the results to the clipboard.

このプログラムの特徴は、TKinter を使用して透明なウィンドウを生成し、画面上のウィンドウの下のすべてをキャプチャし、タグを使用してキーワードを付け、結果をクリップボードに保存することです。

## install
```
Please read https://github.com/corkborg/wd14-tagger-standalone
```
## execute　起動方法

```
usage: tkinter_trans.py

windows:tagger_gui.bat
```
## How to use 使い方
```
As the description in the window,spinbox numericus mean threshold,and [run] button mean execute tagger.

Run tagger_gui.bat, place a transparent window over the part of the screen you want to capture, change the threshold value in the spin box (default is 0.1) as desired, and press the RUN button. After a while, a list of tags will be stored in the clipboard as text.

tagger_gui.batを実行して画面内のキャプチャしたい部分の上に透明ウィンドウを配置して、スピンボックス内のthreshold値（初期値は0.1）を任意に変更して、RUNボタンを押してください。しばらく後にクリップボード内にタグの一覧がテキストにて格納されます。
```
## Copyright
```
Public domain, except borrowed parts (e.g. `dbimutils.py` )
```
