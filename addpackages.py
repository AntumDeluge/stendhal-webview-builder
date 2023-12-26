#!/usr/bin/env python3

# Script to add packages to releases page
#
# License: MIT (see LICENSE.txt)

import codecs
import os
import platform
import shutil
import sys


dir_root = os.path.dirname(__file__)
os_win = platform.system().lower() == "windows"

def exitWithError(code, msg):
  sys.stderr.write(msg + "\n")
  sys.exit(code)

def normPath(path):
  if os_win:
    return path.replace("/", "\\")
  else:
    return path.replace("\\", "/")

def joinPaths(p1, p2, *p3):
  path = os.path.join(normPath(p1), normPath(p2))
  for p in p3:
    path = os.path.join(path, normPath(p))
  return path

def getOldPackages():
  if not os.path.isdir("dist"):
    return []
  packages = []
  for basename in os.listdir("dist"):
    if not basename.endswith(".apk"):
      continue
    packages.append(basename)
  return packages

def getNewPackages():
  if not os.path.isdir("build"):
    return []
  packages = []
  for basename in os.listdir("build"):
    if not basename.endswith(".apk"):
      continue
    packages.append(basename)
  return packages

def writePackageList(packages):
  # HTML page
  text_out = "<html>\
\n<head>\
\n<title>Stendhal Android Client</title>\
\n</head>\
\n\
\n<body>\
\n  Releases:\
\n  <ul>"

  for package in packages:
    text_out = text_out + "\n    <li><a href=\"dist/{0}\">{0}</a></li>".format(package)

  text_out = text_out + "\n  </ul>\
\n</body>\
\n</html>"

  fout = codecs.open("index.html", "w", "utf-8")
  fout.write(text_out.strip() + "\n")
  fout.close()


if __name__ == "__main__":
  os.chdir(dir_root)

  packages = getOldPackages()

  if not os.path.exists("dist"):
    os.makedirs("dist")

  print("New packages:")
  for package in getNewPackages():
    print("  {}".format(package))
    if package not in packages:
      packages.append(package)

    source = joinPaths("build", package)
    target = joinPaths("dist", package)
    if os.path.isfile(target):
      os.remove(target)
    shutil.copy(source, target)

  packages = list(reversed(sorted(packages)))
  writePackageList(packages)
