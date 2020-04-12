# Automatic build number generation
Automatic build version generation for the following languages `powershell`, `batch`, `python` and `c`.


Including the following information: 

* Git branch
* Git commit
* Build Date
* Build Time
* Major
* Minor
* Patch
* Build

The build can be auto incremented. 

## Usage
```
python versioning.py <FILE> <CODESTYLE> <AUTOINC>
```

* `File` = File Path to version file
* `CODESTYLE` = Build the version file inthe following code style:
  * `powershell`
  * `batch`
  * `python`
  * `DEFINEHEADER` header file for `c` / `c++`  
* `AUTOINC` = Increment the build version var. `True` or `False`

## Integrate

### PlatformIO

```
extra_scripts = 
    pre:versioning.py
build_flags = 
    -D VERSIONING_FILE=include/version.h
    -D VERSIONING_INC=True
```
