#!/usr/bin/python3

"""
Generates a .tgz archive from AirBnB clone repo contents
using a function do_pac
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generate a .tgz file from airbnb
    """
    local("mkdir -p versions")

    archive_name = "web_static_{}.tgz".format(
            datetime.utcnow().strftime("%Y%m%d%H%M%S")
            )

    compression = local(
            "tar -cvzf versions/{} web_static".format(archive_name)
            )

    if compression.failed:
        return None
    else:
        return "versions/{}".format(archive_name)
