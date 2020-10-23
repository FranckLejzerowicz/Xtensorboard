# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import re
import sys
import socket
import subprocess
import pkg_resources
from os.path import abspath, dirname, expanduser, isdir, splitext

RESOURCES = pkg_resources.resource_filename('Xtensorboard', 'resources')


def run_xtensorboard(
        i_folder: str,
        o_spawner: str,
        p_port: int,
        p_conda: str,
        p_regex: tuple,
        local: bool
) -> None:
    """
    :param i_folder: str
    :param o_spawner: str
    :param p_port: int
    :param p_conda: str
    """

    i_folder = abspath(i_folder)

    if p_port < 1000 or p_port > 9999:
        print('use a 4-digits port (e.g. 8185)\nExiting...')
        sys.exit(1)

    spawner_temp = '%s/spawner.sh' % RESOURCES
    spawner_temp_local = '%s/spawner_local.sh' % RESOURCES
    killer_temp = '%s/killer.sh' % RESOURCES

    tensorboards = []
    for root, dirs, files in os.walk(i_folder):
        for fil in files:
            if fil == 'checkpoint':
                break
        else:
            continue

        re_root = root.split('%s/' % i_folder)[-1]
        root_split = '__'.join(re_root.split('/'))

        if p_regex:
            for regex in p_regex:
                if re.search(regex, root_split):
                    break
            else:
                continue

        tensorboards.append('%s:%s' % (root_split, root))

    if not len(tensorboards):
        print('no logdir containing a "checkpoint" file found for path\n%s\nExiting' % i_folder)
        sys.exit(0)

    tensorboard_commands = ','.join(tensorboards)

    if o_spawner:
        o_spawner = abspath(o_spawner)
        o_tmp_out = '%s_tmp' % abspath(splitext(o_spawner)[0])
        o_killer = '%s_kill.sh' % abspath(splitext(o_spawner)[0])
    else:
        o_spawner = abspath('%s/spawner.sh' % i_folder)
        o_tmp_out = '%s_tmp' % splitext(o_spawner)[0]
        o_killer = '%s_kill.sh' % splitext(o_spawner)[0]

    o_spawner_dir = dirname(o_spawner)
    if not isdir(o_spawner_dir):
        os.makedirs(o_spawner_dir)

    if local:
        p = subprocess.Popen(['which', 'conda'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        print(p.stdout.readlines())
        # for line in iter(p.stdout.readline, b''):
        #     p_conda = 'conda %s %s' % (str(line).strip().replace('conda', 'activate'), p_conda)
        #     break

        with open(spawner_temp_local) as f, open(o_spawner, 'w') as o:
            for line in f:
                L = line.replace('LOGFOLDERS', tensorboard_commands)
                L = L.replace('PORT_ID', str(p_port))
                if 'CONDA_ENV' in line:
                    L = '%s\n' % p_conda
                L = L.replace('FILE_DIR', o_spawner_dir)
                o.write(L)
        print('1. Run the tensorboard script:\nsh %s' % o_spawner)
        print('2. In chrome/firefox, go to:\nhttp://localhost:%s' % str(p_port))
        print('3. Stop script to free the port (ctrl-C)')
    else:
        with open(spawner_temp) as f, open(o_spawner, 'w') as o:
            for line in f:
                L = line.replace('LOGFOLDERS', tensorboard_commands)
                L = L.replace('PORT_ID', str(p_port))
                L = L.replace('CONDA_ENV', p_conda)
                L = L.replace('FILE_DIR', o_spawner_dir)
                o.write(L.replace('TMP_OUT', o_tmp_out))

        with open(killer_temp) as f, open(o_killer, 'w') as o:
            for line in f:
                L = line.replace('PORT_ID', str(p_port))
                L = L.replace('TMP_OUT', o_tmp_out)
                L = L.replace('FILE_DIR', o_spawner_dir)
                o.write(L)

        home = expanduser('~').split('/')[-1]
        hostname = socket.gethostname()
        print('- To spawn a tunnel job, run:\nsh %s' % o_spawner)
        print('- Then on you local machine, run:')
        print('ssh -nNT -L %s:localhost:%s %s@%s' % (str(p_port), str(p_port), home, hostname))
        print('- In chrome/firefox, go to:\nhttp://localhost:%s' % str(p_port))
        print('!!!Do not forget to kill job and tunnel, by running:\nsh %s' % o_killer)
