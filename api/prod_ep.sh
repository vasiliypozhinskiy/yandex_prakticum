#!/bin/bash

# Start the first process
python3 -m grpc_tools.protoc -I ./protobufs --python_out . --grpc_python_out . ./protobufs/auth.proto && python3 server_grpc.py &

/wait && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?