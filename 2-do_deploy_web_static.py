#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers."""

from fabric.api import run, put, env
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Distributes an archive to web servers."""

    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        archive_filename = archive_path.split('/')[-1]
        release_path = "/data/web_static/releases/{}".format(
            archive_filename.split('.')[0])
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))

        run("rm /tmp/{}".format(archive_filename))

        run("mv {}/web_static/* {}".format(release_path, release_path))

        run("rm -rf {}/web_static".format(release_path))

        current_link = "/data/web_static/current"
        run("rm -rf {}".format(current_link))

        run("ln -s {} {}".format(release_path, current_link))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
