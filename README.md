# DePy
Depy is a python 3 script that help keep your server up to date as well as your git repositories through ssh connection

##### What do i need?

* Paramiko
* ArgParser
* prompt_toolkit

You can install everything with pip.

### Usage
When you launch for the first time, he will create a config file for you, you can set your password or a RSA keys

```python depy.py --update apt``` - Update your debian (or derivatives, like ubuntu)


```python depy.py --update pacman``` - Update your Arch Linux (or derivatives, like Manjaro)


```python depy.py --gitupdate my_repo ``` - Update a particular repository


```python depy.py --gitupdate all``` - Update all repositorys that he finds 


```python depy.py -h ``` - Show help


You can delete your config using

```python depy.py --new ```





##### TODO
- [ ] Deploy or shutdown your applications
- [ ] Custom commands
