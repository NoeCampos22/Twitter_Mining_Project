#!/bin/sh

echo "Starting Python Script"

python Tweepy_Program.py &      # '&' to run in background

LASTPID=$!                      # Save $! in case you do other background-y stuff

sleep 600; kill $LASTPID        # Sleep 10 minutes, then kill to set timeout.

echo "Program Finished"
