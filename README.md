# SPIEK-Following-Line
これはSPIKE PrimeのMicroPythonで動くよ。Pybricksでは使えんで。  
## LineTrace.py
これをパクればSPIEKPrimeでのライントレースと緑マーカーの判定(Uターンを含む)ができてしまうよ!!  
係数は自分で調整しろ  
緑を判定したあとの動作も作ってないよ

## changeRGBtoHSV.py
RGBをHSVに変換する関数  
.get_rgb_intensity()の返り値をそのままぶっこめばHSVの値がタプルで返ってくる  

H(色相)の範囲は0〜360  
S(彩度)の範囲は0〜100  
V(明度)の範囲は0〜255  
直したきゃ直して  