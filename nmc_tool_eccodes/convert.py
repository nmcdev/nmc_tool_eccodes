# _*_ coding: utf-8 _*_

# Copyright (c) 2019 NMC Developers.
# Distributed under the terms of the GPL V3 License.

"""
Call eccodes grib tools to convert grib file to other format.
"""

import os
import pkg_resources
import pathlib
import subprocess


def grib_to_netcdf(filenames, out_dir=None, verbose=False, check_exist=True):
    """
    Convert grib files to netcdf format with "grib_to_netcdf" tool.

    :param filenames: grib file names.
    :param out_dir: set output directory.
    :param verbose: print convert information.
    :param check_exist: check output file is existing or not.
    :return: out filenames.

    :Example:
    >>> filenames = "D:/testworks/python/ecmf_pf_TP_2017093012.grib"
    >>> grib_to_netcdf(filenames,
                       out_dir="D:/testworks/python/nmc_tool_eccodes",
                       verbose=True)
    """

    # check list
    if type(filenames) is not list:
        filenames = [filenames]

    # loop each file to perform conversion
    out_files = []
    for i, file in enumerate(filenames):
        p = pathlib.PureWindowsPath(file)
        if out_dir is not None:
            out_file = pathlib.PureWindowsPath(out_dir, p.stem+".nc")
        else:
            out_file = pathlib.PureWindowsPath(p.parent, p.stem+".nc")
        if check_exist:
            if os.path.isfile(out_file):
                continue
        out_files.append(out_file)
        commands = ['grib_to_netcdf', '-o', str(out_file), str(file)]
        process = subprocess.Popen(
            commands, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if verbose:
            print(out.decode('GBK'))

    # return out filenames
    return out_files

def grib_to_netcdf_with_java(filenames, out_dir=None,
                             verbose=False, check_exist=True,
                             isLargeFile=False):
    """Convert Grib1/2 to Netcdf file with Netcdf-Java.
    Make sure the java.exe in the environment PATH, and netdfAll-<version>.jar in 
    the NETCDF_JAVA environment variable.

    https://www.unidata.ucar.edu/software/thredds/current/netcdf-java/reference/Cookbook.html#writeClasssic
    java -Xmx512m -classpath netdfAll-<version>.jar ucar.nc2.dataset.NetcdfDataset 
         -in<fileIn>  -out<fileOut>  [-isLargeFile]
    
    Arguments:
        filenames {list or string} -- grib file names.
    
    Keyword Arguments:
        out_dir {stirng} -- set output directory. (default: {None})
        verbose {bool} -- print convert information. (default: {False})
        check_exist {bool} -- check output file is existing or not. (default: {True})
        ifLargeFile {bool} -- support large file (>2GB). (default: {False})

    Return:
        out filenames.
    """

    # Netcdf-java jar file path
    jar_path = os.environ.get('NETCDF_JAVA')
    if not jar_path:
        print("The environment variable NETCDF_JAVA should be set. Return.")
        return None

    # check list
    if type(filenames) is not list:
        filenames = [filenames]

    # loop each file to perform conversion
    out_files = []
    for i, file in enumerate(filenames):
        p = pathlib.PureWindowsPath(file)
        if out_dir is not None:
            out_file = pathlib.PureWindowsPath(out_dir, p.stem+".nc")
        else:
            out_file = pathlib.PureWindowsPath(p.parent, p.stem+".nc")
        out_files.append(out_file)
        if check_exist:
            if os.path.isfile(out_file):
                continue
        commands = [
            'java', '-Xmx512m', '-classpath', jar_path,
            'ucar.nc2.dataset.NetcdfDataset',
            '-in', str(file),
            '-out', str(out_file)]
        if isLargeFile:
            commands.append('-isLargeFile')
        process = subprocess.Popen(
            commands, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if verbose:
            print(out.decode('GBK'))

    # return out filenames
    return out_files


def grib_extract_to_netcdf(filenames, short_name, level=None,
                           del_intermediate_file=False,
                           out_dir=None, verbose=False, check_exist=True):
    """
    Extract a variable from grib files with "grib_copy",
    and convert to netcdf file.

    :param filenames: grib file names.
    :param short_name: variable short name.
    :param level: vertical level, default is None.
    :param del_intermediate_file: delete the intermediate file generated
                                  by "grib_copy" tool.
    :param out_dir: specify the output directory.
    :param verbose: print the output information.
    :param check_exist: check the netcdf file existing or not.
    :return: None.
    """

    # check list
    if type(filenames) is not list:
        filenames = [filenames]

    # loop each file to perform conversion
    for file in filenames:
        p = pathlib.PureWindowsPath(file)
        if out_dir is not None:
            out_file1 = pathlib.PureWindowsPath(
                out_dir, p.stem + "_" + short_name + p.suffix)
            out_file2 = pathlib.PureWindowsPath(
                out_dir, out_file1.stem + ".nc")
        else:
            out_file1 = pathlib.PureWindowsPath(
                p.parent, p.stem + "_" + short_name + p.suffix)
            out_file2 = pathlib.PureWindowsPath(
                p.parent, out_file1.stem + ".nc")
        if check_exist:
            if os.path.isfile(out_file2):
                continue

        # extract the specified variable to intermediate file
        condition = 'shortName='+short_name
        if level is not None:
            condition = condition+',level='+str(level)
        command = ['grib_copy', '-w', condition, str(file), str(out_file1)]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if verbose:
            print(out.decode('GBK'))

        # convert netcdf file
        commands = ['grib_to_netcdf', '-o', str(out_file2), str(out_file1)]
        process = subprocess.Popen(
            commands, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if verbose:
            print(out.decode('GBK'))
        if del_intermediate_file:
            os.remove(out_file1)


def ecmf_ensemble_grib_split(filenames, out_dir=None, verbose=False):
    """
    Split ecmf ensemble grib data to
    [dataType]_[levelType]_[dataDate][dataTime]_[endStep] files
    with "grib_copy" tool.

    :param filenames: grib file names.
    :param out_dir: set output directory.
    :param verbose: print the output information.
    :return:
    """

    # check arguments
    if not isinstance(filenames, (list, tuple)):
        filenames = [filenames]

    # loop every file
    for file in filenames:
        if out_dir is None:
            outfile = os.path.join(
                os.path.dirname(file),
                '[dataType]_[levelType]_[dataDate][dataTime]_[endStep].grib')
        else:
            outfile = os.path.join(
                out_dir,
                '[dataType]_[levelType]_[dataDate][dataTime]_[endStep].grib')

        commands = [
            'grib_copy', '-B "level:l"',
            '"' + str(file) + '"', '"' + str(outfile) + '"']
        process = subprocess.Popen(
            commands, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if verbose:
            print(out.decode('GBK'))

    # return
    return None
