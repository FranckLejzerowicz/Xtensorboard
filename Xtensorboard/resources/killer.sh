#!/bin/bash

jup_job=`head -n 1 KILLER`
qdel ${jup_job}
to_kill=`ps aux | grep "PORT_ID:localhost" | awk '{print $2}'`
kill ${to_kill}
rm KILLER
rm nohup.out
rm STDIN.*
