# -*- mode: python -*-
import os
import sys

block_cipher = None

DIR = os.path.realpath(".")

sys.modules['FixTk'] = None

a = Analysis(['main.py'],
             pathex=[DIR],
             datas=[('matplotlibrc', '.')],
             hiddenimports=['scipy._lib.messagestream'],
             hookspath=None,
             runtime_hooks=[],
             excludes=['FixTk', 'tcl', 'tk', '_tkinter', '_tkinter', 'Tkinter', 'gtk3', 'wx', 'gtk+', 'gtk2',
             'gdk', 'cairo', 'wayland', 'xinerama', 'share', 'icons', 'atk', 'pango', 'pil', 'PIL', 'pdf', 'WebAgg',
             'GTK3Agg','GTK3Cairo','WX', 'WXAgg'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='valexa',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='valexa')
