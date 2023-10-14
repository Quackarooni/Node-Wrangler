# SPDX-FileCopyrightText: 2022-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu
from .utils import switch_node_type 

class NODE_MT_NWSwitchNodes_category_texture_input(Menu):
    bl_label = "Input"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "TextureNodeCoordinates")
        switch_node_type(layout, "TextureNodeCurveTime")
        switch_node_type(layout, "TextureNodeImage")
        switch_node_type(layout, "TextureNodeTexture")


class NODE_MT_NWSwitchNodes_category_texture_output(Menu):
    bl_label = "Output"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "TextureNodeOutput")
        switch_node_type(layout, "TextureNodeViewer")


class NODE_MT_NWSwitchNodes_category_texture_color(Menu):
    bl_label = "Color"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "TextureNodeHueSaturation")
        switch_node_type(layout, "TextureNodeInvert")
        switch_node_type(layout, "TextureNodeMixRGB")
        switch_node_type(layout, "TextureNodeCurveRGB")
        layout.separator()
        switch_node_type(layout, "TextureNodeCombineColor")
        switch_node_type(layout, "TextureNodeSeparateColor")


class NODE_MT_NWSwitchNodes_category_texture_converter(Menu):
    bl_label = "Converter"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "TextureNodeValToRGB")
        switch_node_type(layout, "TextureNodeDistance")
        switch_node_type(layout, "TextureNodeMath")
        switch_node_type(layout, "TextureNodeRGBToBW")
        switch_node_type(layout, "TextureNodeValToNor")


class NODE_MT_NWSwitchNodes_category_texture_distort(Menu):
    bl_label = "Distort"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "TextureNodeAt")
        switch_node_type(layout, "TextureNodeRotate")
        switch_node_type(layout, "TextureNodeScale")
        switch_node_type(layout, "TextureNodeTranslate")


class NODE_MT_NWSwitchNodes_category_texture_pattern(Menu):
    bl_label = "Pattern"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "TextureNodeBricks")
        switch_node_type(layout, "TextureNodeChecker")


class NODE_MT_NWSwitchNodes_category_texture_texture(Menu):
    bl_label = "Texture"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "TextureNodeTexBlend")
        switch_node_type(layout, "TextureNodeTexClouds")
        switch_node_type(layout, "TextureNodeTexDistNoise")
        switch_node_type(layout, "TextureNodeTexMagic")
        switch_node_type(layout, "TextureNodeTexMarble")
        switch_node_type(layout, "TextureNodeTexMusgrave")
        switch_node_type(layout, "TextureNodeTexNoise")
        switch_node_type(layout, "TextureNodeTexStucci")
        switch_node_type(layout, "TextureNodeTexVoronoi")
        switch_node_type(layout, "TextureNodeTexWood")


class NODE_MT_texture_node_switch_all(Menu):
    bl_label = "Switch Node Type"

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_texture_input")
        layout.menu("NODE_MT_NWSwitchNodes_category_texture_output")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_texture_color")
        layout.menu("NODE_MT_NWSwitchNodes_category_texture_converter")
        layout.menu("NODE_MT_NWSwitchNodes_category_texture_distort")
        layout.menu("NODE_MT_NWSwitchNodes_category_texture_pattern")
        layout.menu("NODE_MT_NWSwitchNodes_category_texture_texture")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_group")
        layout.menu("NODE_MT_NWSwitchNodes_category_layout")


classes = (
    NODE_MT_texture_node_switch_all,
    NODE_MT_NWSwitchNodes_category_texture_input,
    NODE_MT_NWSwitchNodes_category_texture_output,
    NODE_MT_NWSwitchNodes_category_texture_color,
    NODE_MT_NWSwitchNodes_category_texture_converter,
    NODE_MT_NWSwitchNodes_category_texture_distort,
    NODE_MT_NWSwitchNodes_category_texture_pattern,
    NODE_MT_NWSwitchNodes_category_texture_texture,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)