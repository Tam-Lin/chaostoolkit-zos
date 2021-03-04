#!/usr/bin/env python
# Copyright 2017 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Example that shows how to send a system command.
"""

import sys
import logging
import json
import requests.packages.urllib3

import zhmcclient

# Print metadata for each OS message, before each message
PRINT_METADATA = True

requests.packages.urllib3.disable_warnings()

if len(sys.argv) != 2:
    print("Usage: %s hmccreds.json" % sys.argv[0])
    sys.exit(2)
hmccreds_file = sys.argv[1]

with open(hmccreds_file, 'r') as fp:
    hmccreds = json.load(fp)

examples = hmccreds.get("examples", None)
if examples is None:
    print("examples not found in credentials file %s" % \
          (hmccreds_file))
    sys.exit(1)

send_system_command = examples.get("send_system_command", None)
if send_system_command is None:
    print("send_system_command not found in credentials file %s" % \
          (hmccreds_file))
    sys.exit(1)

loglevel = send_system_command.get("loglevel", None)
if loglevel is not None:
    level = getattr(logging, loglevel.upper(), None)
    if level is None:
        print("Invalid value for loglevel in credentials file %s: %s" % \
              (hmccreds_file, loglevel))
        sys.exit(1)
    logmodule = send_system_command.get("logmodule", None)
    if logmodule is None:
        logmodule = ''  # root logger
    print("Logging for module %s with level %s" % (logmodule, loglevel))
    handler = logging.StreamHandler()
    format_string = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
    handler.setFormatter(logging.Formatter(format_string))
    logger = logging.getLogger(logmodule)
    logger.addHandler(handler)
    logger.setLevel(level)

hmc = send_system_command["hmc"]
cpcname = send_system_command["cpcname"]
partname = send_system_command["partname"]

cred = hmccreds.get(hmc, None)
if cred is None:
    print("Credentials for HMC %s not found in credentials file %s" % \
          (hmc, hmccreds_file))
    sys.exit(1)

userid = cred['userid']
password = cred['password']

print(__doc__)

print("Using HMC %s with userid %s ..." % (hmc, userid))
session = zhmcclient.Session(hmc, userid, password)
cl = zhmcclient.Client(session)

timestats = send_system_command.get("timestats", False)
if timestats:
    session.time_stats_keeper.enable()

try:
    cpc = cl.cpcs.find(name=cpcname)
except zhmcclient.NotFound:
    print("Could not find CPC %s on HMC %s" % (cpcname, hmc))
    sys.exit(1)

try:
    if cpc.dpm_enabled:
        partkind = "partition"
        partition = cpc.partitions.find(name=partname)
    else:
        partkind = "LPAR"
        partition = cpc.lpars.find(name=partname)
except zhmcclient.NotFound:
    print("Could not find %s %s on CPC %s" % (partkind, partname, cpcname))
    sys.exit(1)

command_to_send = send_system_command.get("command_to_send", None)
if command_to_send is None:
    print("No command found in credentials file %s ..." % hmccreds_file)
    sys.exit(1)

message_to_watch_for = send_system_command.get("message_to_watch_for", None)
if message_to_watch_for is None:
    print("No message to watch for found in credentials file %s ..." % hmccreds_file)
    sys.exit(1)

print("Sending command %s for %s %s on CPC %s ..." %
      (command_to_send, partkind, partname, cpcname))

topic = partition.open_os_message_channel(include_refresh_messages=True)
print("OS message channel topic: %s" % topic)

receiver = zhmcclient.NotificationReceiver(topic, hmc, userid, password)
print("Showing OS messages (including refresh messages) ...")
sys.stdout.flush()

try:
    partition.send_os_command(command_to_send)
except:
    print("Command failed")
    sys.exit(1)

try:
    for headers, message in receiver.notifications():
        # print("# HMC notification #%s:" % headers['session-sequence-nr'])
        # sys.stdout.flush()
        os_msg_list = message['os-messages']
        for os_msg in os_msg_list:
            if PRINT_METADATA:
                msg_id = os_msg['message-id']
                held = os_msg['is-held']
                priority = os_msg['is-priority']
                prompt = os_msg.get('prompt-text', None)
                print("# OS message %s (held: %s, priority: %s, prompt: %r):" %
                      (msg_id, held, priority, prompt))
            msg_txt = os_msg['message-text'].strip('\n')
            os_msg_id = msg_txt.split()[0]
            print(msg_txt)
            print("Message ID: %s" % os_msg_id)
            sys.stdout.flush()
            if os_msg_id == message_to_watch_for:
                raise NameError
except KeyboardInterrupt:
    print("Keyboard interrupt - leaving receiver loop")
    sys.stdout.flush()
except NameError:
    print("Message with ID %s occurred - leaving receiver loop" % message_to_watch_for)
    print(msg_txt)
    sys.stdout.flush()
finally:
    print("Closing receiver...")
    sys.stdout.flush()
    receiver.close()

print("Logging off...")
sys.stdout.flush()
session.logoff()

if timestats:
    print(session.time_stats_keeper)

print("Done.")