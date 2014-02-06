# -*- mode: python -*-
a = Analysis(['aggregate.py'],
             pathex=['/Users/dustin/Documents/Aggregate'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='aggregate',
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='aggregate.app',
             icon=None)
