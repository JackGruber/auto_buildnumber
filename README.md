# Automatic build number generation

Automatic build version generation for the following languages `powershell`, `batch`, `python` and `c`.

Including the following information:

- Git branch
- Git commit
- Build Date
- Build Time
- Major
- Minor
- Patch
- Build

The `build` can be auto incremented. The `major`, `minor` and `patch` can be edited by hand in the created file.
With every call the file is loaded and the values are adjusted. All additionally added lines remain in the file.

Example file:

```header
#define VERSION_MAJOR "0"
#define VERSION_MINOR "1"
#define VERSION_PATCH "1"
#define VERSION_BUILD "1"
#define BUILD_BRANCH "master"
#define BUILD_COMMIT "684ee5f"
#define BUILD_DATE "2020-04-13"
#define BUILD_TIME "12:41"
```

## Usage

```cli
python versioning.py <FILE> <CODESTYLE> <AUTOINC> <BUILDFILE>
```

- `File` = File Path to version file
- `CODESTYLE` = Build the version file inthe following code style:
  - `powershell`
  - `batch`
  - `python`
  - `DEFINEHEADER` header file for `c` / `c++`
- `AUTOINC` = Increment the build version var. `True` or `False`
- `BUILDFILE` = (Optional) To save the `BUILD_*` var in a seperated file

## Integration

### PlatformIO

Modify the line `23` in `platformio_versioning.py` to your needs.
Optional Edit the the path to your `versioning.py` file at line `6`.

```ini
extra_scripts =
    pre:platformio_versioning.py
```
