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
  if not os.path.isfile("main.js"):
    return

  fin = codecs.open("main.js", "r", "utf-8")
  lines_in = fin.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
  fin.close()

  lines_out = []
  in_package_list = False
  insert_index = 0

  for idx in range(len(lines_in)):
    li = lines_in[idx]
    if li == "];":
      in_package_list = False
    if in_package_list:
      continue
    if li == "const releases = [":
      in_package_list = True
      insert_index = idx
    lines_out.append(li)

  pcount = len(packages)
  for idx in range(pcount):
    package = packages[idx]
    insert_index += 1
    li = "\t\"{}\"".format(package[17:package.index(".apk")])
    if idx < pcount - 1:
      li += ","
    lines_out.insert(insert_index, li)

  fout = codecs.open("main.js", "w", "utf-8")
  fout.write("\n".join(lines_out))
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
