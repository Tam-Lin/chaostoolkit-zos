
import sys
import logging
import json
import requests.packages.urllib3

import zhmcclient

class Send_Command():

    def __init__(self, hmccreds_location, command_to_send=None, message_to_watch_for=None):

        # Print metadata for each OS message, before each message
        PRINT_METADATA = False

        requests.packages.urllib3.disable_warnings()

        with open(hmccreds_location, 'r') as fp:
            hmccreds = json.load(fp)

        examples = hmccreds.get("examples", None)
        if examples is None:
            print("examples not found in credentials file %s" % \
                  (hmccreds_location))
            sys.exit(1)

        send_system_command = examples.get("send_system_command", None)
        if send_system_command is None:
            print("send_system_command not found in credentials file %s" % \
                  (hmccreds_location))
            sys.exit(1)

        loglevel = send_system_command.get("loglevel", None)
        if loglevel is not None:
            level = getattr(logging, loglevel.upper(), None)
            if level is None:
                print("Invalid value for loglevel in credentials file %s: %s" % \
                      (hmccreds_location, loglevel))
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
                  (hmc, hmccreds_location))
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

        print("Sending command %s for %s %s on CPC %s ..." %
              (command_to_send, partkind, partname, cpcname))

        if message_to_watch_for is not None:

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

        if message_to_watch_for is not None:
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
                            sys.stdout.flush()
                            if os_msg_id == message_to_watch_for:
                                self.message_out = msg_txt
                                raise NameError
            except KeyboardInterrupt:
                print("Keyboard interrupt - leaving receiver loop")
                sys.stdout.flush()
            except NameError:
                print("Message with ID %s occurred - leaving receiver loop" % message_to_watch_for)
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

class TimeoutException(Exception):
    """
    Raised when a command can't be sent in a given time

    """