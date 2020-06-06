#!/bin/bash

job_no=`echo "conda activate CONDA_ENV; tensorboard --logdir LOGFOLDERS --port=PORT_ID" | qsub -V -l walltime=2:00:00,nodes=1:ppn=1,pmem=50mb | grep "barnacle" | cut -d '.' -f1`
sleep 2
barnacle_node=`qstat -f $job_no | grep "exec_host" | cut -d '/' -f1 | cut -d '=' -f2 | sed 's/\ //g'`
echo $job_no > KILLER
echo $barnacle_node >> KILLER
nohup ssh -f -N -L PORT_ID:localhost:PORT_ID $barnacle_node
