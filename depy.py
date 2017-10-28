import paramiko
import argparse
import os
import configparser
from prompt_toolkit import prompt

class Deploy(object):
    ''' Deploy class '''
    def __init__(self, args): ### Read config file for values ;)
        config = configparser.ConfigParser()
        config.read('dpy.conf')
        self.host = config['Host_Info']['hostname']
        self.username = config['Host_Info']['username']
        self.key_path = config['Host_Info']['private_key']
        self.password = config['Host_Info']['password']
        self.ssh = paramiko.SSHClient()
        self.args = args

    def connect_and_launch(self, command,type):
        print("Launching %s to %s !" % (type, self.host))
        if not self.password:
            private_key = paramiko.RSAKey.from_private_key_file(self.key_path)
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.host, username=self.username, pkey=private_key)
        else:
            self.ssh.connect(hostname=self.host, username=self.username, password=self.password)
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)
	        ### Looping in EOF data ###
        for output in iter(ssh_stdout.readline, ""):
            print(output, end="")
        for errors in iter(ssh_stderr.readline, ""):
        	print(errors, end="")

        self.ssh.close()

    def actions(self):
        command = ''
        if self.args.list == 'dir':
            command = 'ls -lah'
            self.connect_and_launch(command,'list')
        if self.args.list == 'git':
        	command = 'for dir in `ls -d */`; do cd $dir; if [ -e .git ]; then echo "Found repository " $dir; fi; cd ..; done'
        	self.connect_and_launch(command,'list git')
        if self.args.update == 'apt':
            command = 'sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y autoremove'
            self.connect_and_launch(command,'system updates')
        elif self.args.update == 'pacman':
            command = 'sudo pacman -Syyyu --noconfirm'
            self.connect_and_launch(command,'system updates')
        if self.args.gitupdate == 'all':
            username = prompt('Git usename: ')
            password = prompt('Git password: ', is_password=True)
            command = 'for dir in `ls -d */`; do cd $dir; if [ -e .git ];then echo -ne "machine github.com\nlogin {0}\npassword {1}\n" > ~/.netrc;echo "Found repository " $dir; git pull; fi; cd ..; rm ~/.netrc; done'.format(username, password)
            self.connect_and_launch(command,'upadint all git')
        elif self.args.gitupdate != 'all' and self.args.gitupdate != None:
            username = prompt('Git usename: ')
            password = prompt('Git password: ', is_password=True)
            repo_name = str(self.args.gitupdate)
            command = 'cd {}; echo -ne "machine github.com\nlogin {}\npassword {}\n" > ~/.netrc; git pull; rm ~/.netrc'.format(repo_name, username, password)
            self.connect_and_launch(command, 'Updating {}...'.format(repo_name))

######### ARGS FOR USE  #######
def setup_args():
    parser = argparse.ArgumentParser(description='Actions you can do in server')
    parser.add_argument('--list', type=str, help='List dir or repositories Example: --list git, --list dir')
    parser.add_argument('--update', type=str, help='Update ssh server Example: --update apt, --upate pacman')
    parser.add_argument('--gitupdate', type=str, help='Update a particular repo or all Example: --git-update all, --git-update <name>')
    parser.add_argument('--deploy', type=str, help='Deploy a application Example: --deploy <app_name>')
    parser.add_argument('--new',help='Create a new config file!',action='store_true')
    args = parser.parse_args()
    main(args)

######### Creating config file #########
def create_conf():
    config = configparser.ConfigParser()

    host = prompt('What is the hostname? > ')
    user = prompt('What is the username to connect? > ')
    password = prompt('What is the password?(if dont have, let in blank) > ', is_password=True)
    rsa_key = ""
    if not password:
        rsa_key = prompt('If have RSA keys insted password, enter the path > ')

    config['Host_Info'] = {
        'hostname' : host,
        'username' : user,
        'password' : password,
        'private_key' : rsa_key
    }
    with open('dpy.conf','w') as config_file:
        config.write(config_file)


def main(args):
    if args.new and os.path.exists('dpy.conf'):
        os.remove('dpy.conf')
    if not os.path.exists('dpy.conf'):
        choose = prompt('Looks you dont have a config file, wanna create now?(Y/n) > ')
        if choose in ['y','Y','yes','Yes','YES']:
            create_conf()
        elif choose in ['n','No','NO','no']:
            print('Goodbye')
            exit()
        else:
            main(args)
    client = Deploy(args)
    client.actions()

if __name__ == '__main__':
    setup_args()
