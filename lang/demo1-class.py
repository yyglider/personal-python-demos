# 类的私有属性 __private_attrs, 类内部的方法中使用  self.__private_attrs
# 类的方法，在类的内部，使用def关键字可以定义一个方法，与一般函数定义不同，类方法必须包含参数self，且为第一个参数
# 私有的类方法，__private_method，在类的内部使用self.__private_method调用

class people:
    # 定义基本属性
    name = ''
    age = 0
    # 定义私有属性，这类外部无法直接访问
    __weight = 0
    # 定义构造方法
    def __init__(self,name,age,weight):
        self.name = name
        self.age = age
        self.__weight = weight
    def speak(self):
        print("%s is speaking : i am %d years old" %(self.name,self.age))




# 单继承
class student(people):
    grade = ''
    def __init__(self,name,age,weight,grade):
        #调用父类的构造函数
        people.__init__(self,name,age,weight)
        self.grade = grade
    # 复写父类的方法
    def speak(self):
        print("%s is speaking : i am %d years old and i am in grade %d" % (self.name, self.age, self.grade))


# 多继承
class speaker():
    topic = ''
    name = ''
    def __init__(self,name,topic):
        self.name = name
        self.topic = topic
    def speak(self):
        print("i am %s, i am a speaker, my topic is %s" % (self.name, self.topic))

class sample(speaker,student):
    def __init__(self,name,age,weight,grade,topic):
        student.__init__(self,name,age,weight,grade)
        speaker.__init__(self,name,topic)


# 使用 @property
class  Celsius:
    def __init__(self, temperature = 0):
        self._temperature = temperature

    def tofahreheit(self):
        return (self._temperature * 1.8) + 32

    @property
    def temperature(self):
        print("get value")
        return self._temperature

    @temperature.setter
    def temperature(self,value):
        if value < -273:
            raise ValueError("temperature below -273 in not possible")
        print("set value")
        self._temperature =  value





if __name__ == '__main__':
    test = sample("Tim",25,80,4,"python")
    test.speak()

    c = Celsius(56)
    print(c.temperature)
    c.temperature=32
    print(c.temperature)