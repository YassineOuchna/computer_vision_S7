#
# Copyright (c) 2021 ADLINK Technology Inc.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
#
# Contributors:
#   ADLINK zenoh team, <zenoh@adlink-labs.tech>
#
import math
import time
import sys
from datetime import datetime
import argparse
import curses
import zenoh
import json
from dataclasses import dataclass
from pycdr2 import IdlStruct
from pycdr2.types import int8, int32, uint32, float64


@dataclass
class Vector3(IdlStruct, typename="Vector3"):
    x: float64
    y: float64
    z: float64


@dataclass
class Twist(IdlStruct, typename="Twist"):
    linear: Vector3
    angular: Vector3


@dataclass
class Time(IdlStruct, typename="Time"):
    sec: int32
    nanosec: uint32


@dataclass
class Log(IdlStruct, typename="Log"):
    stamp: Time
    level: int8
    name: str
    msg: str
    file: str
    function: str
    line: uint32


def main(stdscr):
    stdscr.refresh()

    # --- Command line argument parsing --- --- --- --- --- ---
    parser = argparse.ArgumentParser(
        prog='ros2-teleop',
        description='zenoh ros2 teleop example')
    parser.add_argument('--mode', '-m', dest='mode',
                        choices=['peer', 'client'],
                        type=str,
                        help='The zenoh session mode.')
    parser.add_argument('--connect', '-e', dest='connect',
                        metavar='ENDPOINT',
                        action='append',
                        type=str,
                        help='zenoh endpoints to connect to.')
    parser.add_argument('--listen', '-l', dest='listen',
                        metavar='ENDPOINT',
                        action='append',
                        type=str,
                        help='zenoh endpoints to listen on.')
    parser.add_argument('--config', '-c', dest='config',
                        metavar='FILE',
                        type=str,
                        help='A configuration file.')
    parser.add_argument('--cmd_vel', dest='cmd_vel',
                        default='rt/turtle1/cmd_vel',
                        type=str,
                        help='The "cmd_vel" ROS2 topic.')
    parser.add_argument('--rosout', dest='rosout',
                        default='rt/rosout',
                        type=str,
                        help='The "rosout" ROS2 topic.')
    parser.add_argument('--angular_scale', '-a', dest='angular_scale',
                        default='2.0',
                        type=float,
                        help='The angular scale.')
    parser.add_argument('--linear_scale', '-x', dest='linear_scale',
                        default='2.0',
                        type=float,
                        help='The linear scale.')

    args = parser.parse_args()
    conf = zenoh.Config.from_file(
        args.config) if args.config is not None else zenoh.Config()
    if args.mode is not None:
        conf.insert_json5(zenoh.config.MODE_KEY, json.dumps(args.mode))
    if args.connect is not None:
        conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps(args.connect))
    if args.listen is not None:
        conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps(args.listen))
    cmd_vel = args.cmd_vel
    rosout = args.rosout
    angular_scale = args.angular_scale
    linear_scale = args.linear_scale

    # zenoh-net code  --- --- --- --- --- --- --- --- --- --- ---

    # initiate logging
    zenoh.init_logger()

    print("Openning session...")
    session = zenoh.open(conf)

    print("Subscriber on '{}'...".format(rosout))

    def rosout_callback(sample):
        log = Log.deserialize(sample.payload)
        print('[{}.{}] [{}]: {}'.format(log.stamp.sec,
                                        log.stamp.nanosec, log.name, log.msg))

    sub1 = session.declare_subscriber(rosout, rosout_callback)

    def pub_twist(linear, angular):
        print("Pub twist: {} - {}".format(linear, angular))
        t = Twist(linear=Vector3(x=linear, y=0.0, z=0.0),
                  angular=Vector3(x=0.0, y=0.0, z=angular))
        session.put(cmd_vel, t.serialize())
    def getdata():
        return 20,20,0,90

    print("Waiting commands with arrow keys or space bar to stop. Press ESC or 'q' to quit.")
    #t1 and t2 indicates if there is a turtlebot and an object respectively
    #here we will get 2 distances d1 is the distance between the two turtlebots d2 is the distance between the turtlebot that has a camera and the object
    #we will also get 2 angles: a1 the local angle of the turtlebot and a2 the local angle of the object
    #we will calculate d3 the distance between the blind turtlebot and the object and a3 the angle between them
    t1,t2,d1,d2,a1,a2=getdata()
    d3=d1**2+d2**2-2*d1*d2*math.cos(a1-a2)
    count=60
    while d3 > 0:
        with open('data.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                last = lines[-1].strip()
                t1 = (last[0] == '1')
                t2=(last[1]=='1')
                a1=math.floor(float(last[2]))
                a2=math.floor(float(last[3]))
                time.sleep(0.1)
        if count==60:
            with open('data1.txt','r') as f:
                lines=f.readlines()
                if len(lines)>1:
                    last=lines[-2].strip()
                    d1=last.split(',')[a1]
                    d2=last.split(',')[a2]
                    count=0
            d3=d1**2+d2**2-2*d1*d2*math.cos(a1-a2)
            with open('data2.txt','r') as f:
                lines=f.readlines()
                if len(lines)>1:
                    last=lines[-2].strip()
                    
                    
        
        if (t2==False):
            continue
        elif t1 == False:
            pub_twist(0.0, 1.0 * angular_scale)
            time.sleep(0.1)
        elif (t1 == True) and (abs(c)>20):
            pub_twist(0.0, -c*100/250)
            time.sleep(0.1)
        elif (t1 == True) and (abs(c) < 20):
            pub_twist(-1.0*linear_scale, 0.0)
            time.sleep(0.1)

    sub1.undeclare()
    session.close()


curses.wrapper(main)
