import math
from datetime import datetime


orders = [
    {"date": "2021/1/1",
     "total_price": 2000000},
    {"date": "2021/2/2",
     "total_price": 3000000},
    {"date": "2021/3/3",
     "total_price": 4000000},
    {"date": "2021/4/4",
     "total_price": 5000000},
]


class PointsDefinition:
    intervals = [30, 60, 90, 120]
    modes = [0, 0, 0, 0]
    params = [
        [9, 3, 0.1],
        [0.1],
        [1 / 60, 0.1]
    ]
    methods = [
        lambda a, b, k, order_diff, total_price: k / math.log10(
            a + b * order_diff) * total_price,
        lambda a, order_diff, total_price: a * total_price,
        lambda a, b, order_diff, total_price: -a * order_diff * total_price + b * total_price
    ]

    def __init__(self):
        pass

    @staticmethod
    def cal_score(user_orders):
        current_date = datetime.today().strftime('%Y/%m/%d')
        score = 0
        for order in user_orders:
            order_date = datetime.strptime(order["date"], '%Y/%m/%d')
            order_diff = (datetime.strptime(current_date, '%Y/%m/%d') - order_date).total_seconds() / (60*60*24)
            if order_diff >= PointsDefinition.intervals[-1]:
                score += PointsDefinition.methods[PointsDefinition.modes[-1]](
                    *PointsDefinition.params[PointsDefinition.modes[-1]], order_diff, order["total_price"])
            else:
                for j in range(len(PointsDefinition.intervals)):
                    if order_diff < PointsDefinition.intervals[j]:
                        score += PointsDefinition.methods[PointsDefinition.modes[j]](
                            *PointsDefinition.params[PointsDefinition.modes[j]], order_diff, order["total_price"])
                        break
        return score


score = PointsDefinition.cal_score(orders)
print(score)
