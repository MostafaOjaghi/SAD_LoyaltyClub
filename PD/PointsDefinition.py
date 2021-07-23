import math
from datetime import datetime


class PointsDefinition:

    def __init__(self, db):
        self.score_period = 4
        self.score_coefficient = 0.1
        self.score_function = lambda x: self.score_coefficient * x
        self.db = db
        self.ranks = {
            "newbie": {
                "rank range": [0, 100],
                "off": 0,
                "monthly limit": 0,
                "free shipping": True
            },
            "bronze": {
                "rank range": [100, 200],
                "off": 0.1,
                "monthly limit": 0,
                "free shipping": True
            },
            "silver": {
                "rank range": [200, 300],
                "off": 0.2,
                "monthly limit": 0,
                "free shipping": True
            },
        }

    def get_rank(self, score):
        for key in self.ranks:
            if score >= self.ranks[key]["rank range"][0] and score < self.ranks[key]["rank range"][1]:
                return key
        return None

    def cal_users_scores(self, customer_ids):
        total_prices = [self.db.get_sum_of_purchases(id, self.score_period) for id in customer_ids]
        scores = []
        for price in total_prices:
            scores.append(self.score_function(price))

        # update users scores in DB
        for i in range(len(customer_ids)):
            self.db.update_customer_score(customer_ids[i], scores[i])
        return scores

    def rank_users(self, first, last):
        user_scores = sorted(self.db.get_all_scores().items(), key=lambda item: item[1])
        return [user_scores[i][0] for i in range(first-1, last)]

    def get_rank_info(self, customer_ids):
        total_prices = [self.db.get_sum_of_purchases(id, self.score_period) for id in customer_ids]
        scores = []
        for price in total_prices:
            scores.append(self.score_function(price))
        ranks = dict((customer_ids[i], self.ranks[self.get_rank(scores[i])]) for i in range(len(customer_ids)))
        return ranks


# PD = PointsDefinition("DB")
# score = PD.cal_score("customer IDS")
