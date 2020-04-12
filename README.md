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

The `build` can be auto incremented. The `major`, `minor` and `patch` can be edited by hand in the created file. 
With every call the file is loaded and the values are adjusted. All additionally added lines remain in the file.

Example file:

```
#define VERSION_BRANCH master
#define VERSION_COMMIT 4d08e78
#define VERSION_MAJOR 1
#define VERSION_MINOR 5
#define VERSION_PATCH 2
#define VERSION_BUILD 12
#define BUILD_DATE 2020-04-12
#define BUILD_TIME 22:20
```

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

## Integration

### PlatformIO

```
extra_scripts = 
    pre:versioning.py
build_flags = 
    -D VERSIONING_FILE=include/version.h
    -D VERSIONING_INC=True
```
