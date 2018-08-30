token = "token"
public_key_file_path = "/Users/xx/.ssh/id_rsa.pub"

default_tag_name = 'ssr-boot'
destroy_all_droplet = True


## droplet parameters
region = 'nyc3'
size_slug = 's-1vcpu-1gb'
image = 'centos-7-x64'
# image = 'ubuntu-16-04-x64'
backups = False
ipv6 = True
user_data = None
private_networking = None
volumes = None
monitoring = False

## shadowsocksr config
ssr_config = """{
    "server":"0.0.0.0",
    "server_ipv6":"::",
    "local_address":"127.0.0.1",
    "local_port":1080,
    "port_password":{
        "7788":{"protocol":"auth_chain_a", "password":"xx", "obfs":"tls1.2_ticket_auth_compatible", "obfs_param":""},
        "7789":{"protocol":"auth_chain_a", "password":"xx", "obfs":"tls1.2_ticket_auth_compatible", "obfs_param":""},
    },
    "timeout":300,
    "method":"chacha20",
    "protocol": "auth_sha1_compatible",
    "protocol_param": "",
    "obfs": "http_simple_compatible",
    "obfs_param": "",
    "redirect": "",
    "dns_ipv6": false,
    "fast_open": false,
    "workers": 1
}"""
