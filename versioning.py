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
        pipe = subprocess.Popen("git rev-parse --short HEAD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        res = pipe.communicate()    
        return res[0].replace('\n', '').replace('\r', '')
    except Exception as e:
        return ""
    
def GetGitBranch():
    try:
        pipe = subprocess.Popen("git rev-parse --abbrev-ref HEAD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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
        print( "ExtractFromVarDefinition: split ERROR" )
    
    if remove == True:        
        var = var[1:len(var)-1]

    return(var)
    
def ExtractFromDefineHeader(line, var_name):
    var = ""
    try:
        split = line.split(var_name)
        var = split[1].strip()
    except:
        print( "ExtractFromDefineHeader: split ERROR" )
        
    return(var)
        
def GetDefineHeaderLine(var_name, var):
    return "#define " + var_name + " " + var

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

def WriteVersionFile(file, style, branch, commit, date, time, major, minor, patch, build):
    content = []
    if os.path.isfile(file):
        print("Version file exist")
        with open(file) as f:
            org_content = f.read().splitlines()
            
        for line in org_content:
            if "VERSION_BRANCH" in line:
                content.append(GetVersionLine(style, "VERSION_BRANCH", branch))
            elif "VERSION_COMMIT" in line:
                content.append(GetVersionLine(style, "VERSION_COMMIT", commit))
            elif "VERSION_MAJOR" in line:
                content.append(GetVersionLine(style, "VERSION_MAJOR", str(major)))
            elif "VERSION_MINOR" in line:
                content.append(GetVersionLine(style, "VERSION_MINOR", str(minor)))
            elif "VERSION_PATCH" in line:
                content.append(GetVersionLine(style, "VERSION_PATCH", str(patch)))
            elif "VERSION_BUILD" in line:
                content.append(GetVersionLine(style, "VERSION_BUILD", str(build)))
            elif "BUILD_DATE" in line:
                content.append(GetVersionLine(style, "BUILD_DATE", str(date)))
            elif "BUILD_TIME" in line:
                content.append(GetVersionLine(style, "BUILD_TIME", str(time)))
            else:
                content.append(line)
        
    else:   
        print("No version file exist")
        content.append(GetVersionLine(style, "VERSION_BRANCH", branch))
        content.append(GetVersionLine(style, "VERSION_COMMIT", commit))
        content.append(GetVersionLine(style, "VERSION_MAJOR", str(major)))
        content.append(GetVersionLine(style, "VERSION_MINOR", str(minor)))
        content.append(GetVersionLine(style, "VERSION_PATCH", str(patch)))
        content.append(GetVersionLine(style, "VERSION_BUILD", str(build)))
        content.append(GetVersionLine(style, "BUILD_DATE", date))
        content.append(GetVersionLine(style, "BUILD_TIME", time))
    
    print("VERSION_BRANCH:" + branch)
    print("VERSION_COMMIT:" + commit)
    print("VERSION_MAJOR:" + str(major))
    print("VERSION_MINOR:" + str(minor))
    print("VERSION_PATCH:" + str(patch))
    print("VERSION_BUILD:" + str(build))
    print("BUILD_DATE:" + date)
    print("BUILD_TIME:" + time)
    
    with open(file, 'w') as f:
        for line in content:
            f.write("%s\n" % line)
    
def UpdateVersionFile(file,style,inc_build):
    commit = GetGitCommit()
    branch = GetGitBranch()
    date = GetBuilDate()
    time = GetBuilTime()
    major, minor, patch, build = GetVersionFromFile(file, style, inc_build)
 
    WriteVersionFile(file, style, branch, commit, date, time, major, minor, patch, build)


# PlatformIO
try:
    Import("env")
    my_flags = env.ParseFlags(env['BUILD_FLAGS'])
    defines = {k: v for (k, v) in my_flags.get("CPPDEFINES")}
    print(defines)
    platformio = True
except:
    platformio = False


if platformio == True:
    FILE=defines.get("VERSIONING_FILE")
    AUTOINC=defines.get("VERSIONING_INC")
    CODESTYLE="DEFINEHEADER"
elif len(sys.argv) != 4:
    print("Usage: " + sys.argv[0] + " <VERSIONFILE> <STYLE> <INC BUILD>")
    print("STYLE = BATCH | POWERSHELL | DEFINEHEADER")
    print("INC BUILD = True | False")
    print("")
    sys.exit()
else:
    FILE=sys.argv[1]
    CODESTYLE=sys.argv[2]
    AUTOINC=sys.argv[3]

if "true" in AUTOINC.lower():
    UpdateVersionFile(FILE, CODESTYLE, True)
else:
    UpdateVersionFile(FILE, CODESTYLE, False)