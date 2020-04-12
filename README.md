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
