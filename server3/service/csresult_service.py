from server3.business.csresult_business import CSResultBusiness


class CSResultService(object):

    @classmethod
    def add_result(cls, task_id, evaluation, user_id, sample, sample_label):
        return CSResultBusiness.add_result(user_id, task_id, evaluation, sample, sample_label)

    @classmethod
    def read_all(cls, task, evaluation):
        return CSResultBusiness.read_all_by_id(task, evaluation)

    @classmethod
    def read_by_user_and_task(cls, user_ID, task_id, evaluation=1):
        return CSResultBusiness.read_by_user_ID_and_task_ID(user_ID, task_id, evaluation)

    @classmethod
    def read_by_user_and_sample(cls, user_ID, sample, task_id, evaluation):
        result = CSResultBusiness.read_by_user_and_sample(user_ID, sample, task_id, evaluation)

        print('result', result)
        return result

    @classmethod
    def read_by_id(cls, result_id):
        result = CSResultBusiness.read_by_id(result_id)
        return result