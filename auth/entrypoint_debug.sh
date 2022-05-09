#!/bin/bash

# Start the first process
./flask_debug.sh &

./grpc_debug.sh

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?