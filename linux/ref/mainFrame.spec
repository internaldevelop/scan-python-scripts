# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\..\\..\\2016\xb5\xe7\xcd\xf8\xcf\xee\xc4\xbf\\\xd4\xb4\xb4\xfa\xc2\xeb\\linux\\mainFrame.py'],
             pathex=['Z:\\project\\2016~977\\\xd4\xb4\xb4\xfa\xc2\xeb\\linux'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='mainFrame',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='mainFrame')
