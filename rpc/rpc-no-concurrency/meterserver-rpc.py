#!/usr/bin/env python3

# xml-rpc服务器

import argparse
import datetime
import os
import sys
import xmlrpc.server
if sys.version_info[:2] > (3, 1):
    import warnings
    warnings.simplefilter("ignore", ResourceWarning) # For stdlib socket.py
import Meter


HOST = "localhost"
PORT = 11002
PATH = "/meter"


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = (PATH,)


def main():

    host, port, notify = handle_commandline()
    manager, server = setup(host, port)
    print("Meter server startup at  {} on {}:{}{}".format(
            datetime.datetime.now().isoformat()[:19], host, port, PATH))
    # 如果notify变量中有文件名，那么服务器就会创建该文件，并向其中写入换行符，如果服务器是GUI客户端启动，那么客户端
    # 就会给服务器传递文件名，GUI客户端会一直等服务器创建好该文件，创建好之后客户端就知道服务器已经完全启动了。
    try:
        if notify:
            with open(notify, "wb") as file:
                file.write(b"\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\rMeter server shutdown at {}".format(
                datetime.datetime.now().isoformat()[:19]))
        manager._dump()


def handle_commandline():
    # 指定confilict_handler选项，以便覆写‘-h’选项 （默认是help功能）
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("-h", "--host", default=HOST,
            help="hostname [default %(default)s]")
    parser.add_argument("-p", "--port", default=PORT, type=int,
            help="port number [default %(default)d]")
    parser.add_argument("--notify", help="specify a notification file") 
    args = parser.parse_args()
    return args.host, args.port, args.notify


def setup(host=HOST, port=PORT):
    manager = Meter.Manager()
    server = xmlrpc.server.SimpleXMLRPCServer((host, port),
            requestHandler=RequestHandler, logRequests=False)
    server.register_introspection_functions()
    for method in (manager.login, manager.get_job, manager.submit_reading,
            manager.get_status):
        # 如果想令客户端能够访问manager对象的某个方法，那么必须先在服务器上注册它
        server.register_function(method)
    return manager, server


if __name__ == "__main__":
    main()
