from PyQt5 import QtCore, QtGui, QtWidgets
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()
Message=''
MessageCourse=''
class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(String, primary_key=True)
    name = Column(String)
    pre_req = Column(String)
    pre_reqID = Column(String)
    
    enrollments = relationship("StudentEnrollment", back_populates="course")
    students = relationship("Student", secondary="student_enrollment", back_populates="courses", overlaps="enrollments")
    
    def add_student(self,session, student):
        if not student.has_passed_prerequisite(self):
            global Message
            Message="You cannot enroll in the course due to prerequisite not met."
            return

        if student.is_fee_defaulter():
            Message="You cannot enroll in the course due to unpaid fees."
            return

        if student in self.students:
            Message="You are already enrolled in this course."
            return

        enrollment = StudentEnrollment(student_id=student.student_id, course_id=self.course_id, course_name=self.name)
        session.add(enrollment)
        session.commit()
        print("Student enrolled successfully.")
    
    def display_enrolled_students(self):
        print("Enrolled students:")
        for enrollment in self.enrollments:
            print(enrollment.student.name)


class BatchAdvisor(Base):
    __tablename__ = 'batch_advisors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def add_course(self, session,course_id,name,pre_req_id,pre_req_name):
        course = Course(name=name, course_id=course_id, pre_req=pre_req_name, pre_reqID=pre_req_id)
        session.add(course)
        session.commit()
        print("Course added successfully.")
        
    def update_PassedCourses(self,name,rollno,cname,course_id,grade):
        Session = sessionmaker(bind=create_engine('sqlite:///mydb.db'))
        session = Session()
        student = session.query(Student).filter_by(name=name, student_id=rollno).first()
        if not student:
            global MessageCourse
            MessageCourse="You are entering incorrect student name or rollno!!!"
        else:
            try:
                # Query to check if the student has passed the course
                passed_course = session.query(CoursesPassed).filter_by(student_id=rollno, course_id=course_id).first()
                
            except NoResultFound:  # Handle NoResultFound exception
                passed_course = None

            if not passed_course or passed_course.grade=='F' or passed_course.grade=='f':
                # If the course has not been passed before, insert it into the database
                register=session.query(StudentEnrollment).filter_by(student_id=rollno, course_id=course_id).first()
                if register:
                    passed_course = CoursesPassed(student_id=rollno, course_id=course_id, grade=grade)
                    session.add(passed_course)
                    session.commit()
                    MessageCourse="Data added Successfully!!!"
                else:
                    MessageCourse="Student is not registered in this course so can't enter this data"
            else:
                MessageCourse="This data is already present!!!"

        session.close()  # Close the session at the end of the method
        
class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    name = Column(String)
    passed_courses = relationship("CoursesPassed", back_populates="student")
    courses = relationship("Course", secondary="student_enrollment", back_populates="students", overlaps="enrollments")
    fee_defaulter = relationship("FeeDefaulter", uselist=False, back_populates="student")

    def is_fee_defaulter(self):
        if self.fee_defaulter:
            return True
        return False

    def has_passed_prerequisite(self, course):
        if course.pre_req == "None" or course.pre_req=="none":
            return True
        for pre_req_course in self.passed_courses:
            if course.pre_req == "None" or pre_req_course.course.name == course.pre_req or course.pre_req==None:
                return True
        return False
    
    def display_enrolled_courses(self, session):
        print("Enrolled courses:")
        enrolled_courses = session.query(StudentEnrollment).filter_by(student_id=self.student_id).all()
        for enrollment in enrolled_courses:
            print(enrollment.course_name)
    
class CoursesPassed(Base):
    __tablename__ = 'courses_passed'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    course_id = Column(String, ForeignKey('courses.course_id'))  # Add course_id column
    grade = Column(String)
    student = relationship("Student", back_populates="passed_courses")
    course = relationship("Course")  # Add relationship to Course



