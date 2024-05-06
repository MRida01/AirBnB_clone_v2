#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from the contents of the web_static folder."""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    if not os.path.exists("versions"):
        os.makedirs("versions")

    now = datetime.now()

    archive_name = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"

    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    if result.failed:
        return None
    else:
        return "versions/{}".format(archive_name)
