kill -9 $(ps auxf | grep sftp_watcher.py | awk '{print $2}' | tail -n1)
rm nohup.out

