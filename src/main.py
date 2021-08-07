from line_handler import LineHandler
from liquid_handler import LiquidHandler


def main():
    line_hander = LineHandler()
    liquid_hander = LiquidHandler()
    balance = liquid_hander.fetch_balance()
    line_hander.post_to_igarashi339(balance.JPY)


if __name__ == "__main__":
    main()