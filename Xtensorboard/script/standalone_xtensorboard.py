# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click
from Xtensorboard.xtensorboard import run_xtensorboard
from Xtensorboard import __version__


@click.command()
@click.option(
	"-i", "--i-folder", required=True, nargs=1, type=str,
	help="Folder from which to start to get the tensorboard logs."
)
@click.option(
	"-o", "--o-spawner", required=False, nargs=1, type=str,
	help="Output script (to run to spawn the remote job)."
)
@click.option(
	"-p", "--p-port", required=False, default=8185, type=int,
	help="Port on both machines."
)
@click.option(
	"-c", "--p-conda", required=True, default='qiime2-2020.2', type=str,
	help="Conda environment with tensorboard installed."
)
@click.option(
	"-r", "--p-regex", required=False, default=None, multiple=True, type=str,
	help="Regex(es) to only look at certain runs."
)
@click.version_option(__version__, prog_name="xtensorboard")


def standalone_xtensorboard(
		i_folder,
		o_spawner,
		p_port,
		p_conda,
		p_regex
):
	run_xtensorboard(
		i_folder,
		o_spawner,
		p_port,
		p_conda,
		p_regex
	)


if __name__ == "__main__":
	standalone_xtensorboard()
