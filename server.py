import argparse
import os
import signal
import subprocess

FILENAME = 'heathergraph.py'
SERVICENAME = 'Heathergraph'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation',
                        choices=['start', 'stop', 'restart'],
                        help='start/stop/restart the server')
    return parser.parse_args()


def find_server_process(components):
    proc = subprocess.Popen(['ps', '-e', '-o', 'pid,command'],
                            stdout=subprocess.PIPE)
    (out, dummy) = proc.communicate()
    
    processes = [i.strip() for i in str(out).split('\n')[1:] if i]

    if len(processes) > 0:
        for line in processes:
            fields = line.split(None, 1)
            if fields[1] == ' '.join(components):
                return int(fields[0])

    return None

def get_absolute_filename(relative_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        relative_name))

def start_service(launch_command):
    proc = subprocess.Popen(launch_command)
    print SERVICENAME, 'service started - PID={}'.format(proc.pid)

def stop_service(pid):
    if pid:
        print 'Stopping %s service - PID={}'.format(pid) % SERVICENAME
        os.kill(pid, signal.SIGTERM)            
    else:
        print 'No %s service was found to be running' % SERVICENAME
    

def main():
    args = parse_args()
    launch_command = ['python',
                      get_absolute_filename(FILENAME)]
    pid = find_server_process(launch_command)

    if args.operation == 'start':
        if not pid:
            start_service(launch_command)
        else:
            print SERVICENAME, 'service is already running'

    elif args.operation == 'stop':
        stop_service(pid)
    elif args.operation == 'restart':
        stop_service(pid)
        start_service(launch_command)

if __name__ == '__main__':
    main()
