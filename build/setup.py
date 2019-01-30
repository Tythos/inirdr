"""
"""

import os
import socket
import getpass
import docutils
from docutils import parsers, frontend, utils
import setuptools
import subprocess

BUILD_PATH, _ = os.path.split(os.path.abspath(__file__))
PACK_PATH, _ = os.path.split(BUILD_PATH)
_, PACK_NAME = os.path.split(PACK_PATH)

def getGitTag():
    """Returns the git tag of the latest commit (with a tag), using a system
       call to the repository in located in the module's parent folder.
    """
    p = subprocess.Popen(["git", "describe", "--tags"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=PACK_PATH)
    stdout, _ = p.communicate()
    return stdout.strip().decode("ascii")
    
def getReqs():
    """
    """
    with open(PACK_PATH + "/requirements.txt", 'r') as f:
        return f.readlines()

def getEmail():
    """
    """
    user = getpass.getuser()
    fqdn = socket.getfqdn().split(".")
    return "%s@%s.%s" % (user, fqdn[-2], fqdn[-1])

def getDescriptions():
    """
    """
    with open(PACK_PATH + "/README.rst", 'r') as f:
        readme = f.read()
    Psr = parsers.get_parser_class("rst")
    cfg = frontend.OptionParser(components=(Psr,)).get_default_values()
    doc = utils.new_document("new_document", cfg)
    psr = Psr()
    psr.parse(readme, doc)
    firstLine = doc.children[0].children[1].children[0]
    return firstLine.astext(), readme

def getRepo():
    """
    """
    p = subprocess.Popen(["git", "config", "--get", "remote.origin.url"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=PACK_PATH)
    stdout, _ = p.communicate()
    return stdout.strip().decode("ascii")

def getClassifiers():
    """
    """
    with open(PACK_PATH + "/classifiers.txt", 'r') as f:
        return f.readlines()

def main():
    """
    """
    descs = getDescriptions()
    setuptools.setup(
        name=PACK_NAME,
        version=getGitTag(),
        packages=setuptools.find_packages(),
        install_requires=getReqs(),
        author=getpass.getuser(),
        author_email=getEmail(),
        description=descs[0],
        long_description=descs[1],
        license_file=PACK_PATH + "/LICENSE",
        url=getRepo(),
        test_suite=PACK_NAME + ".tests",
        classifiers=getClassifiers()
    )

if __name__ == "__main__":
    main()
