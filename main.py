# coding: utf8

import time
import random
import string
import logging

from log import init_log
from ssh_client import ssh_connect, ssh_command
from lib import digitalocean
from config import config, load_config


def init_ssh_key():
    ssh_key = digitalocean.SSHKey()
    ssh_key.token = config.token
    try:
        ssh_key.load_by_pub_key(config.public_key)
    except Exception:
        logging.info('Create a new public key.')
        ssh_key = digitalocean.SSHKey(name='boot_ssh_key', public_key=config.public_key)
        ssh_key.token = config.token
        ssh_key.create()
    else:
        logging.info('The public key was loaded successfully.')
    finally:
        return ssh_key

def init_tag():
    try:
        tag = digitalocean.Tag.get_object(config.token, config.default_tag_name)
    except Exception:
        logging.info('Create a new tag.')
        parameters = {
            'name': config.default_tag_name,
            'token': config.token
        }
        tag = digitalocean.Tag(**parameters)
        tag.create()
    else:
        logging.info('The tag was loaded successfully.')
    finally:
        return tag


def destroy_all_droplet():
    manager = digitalocean.Manager(token=config.token)
    droplets = manager.get_all_droplets(tag_name=config.default_tag_name)
    if config.destroy_all_droplet:
        for droplet in droplets:
            droplet.destroy()


def create_new_droplet(ssh_key):
    parameters = {
        'name': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)),
        'region': config.region,
        'ssh_keys': [ssh_key],
        'size_slug': config.size_slug,
        'image': config.image,
        'backups': config.backups,
        'ipv6': config.ipv6,
        'user_data': config.user_data,
        'private_networking': config.private_networking,
        'volumes': config.volumes,
        'monitoring': config.monitoring,
        'token': config.token
    }
    droplet = digitalocean.Droplet(**parameters)
    droplet.create()
    logging.info('The new droplet was created successfully.')
    return droplet

def get_machine_ip():
    manager = digitalocean.Manager(token=config.token)
    while True:
        machine = manager.get_all_droplets(tag_name=config.default_tag_name)[0]
        if not machine.ip_address:
            time.sleep(3)
        else:
            logging.info('machine ip: %s' % machine.ip_address)
            return machine.ip_address


def main():
    init_log()

    # load config from settings.py
    load_config()

    # init ssh_key and tag object
    ssh_key = init_ssh_key()
    tag = init_tag()

    # destroy all droplet if necessary
    destroy_all_droplet()

    # make sure all robot's droplet are destroyed
    time.sleep(3)
    manager = digitalocean.Manager(token=config.token)
    assert len(manager.get_all_droplets(tag_name=config.default_tag_name)) == 0

    # create a new droplet
    droplet = create_new_droplet(ssh_key)

    # add the default tag to the droplet
    tag.add_droplets(droplet)

    # get the necessary information to access machine
    ip = get_machine_ip()

    # execute commands on the remote host
    ssh_connect(ip, 'root', config.public_key_file_path)
    logging.info('update system.....   it takes some time')
    ssh_command('yum install wget git -y')
    ssh_command('wget https://raw.githubusercontent.com/zMingGit/general/master/tcp_nanqinlang-1.3.2.sh')
    ssh_command('chmod u+x tcp_nanqinlang-1.3.2.sh')
    ssh_command('./tcp_nanqinlang-1.3.2.sh install')
    ssh_command('reboot')
    ssh_connect(ip, 'root', config.public_key_file_path)
    logging.info('install tcp TCP congestion algorithm.....  it takes some time')
    ssh_command('./tcp_nanqinlang-1.3.2.sh start')

    logging.info('install SSR...')
    ssh_command('yum install -y epel-release')
    ssh_command('yum install -y libsodium')
    ssh_command('git clone https://github.com/shadowsocksrr/shadowsocksr.git')
    ssh_command("echo '%s' > shadowsocksr/config.json" % config.ssr_config)
    ssh_command('python shadowsocksr/shadowsocks/server.py -c shadowsocksr/config.json -d start')
    logging.info('successfully installed')



if __name__ == '__main__':
    main()
