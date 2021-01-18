import os
import shutil
import subprocess

JAVA_PATH = '/usr/bin/java'

# get box path, given id
def box_path(id=0):
    return '/var/local/lib/isolate/{}/box'.format(id)

# read content from file
def read_file(name):
    with open(name, 'r') as f:
        return f.read()

# write content to file
def write_file(name, content):
    with open(name, 'w') as f:
        f.write(content)

# compile file, return (ok, msg)
# ok (bool) = True if compilation was successful, False otherwise
# msg (str) = error message ('' if none)
def javac(name):
    p = subprocess.Popen(['javac', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = p.communicate()[1].decode()
    ok = p.returncode == 0
    return (ok, err)

def compile(source_code):
    # write source code here
    write_file('Main.java', source_code)
    # compile
    ok, msg = javac('Main.java')
    # remove source code
    os.remove('Main.java')
    return ('OK', '') if ok else ('CE', msg)

def java(root):
    p = subprocess.Popen(['sudo', 'isolate', '-p', '--meta=meta', '--time=1', '--stdin=in', '--run', JAVA_PATH, root], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [x.decode() for x in p.communicate()]

def _get_output(test_input):
    # move binary to the box, write input to the box
    shutil.copy('Main.class', box_path())
    write_file(box_path() + '/in', test_input)
    # execute
    user_output, err = java('Main')
    # remove binary and input
    os.remove(box_path() + '/Main.class')
    os.remove(box_path() + '/in')
    # read and remove metafile
    lines = read_file('meta').split('\n')
    d = dict()
    for line in lines:
        try:
            key, val = line.split(':')
            d[key] = val
        except:
            pass
    os.remove('meta')
    # check if execution completed ok
    if 'status' in d:
        return (d['status'], '') if d['status'] != 'RE' else ('RE', err)
    return ('OK', user_output)
    
def get_output(source_code, test_input):
    code, msg = compile(source_code)
    if code == 'CE':
        return (code, msg)
    return _get_output(test_input)

# compile, copy to box, run, compare output and return verdict
def _get_verdict(test_input, test_output):  
    code, msg = _get_output(test_input)
    if code != 'OK':
        return (code, msg)
    return ('OK', '') if msg == test_output else ('WA', '')

def get_tests(folder):
    tests = []
    for file in os.listdir(folder):
        if file.endswith(".in"):
            tests.append(folder + '/' + file[:-3])
    return tests

def get_verdicts(source_code, test_folder):
    code, msg = compile(source_code)
    if code == 'CE':
        return (code, msg)
    
    tests = get_tests(test_folder)
    verdicts = dict()
    for test in tests:
        verdicts[test] = _get_verdict(read_file(test + '.in'), read_file(test + '.out'))
    return verdicts
    

if __name__ == '__main__':
    folders = ['sol-ok', 'sol-wa', 'sol-to', 'sol-re', 'sol-ce']
    tests = ['1000', '100000']
    for folder in folders:
        print(get_verdicts(read_file(folder + '/Main.java'), '.'))