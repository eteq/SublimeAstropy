from __future__ import print_function, division

import os
import sys


file_dir, file_name = os.path.split(sys.argv[1])

paths = [file_dir]
path = None
found_path = None

while not found_path:
    last_path = path
    path = os.path.abspath(os.sep.join(paths))
    files = os.listdir(path)
    if 'setup.py' in files:
        found_path = path
    if path == os.sep:
        raise ValueError('at root dir but did not find a setup.py')
    paths.append('..')

if file_name.startswith('test_') or file_name.endswith('.rst'):
    file_path = os.path.join(file_dir, file_name)
    dash_t_path = file_path[len(found_path)+1:]
    test_selector = '-t ' + dash_t_path

else:
    file_path = os.path.join(file_dir, file_name)
    test_selector = '-P ' + file_dir[len(last_path)+1:]

if len(sys.argv) > 2:
    pytest_args = '--args="{0}" '.format(' '.join(sys.argv[2:]).replace('"', "'"))
else:
    pytest_args = ''
print('chnging to',found_path)
os.chdir(found_path)
pycmd = 'setup.py test ' + pytest_args + test_selector

print('Running:', sys.executable + ' ' + pycmd)
print('cwd', os.path.abspath(os.curdir))
sys.stdout.flush()

retcode = os.system(sys.executable + ' ' + pycmd)

if retcode:
    if pytest_args == '':
        pytest_args2 = '--args="--ipdb" '
    else:
        pytest_args2 = pytest_args[:-2] + ' --ipdb" '
    pycmd2 = 'setup.py test ' + pytest_args2 + test_selector

    print("If you want to try this test interactively, do:")
    print("cd " + found_path + "; python " + found_path + os.sep + pycmd2)
