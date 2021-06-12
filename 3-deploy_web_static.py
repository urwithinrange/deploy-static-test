#!/usr/bin/python3
"""This module generates a .tgz file from web_static"""
from fabric.api import local, put, run, env
from datetime import datetime
import os.path

env.hosts = ['3.84.180.190', '54.82.73.173']

def deploy():
    """DEPLOY THE STUFF"""
    archive = do_pack()

    if archive is None:
        return False

    status = do_deploy(archive)

    return status

def do_deploy(archive_path):
    """Deploys the archive"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path[9:]
        archive_name_no_extension = archive_name[:-4]

        put(archive_path, '/tmp/' + archive_name)
        run('mkdir -p /data/web_static/releases/' + archive_name_no_extension)
        run('tar -xzvf /tmp/' + archive_name + ' -C ' + '/data/web_static/releases/' + archive_name_no_extension + ' --strip-components=1')
        run('rm -rf /tmp/' + archive_name)
        run('rm -rf /data/web_static/current')
        run('sudo ln -sf /data/web_static/releases/' + archive_name_no_extension + ' /data/web_static/current')

        return True

    except:
        return False

def do_pack():
    """This function packs up all files from web_static"""
    try:
        now = datetime.now()

        tar_archive_name = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"
        tar_archive_path = "versions/" + tar_archive_name

        local("mkdir -p versions")

        local("tar -czvf " + tar_archive_path + " web_static")

        return tar_archive_path

    except:
        return None
