from server3.business.course_business import CourseBusiness
from server3.business.course_unit_business import CourseUnit
from server3.business.course_unit_trigger_business import \
    CourseUnitTriggerBusiness
from server3.business.course_activity_business import CourseActivityBusiness
from server3.business.course_section_business import CourseSectionBusiness
from server3.business.course_unit_business import CourseUnitBusiness
from server3.business.user_business import UserBusiness
from server3.utility import json_utility


class CourseService:
    @classmethod
    def get_all_course(cls, page_no, page_size):
        courses = CourseBusiness.read()
        total = len(courses)
        video_course = courses(course_type='video')
        practice_course = courses(course_type='practice')
        doc_course = courses(course_type='doc')
        video_course = video_course[
                       (page_no - 1) * page_size: page_no * page_size]
        practice_course = practice_course[
                          (page_no - 1) * page_size: page_no * page_size]
        doc_course = doc_course[(page_no - 1) * page_size: page_no * page_size]
        return {'video': json_utility.me_obj_list_to_json_list(video_course),
                'practice': json_utility.me_obj_list_to_json_list(
                    practice_course),
                'doc': json_utility.me_obj_list_to_json_list(
                    doc_course)}, total

    @classmethod
    def get_sections(cls, course, user_ID, page_no=1, page_size=9):
        user = None
        if user_ID:
            user = UserBusiness.get_by_user_ID(user_ID)
        if isinstance(course, str):
            course = CourseBusiness.get_by_id(course)
        total = course.number_of_units
        result = []
        q_list = []
        for section in course.sections:
            item = {'name_cn': section.zh_name, 'name_en': section.name,
                    'id': str(section.id)}
            units = []
            for unit in section.units:
                if user:
                    q_list.append(
                        {'course_section': section, 'course_unit': unit,
                         'user': user})
                units.append({'name': unit.name, 'zh_name': unit.zh_name,
                              'url': unit.url, 'id': str(unit.id)})
            item['units'] = units
            result.append(item)

        if user and q_list:
            activities = CourseActivityBusiness.repo.or_filter(q_list)
            for s in result:
                for u in s['units']:
                    u['learn'] = False
                    for activity in activities:
                        if u['id'] == str(activity.course_unit.id):
                            u['learn'] = True
                            break

            course.progress = activities.count()
        return result[(page_no - 1) * page_size: page_no * page_size], \
               json_utility.convert_to_json(course.to_mongo()), total

    @classmethod
    def get_my_course(cls, user, page_no=1, page_size=10):
        if isinstance(user, str):
            user = UserBusiness.get_by_user_ID(user)
        enroll_activity = CourseActivityBusiness.read({'user': user,
                                                       'status': 'enroll'})
        enroll_activity = enroll_activity(course__exists=True)

        courses = [each_activity.course for each_activity in enroll_activity]
        # 分页
        total = len(courses)
        courses = courses[(page_no - 1) * page_size: page_no * page_size]
        for each_course in courses:
            # 将 Activity的数据读取出来
            num_of_activities = 0
            for section in each_course.sections:
                num_of_activities += CourseActivityBusiness.read(
                    {'user': user, 'course_section': section,
                     'status': 'enroll'}).count()
            # print(each_course)
            # todo 以后查看是否有更好的方式, 因为这样做的话, 两门课包含了同一门就没办法进度同步了
            total_unit = each_course.number_of_units
            each_course.progress = num_of_activities * 1.0 / total_unit
            each_course.total_unit = total_unit
            each_course.learn_unit = num_of_activities
        courses = json_utility.me_obj_list_to_json_list(courses)
        return courses, total

    @classmethod
    def get_my_course_with_detail(cls, user, page_no=1, page_size=10):
        if isinstance(user, str):
            user = UserBusiness.get_by_user_ID(user)
        enroll_activity = CourseActivityBusiness.read({'user': user})
        enroll_activity = enroll_activity(course__exists=True)

        courses = [each_activity.course for each_activity in enroll_activity]
        # 分页
        total = len(courses)
        courses = courses[(page_no - 1) * page_size: page_no * page_size]
        for each_course in courses:
            # 将 Activity的数据读取出来
            num_of_activities = 0
            objects_of_activities = []
            for section in each_course.sections:
                activities = CourseActivityBusiness.read(
                    {'user': user, 'course_section': section})
                for a in activities:
                    # objects_of_activities.append(a.course_unit.to_mongo())
                    objects_of_activities.append(a.course_unit.zh_name)
                    num_of_activities += 1
            # print(each_course)
            # todo 以后查看是否有更好的方式, 因为这样做的话, 两门课包含了同一门就没办法进度同步了
            total_unit = each_course.number_of_units
            each_course.progress = num_of_activities * 1.0 / total_unit
            each_course.total_unit = total_unit
            each_course.learn_unit = num_of_activities
            each_course.learn_activities = objects_of_activities
        courses = json_utility.me_obj_list_to_json_list(courses)
        return courses, total

    # @classmethod
    # def get_all_units(cls, section_id):
    #     section = CourseSectionBusiness.get_by_id(section_id)
    #     units = section.units
    #     for unit in units:
    #         unit.trigger =
    #     return units

    @classmethod
    def get_trigger(cls, unit):
        triggers = CourseUnitTriggerBusiness.read({'unit': unit})
        return json_utility.me_obj_list_to_json_list(triggers), len(triggers)

    @classmethod
    def add_trigger(cls, unit, **kwargs):
        if isinstance(unit, str):
            unit = CourseUnitTriggerBusiness.get_by_id(unit)
        trigger = CourseUnitTriggerBusiness.create_trigger(unit=unit, **kwargs)
        return trigger

    @classmethod
    def delete_sections(cls, course_name, section_names):
        import copy
        course = CourseBusiness.get_course_by_name(course_name)
        # 删除项目
        sections = copy.deepcopy(course.sections)
        for name in section_names:
            for section in sections:
                if section.zh_name == name:
                    sections.remove(section)
                    break
        # print([section.zh_name for section in sections])
        course.sections = sections
        # print([section for section in course.sections])
        # print([section.zh_name for section in course.sections])
        course.save()


