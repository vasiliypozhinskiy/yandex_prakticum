#!/bin/bash

# Start the first process
/wait && flask db upgrade && python3 create_superuser.py && python3 main.py & 

python3 server_grpc.py

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?