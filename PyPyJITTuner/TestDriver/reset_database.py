import os
import subprocess

def reset_db():
    CMD = 'sudo -i -u postgres dropdb saleor'
    proc = subprocess.Popen(CMD, shell=True)
    proc.wait()

    CMD = 'sudo -i -u postgres createdb saleor'
    proc = subprocess.Popen(CMD, shell=True)
    proc.wait()

    CMD = 'sudo -i -u postgres psql saleor < /var/lib/postgresql/new_saleor_backup'
    proc = subprocess.Popen(CMD, shell=True)
    proc.wait()

def reset_db_and_shutdown():
    reset_db()
    os.system('sudo reboot')

if __name__ == '__main__':
    reset_db_and_shutdown()
