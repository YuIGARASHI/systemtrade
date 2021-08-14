from line_handler import LineHandler
from liquid_handler import LiquidHandler
from common import ProductId
import time

YEN_RATIO = 1
ETH_RATIO = 1 - YEN_RATIO


def calc_total_worth(ticker_info, balance):
    """
    現在保有している合計資産額と、Ethの資産額を計算して返す。
    """
    eth_worth = float(ticker_info.best_buy_order) * float(balance.ETH)
    yen_worth = float(balance.JPY)
    return eth_worth, eth_worth + yen_worth


def main():
    line_hander = LineHandler()
    liquid_hander = LiquidHandler()
    balance = liquid_hander.fetch_balance()
    ticker_info = liquid_hander.fetch_ticker_info(product_id=ProductId.ETH_JPY)
    eth_worth, total_worth = calc_total_worth(ticker_info, balance)
    line_hander.post_to_igarashi339("取引前の残高は" + str(total_worth) + "円です。")

    # あるべきETHの価値から3000円以上ずれていれば取引を実行する
    target_eth_worth = (total_worth) * ETH_RATIO
    diff_eth_worth = target_eth_worth - eth_worth # プラスならETHが足りない、マイナスならETH持ちすぎ
    if diff_eth_worth > 3000:
        line_hander.post_to_igarashi339("ETHが足りないため、ETHを買い増します。")
        mount = float(diff_eth_worth) / float(ticker_info.best_sell_order)
        liquid_hander.make_market_order(ProductId.ETH_JPY, mount, "buy")
        time.sleep(5)
        balance_after = liquid_hander.fetch_balance()
        _, total_worth_after = calc_total_worth(ticker_info, balance_after)
        line_hander.post_to_igarashi339("取引後の残高は" + str(total_worth_after) + "円です。")
    elif diff_eth_worth < -3000:
        line_hander.post_to_igarashi339("ETHが多すぎるため、ETHを売ります。")
        mount = float(diff_eth_worth * (-1)) / float(ticker_info.best_buy_order)
        liquid_hander.make_market_order(ProductId.ETH_JPY, mount, "sell")
        time.sleep(5)
        balance_after = liquid_hander.fetch_balance()
        _, total_worth_after = calc_total_worth(ticker_info, balance_after)
        line_hander.post_to_igarashi339("取引後の残高は" + str(total_worth_after) + "円です。")
    else:
        line_hander.post_to_igarashi339("十分にバランスされているため取引を実施しませんでした。")


if __name__ == "__main__":
    main()