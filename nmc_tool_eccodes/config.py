# _*_ coding: utf-8 _*_

# Copyright (c) 2019 NMC Developers.
# Distributed under the terms of the GPL V3 License.

"""
Set environment variables for eccodes tools.
"""

import os
import subprocess

# get environment variables
grib_env = os.environ.copy()

# construct grib home path
grib_env['PATH'] = os.path.join(grib_env['GRIB_HOME'], 'bin')
grib_home = grib_env['GRIB_HOME'].replace('\\', '/').replace(':', '')
grib_home = "/cygdrive/" + grib_home
grib_env['GRIB_DEFINITION_PATH'] = grib_home + "/share/eccodes/definitions"


def grib_run(commands):
    """
    Run grib_api tools commands, and return results.
    :param commands: grib_api tools commands
    :return: out string, and error information.
    """

    process = subprocess.Popen(commands, env=grib_env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    return out.decode('GBK'), err


if __name__ == "__main__":
    out_info, err_info = grib_run('grib_ls')
    print(out_info)
