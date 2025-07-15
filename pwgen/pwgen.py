import argparse
import secrets
import string
import sys

def generate_password(length, char_groups):
    """各文字グループから最低1文字を含むパスワードを生成する"""
    # 1. 各グループから必須文字を1つずつ選ぶ
    password_chars = [secrets.choice(group) for group in char_groups]

    # 2. 残りの長さの分、すべての文字種を結合したセットからランダムに選ぶ
    combined_charset = ''.join(char_groups)
    remaining_length = length - len(password_chars)
    password_chars.extend(secrets.choice(combined_charset) for _ in range(remaining_length))

    # 3. 文字のリストをシャッフルして、最終的なパスワードを作成する
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

def generate_and_print_passwords(length, char_groups, count):
    """指定されたパラメータでパスワードを生成し、出力する"""
    # パスワード長が必須文字数より短い場合はエラー
    if length < len(char_groups):
        # argparse.ArgumentParser.error()はプロセスを終了させるため、
        # ここではよりテストしやすいように例外を送出する
        raise ValueError(
            f"パスワード長は最低 {len(char_groups)} 文字必要です。"
        )

    # パスワードを生成して出力
    for _ in range(count):
        password = generate_password(length, char_groups)
        print(password)

def main():
    # 文字セットをグループとして定義
    char_groups_map = {
        'simple': (string.ascii_lowercase,),
        'medium': (string.ascii_lowercase, string.digits),
        'strong': (string.ascii_lowercase, string.ascii_uppercase, string.digits),
        'complex': (string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*()_+-=[]{}|;:',.<>/?"),
    }

    # コマンドライン引数のパーサーを設定
    parser = argparse.ArgumentParser(
        description="強力なパスワードを生成するコマンドラインツール",
        epilog="使用例: python pwgen.py -t complex -l 24 -c 5"
    )
    parser.add_argument(
        '-t', '--type',
        required=True,
        choices=char_groups_map.keys(),
        help=f"パスワードの文字種を選択します: {', '.join(char_groups_map.keys())}"
    )
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=16,
        help="パスワードの長さを指定します (デフォルト: 16)"
    )
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=1,
        help="生成するパスワードの数を指定します (デフォルト: 1)"
    )

    args = parser.parse_args()
    selected_groups = char_groups_map[args.type]

    try:
        generate_and_print_passwords(args.length, selected_groups, args.count)
    except ValueError as e:
        parser.error(str(e))

if __name__ == '__main__':
    main()