# 添加实战项目
if __name__ == '__main__':
    # local: Machine Learning Operation
    # rc: Machine Learning Practice
    # prod: Machine Learning Practice
    # sections = {"Machine Learning Practice": [
    #     {
    #         'zh_name': '卷积神经网络-猫狗识别',
    #         'name': 'CNN - Dogs And Cats Classification',
    #         'units': [
    #             {
    #                 'zh_name': '卷积神经网络-猫狗识别',
    #                 'name': 'CNN - Dogs And Cats Classification'
    #             }
    #         ]
    #     },
    #     {
    #         'zh_name': '卷积神经网络-人脸关键点识别',
    #         'name': 'CNN - Face KeyPoint Detect',
    #         'units': [
    #             {
    #                 'zh_name': '卷积神经网络-人脸关键点识别',
    #                 'name': 'CNN - Face KeyPoint Detect'
    #             }
    #         ]
    #     }
    # ]}
    # CourseService.add_sections(sections)
    CourseService.delete_sections("Machine Learning Practice",
                                  ['CNN - Face KeyPoint Detect',
                                   'CNN - Dogs And Cats Classification'])


    @classmethod
    def add_sections(cls, sections):
        for course_name in sections.keys():
            course = CourseBusiness.get_course_by_name(course_name)
            items = sections[course_name]
            for item in items:
                sec = CourseSectionBusiness.create_section(name=item['name'],
                                                           zh_name=item[
                                                               'zh_name'])
                course.sections.append(sec)
                course.save()
                sec.units = []
                for uni in item['units']:
                    unit = CourseUnitBusiness.create_unit(name=uni['name'],
                                                          zh_name=uni[
                                                              'zh_name'])
                    sec.units.append(unit)
                sec.save()


    @classmethod
    def delete_sections(cls, course_name, section_names):
        import copy
        course = CourseBusiness.get_course_by_name(course_name)
        # 删除项目
        sections = copy.deepcopy(course.sections)
        for name in section_names:
            for section in sections:
                if section.zh_name == name:
                    sections.remove(section)
                    break
        # print([section.zh_name for section in sections])
        course.sections = sections
        # print([section for section in course.sections])
        # print([section.zh_name for section in course.sections])
        course.save()

# 添加实战项目
if __name__ == '__main__':
    # local: Machine Learning Operation
    # rc: Machine Learning Practice
    # prod: Machine Learning Practice
    # sections = {"Machine Learning Practice": [
    #     {
    #         'zh_name': '卷积神经网络-猫狗识别',
    #         'name': 'CNN - Dogs And Cats Classification',
    #         'units': [
    #             {
    #                 'zh_name': '卷积神经网络-猫狗识别',
    #                 'name': 'CNN - Dogs And Cats Classification'
    #             }
    #         ]
    #     },
    #     {
    #         'zh_name': '卷积神经网络-人脸关键点识别',
    #         'name': 'CNN - Face KeyPoint Detect',
    #         'units': [
    #             {
    #                 'zh_name': '卷积神经网络-人脸关键点识别',
    #                 'name': 'CNN - Face KeyPoint Detect'
    #             }
    #         ]
    #     }
    # ]}
    # CourseService.add_sections(sections)
    CourseService.delete_sections("Machine Learning Practice",
                                  ['CNN - Face KeyPoint Detect',
                                   'CNN - Dogs And Cats Classification'])
