import numpy as np
import json
import pandas as pd
from server3.business.cstask_business import CSTaskBusiness
from server3.business.module_business import ModuleBusiness
from server3.business.project_business import ProjectBusiness
from server3.business.csresult_business import CSResultBusiness
from server3.service.message_service import MessageService
from server3.service.job_service import JobService
from server3.service.module_service import ModuleService
from collections import Counter
from server3.business.user_business import UserBusiness
import pickle
import shutil
# 测试Modules
# from server3.service.cstest.src.main import cstest
import random
import os
from server3.constants import CS_PATH
from server3.utility import json_utility

RESOURCEFILE = './tutorial/8_Crowdsourcing_tutorial.ipynb'


class ConfigFileNotExistsException(Exception):
    def __init__(self):
        super(ConfigFileNotExistsException, self).__init__()


class CSTaskService:
    _rules = [1]

    _choose_people = np.arange(3, 10).tolist()

    # add
    @classmethod
    def add_task(cls, dataset_id, module_id, user_ID, module_version,
                 dataset_version, task_type='classification',
                 data_type='image', evaluation=0, desc='', user_token=None, device='cpu'):
        # insert module
        module = ProjectBusiness.get_by_id(module_id)
        dataset = ProjectBusiness.get_by_id(dataset_id)
        # 数据插入
        config = cls._insert_module_and_parse_json(dataset, module,
                                                   dataset_version)
        task = CSTaskBusiness.add_task(dataset_id, user_ID, 0, 0,
                                       module_id, task_type, data_type,
                                       evaluation,
                                       desc, module_version, dataset_version,
                                       classes=config.get('classes'), device=device)

        # create pickle
        insert_version = '' if dataset_version == 'current' else dataset_version
        data_path = os.path.join(module.path, 'results')
        des_pickle_path = os.path.join(data_path, str(task.id))
        if not os.path.exists(des_pickle_path):
            os.makedirs(des_pickle_path)
        des_pickle_path = os.path.join(des_pickle_path, 'create.pkl')
        with open(des_pickle_path, 'wb') as file:
            user_module_read_dataset_path = os.path.join('./datasets', dataset.user.user_ID + '-' +
                                                         dataset.name + '-' + insert_version)
            pickle.dump({'filename': user_module_read_dataset_path}, file)
        print('dump to pickle:', user_module_read_dataset_path)
        print('pickle path:', des_pickle_path)
        # create done
        # 后期修改, 要删除, 只为了暂时测试, 不需要返回值的
        cls._create_job_for_get_probability(task, module, user_ID, user_token, des_pickle_path, device)
        # 制造
        # tasnform data format
        return task
        # except Exception as e:
        #     raise RuntimeError(e)
        #     return {'msg': 'create task error'}

    @classmethod
    def _create_job_for_get_probability(cls, task, module, user_ID,
                                        user_token, pkl_file, device):
        # create_job
        # print(module.to_mongo())
        # print(task.to_mongo())
        job = JobService.create_job(module.id, 'module', user_ID,
                                    'main.py', device, user_token,
                                    task=task,
                                    function='predict')
        # cls.job_call_the_filter(task.id)

    @classmethod
    def job_call_the_filter(cls, task_id, if_success=True):
        task = CSTaskBusiness.get_task_by_id(task_id)
        # print(task_id, if_success)
        # print(task.to_mongo())
        if if_success:
            # read pickle
            module = ProjectBusiness.get_by_id(task.module.id)
            file_path = os.path.join(module.path, 'results', str(task.id), 'sample.pkl')
            try:
                with open(file_path, 'rb') as file:
                    non_exactly = pickle.load(file)
                    # file.close()
                    # print('non_exactly:', non_exactly)
                    if len(non_exactly.values()) > 2:
                        # raise RuntimeError('The pickle file is not valid.')
                        task.status = 2
                        task.user_operation = True
                        task.save()
                        _ = MessageService.create_message(
                            UserBusiness.get_by_user_ID('admin'),
                            'cs_task_pickle_file_invalid',
                            [task.sponsor],
                            user=task.sponsor,
                            task=task,
                            project=task.module)
                        return

                    if len(non_exactly['results']) > 0:
                        #
                        task.status = 2
                        task.user_operation = True
                        task.save()
                        _ = MessageService.create_message(
                            UserBusiness.get_by_user_ID('admin'),
                            'cs_task_done',
                            [task.sponsor],
                            user=task.sponsor,
                            task=task,
                            project=task.module)
                        return
                    # print(file_path, non_exactly)
                    # print(non_exactly)
                    unmarked_set = cls._filter_probabilities(
                        [non_exactly['results'], non_exactly['max_choose']])
                    # print(unmarked_set)
                    if len(unmarked_set) > 0:
                        task.status = 0
                        task.evaluation += 1
                        task.total_count += len(unmarked_set)
                        cls._dispatch(unmarked_set, task_id, task.evaluation)
                        task.save()
                        # send notification to user
                        message = MessageService.create_message(
                            UserBusiness.get_by_user_ID('admin'),
                            'cs_task_start',
                            [task.sponsor],
                            user=task.sponsor,
                            task=task,
                            project=task.module)
                        # print('success:', message.to_mongo())
                        return task
                    else:
                        task.status = 2
                        task.user_operation = True
                        # return {'msg': 'This task has occurred error when executed, '
                        #                'you can check it in your module job page.'}
                        # send notification to user
                        task.save()
                        message = MessageService.create_message(
                            UserBusiness.get_by_user_ID('admin'),
                            'cs_task_done',
                            [task.sponsor],
                            user=task.sponsor,
                            task=task,
                            project=task.module)
                        print('no unlabeled:', message.to_mongo())
            except FileNotFoundError as e:
                # return {'msg': 'your module don`t create the pickle file.'}
                # send notification to user
                task.status = 2
                task.user_operation = True
                task.save()
                task = cls._add_extra_info_with_task(task)
                message = MessageService.create_message(
                    UserBusiness.get_by_user_ID('admin'),
                    'cs_task_pickle_file_not_found',
                    [task.sponsor],
                    task=task,
                    project=task.module,
                )
                # , 'project': task.module
                print("file not found:", message.to_mongo())
            except Exception as e:
                # return {'msg': 'error occur.'}
                print(e)
                task.status = 2
                task.user_operation = True
                task.save()
                task = cls._add_extra_info_with_task(task)
                message = MessageService.create_message(
                    UserBusiness.get_by_user_ID('admin'),
                    'cs_task_job_error',
                    [task.sponsor],
                    task=task,
                    user=task.sponsor,
                    project=task.module)
                # , 'project': task.module
                print('exception:', e, 'message:', message.to_mongo())
                raise RuntimeError(e)
        else:
            task.status = 2
            task.user_operation = True
            # task.evaluation -= 1
            if task.evaluation > 1:
                message = MessageService.create_message(
                    UserBusiness.get_by_user_ID('admin'),
                    'cs_task_job_error',
                    [task.sponsor],
                    user=task.sponsor,
                    task=task,
                    project=task.module, )
                # , 'project': task.module
                print('train, has exception:', message.to_mongo())
            task.save()
            # return {'msg': 'This task has occurred error when executed, you can check it in your module job page.'}

    # insert the module and parse the json
    @classmethod
    def _insert_module_and_parse_json(cls, dataset, module, version):
        # append path
        old_json_path = os.path.join(module.path, 'src', 'config.json')
        json_path = os.path.join(module.path, 'config.json')
        if not os.path.exists(json_path):
            json_path = old_json_path
        # If sthe version is current,
        if version == 'current':
            version = None
        ModuleBusiness.insert_dataset(module, dataset, version)
        # print(module.to_mongo())
        # read
        if os.path.exists(json_path):
            config = open(json_path)
            config = json.load(config)
            return config
        else:
            # need
            # message = MessageService.create_message(
            #     UserBusiness.get_by_user_ID('admin'),
            #     'cs_task_invited',
            #     invited_users,
            #     project=task.dataset,
            #     task=task,
            # )
            raise ConfigFileNotExistsException('This module don`t contain the config.json file')

    @classmethod
    def _add_extra_info_with_task(cls, task):
        results = CSResultBusiness.read_all_by_id(task, task.evaluation)
        users = results.distinct('user')
        task.invited_users = []
        for user in users:
            task.invited_users.append({"username": user.username, "user_ID": user.user_ID,
                                       "avatar_url": user.avatar_url})

        task.user_ID = task.sponsor.user_ID
        task.username = task.sponsor.username
        task.avatar_url = task.sponsor.avatar_url
        # How many People
        task.accept_user_count = len(task.user_ID)
        # How many sample is marked
        task.sample_marked_for_user, task.need_marked_times, task.marked_times = \
            cls._compute_sample_marked_count(results)
        total_count = 0.01 if task.total_count == 0 else task.total_count
        task.percentage = int(task.sample_marked_for_user / total_count * 100)
        # tasnform data format
        task.dataset_version = task.dataset_version.replace('_', '.')
        task.module_version = task.module_version.replace('_', '.')
        # How many People
        task.accept_user_count = len(task.user_ID)
        # 数据集名字
        task.dataset_name = task.dataset.display_name
        return task

    @classmethod
    def read_single_task(cls, task_id):
        task = CSTaskBusiness.read_task_by_id(task_id)
        task = cls._add_extra_info_with_task(task)

        return task

    # raed all task for user
    @classmethod
    def read_all_task(cls, dataset_id, dataset_version=None,
                      task_status='all'):
        # 做过滤操作
        if dataset_version == '':
            dataset_version = None
        print(dataset_id, dataset_version, task_status)
        if task_status == 'all':
            # , results user_ID,
            tasks = CSTaskBusiness.read_tasks_with_dataset(dataset_id,
                                                           dataset_version)
        elif task_status == 'doing':
            tasks = CSTaskBusiness.read_tasks_with_dataset_and_key(dataset_id,
                                                                   0,
                                                                   dataset_version)
        elif task_status == 'training':
            tasks = CSTaskBusiness.read_tasks_with_dataset_and_key(dataset_id,
                                                                   1,
                                                                   dataset_version)
        else:
            # done
            tasks = CSTaskBusiness.read_tasks_with_dataset_and_key(dataset_id,
                                                                   2,
                                                                   dataset_version)

        results = []

        '''
        
                if task_status != 'training' and task_status != 'all':
                    if task.total_count <= 0:
                        continue
        '''
        if tasks and len(tasks) > 0:
            for task in tasks:
                if task.total_count <= 0:
                    continue
                results.append(cls._add_extra_info_with_task(task))
        # print(results)
        return results

    # read tasks with module for module job page.
    @classmethod
    def read_tasks_with_self_and_modules(cls, user_ID, module_id,
                                         module_version, task_status):
        # 做过滤操作
        if task_status == 'all':
            # , results user_ID,
            tasks = CSTaskBusiness.read_tasks_with_self_and_modules(user_ID,
                                                                    module_id,
                                                                    module_version, None)
        elif task_status == 'doing':
            tasks = CSTaskBusiness.read_tasks_with_self_and_modules(user_ID,
                                                                    module_id,
                                                                    module_version, 0)
        elif task_status == 'training':
            tasks = CSTaskBusiness.read_tasks_with_self_and_modules(user_ID,
                                                                    module_id,
                                                                    module_version, 1)
        else:
            # done
            tasks = CSTaskBusiness.read_tasks_with_self_and_modules(user_ID,
                                                                    module_id,
                                                                    module_version, 2)

        results = []

        if tasks and len(tasks) > 0:
            for task in tasks:
                if task.total_count <= 0:
                    continue
                results.append(cls._add_extra_info_with_task(task))
        return results

    # read all modules
    @classmethod
    def read_all_modules(cls, user_ID):
        modules = ModuleBusiness.get_objects(user=UserBusiness.get_by_user_ID(user_ID), page_size=100)
        return modules

    @classmethod
    def _compute_sample_marked_count(cls, results):
        task_results, _ = cls._analyse_labels(results)
        task_results = [result for result in task_results]

        count = []
        need_marked_times = 0
        marked_times = 0
        for result in task_results:
            # sample count
            if len(np.unique(result.get('labels'))) > 1:
                count.append(result)
            # total times
            need_marked_times += len(result.get('users'))
            # times
            marked_times += np.sum(np.array(result.get('labels')) != '')
        # print([result for result in task_results])
        # print(marked_times)
        return len(count), need_marked_times, marked_times

    @classmethod
    def _load_to_job_for_train(cls, module, task, user_ID, user_token):
        job = JobService.create_job(module.id, 'module', user_ID,
                                    'main.py',
                                    'cpu' if not task.device else task.device, user_token, task=task,
                                    function='train')

    # Train
    @classmethod
    def train(cls, task_id, user_token):
        # load the module
        task = CSTaskBusiness.get_task_by_id(task_id)
        module = ModuleBusiness.get_by_id(task.module.id)
        # load the dataset
        # former_eval_marked = CSResultService.read_all(task_id, task.evaluation)
        # generate the dataset
        old_path = cls._generate_csv_file_for_results(task, task.dataset,
                                                      task.sponsor.user_ID)
        # copy to dataset
        new_path = os.path.join(module.path, CS_PATH)
        print(new_path)
        # if not os.path.exists(new_path):
        # if not os.Path(new_path).exists():
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        # file path
        filename = old_path.split('/')[-1]
        new_path = os.path.join(new_path, filename)
        # create the crowsourcing.pkl
        # pic_file = os.path.join(module.path, 'results', str(task.id) + '.pkl')
        # with open(pic_file, 'wb') as file:
        #     pickle.dump({'filename': os.path.join('./results', 'crowdsourcing', filename)}, file)
        # copy file to indicate path
        shutil.copyfile(old_path, new_path)
        # error
        if task.evaluation < 3:
            task.status = 1
            # update task
            # task.evaluation += 1
            task.save()
            # 调用任务接口
            cls._load_to_job_for_train(task.module, task, task.sponsor.user_ID,
                                       user_token)
            # back the info
            # task.evaluation -= 1
            task = cls._add_extra_info_with_task(task)
            # task.evaluation += 1
            # How many sample is marked
            return task, new_path
        else:
            return {'msg': 'The current task is achieve the max iterator times.'}, new_path

    # read the all marked label
    @classmethod
    def _analyse_labels(cls, results):
        # task_results = CSResultService.read_all(task_id, evaluation)
        # return the data: {path, [users], [labels]}
        # print(json_utility.me_obj_list_to_json_list(results))
        task_results = results.aggregate(
            {
                '$group': {
                    '_id': '$sample',
                    'users': {"$push": "$user"},
                    'labels': {"$push": "$label"},
                }
            }
        )
        # print(task_results.next())
        transform_reuslt = []
        return_tasks = []
        for result in task_results:
            # print(result)
            transform_reuslt.append({'sample': result.get('_id'),
                                     'label': dict(
                                         Counter(result.get('labels')))})
            return_tasks.append(result)
        return return_tasks, transform_reuslt

    # least at all query
    # result write to picker

    @classmethod
    def _filter_probabilities(cls, non_exactly, lower_limit=0.4,
                              upper_limit=0.7):
        predicts, choose_num = non_exactly
        # print(predicts, choose_num)
        # print(predicts)
        # Get the key
        paths = []
        probabilities = []
        # print(predicts)
        for i in range(len(predicts)):
            paths.append(predicts[i]['sample'])
            probabilities.append(predicts[i]['probability'])

        paths = np.array(paths)
        probabilities = np.array(probabilities)
        # print(paths)
        # print(probabilities)
        # softmax/sigmoid
        if len(probabilities.shape) > 1 and probabilities.shape[1] > 1:
            # softmax
            class_idx = np.argmax(probabilities, axis=1)
            judge_probabilities = np.array(
                [probabilities[i, class_idx] for i in range(len(class_idx))])
            # 0.5 - 0.75
            least_confidence = judge_probabilities < upper_limit
        else:
            # 0.4-0.6
            # take the index
            less_probs = probabilities > lower_limit
            lagre_probs = probabilities < upper_limit
            # combine
            least_confidence = [less_probs[i] and lagre_probs[i] for i in
                                range(len(probabilities))]
        # back the non_exactly samples
        least_confidence = np.array(least_confidence).flatten()
        # 如果模型不好, 随便传入10个
        # print('least_confidence:', least_confidence)
        # if np.sum(least_confidence) == 0:
        #     least_confidence = np.arange(int(len(paths) * 0.1))
        # print(least_confidence)
        return paths[least_confidence[:choose_num]]

    # dispatch
    @classmethod
    def _dispatch(cls, non_exactly, task_id, evaluation):
        # non_exactly = cls._get_crowd_sourcing_samples(test)
        # choose the user
        task = CSTaskBusiness.get_task_by_id(task_id)
        count = len(non_exactly)
        # real of users
        real_of_users = UserBusiness.get_all()
        # promise do not send self
        # print(task.sponsor.user_ID)
        real_of_users = [user for user in real_of_users
                         if user.user_ID != task.sponsor.user_ID]
        # real_of_users = [user for user in real_of_users
        #                  if user.user_ID != 'lu_xu_1']
        # print("real_of_users:", [user.user_ID for user in real_of_users])
        # print(type(real_of_users))
        real_of_user_nums = np.arange(len(real_of_users)).tolist()
        # dispatch
        result = {}
        # ever image has dispatch at least to three people
        for sample_idx in range(count):
            result[sample_idx] = {'user': [real_of_users[i]
                                           for i in
                                           random.sample(real_of_user_nums,
                                                         random.sample(
                                                             cls._choose_people,
                                                             1)[-1])],
                                  'sample': non_exactly[sample_idx]}
            # print([user.user_ID for user in result[sample_idx]['user']])
        # 往数据库插入信息
        invited_users = []
        for key in result.keys():
            sample = result[key]['sample']
            # 测试账号
            # CSResultService.add_result(task_id, evaluation, 'lu_xu_1', sample,
            #                            '')
            for user in result[key]['user']:
                # add the invited
                if user.id not in invited_users:
                    invited_users.append(user.id)
                CSResultBusiness.add_result(task_id, evaluation, user.user_ID,
                                            sample, '')
                # print(user.user_ID)
        # invited users
        message = MessageService.create_message(
            UserBusiness.get_by_user_ID('admin'),
            'cs_task_invited',
            invited_users,
            project=task.dataset,
            task=task,
        )
        print('invited:', message.to_mongo())
        # print('invited:', invited_users)
        # print('done create ')

    # read the image
    @classmethod
    def read_need_to_task(cls, user_ID, task_id, evaluation=1):
        results = CSResultBusiness.read_by_user_ID_and_task_ID(user_ID, task_id,
                                                               evaluation)
        task = CSTaskBusiness.get_task_by_id(task_id)
        results = [results[i] for i in range(len(results)) if
                   results[i].label == '']
        part_data = []
        for result in results:
            paths = result.sample.split('/')
            index = 0
            for i in range(len(paths)):
                if paths[i] == 'datasets':
                    index = i
                    break
            result.url = os.path.join(task.module.path,
                                      *paths[index:len(paths) - 1])
            result.filename = paths[-1]
            part_data.append({'_id': str(result.id), 'url': result.url,
                              'filename': result.filename})
            # print('results: ', result.to_mongo())
        return part_data, task.classes

    # unmarked count
    @classmethod
    def get_label_count(cls, task):
        return task.marked_label

    # labeling count
    @classmethod
    def get_total_count(cls, task):
        return task.total_count

    # percentage
    @classmethod
    def get_percentage(cls, task):
        return cls.get_label_count(task) / cls.get_total_count(task)

    # addLabels
    @classmethod
    def marked_sample(cls, result_id, label):
        # trigger two event
        result = CSResultBusiness.read_by_id(result_id)
        result.label = label
        # print('after_result: ', result.to_mongo())
        result.save()
        # 打一个标都记录上去, 同一个标不重复记录
        task = cls._add_marked_count(result.task.id)
        # task.save()
        # 如果打完标签
        results = CSResultBusiness.read_all_by_id(task, task.evaluation)
        sample_marked_for_user, need_marked_times, marked_times = \
            cls._compute_sample_marked_count(results)
        if sample_marked_for_user >= task.total_count:
            # send notification
            admin_user = UserBusiness.get_by_user_ID('admin')
            # reciever = UserBusiness.get_by_id(task.sponsor.id)
            # send notification
            MessageService.create_message(admin_user,
                                          'cs_task_done',
                                          [task.sponsor],
                                          user=task.sponsor,
                                          task=result.task,
                                          project=result.task.module,
                                          )
        # all people is labeled, finish this task
        if task.marked_count == task.total_count:
            task.status = 2
            task.save()
            return cls._add_extra_info_with_task(task)
        return None

    @classmethod
    def cancel(cls, task_id):
        task = CSTaskBusiness.get_task_by_id(task_id)
        # 取消Job
        jobs = JobService.business.get_by_task_id(task)
        for job in jobs:
            JobService.business.terminate(job.id)
        # 修改完成, 让看到最后的信息
        task.status = 2
        task.user_operation = False
        task.save()
        task = cls._add_extra_info_with_task(task)
        return task

    @classmethod
    def _add_marked_count(cls, task_id):
        task = CSTaskBusiness.get_task_by_id(task_id)
        results = CSResultBusiness.read_all_by_id(task, task.evaluation)
        task_results, _ = cls._analyse_labels(results)
        # marked count
        count = len([result for result in task_results
                     if len(np.unique(result.get('labels'))) == 1 and
                     np.unique(result.get('labels'))[-1] != ''])
        # print(count)
        if task.marked_count != count:
            task.marked_count = count
            task.save()

        return task

    @classmethod
    def _read_tasks_for_status(cls, dataset_id):
        # read the all dataset
        tasks = CSTaskBusiness.read_tasks_with_dataset(dataset_id, None)
        results = []
        done_count = 0
        doing_count = 0
        total_count = 0
        users = []
        for task in tasks:
            if task.total_count <= 0:
                continue
            result = CSResultBusiness.read_all_by_id(task, task.evaluation)
            task_results, _ = cls._analyse_labels(result)
            unique_users = result.distinct('user')
            unique_users = [user.user_ID for user in unique_users]
            users.extend(unique_users)
            results.extend([result.get('_id') for result in task_results
                            if len(np.unique(result.get('labels'))) > 1])
            total_count += task.total_count
            if task.status == 2:
                done_count += 1
            elif task.status == 0:
                doing_count += 1
        users = list(set(users))
        return doing_count, done_count, total_count, np.unique(
            results).tolist(), len(users)

    @classmethod
    def read_status(cls, dataset_id):
        status_info = {}
        doing_count, done_count, total_count, results, users_count = cls._read_tasks_for_status(
            dataset_id)
        status_info['doing_count'] = doing_count
        status_info['done_count'] = done_count
        status_info['mark'] = len(results)
        status_info['total_count'] = total_count
        total_count = 0.01 if total_count == 0 else total_count
        status_info['percentage'] = int(
            len(results) / (total_count + 0.01) * 100)
        status_info['user_count'] = users_count
        return status_info

    # generate file
    @classmethod
    def _generate_csv_file_for_results(cls, task, dataset, user_ID):
        # init the path
        moudle = ProjectBusiness.get_by_id(task.module.id)
        dataset_path = dataset.dataset_path
        save_path = os.path.join('crowdsourcing', user_ID, moudle.name, task.dataset_version)
        csv_file_name = str(task.id) + '_' + str(task.evaluation) + '.csv'
        # read the result
        results = CSResultBusiness.read_all_by_id(task, task.evaluation)
        # create the path
        store_path = os.path.join(dataset_path, save_path)
        if not os.path.exists(store_path):
            os.makedirs(store_path)
        # get the statistics result
        full_path = os.path.join(store_path, csv_file_name)
        _, transform_tasks = cls._analyse_labels(results)
        # get the labels
        save_key = []
        for sample in transform_tasks:
            # print(sample)
            max_count = 0
            label = ''
            for key in sample['label'].keys():
                if key != '':
                    if label == '':
                        max_count = sample['label'][key]
                        label = key
                    elif max_count < sample['label'][key]:
                        max_count = sample['label'][key]
                        label = key

            label = 'None' if label == '' else label
            save_key.append({'sample': sample['sample'], 'label': label})
        # save
        if len(save_key) <= 0:
            save_key.append({'sample': 'no samples', 'label': 'no labels'})

        # print(save_key)
        pd.DataFrame(save_key, index=np.arange(len(save_key))).to_csv(
            full_path, index=None)
        # move to module
        # path
        return full_path

    # generate
    @classmethod
    def need_csv_file(cls, task_id, user_ID):
        # what is time for generating this file.
        task = CSTaskBusiness.get_task_by_id(task_id)
        dataset = ProjectBusiness.get_by_id(task.dataset.id)
        # generate file, will overwrite when the next time.
        csv_file = cls._generate_csv_file_for_results(task, dataset, task.sponsor.user_ID)
        # if the sponsor click it
        if task.sponsor.user_ID == user_ID:
            # copy it
            dest_path = os.path.join(task.module.path, CS_PATH, str(task.id))
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            # dest_path = os.path.join(module_path, task.task_type + '_' + str(task.evaluation))
            dest_path = os.path.join(dest_path, csv_file.split('/')[-1])
            shutil.copyfile(csv_file, dest_path)
            return csv_file, task, dest_path
        # print(csv_file)
        return csv_file, task

    # done
    # finish the task
    @classmethod
    def fulfil_task(cls, task_id, user_ID):
        task = CSTaskBusiness.get_task_by_id(task_id)
        dataset = ProjectBusiness.get_by_id(task.dataset.id)
        # complete
        task.status = 2
        task.save()
        # file_path
        csv_file = cls._generate_csv_file_for_results(task, dataset, user_ID)
        # print(csv_file)
        dest_path = os.path.join(task.module.path, CS_PATH, str(task.id))
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        # dest_path = os.path.join(module_path, task.task_type + '_' + str(task.evaluation))
        dest_path = os.path.join(dest_path, csv_file.split('/')[-1])
        shutil.copyfile(csv_file, dest_path)
        # print('error:', task.to_mongo())
        results = CSResultBusiness.read_all_by_id(task.id, task.evaluation)
        sample_marked_for_user, need_marked_times, marked_times = \
            cls._compute_sample_marked_count(results)
        # 结束
        if task.evaluation >= 3 or sample_marked_for_user < task.total_count:
            task.user_operation = True
        task.save()
        # add the info
        task = cls._add_extra_info_with_task(task)
        print('back')
        return csv_file, task, dest_path

    @classmethod
    def _read_directory(cls, path):
        results = []
        for root, dirs, files in os.walk(path):
            if len(files) > 0:
                for file in files:
                    # statical info of csv file.
                    file_path = os.path.join(root, file)
                    task_id = file.split('_')[0]
                    # read it
                    task = CSTaskBusiness.read_task_by_id(task_id)
                    results.append({'file_path': file_path,
                                    'file_name': file,
                                    'info': sum(1 for _ in open(file_path, encoding='utf-8', )),
                                    'class_type': task.task_type,
                                    'classes': task.classes})
        return results

    @classmethod
    def get_crowdsoucring_list(cls, dataset_id):
        dataset = ProjectBusiness.get_by_id(dataset_id)
        # get the path
        dataset_path = dataset.dataset_path
        # concanated
        crowdsoucing_path = os.path.join(dataset_path, 'crowdsourcing')
        # print(crowdsoucing_path)
        if os.path.exists(crowdsoucing_path):
            # read the all files
            return cls._read_directory(crowdsoucing_path)
        else:
            return False

    @classmethod
    def get_task_detail(cls, task_id):
        task = CSTaskBusiness.read_task_by_id(task_id)
        # former info
        former = {}
        for i in range(1, task.evaluation + 1):
            # read the result for evaluation
            results = CSResultBusiness.read_all_by_id(task, i + 1)
            task.evaluation = i
            file_path = cls._generate_csv_file_for_results(task, task.dataset, task.sponsor.user_ID)
            # sub_directory = file_path.split('/')
            # file_path = os.path.join(sub_directory[1], *sub_directory[1:])
            # file_path =
            file_name = str(task.id) + '_' + str(task.evaluation) + '.csv'
            # file_path = os.path.join('crowdsourcing', task.sponsor.user_ID,
            #                                      task.module.name, task.dataset_version, file_name)
            sample_marked_for_user, need_marked_times, marked_times = cls._compute_sample_marked_count(results)
            if i not in former:
                former[i] = {'file_name': file_name,
                             'file_path': file_path,
                             'samples': sample_marked_for_user,
                             'need_marked_times': need_marked_times,
                             'marked_times': marked_times}
        if len(former):
            return former
        else:
            return False

    @classmethod
    def get_evalution_csv(cls, task_id, evaluation):
        task = CSTaskBusiness.read_task_by_id(task_id)
        task.evaluation = int(evaluation)
        file_path = CSTaskService._generate_csv_file_for_results(task, task.dataset, task.sponsor.user_ID)

        return file_path

    @classmethod
    def copy_cs_template_file(cls, module_id):
        module = ModuleBusiness.get_by_id(module_id)
        module_path = module.path.split('/')[1:]
        old_des_path = os.path.join(module_path[0], *module_path[1:], 'src')
        des_path = os.path.join(module_path[0], *module_path[1:])
        if not os.path.exists(des_path):
            des_path = old_des_path
        print(des_path)
        shutil.copy(RESOURCEFILE, des_path)

    @classmethod
    def create_cs_project(cls, **args):
        user_ID = args.pop('user_ID')
        display_name = args.pop('display_name')
        type = args.pop('type')
        description = args.pop('description')
        tags = args.pop('tags')
        dataset_Id = args.pop('datasetId')
        dataset_version = args.pop('datasetVersion')
        tags = args['tags']
        user_token = args.pop('Authorization').split()[1]

        module = ModuleService.create_project(display_name, description, user_ID,
                                              tags=tags, type=type, user_token=user_token, **args)
        # 拷贝模板文件
        cls.copy_cs_template_file(module.id)

        return module


if __name__ == '__main__':
    print(os.path.exists(RESOURCEFILE))
    shutil.copy(RESOURCEFILE, '../')
