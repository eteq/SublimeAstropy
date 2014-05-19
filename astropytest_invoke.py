from __future__ import print_function, division

import os
import sys

paths = ['.']
found_path = None

file_dir, file_name = os.path.split(sys.argv[1])

while not found_path:
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
    test_selector = '-P ' + file_dir[len(found_path)+1+len('astropy/'):]

if len(sys.argv) > 2:
    pytest_args = '--args="{0}" '.format(' '.join(sys.argv[2:]).replace('"', "'"))
else:
    pytest_args = ''

os.chdir(found_path)
pycmd = 'setup.py test ' + pytest_args + test_selector

print('Running:', sys.executable + ' ' + pycmd)
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
