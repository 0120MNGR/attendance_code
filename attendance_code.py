import pyautogui
import time

# 0000から9999までの4桁の数を全て生成
time.sleep(5)
for i in range(10000):
    password = str(i).zfill(4)  # 数を4桁になるように0を前に追加

    # パスワードを1文字ずつ入力
    for char in password:
        pyautogui.press(char)

    # Tabキーを2回押す
    pyautogui.press('tab', presses=2)

    # Enterキーを押す
    pyautogui.press('enter')

    # 1.5秒待つ
    time.sleep(3.0)
