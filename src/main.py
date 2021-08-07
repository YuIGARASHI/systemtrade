from line_handler import LineHandler
from liquid_handler import LiquidHandler
from common import ProductId

YEN_RATIO = 0.84
ETH_RATIO = 1 - YEN_RATIO


def main():
    line_hander = LineHandler()
    liquid_hander = LiquidHandler()
    balance = liquid_hander.fetch_balance()
    ticker_info = liquid_hander.fetch_ticker_info(product_id=ProductId.ETH_JPY)

    # YENとETHそれぞれの価値を算出
    eth_worth = float(ticker_info.best_buy_order) * float(balance.ETH)
    yen_worth = float(balance.JPY)

    # あるべきETHの価値から3000円以上ずれていれば取引を実行する
    target_eth_worth = (eth_worth + yen_worth) * ETH_RATIO
    diff_eth_worth = target_eth_worth - eth_worth # プラスならETHが足りない、マイナスならETH持ちすぎ
    if diff_eth_worth > 3000:
        line_hander.post_to_igarashi339("ETHが足りないため、ETHを買い増します。")
    elif diff_eth_worth < -3000:
        line_hander.post_to_igarashi339("ETHが多すぎるため、ETHを売ります。")
    else:
        line_hander.post_to_igarashi339("十分にバランスされているため取引を実施しませんでした。")


if __name__ == "__main__":
    main()