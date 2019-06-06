from server3.repository.temperature_predict_repo import TemperaturePredictRepo
from server3.entity.temperature_predict import TemperaturePredict
from server3.business.general_business import GeneralBusiness
from server3.utility import json_utility
import pandas as pd
import datetime
# from datetime import datetime
import time


class TemperaturePredictBusiness(GeneralBusiness):
    repo = TemperaturePredictRepo(TemperaturePredict)
    entity = TemperaturePredict

    @classmethod
    def create(cls, data, **kwargs):
        return cls.repo.create_one(
            out_temperature=data['out_temperature'],
            out_humidity=data['out_humidity'],
            in_temperature=data['in_temperature'],
            in_humidity=data['in_humidity'],
            power_consumption=data['power_consumption'],
            access_control=data['access_control'],
            fan_status=data['fan_status'],
            create_time=data['create_time'],
            **kwargs
        )

    @classmethod
    def get_by_time(cls, start_time, end_time):
        response = cls.entity.objects(create_time__gt=start_time, create_time__lte=end_time).order_by('-create_time')
        if response.count() < 240:
            return None
        response = json_utility.me_obj_list_to_dict_list(response)
        data_frame = pd.DataFrame(response)[['create_time', 'in_temperature', 'in_humidity', 'power_consumption',
                                             'access_control', 'out_humidity', 'out_temperature']]
        return data_frame


if __name__ == '__main__':
    # create_time = datetime.datetime.utcnow()
    time_delay = datetime.timedelta(minutes=20)
    # start_time = create_time - time_delay
    start_time = datetime.datetime.strptime('2019-05-30 05:46:55', '%Y-%m-%d %H:%M:%S')
    end_time = start_time + time_delay
    start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
    df = TemperaturePredictBusiness.get_by_time(start_time, end_time)
    print(df['create_time'][0])
    # print(df.values)
    # data_frame.to_csv('all_data.csv')
    # print(data_frame)
    # for i in res:
    #     print(i.to_mongo())
    # print(res)
    # print(len(res))
    # print(res.to_mongo())
    # data = {'out_temperature': 25, 'out_humidity': 0.99, 'in_temperature': 30, 'in_humidity': 0.66,
    #         'power_consumption': 3574, 'access_control': 1, 'create_time': create_time}

    #
    # for i in range(2000):
    #     create_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    #     data = {'out_temperature': 25, 'out_humidity': 0.99, 'in_temperature': 30, 'in_humidity': 0.66,
    #            'power_consumption': 3574, 'access_control': 1, 'create_time': create_time}
    #     aa = TemperaturePredictBusiness.create(data)
    #     print(aa.create_time)
    #     time.sleep(10)
