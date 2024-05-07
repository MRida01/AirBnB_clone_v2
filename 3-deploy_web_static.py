#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers."""

from fabric.api import local, put, run, env
from os.path import exists, isdir
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        if not isdir("versions"):
            local("mkdir -p versions")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_{}.tgz".format(timestamp)

        local("tar -cvzf {} web_static".format(filename))

        return filename
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")

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


def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
