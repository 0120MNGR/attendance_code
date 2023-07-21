import cv2
import numpy as np
from PIL import ImageGrab
import sys
import pyautogui
import time
from itertools import permutations, product

def check_image_match(target_image):
    # スクリーンショットを撮る
    screenshot = ImageGrab.grab()

    # PILのImageオブジェクトをOpenCVの画像データ（グレースケール）に変換
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 比較する画像を読み込む（グレースケール）
    template = cv2.imread(target_image, 0)

    # 画像マッチングのメソッドを設定
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        method = eval(meth)
        
        # テンプレートマッチング
        res = cv2.matchTemplate(screenshot_cv,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        h, w = template.shape[::]

        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 画像がマッチした場合、その位置を四角で囲む
        cv2.rectangle(screenshot_cv,top_left, bottom_right, 255, 2)
        
        # 一定の閾値以上ならマッチと判断しプログラムを終了
        if max_val > 0.95:
            print("Image matched. Stopping the program.")
            sys.exit()


def enter_password(password):
    # パスワードを1文字ずつ入力
    for char in password:
        pyautogui.press(char)

    # Tabキーを2回押す
    pyautogui.press('tab', presses=2)

    # Enterキーを押す
    pyautogui.press('enter')

    # 1.5秒待つ
    time.sleep(1.5)

    # 画像マッチングを行い、マッチしたらプログラムを停止
    check_image_match('success.png')

def generate_passwords(digits):
    # "?"の数を数え、その数の全通りの組み合わせを生成
    wildcard_count = digits.count("?")

    # 全ての桁の数値が異なる組み合わせを先に試す
    for combination in permutations(range(10), wildcard_count):
        password = digits
        # "?"を順に置換
        for num in combination:
            password = password.replace("?", str(num), 1)
        enter_password(password)

    # 全ての桁の数値が異なる以外の組み合わせを試す
    for combination in product(range(10), repeat=wildcard_count):
        if len(set(combination)) == wildcard_count:  # すでに試した組み合わせをスキップ
            continue
        password = digits
        # "?"を順に置換
        for num in combination:
            password = password.replace("?", str(num), 1)
        enter_password(password)

def main():
    # 5秒待つ（プログラムを開始してから操作対象のアプリケーションをアクティブにするための待機時間）
    time.sleep(5)

    # パスワードを生成して入力
    generate_passwords("059?")

if __name__ == "__main__":
    main()
