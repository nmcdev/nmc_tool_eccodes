# 调用ECMWF eccodes命令工具操作grib格式数据
Call ECMWF eccodes tools to manipulate .grib format file with Python.

Only Python 3 is supported.

## Dependencies

需要安装eccodes程序库, 以Windows 7 64bit环境为例:

* 安装Windows下的类Linux系统[Cygwin](https://www.cygwin.com/), 安装时保证选择gcc, gfortran等开发套件, cmake, openjpeg, netcdf, jasper, png等程序库也被选择安装.
* 下载[eccdoes](https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home)源代码放入一个新建文件夹(如eccdoes). 进入文件夹, 执行以下命令进行编译:
```
  tar -xzf  eccodes-x.y.z-Source.tar.gz
  make build
  cd build
  cmake  ../eccodes-x.y.z-Source  -DCMAKE_INSTALL_PREFIX=/usr/local/eccodes
         -DBUILD_SHARED_LIBS=OFF -DENABLE_JPG=ON -DENABLE_NETCDF=ON
         -DDISABLE_OS_CHECK=ON -DENABLE_FORTRAN=ON -DENABLE_PNG=ON
         -DENABLE_PYTHON=OFF
  make
  make install
```
* 设置环境变量
```
1. 将Cygwin的bin目录放入环境Path路径.
2. 设置GRIB_HOME为eccodes的程序目录, 如 GRIB_HOME="C:\cygwin\usr\local\eccodes"

如果要使用netcdf-java转化grib文件为Netcdf格式, 需要:
1. 按照java程序库;
2. 下载[netcdf-java程序包](https://www.unidata.ucar.edu/software/thredds/current/netcdf-java/)
3. 设置环境变量 NETCDF_JAVA="netdfAll-<version>.jar"
```

## 安装程序库
```
  pip install git+git://github.com/nmcdev/nmc_tool_eccodes.git
```