rm -rf log/*
pid=`ps -ef | grep "[0-9] python main.py" | awk '{print $2}'`
kill $pid
sleep 1
python main.py
#sleep 0.5
#tail -f ./log/*
