# SPIEK-Following-Line
ロボカップジュニアのレスキューライン向けのコード  
これはSPIKE Primeのバージョン2代のMicroPython([SPIKE Legacy](https://spikelegacy.legoeducation.com/))で動作確認済み  
SPIKE3以降と互換性があるかは不明(2022/12/31時点でMicroPython機能がリリースすらされてない)  
Pybricksでは利用不可  

## LineTrace.py
これをパクればSPIEKPrimeでのライントレースと緑マーカーの"判定"(Uターンを含む)ができてしまうよ!!  
PID制御の比例定数(Kp,Ki,Kd)は自分で機体に合わせた調整が必要  
緑を判定したあとの動作は未作成(機体によって異なるから)  
緑のHSVのしきい値は環境によって変化しうるのでそれぞれ対応が必要

<details><summary>詳細</summary><div>

### 制御周期
制御周期は7.3ms前後  
関数化では0.1ms程度しか変化しなかった  
ネイティブコードエミッターはそもそもSPIKE Primeのアプリではエンコードできなかった=>`SyntaxError: invalid micropython decorator`  
バイパーコードエミッターも同様  
進むスピードは`basic_speed`で設定(デフォルトは30)

### 基本的なフロー
RGBのGの値をもとにPID制御をし、それと同時にRGBをHSVに変換して緑マーカの判定をする  
デフォルトでの緑の範囲はHue(色相)が150~180、Saturation(彩度)が20以上、Value(明度)が10以上になっている(だいぶ緩め)  
緑発見後は50度前進しつつ反対側にも緑マーカーがないかを確認 ※この後モーターは一時停止する  
反対にも緑マーカーがある(つまりUターンの指示である)と`u_turn()`関数に飛ぶ  

無限ループなのでボタンを押すまでは永遠に停止しない
</div></details>

## changeRGBtoHSV.py
RGBをHSVに変換する関数  
.get_rgb_intensity()の返り値をそのままぶっこめばHSVの値がタプルで返ってくる  
LineTrace.pyでも緑マーカの判定に使用  

H(色相)の範囲は0〜360  
S(彩度)の範囲は0〜100  
V(明度)の範囲は0〜255  

RGBのしきい値を調整すればPybricksやEV3でも使用可能
