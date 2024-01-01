#!/usr/bin/env python3

# Script to build Android WebView client for Stendhal
#
# License: MIT (see LICENSE.txt)

import os
import platform
import shutil
import subprocess
import sys


dir_root = os.path.dirname(__file__)
os_win = platform.system().lower() == "windows"

def exitWithError(code, msg):
  sys.stderr.write(msg + "\n")
  sys.exit(code)

def checkExecutable(cmd, ext="exe"):
  # TODO: check that file exists
  return cmd if not os_win else (cmd + "." + ext).lstrip("./")

def normPath(path):
  if os_win:
    return path.replace("/", "\\")
  else:
    return path.replace("\\", "/")

def joinPath(p1, p2, *p3):
  path = os.path.join(normPath(p1), normPath(p2))
  for p in p3:
    path = os.path.join(path, normPath(p))
  return path

def execute(cmd, params):
  params = [cmd] + params
  try:
    res = subprocess.run(params, check=True)
  except subprocess.CalledProcessError as e:
    exitWithError(e.returncode, e.stderr or "Failed to execute \"{}\"".format(" ".join(params)))

def cloneSource(url, target, branch="master"):
  print("Cloning \"" + url + "\" to \"" + target + "\"")

  if not os.path.exists(target):
    os.makedirs(target)
  try:
    execute(checkExecutable("git"), ["clone", "--single-branch", "--branch={}".format(branch), "--depth=1", url, target])
  except KeyboardInterrupt:
    print("Cancelled")
    sys.exit(0)

def prepareStendhal():
  if not os.path.exists("android"):
    if not os.path.exists(normPath("stendhal/build.xml")):
      cloneSource("https://github.com/arianne/stendhal.git", "stendhal")
    shutil.copytree(normPath("stendhal/android"), "android")

def buildClient():
  os.chdir("android")
  execute(checkExecutable("./gradlew", "bat"), ["assembleDebug", "assembleRelease"])
  os.chdir(dir_root)
  for ROOT, DIRS, FILES in os.walk(normPath("build/build_android_client")):
    for basename in FILES:
      if not basename.endswith(".apk"):
        continue
      filepath = joinPath(ROOT, basename)
      target = basename
      if target.endswith("-release.apk"):
        target = target[:target.rfind("-release.apk")] + ".apk"
      target = joinPath("build", target)
      if os.path.isfile(target):
        os.remove(target)
      shutil.move(filepath, target)

if __name__ == "__main__":
  os.chdir(dir_root)
  prepareStendhal()

  target = joinPath("android", "keystore.properties")
  if os.path.isfile("keystore.properties"):
    if os.path.isfile(target):
      os.remove(target)
    shutil.copy("keystore.properties", target)
  elif not os.path.isfile(target):
    print("WARNING: keystore.properties file not available, packages will be signed using debug key")

  buildClient()
