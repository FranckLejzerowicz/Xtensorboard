# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import sys
import pkg_resources
from os.path import abspath, dirname, isdir, splitext

RESOURCES = pkg_resources.resource_filename('Xtensorboard', 'resources')


def run_xtensorboard(
        i_folder: str,
        o_spawner: str,
        p_port: int,
        p_conda: str
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
        tensorboards.append('%s:%s' % (root_split, root))

    if not len(tensorboards):
        print('no logdir containing a "checkpoint" file found for path\n%s\nExiting' % i_folder)
        sys.exit(0)

    tensorboard_commands = ','.join(tensorboards)

    if o_spawner:
        o_tmp_out = '%s_tmp' % splitext(o_spawner)[0]
        o_killer = '%s_kill.sh' % splitext(o_spawner)[0]
    else:
        o_spawner = abspath('%s/spawner.sh' % i_folder)
        o_tmp_out = '%s_tmp' % splitext(o_spawner)[0]
        o_killer = '%s_kill.sh' % splitext(o_spawner)[0]

    o_spawner_dir = dirname(o_spawner)
    if not isdir(o_spawner_dir):
        os.makedirs(o_spawner_dir)

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

    print('- To spawn a tunnel job, run:\nsh %s' % o_spawner)
    print('- Then on you local machine, run:')
    print('ssh -nNT -L %s:localhost:%s <username>@barnacle.ucsd.edu' % (str(p_port), str(p_port)))
    print('- In chrome/firefox, go to:\nhttps://localhost:%s' % str(p_port))
    print('!!!Do not forget to kill job and tunnel, by running:\nsh %s' % o_killer)
