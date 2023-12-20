import sys
import json
import time
import zenoh
import parsing_file

# --- Command line argument parsing --- --- --- --- --- ---
parser = parsing_file.create_parser()
args = parser.parse_args()
conf = zenoh.Config.from_file(args.config) if args.config is not None else zenoh.Config()
if args.connect is not None:
    conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps(args.connect))
if args.listen is not None:
    conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps(args.listen))
if args.mode is not None:
    conf.insert_json5(zenoh.config.MODE_KEY, json.dumps(args.mode))
count=0

# Zenoh code  --- --- --- --- --- --- --- --- --- --- ---

def callback(sample: zenoh.Sample):
    # print(f"Sub: {sample.kind} ('{sample.key_expr}': '{sample.payload.decode('utf-8')}')")
    global count
    count +=1
    if count>20:
        count=0
        with open('data1.txt','w') as f:
            f.write(sample.payload.decode('utf-8')+'\n')

    else: 
        with open('data1.txt','a') as f:
            f.write(sample.payload.decode('utf-8')+'\n')

# "Open" zenoh
print("Opening session...")
zenoh.init_logger() # initiate logging
print(f"Declaring Subscriber on '{args.key}'...")
session = zenoh.open(conf) # open session
sub = session.declare_subscriber(args.key, callback, reliability=zenoh.Reliability.RELIABLE()) # declare subscriber

# Loop
print("Enter 'q' to quit...",'\n')
c = ''
while c != 'q':
    c = sys.stdin.read(1)
    time.sleep(1)

sub.undeclare()
session.close()

#python3 z_sub.py -l tcp/0.0.0.0:7500
#python3 z_sub.py -l tcp/localhost:8000
#python3 z_sub.py -l tcp/localhost:7447 -m client

# zenoh-0.7.0-rc-x86_64-pc-windows-msvc/zenohd -l tcp/localhost:7447
# python3 z_sub.py -l tcp/localhost:7447 -m client -k /demo/example/test