# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['skin_searcher.py'],
    pathex=["C:\\Users\\Core\\Desktop\\Klasör"],
    binaries=[],
    datas=[('files/skins.json', 'files'), ('files/icon.ico', 'files')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='skin_searcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon=['files/icon.ico'],
)
