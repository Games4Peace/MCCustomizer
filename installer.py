import sys
import os
import json
import re
from shutil import copyfile
import argparse

print("version 1.3")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument(
    'minecraftPath', nargs='?', default=os.path.join(os.environ['APPDATA'], '.minecraft'),
    help='the path to the .minecraft folder')
parser.parse_args()

args = parser.parse_args()

local_path = ''
if hasattr(sys, 'frozen'):
    local_path = sys._MEIPASS
else:
    local_path =  os.path.dirname(__file__)
local_path = os.path.join(local_path, 'data')

print('.')
installer_settings_filepath = os.path.join(local_path, 'settings.json')
installer_settings = {}
try:
    with open(installer_settings_filepath, 'r') as f:
        installer_settings=json.loads(f.read())
except Exception as e:
    input('(Error 4)Error in installer. Try:\n' +
        '\t1. Rerunning this script as administrator\n' +
        '\t2. Contacting a Games4Peace tech-person with this msg:\n\n' + str(e))
    exit()

print('..')
minecraft_filepath = args.minecraftPath
if(args.verbose):
    print("Using minecraft path: " + minecraft_filepath)
launcher_profiles_filepath = os.path.join(minecraft_filepath, 'launcher_profiles.json')
options_filepath = os.path.join(minecraft_filepath, 'options.txt')

launcher_profiles_content = ''
options_content = ''
try:
    with open(launcher_profiles_filepath, 'r') as f:
        launcher_profiles_content=json.loads(f.read())
except Exception as e:
    if(args.verbose):
        print("Couldn't find profiles file, creating from default")
    launcher_profiles_content={}

try:
    with open(options_filepath, 'r') as f:
        options_content=f.read()
except Exception as e:
    if(args.verbose):
        print("Couldn't find options file, creating from default")
    options_content="lang:he_il"

print('...')
try:
    ### Setting Launcher Configs
    launcher_settings = installer_settings['launcher']
    # Set the launcher language
    launcher_profiles_content['settings'] = {
        'locale': launcher_settings['setting_lang'],
        'showMenu': False
    }
    # Setting the launcher profile
    launcher_profiles_content['profiles'] = {
        'd85fae5bc5e1604a2ad85af55cd5055f': {
            'name': launcher_settings['profile_name'],
            'type': 'custom',
            'created': '2018-09-09T08:02:26.039Z',
            'lastUsed': '2018-09-09T08:03:47.758Z',
            'lastVersionId': launcher_settings['profile_version']
        }
    }

    ### Setting game configs
    # Setting the game language
    options_content = re.sub(
            'lang:.*',
            'lang:' + installer_settings['options']['lang'],
            options_content
        )
except Exception as e:
    input('(Error 5)Error in minecraft installation settings file. Try:\n' +
        '\t1. Contacting a Games4Peace tech-person with this msg:\n\n' + str(e))
    exit()

print('....')
try:
    with open(launcher_profiles_filepath, 'w') as f:
        f.write(json.dumps(launcher_profiles_content))
    with open(options_filepath, 'w') as f:
        f.write(options_content)
except Exception as e:
    input('(Error 2)Error editing minecraft files. Try:\n' +
        '\t1. Making sure that minecraft is closed\n' +
        '\t2. Rerunning this script as administrator\n' +
        '\t3. Contacting a Games4Peace tech-person with this msg:\n\n' + str(e))
    exit()

print('.....')
servers_filename = 'servers.dat'
g4p_servers_filepath = os.path.join(local_path, servers_filename)
minecraft_servers_file_path = os.path.join(minecraft_filepath, servers_filename)

try:
    copyfile(g4p_servers_filepath, minecraft_servers_file_path)
except Exception as e:
    input('(Error 3)Error editing minecraft files. Try:\n' +
        '\t1. Making sure that minecraft is closed\n' +
        '\t2. Rerunning this script as administrator\n' +
        '\t3. Contacting a Games4Peace tech-person with this msg:\n\n' + str(e))
    exit()

raw_input('Finished installation.\nPlease run launcher, than press "Play" to test the game is working.')
