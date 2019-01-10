import json

def load_json(file_path):
    result = json.load(open(file_path,'r'))
    return result

def measure_coverage(profile_dict, test_dict):
    profiled_covered = {}
    not_profiled_covered = {}
    for key in test_dict:
        if key in profile_dict:
            temp_list = []
            temp_list2 = []
            for line_num in test_dict[key]:
                if line_num not in profile_dict[key]:
                    temp_list.append(line_num)
                else:
                    temp_list2.append(line_num)
            profiled_covered[key] = temp_list
            not_profiled_covered[key] = temp_list2
        else:
            print len(test_dict[key])
            not_profiled_covered[key] = test_dict[key]
    
    return profiled_covered, not_profiled_covered

def get_number_of_lines(result_dict):
    count = 0
    for key in result_dict:
        count += len(result_dict[key])
    return count


