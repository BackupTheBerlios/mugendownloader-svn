#!/usr/bin/python
# -*- coding: utf-8 -*-
# main.py
# Copyright (C) WoodenJesus 2007 <woodenjesus666@gmail.com>
# 
# main.py is free software.
# 
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
# 
# main.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with main.py.  If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.



from distutils.core import setup
import py2exe
import glob

opts = {
    "py2exe": {
        "includes": "pango,atk,gobject,cairo, pangocairo",
        "dll_excludes": [
        "iconv.dll","intl.dll","libatk-1.0-0.dll",
        "libgdk_pixbuf-2.0-0.dll","libgdk-win32-2.0-0.dll",
        "libglib-2.0-0.dll","libgmodule-2.0-0.dll",
        "libgobject-2.0-0.dll","libgthread-2.0-0.dll",
        "libgtk-win32-2.0-0.dll","libpango-1.0-0.dll",
        "libpangowin32-1.0-0.dll"],
        }
    }

setup(
    name = "mugendownloader",
    description = "Prosty program do pobierania napisow z animesub.info",
    version = "0.1",
    windows = [
        {"script": "mugendownloader.py",
        "icon_resources": [(1, "mugendownloader.ico")]
        }
    ],
    options=opts,
    data_files=[("GPL"),
                ("pixmaps", glob.glob("pixmaps/*.png")),
                ("interface.glade")
    ],
)
