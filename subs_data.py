""" asdasd """
import os
import json
from datetime import datetime

class SubscriberData():
    """ asdasd """
    now = None
    max = None
    min = None
    mean = list()
    def __init__(self):
        # read Computed data
        if os.path.exists('data.json'):
            with open('data.json', 'r') as dfp:
                self.old = json.load(dfp)
            if self._remove_old_data():
                print("clearning data on first read")
                with open('data.json', 'w') as dfp:
                    json.dump(self.old, dfp, indent=1)
        else:
            self.old = dict()

        # read previous logfile
        self.reload_previous_data()
        # read current logfile
        now = datetime.now().strftime('%Y%m%d')
        self.now = now
        if os.path.exists('{}.log'.format(now)):
            aux = self._read_file(now)
            self.now = now
            self.max = max(aux)
            self.min = min(aux)
            self.mean = aux[-5:]

    def reload_previous_data(self):
        """ asdasdasd """
        old = str(int(datetime.now().strftime('%Y%m%d'))-1)
        if os.path.exists('{}.log'.format(old)):
            self.old[old] = self._compute_log(old)
            # remove old data
            self._remove_old_data()
            # write old data to json
            with open('data.json', 'w') as dfp:
                json.dump(self.old, dfp, indent=1)
            # remove old file
            os.remove('{}.log'.format(old))

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
        dtime.append('{}-{}-{}'.format(self.now[:4], self.now[4:6], self.now[6:]))
        dmax.append(self.max)
        dmin.append(self.min)
        dmean.append(sum(self.mean)/len(self.mean))

        return dtime, dmax, dmin, dmean

    def add_data_points(self, data):
        """ Add data points """
        now = datetime.now().strftime('%Y%m%d')
        if self.max is None:
            self.max = data
            self.min = data
            self.mean = [data]
        else:
            # new day
            if self.now != now:
                # write data to old (json)
                self.old[self.now] = {'max': self.max, 'min': self.min, 'mean': sum(self.mean)/len(self.mean)}
                with open('data.json', 'w') as dfp:
                    json.dump(self.old, dfp, indent=1)
                # remove older data
                self._remove_old_data()
                os.remove('{}.log'.format(self.now))

                # get data as new day
                self.now = now
                self.max = data
                self.min = data
                self.mean = [data]
            else:
                self.max = max(self.max, data)
                self.min = min(self.min, data)
                self.mean.append(data)
                self.mean = self.mean[-5:]
        
        with open('{}.log'.format(now), 'a') as logfp:
            logfp.write('{}\n'.format(data))

    def _remove_old_data(self, keep_days=5):
        """ clear data and remain "keep_days" """
        keys = list(self.old.keys())
        keys.sort()
        prev = len(keys)
        for i in range(len(keys)-keep_days):
            _ = self.old.pop(keys[i])
        return prev != len(self.old.keys())q

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
