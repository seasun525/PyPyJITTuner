import sys
import os
import subprocess
import logging
import shutil
import time
import ConfigParser
from reset_database import *
from configuration import jit_config
from parse_result import result_parser 

config = ConfigParser.RawConfigParser()
config.read('load_test.cfg')

result_root_dir = config.get('LoadTest', 'result_root_dir')
jitlog_temp_dir = config.get('LoadTest', 'jitlog_temp_dir')
client_dir = config.get('LoadTest', 'client_dir')
client_ip = config.get('LoadTest', 'client_ip')
client_user = config.get('LoadTest', 'client_user')
client_jmeter = config.get('LoadTest', 'client_jmeter')
client_test_plan = config.get('LoadTest', 'client_test_plan')
test_duration = config.getint('LoadTest', 'duration')
pypy_path = config.get('LoadTest', 'pypy_path')
app_path = config.get('LoadTest', 'app_path')

def copy_jitlog(individual_string):
    new_folder = result_root_dir + individual_string
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)
    shutil.copytree(jitlog_temp_dir, new_folder)
    shutil.rmtree(jitlog_temp_dir)
    os.mkdir(jitlog_temp_dir)

def copy_response_time(individual_string):
    new_folder = result_root_dir + individual_string

    CMD = 'scp %s@%s:%sjmeter_responses.csv %s'%(client_user, client_ip, client_dir, new_folder)
    proc = subprocess.Popen(CMD, shell=True)
    proc.wait()

    CMD = 'scp %s@%s:%sjmeter_returning_user.csv %s'%(client_user, client_ip, client_dir, new_folder)
    proc = subprocess.Popen(CMD, shell=True)
    proc.wait()

    CMD = ['ssh', '%s@%s'%(client_user, client_ip), 'rm', '-rf', client_dir]
    proc = subprocess.Popen(' '.join(CMD), shell=True)
    proc.wait()

    CMD = ['ssh', '%s@%s'%(client_user, client_ip), 'mkdir', client_dir]
    proc = subprocess.Popen(' '.join(CMD), shell=True)
    proc.wait()

def main():
    individual = sys.argv[1]
    client_ip = sys.argv[2]

    logging.basicConfig(filename=jitlog_temp_dir+'logger.log', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', level=logging.INFO, filemode='w')
    logging.info('Start load test for config: '+individual)
    logging.info('Workload is generated from: '+client_ip)

    #set environment variable
    os.system('export SECRET_KEY=\"308159\"')
    os.system('export ALLOWED_HOSTS=\"xx.xx.xx.xx\"')

    #get jit configuration
    Config = jit_config()
    pypy_config = Config.string_to_config(individual)

    #start application
    logging.info('Starting application with:')
    CMD = [pypy_path+'/pypy2-v5.7.1-linux64/bin/pypy', pypy_config, pypy_path+'/pypy2-v5.7.1-linux64/bin/gunicorn', '-pid=gunicorn.pid saleor.wsgi:application --workers 3 --timeout 60000 -c gunicorn_conf.py --env DJANGO_DB=mysql', '>', '%sgunicorn.log'%jitlog_temp_dir]
    logging.info(' '.join(CMD))
    sys.stdout.flush()
    proc = subprocess.Popen(' '.join(CMD), cwd=app_path, shell=True)

    #start work load
    logging.info('Start work load with:')
    client_CMD = ['ssh', '%s@%s'%(client_user, client_ip), client_jmeter, '-n', '-t', client_test_plan, '>', '%sload_test.log'%jitlog_temp_dir]
    logging.info(' '.join(client_CMD))
    sys.stdout.flush()
    proc_client = subprocess.Popen(' '.join(client_CMD), shell=True)

    #monitor pid status of postgres
    time.sleep(10)
    psql_CMD = ['pypy', 'pid_record.py']
    psql_proc = subprocess.Popen(' '.join(psql_CMD), shell=True)

    #wait for workload finish
    sleep_time = test_duration# - 7200
    logging.info('Sleep ' + str(sleep_time) + ' for test...')
    time.sleep(sleep_time)

    #stop application
    logging.info('Stoping the application')
    proc_getpid = subprocess.Popen('cat '+app_path+'/id=gunicorn.pid', stdout=subprocess.PIPE, shell=True)
    for line in proc_getpid.stdout:
        pid_number = line.strip()
        break
    proc_shutdown = subprocess.Popen('kill '+pid_number, shell=True)
    
    time.sleep(3*60)
    logging.info('Restore the results')
    copy_jitlog(individual)
    copy_response_time(individual)
    
    Parser = result_parser()
    Parser.parse_for_pages(result_root_dir + individual + '/')


if __name__ == '__main__':
    main()
