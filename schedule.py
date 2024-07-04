from datetime import datetime
import csv

valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
valid_sex_limits = ['not', 'male', 'female']
valid_major = ['计算机科学与技术', '电子信息工程', '物理学', '化学', '材料科学与工程', '生物科学', '生物技术',
               '生物医学工程', '数学与应用数学', '管理科学', '工业设计-智能设计', '工业设计-娱乐设计', '外国语言与外国历史']
valid_english_level = ['人文英语', '基础英语-EF', '基础英语-人文']

advanced_english_level_restriction = [
    ('Monday', 8, 9), ('Tuesday', 5, 6), ('Tuesday', 8, 9), ('Tuesday', 10, 11), ('Thursday', 8, 9)]

course_group = {
    '体育': ['游泳', '田径'],
    '大学英语': ['基础英语-EF', '基础英语-人文']
}


def check_overlap(day1, start1, end1, day2, start2, end2):
    if day1 != day2:
        return False

    return start1 < end2 and start2 < end1


def check_advanced_english_overlap(day, start, end):
    for (e_day, e_start, e_end) in advanced_english_level_restriction:
        if check_overlap(day, start, end, e_day, e_start, e_end):
            return True
    return False


'''
course_id,  course_day, course_start,   course_end, sex_limit,  number_limit
CS101,      Monday,     1,              3,          not,        30
MA201,      Monday,     2,              4,          not,        25
PH301,      Tuesday,    3,              5,          not,        20
CH401,      Wednesday,  4,              6,          not,        15
BI501,      Thursday,   5,              7,          male,       40
HS601,      Friday,     6,              8,          female,     35
'''


def read_course_data(file_path):
    course_data = {}
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            course_id = row['course_id']
            course_day = row['course_day']
            course_start = int(row['course_start'])
            course_end = int(row['course_end'])
            sex_limit = row['sex_limit']
            number_limit = int(row['number_limit'])
            course_name = row['course_name']

            if course_name == "游泳" or course_name == "田径":
                course_end += 2

            # Validation
            if course_day not in valid_days:
                raise ValueError(
                    f"Invalid course_day '{course_day}' for course_id '{course_id}'. Must be one of {valid_days}.")
            if sex_limit not in valid_sex_limits:
                raise ValueError(
                    f"Invalid sex_limit '{sex_limit}' for course_id '{course_id}'. Must be one of {valid_sex_limits}.")

            course_info = {
                'course_id': course_id,
                'course_name': course_name,
                'course_day': course_day,
                'course_start': course_start,
                'course_end': course_end,
                'sex_limit': sex_limit,
                'number_limit': number_limit,
                'enrolled_students': 0
            }

            course_data[course_id] = course_info

    return course_data


'''
student_id,student_sex,student_major,student_english_level
S001,male,计算机,人文英语
S002,female,电子,基础英语I-人文阅读
S003,male,物理学,基础英语I-公共演讲
S004,female,化学,人文英语
S005,male,生物科学,基础英语I-人文阅读
'''


def read_student_data(file_path):
    student_data = []
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            student_id = row['student_id']
            student_sex = row['student_sex']
            student_major = row['student_major']
            student_english_level = row['student_english_level']

            if student_major not in valid_major:
                raise ValueError(
                    f"Invalid student_major '{student_major}' for student '{student_id}'. Must be one of {valid_major}.")
            if student_english_level not in valid_english_level:
                raise ValueError(
                    f"Invalid student_english_level '{student_english_level}' for student '{student_id}'. Must be one of {valid_english_level}.")

            student_info = {
                'student_id': student_id,
                'student_sex': student_sex,
                'student_major': student_major,
                'student_english_level': student_english_level
            }

            student_data.append(student_info)

    return student_data


