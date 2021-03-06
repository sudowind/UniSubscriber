import code
import os

from Announcer import BaseAnnouncer
from Master import SubscriberMaster
from Monitor import BaseMonitor


class MyMonitor(BaseMonitor):
    def __init__(self, name, dir_path, **kwargs):
        super(MyMonitor, self).__init__(name, **kwargs)
        self.dir_path = dir_path

    def diff(self, prev_content, now_content):
        return set(now_content).difference(set(prev_content))

    def extract_content(self):
        files = []
        for a, b, c in os.walk(self.dir_path):
            for cc in c:
                files.append(cc)
        return files

    def gen_msg(self):
        msg = dict()
        msg['msg'] = 'find new item {} in {}'.format(' '.join(self.diff_content), self.dir_path)
        return msg


class MyAnnouncer(BaseAnnouncer):
    def announce(self, msg):
        print msg[0], msg[1]['diff_content'], msg[1]['msg']


if __name__ == '__main__':
    master = SubscriberMaster('sm1')
    monitor = MyMonitor('m1', './', interval=5)
    announcer = MyAnnouncer(name='a1')
    master.add_monitor(monitor)
    master.add_announcer(announcer)
    master.start()
    code.interact(banner="", local=locals())

