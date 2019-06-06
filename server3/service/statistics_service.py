from server3.business.statistics_business import StatisticsBusiness


class StatisticsService:
    @classmethod
    def use_app(cls, user_obj, app_obj, input_json, output_json):
        statistics = StatisticsBusiness.use_app(user_obj, app_obj, input_json, output_json)

        return statistics