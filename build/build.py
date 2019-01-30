"""Copies pacakge contents into build folder before invoking setup function
"""

import os
import shutil
import importlib
import subprocess
from pipreqs import pipreqs

BUILD_PATH, _ = os.path.split(os.path.abspath(__file__))
PACK_PATH, _ = os.path.split(BUILD_PATH)

def getBuildPack():
    """
    """
    _, packName = os.path.split(PACK_PATH)
    return BUILD_PATH + "/" + packName

def createFolder():
    """
    """
    print("Creating package build folder...")
    buildPack = getBuildPack()
    if os.path.isdir(buildPack):
        shutil.rmtree(buildPack)
    os.mkdir(buildPack)

def copyPackage():
    """
    """
    print("Copying package contents...")
    artifacts = [
        "tests/",
        "__init__.py",
        "classifiers.txt",
        "LICENSE",
        "README.rst",
        "requirements.txt"
    ]
    buildPack = getBuildPack()
    for artifact in artifacts:
        absPath = os.path.abspath(PACK_PATH + "/" + artifact)
        if os.path.isfile(absPath):
            shutil.copy(absPath, buildPack + "/" + artifact)
        elif os.path.isdir(absPath):
            shutil.copytree(absPath, buildPack + "/" + artifact)
        else:
            raise Exception("Package artifact '%s' does not exist" % artifact)

def runTests():
    """
    """
    print("Running package tests...")
    p = subprocess.Popen(["python", "setup.py", "test"], cwd=BUILD_PATH)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #p.communicate()

def runUpload():
    """
    """
    print("Uploading package...")
    p = subprocess.Popen(["python", "setup.py", "register", "sdist", "upload"], cwd=BUILD_PATH)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #p.communicate()

def updateRequirements():
    """Refreshes and loads the contents of requirements.txt
    """
    reqs = pipreqs.get_all_imports(PACK_PATH)
    lines = []
    for req in reqs:
        mod = importlib.import_module(req)
        ver = [int(v) for v in mod.__version__.split(".")]
        lines.append("%s >= %u.%u" % (req, ver[0], ver[1]))
    with open(PACK_PATH + "/requirements.txt", 'w') as f:
        f.write('\n'.join(lines))

def main():
    """
    """
    createFolder()
    copyPackage()
    updateRequirements()
    runTests()
    #runUpload()

if __name__ == "__main__":
    main()
