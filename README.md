# Xtensorboard

## Description

 # Install

```
pip install --upgrade git+https://github.com/FranckLejzerowicz/Xtensorboard.git
```
or
```
git clone https://github.com/FranckLejzerowicz/Xtensorboard.git
cd Xpbs
pip install -e .
```

## Usage example

```
Xtensorboard \
    -i path/to/a/folder/containing/mmvec/result(s) \
    -o my/folder/spawner.sh \
    -p 8185 \
    -c qiime2-2020.2
```

### Optional arguments

```
Options:
  -i, --i-folder TEXT   Folder from which to start to get the tensorboard
                        logs.  [required]

  -o, --o-spawner TEXT  Output script (to run to spawn the remote job).
  -p, --p-port INTEGER  Port on both machines.
  -c, --p-conda TEXT    Conda environment with tensorboard installed.
                        [required]

  -r, --p-regex TEXT    Regex(es) to only look at certain runs.
  --local / --no-local  Run locally, or on distant server (the default).
  --version             Show the version and exit.
  --help                Show this message and exit. 
``` 

### Bug Reports

contact `flejzerowicz@health.ucsd.edu`
