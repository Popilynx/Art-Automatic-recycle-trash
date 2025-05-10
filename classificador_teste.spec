# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tests\\test_classificador.py'],
    pathex=[],
    binaries=[],
    datas=[('modelo.tflite', '.'), ('labels.txt', '.'), ('tests', '.'), ('classificador_lixo\\build_utils.py', '.'), ('classificador_lixo\\classificador.py', '.'), ('classificador_lixo\\main.py', '.'), ('classificador_lixo\\motores.py', '.'), ('classificador_lixo\\__init__.py', '.')],
    hiddenimports=['classificador_lixo', 'tensorflow', 'tensorflow.lite', 'numpy', 'cv2', 'PIL'],
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
    name='classificador_teste',
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
)
