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

    def __init__(self):
        self.intervals = [30, 60, 90, 120]
        self.modes = [2, 2, 2, 2]
        self.params = [
            [0.01, 1],
            [0.01, 1],
            [0.01, 1],
            [0.01, 1]
        ]
        self.methods = [
            lambda a, b, k, order_diff, total_price: k / math.log10(
                a + b * order_diff) * total_price,
            lambda a, order_diff, total_price: a * total_price,
            lambda a, b, order_diff, total_price: -a * order_diff * total_price + b * total_price
        ]

    def cal_score(self, user_orders): 
        current_date = datetime.today().strftime('%Y/%m/%d')
        score = 0
        for order in user_orders:
            order_date = datetime.strptime(order["date"], '%Y/%m/%d')
            order_diff = (datetime.strptime(current_date, '%Y/%m/%d') - order_date).total_seconds() / (60*60*24)
            for j in range(len(self.intervals)):
                if order_diff <= self.intervals[j]:
                    score += self.methods[self.modes[j]](
                        *self.params[j], order_diff, order["total_price"])
                    break
        return score


# score = PointsDefinition.cal_score(orders)
# print(score)
