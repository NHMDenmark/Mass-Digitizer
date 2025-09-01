# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['DaSSCo.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('ui/specimendataentry.ui', 'ui'),  # Path to specimendataentry.ui
        ('ui/homescreen.ui', 'ui'),         # Path to homescreen.ui
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,  # Set noarchive to False for onefile mode
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,  # Include binaries in the single file
    name='DaSSCo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Prevent console window from opening
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DaSSCo',
)

app = BUNDLE(
    coll,
    name='DaSSCo',
    icon=None,
    bundle_identifier=None,
    info_plist=None,
    codesign_identity=None,
    entitlements_file=None,
)