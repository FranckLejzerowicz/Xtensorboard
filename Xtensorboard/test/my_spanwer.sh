#!/bin/bash

job_no=`echo "conda activate qiime2-2028.10; tensorboard --logdir A2__B2:Xtensorboard/test/A2/B2,A__B__C:Xtensorboard/test/A/B/C --port=8185" | qsub -V -l walltime=2:00:00,nodes=1:ppn=1,pmem=50mb | grep "barnacle" | cut -d '.' -f1`
sleep 2
barnacle_node=`qstat -f $job_no | grep "exec_host" | cut -d '/' -f1 | cut -d '=' -f2 | sed 's/\ //g'`
echo $job_no > Xtensorboard/test/my_spanwer_kill.sh
echo $barnacle_node >> Xtensorboard/test/my_spanwer_kill.sh
nohup ssh -f -N -L 8185:localhost:8185 $barnacle_node
