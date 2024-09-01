kill -9 $(ps auxf | grep wonderland_bot_v2.py | awk '{print $2}' | tail -n1)
rm nohup.out
