#!/usr/bin/env python3

# 数据包封装
# 该模块用于提供Manager类存放仪表读数，并提供相关方法

import collections
import datetime
import hashlib
import random
import sys
import xmlrpc.client


random.seed(917) # Predictable random numbers for regression testing

Reading = collections.namedtuple("Reading", "when reading reason username")


class Error(Exception): pass


class Manager:

    # 不需要做成线程安全，因为xmlrpc服务器不是并发服务器，MeterMT.py的模块支持并发
    # 实际应用中，数据会存在数据库中
    SessionId = 0   # 唯一的会话标识
    UsernameForSessionId = {}   # 会话id:用户名
    ReadingForMeter = {}    # 仪表编号:仪表读数

    # 如果用户密码正确，那么就返回唯一的sessionID和姓名，调用其他方法时都必须传入这个sessionID
    def login(self, username, password):
        name = name_for_credentials(username, password)
        if name is None:
            raise Error("Invalid username or password")
        Manager.SessionId += 1
        sessionId = Manager.SessionId
        Manager.UsernameForSessionId[sessionId] = username
        return sessionId, name


    def get_status(self, sessionId):
        username = self._username_for_sessionid(sessionId)
        count = total = 0
        for reading in Manager.ReadingForMeter.values():
            if reading is not None:
                total += 1
                if reading.username == username:
                    count += 1
        return count, total

    # 虚拟出一个仪表
    def get_job(self, sessionId):
        self._username_for_sessionid(sessionId)
        while True: # Create fake meter
            kind = random.choice("GE")
            meter = "{}{}".format(kind, random.randint(40000,
                    99999 if kind == "G" else 999999))
            if meter not in Manager.ReadingForMeter:
                Manager.ReadingForMeter[meter] = None
                return meter

    # 认证sessionId
    def _username_for_sessionid(self, sessionId):
        try:
            return Manager.UsernameForSessionId[sessionId]
        except KeyError:
            raise Error("Invalid session ID")


    def submit_reading(self, sessionId, meter, when, reading, reason=""):
        if isinstance(when, xmlrpc.client.DateTime):
            when = datetime.datetime.strptime(when.value,
                    "%Y%m%dT%H:%M:%S")
        if (not isinstance(reading, int) or reading < 0) and not reason:
            raise Error("Invalid reading")
        if meter not in Manager.ReadingForMeter:
            raise Error("Invalid meter ID")
        username = self._username_for_sessionid(sessionId)
        reading = Reading(when, reading, reason, username)
        Manager.ReadingForMeter[meter] = reading
        return True


    @staticmethod
    def _dump(file=sys.stdout):
        for meter, reading in sorted(Manager.ReadingForMeter.items()):
            if reading is not None:
                print("{}={}@{}[{}]{}".format(meter, reading.reading,
                        reading.when.isoformat()[:16], reading.reason,
                        reading.username), file=file)


_User = collections.namedtuple("User", "username sha256")

# 根据传入的password计算sha-256哈希码
def name_for_credentials(username, password):
    sha = hashlib.sha256()
    sha.update(password.encode("utf-8"))
    user = _User(username, sha.hexdigest())
    return _Users.get(user)

# No locks for read-only data. Returns None for invalid username or password

# 每个条目都是_User元组，还有种方法，使用第三方passlib库

# Passwords are stored as SHA256 hex digests, e.g.,
#   sha = hashlib.sha256()
#   sha.update(b"pear")         # "pear" is the password
#   digest = sha.hexdigest()    # digest is what's stored as the sha256
_Users = {
    _User("adam",   # Password: adam
    "f7f376a1fcd0d0e11a10ed1b6577c99784d3a6bbe669b1d13fae43eb64634f6e"):
    "Adam Best",
    _User("carol",  # Password: carol
    "4c26d9074c27d89ede59270c0ac14b71e071b15239519f75474b2f3ba63481f5"):
    "Carol Dent",
    _User("eric",   # Password: eric
    "6f9edcd3408cbda14a837e6a44fc5b7f64ccc9a2477c1498fcb13c777ffb9605"):
    "Eric Fawn",
    _User("gwenda", # Password: gwenda
    "b0d0c7e0a2c7251768699b85e2ac9cdee23521ac6b1645fafec35eb93ca8870a"):
    "Gwenda Harris"
    }


if __name__ == "__main__":
    print("Loaded OK")
