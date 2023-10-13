# SPDX-FileCopyrightText: 2022-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later
from . import compositor, geometry, shader, texture, utils
modules = compositor, geometry, shader, texture, utils

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()
