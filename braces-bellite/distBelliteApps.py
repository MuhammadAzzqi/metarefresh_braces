#!/usr/bin/env python
# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~ Copyright (C) 2012 [Bellite.io](http://bellite.io)
##~ Open Source as [CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/)
import os, glob, zipfile, datetime
def timestamp():
    ts = datetime.datetime.now().isoformat('T')[:19]
    return ts.replace(':','').replace('-','')

binaryTags = {
  '#!': 'Hashbang Script',
  'cafebabe'.decode('hex'): 'Mach-O Universal',
  'cefaedfe'.decode('hex'): 'Mach-O i386',
  'cffaedfe'.decode('hex'): 'Mach-O x64',
  #'4d5a9000'.decode('hex'): 'PE32 executable',
}
binaryTagLengths = set(len(k) for k in binaryTags)
def matchBinaryTags(data):
    tags = [data[:i] for i in binaryTagLengths]
    return filter(None, map(binaryTags.get, tags))

def isLikelySymlink(ffn, base, tgt):
    if '\0' in tgt: return False
    parts = tgt.split('/')
    if parts[0] and os.path.exists(os.path.join(base, parts[0])):
        return len(parts)
    else: return False

def walkAppFixups(appPath):
    symlinkQueue = {}
    for base,dirs,files in os.walk(appPath):
        dirs[:] = [e for e in dirs if e[:1]!='.']
        for fn in dirs:
            ffn = os.path.abspath(os.path.join(base, fn))
            if os.path.islink(ffn):
                yield 'symlink', ffn, os.readlink(ffn)
            else: yield 'plain_dir', ffn

        files[:] = [e for e in files if e[:1]!='.']
        for fn in files:
            if fn[:1]=='.': continue

            ffn = os.path.abspath(os.path.join(base, fn))
            data = file(ffn, 'rb').read(2048)

            if os.path.islink(ffn):
                yield 'symlink', ffn, os.readlink(ffn)
                continue

            if matchBinaryTags(data):
                yield 'binary', ffn
                continue

            if binaryTags.get(data[:4]):
                yield 'binary', ffn
                continue

            if fn.endswith('.lnk'):
                print "TODO:", ffn
                print ' ==> may be symlink?!', lines

            else: lines = data.split('\n',2)

            if len(lines)==1:
                tgt = lines[0]
                if isLikelySymlink(ffn, base, tgt):
                    yield 'mk_symlink', ffn,tgt
            else:
                yield 'plain_file', ffn

    while symlinkQueue:
        for key, fq_tgt in symlinkQueue.items():
            if os.path.lexists(fq_tgt):
                del symlinkQueue[key]
                yield 'mk_symlink', key[0], key[1]
                break
        else: return

def fixupApp(appPath):
    mode_rwxrx_r_x = int('755',8)
    def binary(ffn):
        print 'Fixing binary mode (rwxr-xr-x): "%s"' % (ffn,)
        os.chmod(ffn, mode_rwxrx_r_x)
    def mk_symlink(ffn, tgt):
        print 'Fixing symlink: "%s" -> "%s"' % (ffn, tgt)
        ffnTag = ffn+os.urandom(4).encode('hex')
        os.rename(ffn, ffnTag)
        try: os.symlink(tgt, ffn)
        except OSError:
            os.rename(ffnTag, ffn)
        else: os.unlink(ffnTag)

    ns={'binary':binary, 'mk_symlink':mk_symlink}
    for args in walkAppFixups(appPath):
        cmd = ns.get(args[0])
        if cmd: cmd(*args[1:])

def zipApp(appPath, distPaths=None, fnZip=None):
    if fnZip is None:
        fnZip = '%s.zip'%(appPath,)
    zout = zipfile.ZipFile(fnZip, 'w', zipfile.ZIP_DEFLATED)

    def arcname(ffn):
        ffn = ffn.split(src,1)[1]
        arc = ffn.replace(os.sep,'/')
        return dst+arc

    mode_symlink = int('120755',8)<<16
    mode_binary = int('100755',8)<<16
    def plain_dir(ffn):
        pass #print 'Add dir: "%s"' % (ffn,)
    def plain_file(ffn):
        arc = arcname(ffn)
        print 'Add file: "%s"' % (arc,)
        zout.write(ffn, arc)
    def binary(ffn):
        arc = arcname(ffn)
        print 'Add binary: "%s"' % (arc,)
        zi = zipfile.ZipInfo(arc)
        zi.create_system = 3
        zi.external_attr = mode_binary
        with file(ffn, 'rb') as fh:
            zout.writestr(zi, fh.read())
    def symlink(ffn, tgt):
        arc = arcname(ffn)
        print 'Add symlink: "%s" -> "%s"' % (arc, tgt)
        zi = zipfile.ZipInfo(arc)
        zi.create_system = 3
        zi.external_attr = mode_symlink
        zout.writestr(zi, tgt)

    ns={'binary':binary,
        'mk_symlink':symlink, 'symlink':symlink,
        'plain_file':plain_file, 'plain_dir':plain_dir}

    appPath = os.path.abspath(appPath)
    appFilename = os.path.basename(appPath.rstrip(r'\/'))
    distPaths = dict(distPaths or {})
    distPaths[''] = ''
    for src, dst in distPaths.items():
        src = os.path.abspath(os.path.join(appPath, src,''))
        src = os.path.join(src,'')
        dst = os.path.join(appFilename, dst, '')
        dst = dst.replace(os.sep, '/') # zipfile always uses '/'
        print 'src:', repr(src)
        print 'dst:', repr(dst)
        for args in walkAppFixups(src):
            cmd = ns.get(args[0])
            if cmd: cmd(*args[1:])

    zout.close()
    return fnZip

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    _dirname_ = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_dirname_)
    if hasattr(os, 'symlink'):
        fixupApp(_dirname_)

    for appRoot in glob.glob('*.app'):
        print

        if 0:
            print
            print "> codesign *.app"

        print '> archive Mac OSX app: "%s"'%(appRoot,)
        zipApp(appRoot, {'../PlugIns': 'Contents/PlugIns'})

        appRoot = appRoot[:-4]
        print
        print '> archive Windows app: "%s"'%(appRoot,)
        if os.path.isdir(appRoot):
            zipApp(appRoot, {'../PlugIns': 'PlugIns'})
    print

