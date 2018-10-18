import os, json, re, sys
class Db_Search:
    acceptable_intents=[
        'Course_Average_Size_Of',
        'Course_Credits_Of',
        'Course_Description_Of',
        'Course_Instructor_Of',
        'Course_Opentime_Of',
        'Course_Title_Of',
        'Credit_Course_Is',
        'Instructor_Teaches',
        'Semester_Has_Courses'
    ]

    def __init__(self,debug_mode):
        self.debug_mode = debug_mode
        path_to_json = 'crawler/courseInformation/Json'
        self.json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        self.courses_info = []
        for js in self.json_files:
            with open(path_to_json + '/' + js) as f:
                self.courses_info.append(json.load(f))

    '''
    Check if the passed in intent can be processed in this model and process it.
    :param potato: a list of the same format as the return list which is passed in to this module.
    :param assistant_returned_info: a list contains processed returned info from assistant in the format of
        [intend(str),flag(bool),context(dict),response(str)]
    :returns: a list [is_successfully_processed (bool), result (str)], where result can also be a string contains
        necessary info about processing a request which involves more than 1 modules if is_successfully_processed is. It will be passed to other
        modules.
    '''
    def process(self, potato, assistant_returned_info):
        result=[]
        intent=assistant_returned_info[0]
        if intent in Db_Search.acceptable_intents:
            result.append(True) #This is hard coded for now since current requests do not involve more than 1 module
            paramlist=[]
            result.append(getattr(Db_Search, 'Course_Average_Size_Of')(self, 'qwe'))
        else:
            result.append(False)
            result.append('No result')
        #TODO: change formal parameter of the following functions to context(dict) of assistant_returned_info

    def Course_Average_Size_Of(self, course_num):
        #For test purpose only
        print(course_num)
    # def Course_Average_Size_Of(self, course_num):
    #     course_num = re.sub(r"\D", "", course_num)
    #     json_file_name = 'CSE' + course_num + '.json'
    #     if json_file_name in self.json_files:
    #         course_index = self.json_files.index(json_file_name)
    #         response_header = 'The average size of ' + str(course_num) + ' is '
    #         return response_header + str(self.courses_info[course_index].get('average_size'))
    #     else:
    #         return 'Cannot find the given course number'

    def Course_Credits_Of(self, course_num):
        course_num = re.sub(r"\D", "", course_num)
        json_file_name = 'CSE' + course_num + '.json'
        if json_file_name in self.json_files:
            course_index = self.json_files.index(json_file_name)
            response_header = 'The credit hours of ' + str(course_num) + ' is '
            return response_header + str(self.courses_info[course_index].get('credits'))
        else:
            return 'Cannot find the given course number'

    def Course_Description_Of(self, course_num):
        course_num = re.sub(r"\D", "", course_num)
        json_file_name = 'CSE' + course_num + '.json'
        if json_file_name in self.json_files:
            course_index = self.json_files.index(json_file_name)
            response_header = str(course_num) + ' is about '
            return response_header + self.courses_info[course_index].get('description')
        else:
            return 'Cannot find the given course number'

    def Course_Instructor_Of(self, course_num):
        course_num = re.sub(r"\D", "", course_num)
        json_file_name = 'CSE' + course_num + '.json'
        if json_file_name in self.json_files:
            course_index = self.json_files.index(json_file_name)
            response_header = 'The instructors of ' + str(course_num) + ' are '
            return response_header + self.courses_info[course_index].get('professors')
        else:
            return 'Cannot find the given course number'

    # def Email_Send_Appointment(email_module, user, question, professor, email):
    #     text = construct_email_appointment(professor, question, user.name)
    #     email_module.send(email, 'Appointment Scheduling', text)
    #     return 'Email Sent!'


    # def Course_Opentime_Of(course_num):
    #     course_num=re.sub(r"\D", "", course_num)
    #     json_file_name='CSE'+course_num+'.json'
    #     if json_file_name in json_files:
    #         course_index=json_files.index(json_file_name)
    #         response_header='The open time of '+str(course_num)+' is '
    #         return response_header+courses_info[course_index].get('open_time')
    #     else:
    #         return 'Cannot find the given course number'

    def Course_Opentime_Of(self, course_num):
        num = re.sub(r"\D", "", course_num)
        course_num = "CSE " + num
        for course_info in self.courses_info:
            if course_info["title"] != None and course_num in course_info['title']:
                return course_info['open_time']

        not_found_message = "\nThere does not exit course_num in Ohio State University.\n"

        return not_found_message.replace("course_num", course_num)

    def Course_Title_Of(self, course_num):
        num = re.sub(r"\D", "", course_num)
        course_num = "CSE " + num
        for course_info in self.courses_info:
            if course_info['title'] != None and course_num in course_info['title']:
                return course_info['title']

        not_found_message = "\nThere does not exit course_num in Ohio State University.\n"
        return not_found_message.replace("course_num", course_num)

    def Credit_Course_Is(self, credits):
        courses = []
        credits = credits[:len(credits) - 1]
        for course_info in self.courses_info:
            if course_info["credits"] != None and credits in str(course_info["credits"]):
                courses.append(course_info["title"][:8])
        if len(courses) == 0:
            not_found_message = "\nThere does not exit course of $ credit hours.\n"

            return not_found_message.replace("$", credits)
        else:
            course_names = ""
            for course in courses:
                course_names += course
                course_names += ","

            return course_names

    def Instructor_Teaches(self, name):
        courses = []
        first_char = 0
        second_char = 0
        for i in range(len(name)):
            if name[i] == " ":
                second_char = i + 1
                break
        if second_char != 0:
            name = name[:first_char + 1].upper() + name[first_char + 1:second_char] + name[
                                                                                      second_char:second_char + 1].upper() + name[
                                                                                                                             second_char + 1:]
        else:
            name = name[:first_char + 1].upper() + name[first_char + 1:]

        for course_info in self.courses_info:
            if course_info['professors'] != None and name in course_info['professors']:
                courses.append(course_info['title'][:8])
        if len(courses) == 0:
            not_found_message = "\nIt seems $ haven't taught any courses in Ohio State University.\n"

            return not_found_message.replace("$", name)
        else:
            course_names = ""
            for course in courses:
                course_names += course
                course_names += ","

            return course_names

    def Semester_Has_Courses(self, semester):
        year = re.sub(r"\D", "", semester)
        if len(str(year)) == 2:
            year = "20" + year
        if semester[0] == 'a' or semester[0] == 'A' or semester[0] == 'F' or semester[0] == 'f':
            semester = "Fall " + year
        elif semester[0:3] == "SU" or semester[0:3] == "su" or semester[0:3] == "Su" or semester[0:3] == "sU":
            semester = "Summer " + year
        elif semester[0:3] == "Sp" or semester[0:3] == "sp" or semester[0:3] == "sP" or semester[0:3] == "SP":
            semester = "Spring " + year
        courses = []
        for course_info in self.courses_info:
            if course_info["open_time"] != None and semester in course_info["open_time"]:
                courses.append(course_info["title"][:8])
        if len(courses) == 0:
            not_found_message = "\nNo course opens in $.\n"

            return not_found_message.replace("$", semester)
        else:
            course_names = ""
            for course in courses:
                course_names += course
                course_names += ","

            return course_names