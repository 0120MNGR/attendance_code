import pyautogui
import time
from itertools import permutations, product

def enter_password(password):
    # パスワードを1文字ずつ入力
    for char in password:
        pyautogui.press(char)

    # Tabキーを2回押す
    pyautogui.press('tab', presses=2)

    # Enterキーを押す
    pyautogui.press('enter')

    # 1.5秒待つ
    time.sleep(1.1)

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
    # generate_passwords("1???")  # 1??? の形式のパスワードを入力
    # generate_passwords("2?4?")  # 2?4? の形式のパスワードを入力
    generate_passwords("1???")

if __name__ == "__main__":
    main()