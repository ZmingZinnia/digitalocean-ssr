# coding: utf8

import logging
import paramiko

ssh = paramiko.SSHClient()


def ssh_connect(host, user, key):
    while True:
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=user, key_filename=key)
        except Exception as e:
            logging.error('Connection Failed')
            logging.error(e)
        else:
            break

def ssh_command(cmd, output=False):
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command(cmd)
    if output:
        logging.info(stdout.read())
    if stderr:
        logging.info(stderr.read())
