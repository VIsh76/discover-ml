# NO 'rc' lib is used to avoid depencies
# Rc is read as a txt file

class CapRC():
    def __init__(self, file_path):
        self._dict = {"HEARTBEAT_DT":0, 
                      "JOB_SGMT":'',
                      "BEG_DATE":'',
                      "END_DATE":''
                      }
        file = open(file_path)
        lines = file.readlines()
        for line in lines:
            line0 = line.strip('\n').split('#')[0].split(':') # Takeout comments
            if len(line0) == 2 and line0[0] in self._dict:
                print(line0)
                self._dict[line0[0]] = line0[1]
                
    @property
    def end_date(self):
        return self._dict['END_DATE']

    @property
    def beg_date(self):
        return self._dict['BEG_DATE']

    @property
    def job_segment(self):
        return self._dict['JOB_SGMT']

    @property
    def heartbeat_dt(self):
        return self._dict['HEARTBEAT_DT']
 
    def initialised(self):
        for element in self._dict:
            if not self._dict[element]:
                return False
        return True