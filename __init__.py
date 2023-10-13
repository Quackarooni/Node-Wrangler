# SPDX-FileCopyrightText: 2019-2022 Blender Foundation
#

# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Forked Wrangler",
    "author": "Bartek Skorupa, Greg Zaal, Sebastian Koenig, Christian Brinkmann, Florian Meyer",
    "version": (3, 45),
    "blender": (3, 5, 0),
    "location": "Node Editor Toolbar or Shift-W",
    "description": "Various tools to enhance and speed up node-based workflow",
    "warning": "",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/node/node_wrangler.html",
    "category": "Node",
}

import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    StringProperty,
)

from . import operators, preferences, interface, switch_nodes_geometrymenus
modules = (operators, preferences, interface, switch_nodes_geometrymenus)

def register():
    # props
    bpy.types.Scene.NWBusyDrawing = StringProperty(
        name="Busy Drawing!",
        default="",
        description="An internal property used to store only the first mouse position")
    bpy.types.Scene.NWLazySource = StringProperty(
        name="Lazy Source!",
        default="x",
        description="An internal property used to store the first node in a Lazy Connect operation")
    bpy.types.Scene.NWLazyTarget = StringProperty(
        name="Lazy Target!",
        default="x",
        description="An internal property used to store the last node in a Lazy Connect operation")
    bpy.types.Scene.NWSourceSocket = IntProperty(
        name="Source Socket!",
        default=0,
        description="An internal property used to store the source socket in a Lazy Connect operation")
    bpy.types.NodeTreeInterfaceSocket.NWViewerSocket = BoolProperty(
        name="NW Socket",
        default=False,
        description="An internal property used to determine if a socket is generated by the addon")

    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()

    # props
    del bpy.types.Scene.NWBusyDrawing
    del bpy.types.Scene.NWLazySource
    del bpy.types.Scene.NWLazyTarget
    del bpy.types.Scene.NWSourceSocket
    del bpy.types.NodeTreeInterfaceSocket.NWViewerSocket