'''
专业,课程
计算机,体育,习思想,中华文明通论
数学与应用数学,体育,习思想,中华文明通论
物理学,体育,思想道德与法治,哲学导论,物理原理实验
化学,体育,思想道德与法治,哲学导论,普通化学实验I
材料,体育,思想道德与法治,哲学导论,普通化学实验I
生物科学,体育,思想道德与法治,哲学导论,普通化学实验I
生物技术,体育,思想道德与法治,哲学导论,普通化学实验I
生物医学工程,体育,思想道德与法治,哲学导论
数学与应用数学,体育,思想道德与法治,哲学导论,普通化学实验I
管理科学,体育,思想道德与法治,哲学导论
工业设计-智能设计方向,体育,思想道德与法治,哲学导论
工业设计-娱乐设计方向,体育,思想道德与法治,哲学导论
外国语言与外国历史,体育,思想道德与法治,哲学导论
'''


def sort_courses(courses):
    # Define the priority of each course
    priority = {
        '物理原理实验': 1,
        '普通化学实验': 2,
        '游泳': 100,
        '田径': 101
    }

    # Sort courses based on their defined priority, defaulting to a middle value for unspecified courses
    sorted_courses = sorted(courses, key=lambda x: priority.get(x, 50))
    return sorted_courses


def read_major_data(file_path):
    major_data = {}
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            major_name = row[0]
            courses = [course_prefix for course_prefix in row[1:]
                       if course_prefix]

            if major_name not in valid_major:
                raise ValueError(
                    f"Invalid major_name '{major_name}'. Must be one of {valid_major}.")

            sorted_courses = sort_courses(courses)

            major_info = {
                'major_name': major_name,
                'courses': sorted_courses
            }
            major_data[major_name] = major_info

    return major_data


def assign_courses_to_student(student, major_data, course_data):
    major_courses = major_data[student['student_major']]['courses']
    assigned_courses = []
    enrolled_courses = set()
    unassigned_courses = []

    for course_prefix in major_courses:
        successfully_assigned = False
        for course_id, course_info in course_data.items():
            if course_info['course_name'].startswith(course_prefix) and course_id not in enrolled_courses:
                if (course_info['sex_limit'] == 'not' or course_info['sex_limit'] == student['student_sex']):
                    if course_info['enrolled_students'] < course_info['number_limit']:
                        overlap = False
                        if student['student_english_level'] == "人文英语":
                            if check_advanced_english_overlap(course_info['course_day'], course_info['course_start'], course_info['course_end']):
                                overlap = True

                        for ac in assigned_courses:
                            if check_overlap(course_info['course_day'], course_info['course_start'], course_info['course_end'],
                                             ac['course_day'], ac['course_start'], ac['course_end']):
                                overlap = True
                                break
                        if not overlap:
                            assigned_courses.append(course_info)
                            course_info['enrolled_students'] += 1
                            enrolled_courses.add(course_id)
                            successfully_assigned = True
                            break
        if not successfully_assigned:
            # Add prefix indicating unassigned course
            unassigned_courses.append(course_prefix)

    # Assign English course
    english_course_prefix = student['student_english_level']
    english_successfully_assigned = False
    for course_id, course_info in course_data.items():
        if course_info['course_name'].startswith(english_course_prefix) and course_id not in enrolled_courses:
            if course_info['enrolled_students'] < course_info['number_limit']:
                overlap = False
                for ac in assigned_courses:
                    if check_overlap(course_info['course_day'], course_info['course_start'], course_info['course_end'],
                                     ac['course_day'], ac['course_start'], ac['course_end']):
                        overlap = True
                        break
                if not overlap:
                    assigned_courses.append(course_info)
                    course_info['enrolled_students'] += 1
                    english_successfully_assigned = True
                    break
    if not english_successfully_assigned and not student['student_english_level'] == "人文英语":
        unassigned_courses.append(english_course_prefix)

    student['courses'] = [course['course_id'] for course in assigned_courses]
    student['unassigned_courses'] = unassigned_courses

    if student['student_english_level'] == "人文英语":
        return len(assigned_courses) == len(major_courses)
    else:
        return len(assigned_courses) == len(major_courses) + 1


