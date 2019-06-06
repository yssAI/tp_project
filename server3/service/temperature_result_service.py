from server3.business.grpc_request_business import GrpcRequestBusiness
from server3.business.temperature_predict_business import TemperaturePredictBusiness
from server3.business.temperature_result_business import TemperatureResultBusiness

import datetime
import time


class TemperatureResultService:

    @classmethod
    def inference_table(cls, data):
        new_data = TemperaturePredictBusiness.create(data)
        end_time = new_data.create_time
        start_time = end_time - datetime.timedelta(minutes=40)
        df = TemperaturePredictBusiness.get_by_time(start_time, end_time)
        if df is not None:
            end_time_check = df['create_time'][0]
        if end_time != end_time_check:
            time.sleep(0.2)
            df = TemperaturePredictBusiness.get_by_time(start_time, end_time)
        else:
            pass
        if df is not None:
            predict_temperature = GrpcRequestBusiness.request_client(df.values)
        else:
            predict_temperature = None
        real_temperature = new_data.in_temperature
        data_time = end_time
        dic = {'result_temperature': predict_temperature, 'real_temperature': real_temperature, 'date_time': data_time}
        res = TemperatureResultBusiness.create(dic)
        return res


if __name__ == '__main__':
    create_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    data = {'out_temperature': 25, 'out_humidity': 0.99, 'in_temperature': 30, 'in_humidity': 0.66,
            'power_consumption': 3574, 'access_control': 1, 'create_time': create_time}
    resp = TemperatureResultService.inference_table(data)
    print(resp)
