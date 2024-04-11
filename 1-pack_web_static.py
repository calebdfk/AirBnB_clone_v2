#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    generates .tgz archive
    """
    time = datetime.now()
    archive = "web_static_" + time.strftime("%Y%m%d%H%M%S") + ".tgz"

    local('mkdir -p versions')
    create_archive = local('tar -cvzf versions/{} web_static'.format(archive))
    if create_archive is not None:
        return archive
    else:
        return None
