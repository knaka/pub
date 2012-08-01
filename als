#!/usr/bin/env python

import os
import sys
import getopt
import re

# hoge

if len(sys.argv) < 2:
  sys.exit(1)
(opts, args) = getopt.getopt(sys.argv[1:], "t:", ["type="])
type0 = None
for (key, val,) in opts:
  if key == "-t" or key == "--type":
    type0 = val

# Long ones precede (e.g.: "cpio.gz" > "gz")
cmds = {}
cmds["ama"] = 'appmod arc geo "%s"'
cmds["a"] = 'ar tv "%s"'
cmds["tgz"] = cmds["tar.gz"] = 'tar ztvf "%s"'
cmds["cgz"] = cmds["cpio.gz"] = 'gzip -d -c "%s" | cpio --list --verbose'
cmds["cpio"] = 'cat "%s" | cpio --list --verbose'
cmds["tbz"] = cmds["tar.bz2"] = 'tar -t -v -f "%s" --bzip2'
cmds["zip"] = cmds["ZIP"] = cmds["jar"] = cmds["xpi"] = cmds["egg"] = cmds["war"] = cmds["crx"] = 'unzip -l "%s"'
cmds["tar.lzma"] = 'tar Ytvf "%s"'
cmds["tar.Z"] = 'tar Ztvf "%s"'
cmds["tar"] = cmds["gem"] = 'tar tvf "%s"'
cmds["rpm"] = 'rpm2cpio "%s" | cpio --unconditional --list -v'
cmds["lzh"] = cmds["Lzh"] = cmds["LZH"] = 'lha l "%s"'
cmds["7z"] = '7z l "%s"'
cmds["rar"] = 'unrar l "%s"'
cmds["txz"] = cmds["tar.xz"] = 'tar Jtvf "%s"'

re_ext = re.compile("\\.(.*)")
rcRet = 0
for filename in args:
  if not os.path.exists(filename):
    raise Exception, "No such file or directory \"%s\"." % (filename,)
  if type0:
    types = [type0,]
  else:
    types = []
    m = re_ext.search(filename)
    while m:
      ext = m.group(1)
      types.append(ext)
      m = re_ext.search(ext)
  if len(types) == 0:
    raise Exception, "Type unknwon."
  rc = -1
  for type0 in types:
    if cmds.has_key(type0):
      rc = os.system(cmds[type0] % (filename,))
      break
  else:
    raise Exception, "Failed to manage \"%s\"." % (filename,)
sys.exit(rcRet)
