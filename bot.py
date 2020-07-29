import platform
import os
import re
import slickrpc
import shutil
import time
import threading
import math
import requests


def def_credentials(chain, mode="usual"):
    rpcport = ''
    ac_dir = ''
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Win64' or operating_system == 'Windows':
        ac_dir = '%s/komodo/' % os.environ['APPDATA']
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    if len(rpcport) == 0:
        if chain == 'KMD':
            rpcport = 7771
        else:
            print("rpcport not in conf file, exiting")
            print("check "+coin_config_file)
            exit(1)
    return slickrpc.Proxy("http://%s:%s@127.0.0.1:%d" % (rpcuser, rpcpassword, int(rpcport)))


marmara_proxy = def_credentials("MCL")

mlad_info = marmara_proxy.marmaralistactivatedaddresses()

total_amount = 0

for address in mlad_info["WalletActivatedAddresses"]:
    total_amount += address["amount"]

bot_api_key = "1150319447:AAGy-ygw0ra6XmlsQhTaV1j6nt_rJqtuiMY"
chat_id="-1001395970865"

not_locked_balance_string = "Not locked balance: " + str(marmara_proxy.getbalance())
locked_balance_string = "Marmaralocked balance: " + str(total_amount)
text = "Staking node:\n" + not_locked_balance_string + "\n" + locked_balance_string
mcl_info = marmara_proxy.getinfo()
if mcl_info["blocks"] != mcl_info["longestchain"]:
    text += "\nDaemon stuck. Please check!"
else:
    text += "\nDaemon on latest chain"

message_url = "https://api.telegram.org/bot"  + bot_api_key + "/sendMessage?chat_id=" + chat_id + "&text=" + text
r = requests.get(url = message_url)
