class ContextManagerDemo:
    def __init__(self,msg):
        self.msg = msg

    def __enter__(self):
        if self.msg is None:
            raise ValueError('msg should not be none')
        return self.msg

    def __exit__(self, exc_ty, exc_val, tb):
        print('exit')
        self.msg = None




if __name__ == '__main__':
    t = ContextManagerDemo('hello msg')
    with t:
        print(t.msg)


