""" asdasd """
import os
import json
from datetime import datetime

class SubscriberData():
    """ asdasd """
    now = None
    max = 0
    min = 0
    mean = [0]
    def __init__(self):
        # read Computed data
        if os.path.exists('data.json'):
            with open('data.json', 'r') as dfp:
                self.old = json.load(dfp)
        else:
            self.old = dict()

        old = str(int(datetime.now().strftime('%Y%m%d'))-1)
        if os.path.exists('{}.log'.format(old)):
            self.old[old] = self._compute_log(old)
            # write old data to json
            print(self.old)
            with open('data.json', 'w') as dfp:
                json.dump(self.old, dfp, indent=1)
            # remove old file
            os.remove('{}.log'.format(old))

        now = datetime.now().strftime('%Y%m%d')
        self.now = now
        if os.path.exists('{}.log'.format(now)):
            aux = self._read_file(now)
            self.now = now
            self.max = max(aux)
            self.min = min(aux)
            self.mean = aux[-5:]

    def get_data_points(self):
        """ asdasdasd """
        dtime = list()
        dmax = list()
        dmin = list()
        dmean = list()
        for i in self.old:
            # dtime.append(int(i))
            dtime.append('{}-{}-{}'.format(i[:4], i[4:6], i[6:]))
            dmax.append(self.old[i]['max'])
            dmin.append(self.old[i]['min'])
            dmean.append(self.old[i]['mean'])
        # dtime.append(int(self.now))
        dtime.append('{}-{}-{}'.format(self.now[:4], self.now[4:6], self.now[6:]))
        dmax.append(self.max)
        dmin.append(self.min)
        dmean.append(sum(self.mean)/5)
        print(dmean)

        return dtime, dmax, dmin, dmean

    def add_data_points(self, data):
        """ Add data points """
        self.max = max(self.max, data)
        self.min = min(self.min, data)
        self.mean.append(data)
        self.mean = self.mean[-5:]
        with open('{}.log'.format(self.now), 'a') as logfp:
            logfp.write('{}\n'.format(data))

    def _remove_old_data(self, keep_days=5):
        """ clear data and remain "keep_days" """
        keys = list(self.old.keys())
        keys.sort()
        for i in range(len(keys)-keep_days):
            _ = self.old.pop(keys[i])

    def _read_file(self, filename):
        """ read file and return list """
        data = list()
        with open("{}.log".format(filename), 'r') as log_fp:
            for line in log_fp:
                data.append(int(line.strip()))
        return data

    def _compute_log(self, date):
        """ read lof file with filename as date.log """
        data = self._read_file(date)
        return {'max': max(data), 'min': min(data), 'mean': sum(data)/len(data)}
