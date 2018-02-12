rm -rf outlog
mkdir outlog

mkdir outlog/sendrecv
python pt_sendrecv.py 1    1000  >outlog/sendrecv/out_1 &
python pt_sendrecv.py 1001 2000  >outlog/sendrecv/out_2 &
python pt_sendrecv.py 2001 3000  >outlog/sendrecv/out_3 &
python pt_sendrecv.py 3001 4000  >outlog/sendrecv/out_4 &
