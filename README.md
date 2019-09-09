# 调用ECMWF eccodes命令工具操作grib格式数据
Call ECMWF eccodes tools to manipulate .grib format file with Python.

Only Python 3 is supported.

## Dependencies

### 需要安装eccodes程序库(https://anaconda.org/conda-forge/eccodes)
```
conda install -c conda-forge eccodes
```

### 如果要使用netcdf-java转化grib文件为Netcdf格式, 需要:
```
1. 按照java程序库;
2. 下载[netcdf-java程序包](https://www.unidata.ucar.edu/software/thredds/current/netcdf-java/)
3. 设置环境变量 NETCDF_JAVA="netdfAll-<version>.jar"
```

## 安装程序库
```
  pip install git+git://github.com/nmcdev/nmc_tool_eccodes.git
```