class StudentEnrollment(Base):
    __tablename__ = 'student_enrollment'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    course_id = Column(String, ForeignKey('courses.course_id'))
    course_name = Column(String)
    student = relationship("Student", overlaps="courses,students")
    course = relationship("Course", overlaps="courses,students")
    
    
class FeeDefaulter(Base):
    __tablename__ = 'fee_defaulter'
    student = relationship("Student", back_populates="fee_defaulter")
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    is_defaulter = Column(Boolean)



engine = create_engine('sqlite:///mydb.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
from Ui_Register import Ui_CourseRegister
from Ui_AdvisorLogin import Ui_BatchAdvisorLogin
from Ui_AdvisorMenu import Ui_AdvisorMenu
from Ui_AddCourse import Ui_AddCoursePage
from Ui_PassedCourseUpdate import Ui_PassedCourse
from Ui_HelpStudent import Ui_helpStudent
from Ui_CourseRegistered import Ui_CourseRegistered
from Ui_RegisteredCoursesbyStudent import Ui_RegisteredCoursesbyStudent
from Ui_RegisterationCourses import Ui_StudentRegisterationCourses
id=''
name=''
class Ui_MainWindow(object):
    def openRegister(self):
        self.window=QtWidgets.QMainWindow()
        self.ui=Ui_CourseRegister()
        self.ui.setupUi(self.window)
        self.ui.RegisterButton.clicked.connect(self.register)
        self.ui.pushButton.clicked.connect(self.openHelp)
        self.ui.click.clicked.connect(self.RegisteredCourseByStudent)
        MainWindow.close()
        self.window.show()
        
    def loginStudent(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_Student=Ui_MainWindow()
        self.ui_Student.setupUi(self.window)
        self.ui_Student.LoginButton.clicked.connect(self.login)
        self.window.show()
        
        
    def RegisteredCourseByStudent(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_regCourse=Ui_RegisteredCoursesbyStudent()
        self.ui_regCourse.setupUi(self.window)
        enrolled_courses = session.query(StudentEnrollment).filter_by(student_id=self.roll_no).all()
        courses_text=''
        course_width = 34
        if not enrolled_courses:
            courses_text = "No courses enrolled yet."

        else:
            # Header
            header = f"{'Courses Registered'.ljust(course_width)}\n\n"
            courses_text += header
            courses_text += "-" * (course_width) + "\n"

            
            for course in enrolled_courses:
                coursest = course.course_name.ljust(course_width)
                courses_text += f"{coursest}\n"

        # Set the accumulated text to the label
        self.ui_regCourse.Content_Data.setText(courses_text)
        self.ui_regCourse.pushButton.clicked.connect(self.openRegister)
        self.window.show()
        
        
    def AdminLoginPage(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_Admin=Ui_BatchAdvisorLogin()
        self.ui_Admin.setupUi(self.window)
        self.ui_Admin.LoginButton.clicked.connect(self.loginAdmin)
        self.ui_Admin.LoginStudent.clicked.connect(self.loginStudent)
        MainWindow.close()
        self.window.show()
    
    def openAdvisorMenu(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_AdminMenu=Ui_AdvisorMenu()
        self.ui_AdminMenu.setupUi(self.window)
        self.ui_AdminMenu.addCourse.clicked.connect(self.openAddCourse)
        self.ui_AdminMenu.UpdateGrade.clicked.connect(self.openupdateGrade)
        self.window.show()
    
    def openAddCourse(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_addC=Ui_AddCoursePage()
        self.ui_addC.setupUi(self.window)
        self.ui_addC.AddCourseBtn.clicked.connect(self.addCourse)
        self.ui_addC.pushButton.clicked.connect(self.opencourseRegistered)
        self.ui_addC.back.clicked.connect(self.openAdvisorMenu)
        self.window.show()
        
    def opencourseRegistered(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_Course=Ui_CourseRegistered()
        self.ui_Course.setupUi(self.window)
        courses_text = ""

        # Define the width for the columns
        name_width = 34
        prereq_width = 20

        # Retrieve all courses from the database
        CoursesList = session.query(Course).all()

        # If the course list is empty, handle it gracefully
        if not CoursesList:
            courses_text = "No courses available."

        else:
            # Header
            header = f"{'Course Name'.ljust(name_width)}{'Pre-requisite'.ljust(prereq_width)}\n\n"
            courses_text += header
            courses_text += "-" * (name_width + prereq_width) + "\n"

            # Loop through the courses and build the text
            for course in CoursesList:
                name = course.name.ljust(name_width)
                prereq = course.pre_req.ljust(prereq_width)
                courses_text += f"{name}{prereq}\n"
                
        # Set the accumulated text to the label
        self.ui_Course.Content_Data.setText(courses_text)   
        self.ui_Course.pushButton.clicked.connect(self.openAddCourse)   
        self.window.show()
        
        
    def openupdateGrade(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_UpdateGrade=Ui_PassedCourse()
        self.ui_UpdateGrade.setupUi(self.window)
        self.ui_UpdateGrade.Updatebtn.clicked.connect(self.updategrades)
        self.ui_UpdateGrade.back.clicked.connect(self.openAdvisorMenu)
        self.window.show()
        
    def openHelp(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_Help=Ui_helpStudent()
        self.ui_Help.setupUi(self.window)
        self.ui_Help.pushButton.clicked.connect(self.getID)
        self.ui_Help.backbtn.clicked.connect(self.openRegister)
        self.ui_Help.click.clicked.connect(self.openStudentRegisterationCourseAfterHelp)
        self.window.show()
        
    
    def openStudentRegisterationCourseAfterHelp(self):
        self.window=QtWidgets.QMainWindow()
        self.ui_CourseRegistered=Ui_StudentRegisterationCourses()
        self.ui_CourseRegistered.setupUi(self.window)
        courses_text = ""

        # Define the width for the columns
        name_width = 34
        prereq_width = 20

        # Retrieve all courses from the database
        CoursesList = session.query(Course).all()

        # If the course list is empty, handle it gracefully
        if not CoursesList:
            courses_text = "No courses available."

        else:
            # Header
            header = f"{'Course Name'.ljust(name_width)}{'Pre-requisite'.ljust(prereq_width)}\n\n"
            courses_text += header
            courses_text += "-" * (name_width + prereq_width) + "\n"

            # Loop through the courses and build the text
            for course in CoursesList:
                name = course.name.ljust(name_width)
                prereq = course.pre_req.ljust(prereq_width)
                courses_text += f"{name}{prereq}\n"
                

        # Set the accumulated text to the label
        self.ui_CourseRegistered.Content_Data.setText(courses_text)   
        self.ui_CourseRegistered.pushButton.clicked.connect(self.openHelp)   
        self.window.show()
          
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(461, 412)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LoginPage = QtWidgets.QWidget(self.centralwidget)
        self.LoginPage.setEnabled(True)
        self.LoginPage.setGeometry(QtCore.QRect(0, 0, 461, 391))
        self.LoginPage.setAutoFillBackground(False)
        self.LoginPage.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.LoginPage.setInputMethodHints(QtCore.Qt.ImhNone)
        self.LoginPage.setObjectName("LoginPage")
        self.LoginButton = QtWidgets.QPushButton(self.LoginPage)
        self.LoginButton.setGeometry(QtCore.QRect(190, 260, 91, 41))
        self.LoginButton.setStyleSheet("background-color: rgb(46, 172, 255);\n"
"font: 87 11pt \"Arial Black\";")
        self.LoginButton.setObjectName("LoginButton")
        self.PassLine = QtWidgets.QLineEdit(self.LoginPage)
        self.PassLine.setGeometry(QtCore.QRect(70, 210, 321, 31))
        self.PassLine.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.PassLine.setObjectName("PassLine")
        self.nameLine = QtWidgets.QLineEdit(self.LoginPage)
        self.nameLine.setGeometry(QtCore.QRect(70, 140, 321, 31))
        self.nameLine.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.nameLine.setObjectName("nameLine")
        self.StudentNamelabel = QtWidgets.QLabel(self.LoginPage)
        self.StudentNamelabel.setGeometry(QtCore.QRect(70, 110, 121, 16))
        self.StudentNamelabel.setStyleSheet("font: 63 14pt \"Sitka Display Semibold\";")
        self.StudentNamelabel.setObjectName("StudentNamelabel")
        self.IDlabel = QtWidgets.QLabel(self.LoginPage)
        self.IDlabel.setGeometry(QtCore.QRect(70, 180, 101, 16))
        self.IDlabel.setStyleSheet("font: 63 14pt \"Sitka Display Semibold\";")
        self.IDlabel.setObjectName("IDlabel")
        self.label = QtWidgets.QLabel(self.LoginPage)
        self.label.setGeometry(QtCore.QRect(130, 30, 231, 31))
        self.label.setStyleSheet("font: 63 14pt \"Sitka Display Semibold\";\n"
"background-color: rgb(66, 167, 255);\n"
"")
        self.label.setObjectName("label")
        self.LoginDetailLabel = QtWidgets.QLabel(self.LoginPage)
        self.LoginDetailLabel.setGeometry(QtCore.QRect(50, 310, 361, 20))
        self.LoginDetailLabel.setText("")
        self.LoginDetailLabel.setObjectName("LoginDetailLabel")
        self.widget_2 = QtWidgets.QWidget(self.LoginPage)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 461, 81))
        self.widget_2.setStyleSheet("background-color: rgb(66, 167, 255);")
        self.widget_2.setObjectName("widget_2")
        self.LoginDetailLabel_2 = QtWidgets.QLabel(self.LoginPage)
        self.LoginDetailLabel_2.setGeometry(QtCore.QRect(120, 340, 141, 20))
        self.LoginDetailLabel_2.setStyleSheet("font: 75 10pt \"Arial\";")
        self.LoginDetailLabel_2.setObjectName("LoginDetailLabel_2")
        self.loginAdvisor = QtWidgets.QPushButton(self.LoginPage)
        self.loginAdvisor.setGeometry(QtCore.QRect(260, 340, 51, 23))
        self.loginAdvisor.setStyleSheet("background-color: rgb(46, 172, 255);\n"
"font: 75 10pt \"Arial\";")
        self.loginAdvisor.setObjectName("loginAdvisor")
        self.widget_2.raise_()
        self.LoginButton.raise_()
        self.PassLine.raise_()
        self.nameLine.raise_()
        self.StudentNamelabel.raise_()
        self.IDlabel.raise_()
        self.label.raise_()
        self.LoginDetailLabel.raise_()
        self.LoginDetailLabel_2.raise_()
        self.loginAdvisor.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 461, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LoginButton.setText(_translate("MainWindow", "login"))
        self.StudentNamelabel.setText(_translate("MainWindow", "Student Name:"))
        self.IDlabel.setText(_translate("MainWindow", "Password:"))
        self.label.setText(_translate("MainWindow", "Student Registration Form"))
        self.LoginDetailLabel_2.setText(_translate("MainWindow", "Log in as batch advisor"))
        self.loginAdvisor.setText(_translate("MainWindow", "login"))
        self.LoginButton.clicked.connect(self.login)
        self.loginAdvisor.clicked.connect(self.AdminLoginPage)
        self.name=''
        self.roll_no=''
    
    def login(self):
        try:
            self.name = str(self.nameLine.text())
            self.roll_no = int(self.PassLine.text())
            student = session.query(Student).filter_by(name=self.name, student_id= self.roll_no).first()
            if student is None:
                self.LoginDetailLabel.setText(f"You are not Registered Successfully. Incorrect Roll No or Username")
                self.nameLine.clear()
                self.PassLine.clear()
            else:
                self.openRegister()
        except ValueError:
            self.LoginDetailLabel.setText("Something went Wrong!!!")
            
    def register(self):
        student = session.query(Student).filter_by(name=self.name, student_id=self.roll_no).first()
        course_id = str(self.ui.CourseID.text())
        course_name=str(self.ui.CourseName.text())
        course = session.query(Course).filter_by(course_id=course_id,name=course_name).first()
        try:
            if course:
                course.add_student(session, student)
                self.ui.messagealert.setText("Course Registered!!!")
                self.ui.CourseID.clear()
                self.ui.CourseName.clear()
            else:
                self.ui.messagealert.setText("No such Course!!!")
                self.ui.CourseID.clear()
                self.ui.CourseName.clear()
            if Message:
                self.ui.messagealert.setText(str(Message))
                self.ui.CourseID.clear()
                self.ui.CourseName.clear()
        except ValueError:
            self.ui.messagealert.setText("Something went Wrong!!!")
            
    def loginAdmin(self):
        try:
            self.ui_Admin.advisor_name = str(self.ui_Admin.nameLine.text())
            self.ui_Admin.advisor_password = str(self.ui_Admin.PassLine.text())
            advisor = session.query(BatchAdvisor).filter_by(name=self.ui_Admin.advisor_name, password=self.ui_Admin.advisor_password).first()
            if advisor is None:
                self.ui_Admin.LoginDetailLabel.setText("Login Unsuccessful")
                self.ui_Admin.nameLine.clear()
                self.ui_Admin.PassLine.clear()
            else:
                self.openAdvisorMenu()
        except ValueError:
            self.LoginDetailLabel.setText("Something went Wrong!!!")
            
    def addCourse(self):
        advisor = session.query(BatchAdvisor).filter_by(name=self.ui_Admin.advisor_name, password=self.ui_Admin.advisor_password).first()
        c_id=str(self.ui_addC.CourseIDLine.text())
        c_name=str(self.ui_addC.CoursenameLine.text())
        pre_Id=str(self.ui_addC.PreReqID.text())
        pre_name=str(self.ui_addC.PreReqName.text())
        advisor.add_course(session,c_id,c_name,pre_Id,pre_name)
        self.ui_addC.MESSAGE.setText("Course is added successfully")
        self.ui_addC.CourseIDLine.clear()
        self.ui_addC.CoursenameLine.clear()
        self.ui_addC.PreReqID.clear()
        self.ui_addC.PreReqName.clear()
        
    def updategrades(self):
        advisor = session.query(BatchAdvisor).filter_by(name=self.ui_Admin.advisor_name, password=self.ui_Admin.advisor_password).first()
        name=str(self.ui_UpdateGrade.StudentnameLine.text())
        rollno=int(self.ui_UpdateGrade.StudentIDLine.text())
        cname=str(self.ui_UpdateGrade.CourseNameLine.text())
        course_id=str(self.ui_UpdateGrade.CourseIDLine.text())
        grade=str(self.ui_UpdateGrade.GradeLine.text())
        advisor.update_PassedCourses(name,rollno,cname,course_id,grade)
        if MessageCourse:
            self.ui_UpdateGrade.Message.setText(str(MessageCourse))
        self.ui_UpdateGrade.StudentnameLine.clear()
        self.ui_UpdateGrade.StudentIDLine.clear()
        self.ui_UpdateGrade.CourseNameLine.clear()
        self.ui_UpdateGrade.CourseIDLine.clear()
        self.ui_UpdateGrade.GradeLine.clear()
        
    def getID(self):
        cname=str(self.ui_Help.CourseName.text())
        id=session.query(Course).filter_by(name=cname).first()
        if id:
            self.ui_Help.label_3.setText(str(id.course_id))
        else:
            self.ui_Help.messagealert.setText("No such Course exist!!!")
        self.ui_Help.CourseName.clear()

if __name__=="__main__":     
    import sys        
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

 