def assign_courses_to_students(students: dict, major_data, course_data):
    assigned_students = []
    unassigned_students = []

    for student in students:
        if not assign_courses_to_student(student, major_data, course_data):
            unassigned_students.append(student)
        else:
            assigned_students.append(student)

    return assigned_students, unassigned_students


def validate_assignments(assigned_students, course_data, major_data):
    for student in assigned_students:
        assigned_courses = student['courses']
        assigned_course_infos = [course_data[course_id]
                                 for course_id in assigned_courses]

        # Check if all required major courses are assigned
        major_courses = major_data[student['student_major']]['courses']
        assigned_major_courses = [course['course_name'] for course in assigned_course_infos if not course['course_name'].startswith(
            '基础英语') and not course['course_name'].startswith('人文英语')]
        if not all(any(course.startswith(prefix) for course in assigned_major_courses) for prefix in major_courses):
            return False, f"Student {student['student_id']} does not have all required major courses."

        # Check for time conflicts
        for i, course_info1 in enumerate(assigned_course_infos):
            for j, course_info2 in enumerate(assigned_course_infos):
                if i != j and check_overlap(course_info1['course_day'], course_info1['course_start'], course_info1['course_end'],
                                            course_info2['course_day'], course_info2['course_start'], course_info2['course_end']):
                    return False, f"Student {student['student_id']} has time conflicts between courses {course_info1['course_id']} and {course_info2['course_id']}."

        # Check if sex limit is respected
        for course_info in assigned_course_infos:
            if course_info['sex_limit'] != 'not' and course_info['sex_limit'] != student['student_sex']:
                return False, f"Student {student['student_id']} is assigned to course {course_info['course_id']} which does not meet the sex limit."

        # Check if number limit is respected
        for course_info in assigned_course_infos:
            if course_info['enrolled_students'] > course_info['number_limit']:
                return False, f"Course {course_info['course_id']} exceeds number limit."

        # Check if correct English course is assigned
        english_course_prefix = student['student_english_level']
        if english_course_prefix != '人文英语':
            assigned_english_courses = [course['course_name']
                                        for course in assigned_course_infos if course['course_name'].startswith(english_course_prefix)]
            if len(assigned_english_courses) == 0:
                return False, f"Student {student['student_id']} does not have the required English course."

    return True, "All assignments are valid."


def export_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def main():
    courses_file = './data/courses.csv'
    students_file = './data/students.csv'
    majors_file = './data/majors.csv'

    course_data = read_course_data(courses_file)
    student_data = read_student_data(students_file)
    major_data = read_major_data(majors_file)

    assigned_students, unassigned_students = assign_courses_to_students(
        student_data, major_data, course_data)

    valid, message = validate_assignments(
        assigned_students, course_data, major_data)
    if not valid:
        print("Validation failed:", message)
    else:
        print("All assignments are valid.")

    assigned_students_data = []
    unassigned_students_data = []

    # Prepare data for assigned students
    for student in assigned_students:
        courses = [student['student_id']] + student['courses']
        assigned_students_data.append(courses)
        print(
            f"Student ID: {student['student_id']}, Courses: {student['courses']}")

    # Prepare data for unassigned students
    for student in unassigned_students:
        row = [student['student_id']] + \
            student['courses'] + student['unassigned_courses']
        unassigned_students_data.append(row)
        print(
            f"Student ID: {student['student_id']}, Courses: {student['courses']}, Unassigned Courses: {student['unassigned_courses']}")

    # Export to CSV without headers
    if assigned_students_data:
        export_to_csv('./result/assigned_students.csv', assigned_students_data)
    if unassigned_students_data:
        export_to_csv('./result/unassigned_students.csv',
                      unassigned_students_data)


if __name__ == "__main__":
    # print(read_major_data('./majors.csv'))
    # print(read_student_data('./students.csv'))
    # print(read_course_data('./courses.csv'))
    main()
