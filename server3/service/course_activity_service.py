# -*- coding: UTF-8 -*-
from server3.business.course_activity_business import CourseActivityBusiness
from server3.entity.course import Course
from server3.repository.general_repo import Repo


class CourseActivityService:
    business = CourseActivityBusiness

    @classmethod
    def get_by_user(cls, user):
        courses = Repo(Course).read()
        res = {}
        for course in courses:
            res[course.id] = cls.business.get_by_user(user, course)
        return res


