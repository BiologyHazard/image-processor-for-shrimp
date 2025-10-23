# -*- mode: python ; coding: utf-8 -*-
import shutil
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

if TYPE_CHECKING:
    from typing import cast

    from PyInstaller.building.api import COLLECT, EXE, PYZ
    from PyInstaller.building.build_main import Analysis
    from PyInstaller.config import CONF

    DISTPATH = cast(str, CONF["distpath"])


a = Analysis(
    ["image_processor_for_shrimp\\__main__.py"],
    pathex=[],
    binaries=[],
    datas=[],
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
    [],
    exclude_binaries=True,
    name="image-processor-for-shrimp",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="image-processor-for-shrimp",
)

# Copy README.md to the output directory
dist_path = Path(DISTPATH) / "image-processor-for-shrimp"
readme_src = Path("README.md")
readme_dst = dist_path / "README.md"

if readme_src.exists():
    shutil.copy(readme_src, readme_dst)

# Create a zip file of the output directory
zip_filename = dist_path.with_suffix(".zip")
with ZipFile(zip_filename, "w", ZIP_DEFLATED) as zipf:
    for file in dist_path.rglob("*"):
        zipf.write(file, file.relative_to(dist_path))
