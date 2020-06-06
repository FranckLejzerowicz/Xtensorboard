#!/bin/bash

jup_job=`head -n 1 TMP_OUT`
qdel ${jup_job}
to_kill=`ps aux | grep "localhost" | grep PORT_ID | awk '{print $2}'`
kill ${to_kill}
rm TMP_OUT
rm nohup.out
sleep 5
cd FILE_DIR
rm STDIN.*
