@echo off
echo start to run ygmws_sheduler...
echo %CD%
set ETCD_SERVICE_SERVICE_HOST=192.168.0.203
set ETCD_SERVICE_SERVICE_PORT=22379
set PYTHONPATH=%CD%\..\..\src

cd %CD%\..\tester

python put_test_task_to_api_queue.py
pause
