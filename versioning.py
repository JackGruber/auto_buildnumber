import datetime
import subprocess
import os.path
import sys


def GetBuilDate():
    now = datetime.datetime.today()
    return now.strftime("%Y-%m-%d")


def GetBuilTime():
    now = datetime.datetime.today()
    return now.strftime("%H:%M")


def GetGitCommit():
    try:
        pipe = subprocess.Popen("git rev-parse --short HEAD", shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        res = pipe.communicate()
        return res[0].replace('\n', '').replace('\r', '')
    except Exception as e:
        return ""


def GetGitBranch():
    try:
        pipe = subprocess.Popen("git rev-parse --abbrev-ref HEAD", shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        res = pipe.communicate()
        return res[0].replace('\n', '').replace('\r', '')
    except Exception as e:
        return ""


def GetVersionFromFile(file, style, inc_build):
    major = 0
    minor = 0
    patch = 0
    build = 0

    try:
        with open(file) as f:
            content = f.read().splitlines()
    except:
        major = 0
        minor = 0
        patch = 1
        build = 1
    else:
        for line in content:
            if "VERSION_MAJOR" in line:
                major = ExtractVar(line, style, "VERSION_MAJOR")
            elif "VERSION_MINOR" in line:
                minor = ExtractVar(line, style, "VERSION_MINOR")
            elif "VERSION_PATCH" in line:
                patch = ExtractVar(line, style, "VERSION_PATCH")
            elif "VERSION_BUILD" in line:
                build = ExtractVar(line, style, "VERSION_BUILD")

        if inc_build == True:
            build = int(build) + 1

    return major, minor, patch, build


def ExtractVar(line, style, var_name):
    var = ""
    if style.upper() == "DEFINEHEADER":
        var = ExtractFromDefineHeader(line, var_name)
    elif style.upper() == "POWERSHELL":
        var = ExtractFromVarDefinition(line, var_name, True)
    elif style.upper() == "BATCH":
        var = ExtractFromVarDefinition(line, var_name, False)
    elif style.upper() == "PYTHON":
        var = ExtractFromVarDefinition(line, var_name, True)

    return var.strip()


def ExtractFromVarDefinition(line, var_name, remove):
    var = ""
    try:
        if var_name + " =" in line:
            split = line.split(var_name + " =")
        else:
            split = line.split(var_name + "=")

        var = split[1].strip()
    except:
        print("ExtractFromVarDefinition: split ERROR")

    if remove == True:
        var = var[1:len(var)-1]

    return(var)


def ExtractFromDefineHeader(line, var_name):
    var = ""
    try:
        split = line.split(var_name)
        var = split[1].strip()
        var = var[1:len(var)-1]
    except:
        print("ExtractFromDefineHeader: split ERROR")

    return(var)


def GetDefineHeaderLine(var_name, var):
    return '#define ' + var_name + ' "' + var + '"'


def GetPowershellLine(var_name, var):
    return "$GLOBAL:" + var_name + " = '" + var + "'"


def GetBatchLine(var_name, var):
    return "set " + var_name + "=" + var


def GetPythonLine(var_name, var):
    return var_name + " = '" + var + "'"


def GetVersionLine(style, var_name, var):
    if style.upper() == "DEFINEHEADER":
        return GetDefineHeaderLine(var_name, var)
    elif style.upper() == "POWERSHELL":
        return GetPowershellLine(var_name, var)
    elif style.upper() == "BATCH":
        return GetBatchLine(var_name, var)
    elif style.upper() == "PYTHON":
        return GetPythonLine(var_name, var)
    else:
        return ""


def WriteVersionFile(file, style, major, minor, patch, build):
    content = []

    insert_major = False
    insert_minor = False
    insert_patch = False
    insert_build = False

    if os.path.isfile(file):
        print("Version file exist")
        with open(file) as f:
            org_content = f.read().splitlines()

        for line in org_content:
            if "VERSION_MAJOR" in line:
                content.append(GetVersionLine(
                    style, "VERSION_MAJOR", str(major)))
                insert_major = True
            elif "VERSION_MINOR" in line:
                content.append(GetVersionLine(
                    style, "VERSION_MINOR", str(minor)))
                insert_minor = True
            elif "VERSION_PATCH" in line:
                content.append(GetVersionLine(
                    style, "VERSION_PATCH", str(patch)))
                insert_patch = True
            elif "VERSION_BUILD" in line:
                content.append(GetVersionLine(
                    style, "VERSION_BUILD", str(build)))
                insert_build = True
            else:
                content.append(line)

    if insert_major == False:
        content.append(GetVersionLine(style, "VERSION_MAJOR", str(major)))
    if insert_minor == False:
        content.append(GetVersionLine(style, "VERSION_MINOR", str(minor)))
    if insert_patch == False:
        content.append(GetVersionLine(style, "VERSION_PATCH", str(patch)))
    if insert_build == False:
        content.append(GetVersionLine(style, "VERSION_BUILD", str(build)))

    with open(file, 'w') as f:
        for line in content:
            f.write("%s\n" % line)


def WriteBuildFile(file, style, branch, commit, date, time):
    content = []

    insert_branch = False
    insert_commit = False
    insert_date = False
    insert_time = False

    if os.path.isfile(file):
        print("Dynamic version file exist")
        with open(file) as f:
            org_content = f.read().splitlines()

        for line in org_content:
            if "BUILD_BRANCH" in line:
                content.append(GetVersionLine(style, "BUILD_BRANCH", branch))
                insert_branch = True
            elif "BUILD_COMMIT" in line:
                content.append(GetVersionLine(style, "BUILD_COMMIT", commit))
                insert_commit = True
            elif "BUILD_DATE" in line:
                content.append(GetVersionLine(style, "BUILD_DATE", str(date)))
                insert_date = True
            elif "BUILD_TIME" in line:
                content.append(GetVersionLine(style, "BUILD_TIME", str(time)))
                insert_time = True
            else:
                content.append(line)

    if insert_branch == False:
        content.append(GetVersionLine(style, "BUILD_BRANCH", branch))
    if insert_commit == False:
        content.append(GetVersionLine(style, "BUILD_COMMIT", commit))
    if insert_date == False:
        content.append(GetVersionLine(style, "BUILD_DATE", str(date)))
    if insert_time == False:
        content.append(GetVersionLine(style, "BUILD_TIME", str(time)))

    with open(file, 'w') as f:
        for line in content:
            f.write("%s\n" % line)


def UpdateVersionFile(file, style, inc_build, build_file=""):
    if type(inc_build) == str:
        if "true" in inc_build.lower():
            inc = True
        else:
            inc = False
    else:
        inc = inc_build

    if build_file == "":
        build_file = file

    commit = GetGitCommit()
    branch = GetGitBranch()
    date = GetBuilDate()
    time = GetBuilTime()
    major, minor, patch, build = GetVersionFromFile(file, style, inc)

    print("VERSION_MAJOR:" + str(major))
    print("VERSION_MINOR:" + str(minor))
    print("VERSION_PATCH:" + str(patch))
    print("VERSION_BUILD:" + str(build))
    print("BUILD_BRANCH:" + branch)
    print("BUILD_COMMIT:" + commit)
    print("BUILD_DATE:" + date)
    print("BUILD_TIME:" + time)

    WriteVersionFile(file, style, major, minor, patch, build)
    WriteBuildFile(build_file, style, branch, commit, date, time)


# executed as script
if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: " + sys.argv[0] +
              " <VERSIONFILE> <STYLE> <INC BUILD> <BUILDFILE>")
        print("STYLE = BATCH | POWERSHELL | DEFINEHEADER")
        print("INC BUILD = True | False")
        print("BUILDFILE = Filepath for file with BUILD_* informations (optional)")
        print("")
        sys.exit()
    else:
        FILE = sys.argv[1]
        CODESTYLE = sys.argv[2]
        AUTOINC = sys.argv[3]
        if len(sys.argv) == 5:
            UpdateVersionFile(FILE, CODESTYLE, AUTOINC, sys.argv[4])
        else:
            UpdateVersionFile(FILE, CODESTYLE, AUTOINC)
