from line_handler import LineHandler
from liquid_handler import LiquidHandler


def main():
    line_hander = LineHandler()
    line_hander.post_to_igarashi339("サンプル実行です")


if __name__ == "__main__":
    main()