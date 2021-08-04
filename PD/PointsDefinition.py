import numpy as np


class PointsDefinition:

    def __init__(self, db):
        self.score_period = 4
        self.score_coefficient = 0.1
        self.score_function = lambda x: self.score_coefficient * x
        self.max_order_score = 150
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
        scores = []
        for id in customer_ids:
            recent_purchases = self.db.get_recent_purchases(id, self.score_period)
            score = int(sum([np.min([self.score_function(purchase), self.max_order_score]) for purchase in recent_purchases]))
            scores.append(score)

        for i in range(len(customer_ids)):
            self.db.update_customer_score(customer_ids[i], int(scores[i]))
        return scores

    def get_rank_range(self, first, last):
        user_scores = sorted(self.db.get_all_scores().items(), key=lambda item: item[1])
        return [user_scores[i][0] for i in range(first-1, last)]

    def get_users_ranks(self, userIDs):
        user_scores = sorted(self.db.get_all_scores().items(), key=lambda item: item[1])
        ranks = {}
        for id in userIDs:
            for i in range(len(user_scores)):
                if user_scores[i][0] == id:
                    ranks[id] = i
                    break
        return ranks

    def get_rank_info(self, customer_ids):
        total_prices = [self.db.get_sum_of_purchases(id, self.score_period) for id in customer_ids]
        scores = []
        for price in total_prices:
            scores.append(self.score_function(float(price)))
        ranks = {}
        for i in range(len(customer_ids)):
            rank_name = self.get_rank(scores[i])
            rank = self.ranks[rank_name].copy()
            rank["name"] = rank_name
            ranks[customer_ids[i]] = rank
        # ranks = dict((customer_ids[i], self.ranks[self.get_rank(scores[i])]) for i in range(len(customer_ids)))
        return ranks
