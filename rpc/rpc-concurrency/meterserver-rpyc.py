#!/usr/bin/env python3

# 使用RPyC创建服务器

import datetime
import threading
import rpyc
import sys
import MeterMT

PORT = 11003

Manager = MeterMT.Manager()


class MeterService(rpyc.Service):

    def on_connect(self):
        pass


    def on_disconnect(self):
        pass


    exposed_login = Manager.login
    exposed_get_status = Manager.get_status
    exposed_get_job = Manager.get_job


    def exposed_submit_reading(self, sessionId, meter, when, reading,
            reason=""):
        when = datetime.datetime.strptime(str(when)[:19],
                "%Y-%m-%d %H:%M:%S")
        Manager.submit_reading(sessionId, meter, when, reading, reason)


if __name__ == "__main__":
    import rpyc.utils.server
    print("Meter server startup at {}".format(
            datetime.datetime.now().isoformat()[:19]))

    server = rpyc.utils.server.ThreadedServer(MeterService, port=PORT)
    thread = threading.Thread(target=server.start)
    thread.start()

    try:
        if len(sys.argv) > 1: # Notify if called by a GUI client
            with open(sys.argv[1], "wb") as file:
                file.write(b"\n")
        thread.join()
    except KeyboardInterrupt:
        pass
    server.close()
    print("\rMeter server shutdown at {}".format(
            datetime.datetime.now().isoformat()[:19]))
    MeterMT.Manager._dump()
