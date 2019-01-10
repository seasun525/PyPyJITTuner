import sys
import os

class result_parser():
    
    def __init__(self):
        self.response_start = 40*60
        self.response_end = 50*60
        self.skip_records = 1
        self.page_index = [[4149, 4150, 4151], 
            [4152, 4153, 4154, 4155], 
            [4156, 4157, 4159, 4167], 
            [4168, 4169, 4171, 4173],
            [4194, 4196, 4205],
            [4206, 4207], 
            [4208, 4209, 4211, 4212],
            [4213, 4214, 4214, 4216],
            [4217, 4218, 4219, 4220],
            [4221, 4222, 4223, 4224, 4225], 
            [4226, 4227, 4228],
            [4229, 4231, 4232]]

    def parse_response(self, input_folder):
        file_in = open(input_folder+'/jmeter_responses.csv', 'r')
        lines = file_in.readlines()
        start_time = int(lines[self.skip_records].split(',')[0])/1000

        response_time_list = []
        last_time = start_time
        
        for line in lines[self.skip_records:]:
            
            timestamp = int(line.split(',')[0])/1000
            elapsed = int(line.split(',')[1])
            response_code = str(line.split(',')[3])
            if not cmp(response_code, '200') and timestamp - start_time < self.response_end and timestamp - start_time > self.response_start:
                response_time_list.append(elapsed)
            
        return response_time_list

    def parse_response_1(self, input_folder):
        file_in = open(input_folder+'/jmeter_responses.csv', 'r')
        lines = file_in.readlines()
        start_time = int(lines[self.skip_records].split(',')[0])/1000

        response_time_list_for_pages = []
        for i in range(len(self.page_index)):
            response_time_dict = {}
            #initialize thread 
            for thread_id in range(11)[1:]:
                thread_name = '1-'+str(thread_id)
                for k in self.page_index[i]:
                    response_time_dict[str(k)+thread_name] = []
            #get response time from file
            for line in lines[self.skip_records:]:
                timestamp = int(line.split(',')[0])/1000
                response_code = str(line.split(',')[3])
                if not cmp(response_code, '200') and timestamp - start_time < self.response_end and timestamp - start_time > self.response_start:
                    elapsed = int(line.split(',')[1])
                    label = int(line.split(',')[2].split(' ')[0])
                    thread = line.split(',')[5].split(' ')[2]
                    #store response time for individual label, and  add up one by one later
                    if label in self.page_index[i]:
                        response_time_dict[str(label)+thread].append(elapsed) 

            thread_response_time_list = []
            #loop for each thread, 10 threads in total
            for thread_id in range(11)[1:]:
                thread_name = '1-'+str(thread_id)
                len_list = []
                for index in self.page_index[i]:
                    len_list.append(len(response_time_dict[str(index)+thread_name]))
                thread_response_time_list_temp = [0]*max(len_list)
                for j in range(max(len_list)):
                    for index in self.page_index[i]:
                        if j < len(response_time_dict[str(index)+thread_name]):
                            thread_response_time_list_temp[j] += response_time_dict[str(index)+thread_name][j]
                thread_response_time_list = thread_response_time_list + thread_response_time_list_temp
            response_time_list_for_pages.append(thread_response_time_list)
        print 'hello'
        return response_time_list_for_pages  

    def parse_pid(self, input_file_path):
        file_in = open(input_file_path)
        lines = file_in.readlines()
        
        CPU_list = []
        Memory_list = []

        for line in lines[1+self.response_start/10:]:
            CPU = float(line.split(',')[1])
            Memory = int(line.split(',')[2])

            CPU_list.append(CPU)
            Memory_list.append(Memory)

        return CPU_list, Memory_list

    def parse_pids(self, input_folder, name): #name is postgres or pid
        CPU_result_list = []
        Memory_result_list = []
        count = 0
        file_list = os.listdir(input_folder)
        for file_name in file_list:
            if file_name.startswith(name+'_status') and file_name.endswith('.csv'):
                temp_cpu, temp_memory = self.parse_pid(input_folder+'/'+file_name)
                CPU_result_list.append(temp_cpu)
                Memory_result_list.append(temp_memory)
                count += 1

        CPU_list = []
        Memory_list = []
        for i in range(len(CPU_result_list[0])):
            CPU_temp = 0
            Memory_temp = 0
            for j in range(count):
                CPU_temp += CPU_result_list[j][i]
                Memory_temp += Memory_result_list[j][i]
            CPU_list.append(CPU_temp/count)
            Memory_list.append(Memory_temp/count)
        
        return CPU_list, Memory_list


    def parse(self, input_folder):
        response_time_list = self.parse_response(input_folder)
        response_file_out = open(input_folder+'/statistic_response.csv', 'w')
        response_file_out.write('\n'.join(map(str, response_time_list)))
        response_file_out.close()

        CPU_list, Memory_list = self.parse_pids(input_folder, 'pid')
        CPU_file_out = open(input_folder+'/worker_statistic_CPU.csv', 'w')
        Memory_file_out = open(input_folder+'/worker_statistic_Memory.csv', 'w')
        CPU_file_out.write('\n'.join(map(str, CPU_list)))
        Memory_file_out.write('\n'.join(map(str, Memory_list)))
        CPU_file_out.close()
        Memory_file_out.close()

        CPU_list, Memory_list = self.parse_pids(input_folder, 'postgres')
        CPU_file_out = open(input_folder+'/postgres_statistic_CPU.csv', 'w')
        Memory_file_out = open(input_folder+'/postgres_statistic_Memory.csv', 'w')
        CPU_file_out.write('\n'.join(map(str, CPU_list)))
        Memory_file_out.write('\n'.join(map(str, Memory_list)))
        CPU_file_out.close()
        Memory_file_out.close()
     
    def parse_for_pages(self, input_folder):
        result = []
        response_time_list_for_page = self.parse_response_1(input_folder)
        for i in range(len(self.page_index)):
            result.append(response_time_list_for_page[i])

        output_file = open(input_folder+'/individual_value', 'w')
        for l in result:
            output_file.write(','.join(map(str, l))+'\n')
        output_file.close()

if __name__ == '__main__':
    input_folder = sys.argv[1]
    Parser = result_parser() 
    Parser.parse_for_pages(input_folder)
