#!/bin/bash

jup_job=`head -n 1 Xtensorboard/test/my_spanwer_kill.sh`
qdel ${jup_job}
to_kill=`ps aux | grep "8185:localhost" | awk '{print $2}'`
kill ${to_kill}
rm Xtensorboard/test/my_spanwer_kill.sh
rm nohup.out
rm STDIN.*
