class jit_config():

    def __init__(self):
        self.decay_default = 40
        self.function_threshold_default = 1619
        self.loop_longevity = 1000
        self.threshold = 1039
        self.trace_eagerness = 200
        self.trace_limit = 3000 #note: default is 6000 but the upper bound is less than defaultx4
        self.mul_list = [4, 3, 2, 1, float(1)/2, float(1)/4, float(1)/8, float(1)/16]
        self.config_value_list = [self.decay_default, self.function_threshold_default, self.loop_longevity, 
            self.threshold, self.trace_eagerness, self.trace_limit]
        self.config_name_list = ['decay', 'function_threshold', 'loop_longevity', 'threshold', 'trace_eagerness',
            'trace_limit']

    def individual_to_config(self, individual):
        temp_list = []
        value_list = decode_string(individual)
        for i in range(6):
            temp_value = int(int(self.config_value_list[i])*self.mul_list[value_list[i]])
            temp_string = self.config_name_list[i]+'='+str(temp_value)
            temp_list.append(temp_string)

        return '--jit '+','.join(temp_list)
        
    def decode_list(self, individual):
        temp_list = []
        for i in range(6):
            string_value = ''.join(map(str, individual[i*3:(i+1)*3]))
            value = int(string_value, 2)
            temp_list.append(value)

        return temp_list

    def string_to_config(self, individual):
        temp_list = []
        value_list = self.decode_list(individual)
        for i in range(6):
            temp_value = int(int(self.config_value_list[i])*self.mul_list[value_list[i]])
            temp_string = self.config_name_list[i]+'='+str(temp_value)
            temp_list.append(temp_string)

        return '--jit '+','.join(temp_list)    

    def list_to_string(self, individual):
        return ''.join(individual)

