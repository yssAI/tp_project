import datetime
import time

from server3.repository.temperature_result_repo import TemperatureResultRepo
from server3.entity.temperature_result import TemperatureResult
from server3.business.general_business import GeneralBusiness
from pprint import pprint

from server3.utility import json_utility


class TemperatureResultBusiness(GeneralBusiness):
    repo = TemperatureResultRepo(TemperatureResult)
    entity = TemperatureResult

    @classmethod
    def create(cls, data_dic, **kwargs):
        return cls.repo.create_one(
            result_temperature=data_dic['result_temperature'],
            real_temperature=data_dic['real_temperature'],
            date_time=data_dic['date_time'],
            **kwargs)

    @classmethod
    def get_by_time(cls, start_time, end_time):
        response = cls.entity.objects(date_time__gte=start_time, date_time__lte=end_time).order_by('-date_time')
        response = json_utility.me_obj_list_to_dict_list(response)
        response = [{'result_temperature': i['result_temperature'], 'date_time': i['date_time'],
                     'real_temperature': i['real_temperature']} for i in response]
        return response


if __name__ == '__main__':
    time_delay = datetime.timedelta(minutes=20)
    start_time = datetime.datetime.strptime('2019-05-30 05:46:55', '%Y-%m-%d %H:%M:%S')
    end_time = start_time + time_delay
    res = TemperatureResultBusiness.get_by_time(start_time, end_time)
    pprint(res)
    # for i in range(1000):
    #     create_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    #     data = {'result_temperature': 25.5, 'real_temperature': 26, 'date_time': create_time}
    #     aa = TemperatureResultBusiness.create(data)
    #     print(aa.date_time)
    #     time.sleep(10)
