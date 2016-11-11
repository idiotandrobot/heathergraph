import argparse
import os
import signal
import subprocess

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

def start_service():
    proc = subprocess.Popen(launch_command)
    print('Heathergraph service started - PID={}'.format(proc.pid))

def stop_service(pid):
    if pid:
        print('Stopping Heathergraph service - PID={}'.format(pid))
        os.kill(pid, signal.SIGTERM)            
    else:
        print('No Heathergraph service was found to be running')
    

def main():
    args = parse_args()
    launch_command = ['python',
                      get_absolute_filename('heathergraph.py')]
    pid = find_server_process(launch_command)

    if args.operation == 'start':
        if not pid:
            start_service()
        else:
            print('Heathergraph service is already running')

    elif args.operation == 'stop':
        stop_service(pid)
    elif args.operation == 'restart':
        stop_service(pid)
        start_service()

if __name__ == '__main__':
    main()
