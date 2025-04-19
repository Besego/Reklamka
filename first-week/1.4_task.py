class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def display_info(self):
        print(f"Студент: {self.name}, Возраст: {self.age}, Класс: {self.grade}")

class GraduateStudent(Student):
    def __init__(self, name, age, grade, thesis_title):
        super().__init__(name, age, grade)
        self.thesis_title = thesis_title

    def display_info(self):
        super().display_info()
        print(f"Тема дессертации: {self.thesis_title}")

class UndergraduateStudent(Student):
    def __init__(self, name, age, grade, major):
        super().__init__(name, age, grade)
        self.major = major

    def display_info(self):
        super().display_info()
        print(f"Специальность: {self.major}")  

student1 = Student("Иван", 20, "A")
graduateStudent = GraduateStudent("Александр", 22, "В", "Уроки пайтона")
undergraduateStudent = UndergraduateStudent("Михаил", 23, "Г", "Программист")

student1.display_info()
graduateStudent.display_info()
undergraduateStudent.display_info()