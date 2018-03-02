#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: alidns/alidns.py 
@time: 05/02/186 12:02
"""

import os
import sys
import click

from core import DNS

if os.path.exists(os.path.join(os.path.abspath('.'), 'config.py')):
    from config import AccessKeyId as aliid, AccessKeySecret as alikey
    print(alikey)
elif os.path.exists(os.path.join(os.path.abspath('.'), 'config_same.py')):
    from config_same import AccessKeyId as aliid, AccessKeySecret as alikey
    print(alikey)
else:
    print('just run dns init ')
    sys.exit('0')

dns = DNS(aliid=aliid, alikey=alikey)


@click.group()
def cli():
    pass


@click.command(help='add new domain record')
@click.argument('domain')
@click.option('--types', '-t', default='A')
@click.option('-ip', default='127.0.0.1')
def add(domain, types, ip):
    add_cmd = dns.add_record(domain=domain, types=types, ip=ip)
    click.echo("add record. {}".format(add_cmd))


@click.command(help='update domain record')
@click.argument('domain')
@click.option('--types', '-t', default='A')
@click.option('-ip', default='127.0.0.1')
def update(domain, types, ip):
    up_cmd = dns.update_record(domain, types, ip)
    click.echo('update domain record {}'.format(up_cmd))


@click.command(help='delete domain record')
@click.argument('domain')
def delete(domain):
    del_cmd = dns.del_record(domain=domain)
    click.echo('delete recird: {}'.format(del_cmd))


@click.command(help='show domain record')
@click.argument('domain')
def show(domain):
    ckd_two = dns.check_rr(domain=domain)
    click.echo('show domain info{}'.format(ckd_two))


@click.command(help='init domain')
@click.option('--aliid')
@click.option('--alikey')
def init(aliid, alikey):
    with open('config_same.py', 'w') as f:
        f.write('AccessKeyId = "{}"\n'.format(aliid))
        f.write('AccessKeySecret = "{}"\n'.format(alikey))


cli.add_command(init)
cli.add_command(add)
cli.add_command(update)
cli.add_command(delete)
cli.add_command(show)


if __name__ == '__main__':
    cli()
