# SPDX-FileCopyrightText: 2022-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu
from .utils import switch_node_type
from bpy.app.translations import (
    pgettext_iface as iface_,
)


class NODE_MT_NWSwitchNodes_category_compositor_input(Menu):
    bl_label = "Input"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        snode = context.space_data
        is_group = (len(snode.path) > 1)

        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_input_constant")
        layout.separator()
        switch_node_type(layout, "CompositorNodeBokehImage")
        switch_node_type(layout, "CompositorNodeImage")
        switch_node_type(layout, "CompositorNodeMask")
        switch_node_type(layout, "CompositorNodeMovieClip")
        switch_node_type(layout, "CompositorNodeTexture")

        if is_group:
            layout.separator()
            switch_node_type(layout, "NodeGroupInput")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_input_scene")


class NODE_MT_NWSwitchNodes_category_compositor_input_constant(Menu):
    bl_label = "Constant"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeRGB")
        switch_node_type(layout, "CompositorNodeValue")


class NODE_MT_NWSwitchNodes_category_compositor_input_scene(Menu):
    bl_label = "Scene"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeRLayers")
        switch_node_type(layout, "CompositorNodeSceneTime")
        switch_node_type(layout, "CompositorNodeTime")


class NODE_MT_NWSwitchNodes_category_compositor_output(Menu):
    bl_label = "Output"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        snode = context.space_data
        is_group = (len(snode.path) > 1)

        layout = self.layout
        switch_node_type(layout, "CompositorNodeComposite")
        switch_node_type(layout, "CompositorNodeSplitViewer")
        switch_node_type(layout, "CompositorNodeViewer")
        layout.separator()
        switch_node_type(layout, "CompositorNodeOutputFile")

        if is_group:
            layout.separator()
            switch_node_type(layout, "NodeGroupOutput")


class NODE_MT_NWSwitchNodes_category_compositor_color(Menu):
    bl_label = "Color"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_color_adjust")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_color_mix")
        layout.separator()
        switch_node_type(layout, "CompositorNodePremulKey")
        switch_node_type(layout, "CompositorNodeValToRGB")
        switch_node_type(layout, "CompositorNodeConvertColorSpace")
        switch_node_type(layout, "CompositorNodeSetAlpha")
        layout.separator()
        switch_node_type(layout, "CompositorNodeInvert")
        switch_node_type(layout, "CompositorNodeRGBToBW")


class NODE_MT_NWSwitchNodes_category_compositor_color_adjust(Menu):
    bl_label = "Adjust"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeBrightContrast")
        switch_node_type(layout, "CompositorNodeColorBalance")
        switch_node_type(layout, "CompositorNodeColorCorrection")
        switch_node_type(layout, "CompositorNodeExposure")
        switch_node_type(layout, "CompositorNodeGamma")
        switch_node_type(layout, "CompositorNodeHueCorrect")
        switch_node_type(layout, "CompositorNodeHueSat")
        switch_node_type(layout, "CompositorNodeCurveRGB")
        switch_node_type(layout, "CompositorNodeTonemap")


class NODE_MT_NWSwitchNodes_category_compositor_color_mix(Menu):
    bl_label = "Mix"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeAlphaOver")
        layout.separator()
        switch_node_type(layout, "CompositorNodeCombineColor")
        switch_node_type(layout, "CompositorNodeSeparateColor")
        layout.separator()
        switch_node_type(
            layout, "CompositorNodeMixRGB",
            label=iface_("Mix Color"))
        switch_node_type(layout, "CompositorNodeZcombine")


class NODE_MT_NWSwitchNodes_category_compositor_filter(Menu):
    bl_label = "Filter"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_filter_blur")
        layout.separator()
        switch_node_type(layout, "CompositorNodeAntiAliasing")
        switch_node_type(layout, "CompositorNodeDenoise")
        switch_node_type(layout, "CompositorNodeDespeckle")
        layout.separator()
        switch_node_type(layout, "CompositorNodeDilateErode")
        switch_node_type(layout, "CompositorNodeInpaint")
        layout.separator()
        switch_node_type(layout, "CompositorNodeFilter")
        switch_node_type(layout, "CompositorNodeGlare")
        switch_node_type(layout, "CompositorNodeKuwahara")
        switch_node_type(layout, "CompositorNodePixelate")
        switch_node_type(layout, "CompositorNodePosterize")
        switch_node_type(layout, "CompositorNodeSunBeams")


class NODE_MT_NWSwitchNodes_category_compositor_filter_blur(Menu):
    bl_label = "Blur"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeBilateralblur")
        switch_node_type(layout, "CompositorNodeBlur")
        switch_node_type(layout, "CompositorNodeBokehBlur")
        switch_node_type(layout, "CompositorNodeDefocus")
        switch_node_type(layout, "CompositorNodeDBlur")
        switch_node_type(layout, "CompositorNodeVecBlur")


class NODE_MT_NWSwitchNodes_category_compositor_keying(Menu):
    bl_label = "Keying"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeChannelMatte")
        switch_node_type(layout, "CompositorNodeChromaMatte")
        switch_node_type(layout, "CompositorNodeColorMatte")
        switch_node_type(layout, "CompositorNodeColorSpill")
        switch_node_type(layout, "CompositorNodeDiffMatte")
        switch_node_type(layout, "CompositorNodeDistanceMatte")
        switch_node_type(layout, "CompositorNodeKeying")
        switch_node_type(layout, "CompositorNodeKeyingScreen")
        switch_node_type(layout, "CompositorNodeLumaMatte")


class NODE_MT_NWSwitchNodes_category_compositor_mask(Menu):
    bl_label = "Mask"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeCryptomatteV2")
        switch_node_type(layout, "CompositorNodeCryptomatte")
        layout.separator()
        switch_node_type(layout, "CompositorNodeBoxMask")
        switch_node_type(layout, "CompositorNodeEllipseMask")
        layout.separator()
        switch_node_type(layout, "CompositorNodeDoubleEdgeMask")
        switch_node_type(layout, "CompositorNodeIDMask")


class NODE_MT_NWSwitchNodes_category_compositor_tracking(Menu):
    bl_label = "Tracking"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodePlaneTrackDeform")
        switch_node_type(layout, "CompositorNodeStabilize")
        switch_node_type(layout, "CompositorNodeTrackPos")


class NODE_MT_NWSwitchNodes_category_compositor_transform(Menu):
    bl_label = "Transform"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeRotate")
        switch_node_type(layout, "CompositorNodeScale")
        switch_node_type(layout, "CompositorNodeTransform")
        switch_node_type(layout, "CompositorNodeTranslate")
        layout.separator()
        switch_node_type(layout, "CompositorNodeCornerPin")
        switch_node_type(layout, "CompositorNodeCrop")
        layout.separator()
        switch_node_type(layout, "CompositorNodeDisplace")
        switch_node_type(layout, "CompositorNodeFlip")
        switch_node_type(layout, "CompositorNodeMapUV")
        layout.separator()
        switch_node_type(layout, "CompositorNodeLensdist")
        switch_node_type(layout, "CompositorNodeMovieDistortion")


class NODE_MT_NWSwitchNodes_category_compositor_utilities(Menu):
    bl_label = "Utilities"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeMapRange")
        switch_node_type(layout, "CompositorNodeMapValue")
        switch_node_type(layout, "CompositorNodeMath")
        layout.separator()
        switch_node_type(layout, "CompositorNodeLevels")
        switch_node_type(layout, "CompositorNodeNormalize")
        layout.separator()
        switch_node_type(layout, "CompositorNodeSwitch")
        switch_node_type(
            layout, "CompositorNodeSwitchView",
            label=iface_("Switch Stereo View"))


class NODE_MT_NWSwitchNodes_category_compositor_vector(Menu):
    bl_label = "Vector"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "CompositorNodeCombineXYZ")
        switch_node_type(layout, "CompositorNodeSeparateXYZ")
        layout.separator()
        switch_node_type(layout, "CompositorNodeNormal")
        switch_node_type(layout, "CompositorNodeCurveVec")


class NODE_MT_NWSwitchNodes_category_compositor_LAYOUT(Menu):
    bl_label = "Layout"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "NodeFrame")
        switch_node_type(layout, "NodeReroute")


class NODE_MT_compositor_node_switch_all(Menu):
    bl_label = "Switch Node Type"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_input")
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_output")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_color")
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_filter")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_keying")
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_mask")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_tracking")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_transform")
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_utilities")
        layout.menu("NODE_MT_NWSwitchNodes_category_compositor_vector")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_group")
        layout.menu("NODE_MT_NWSwitchNodes_category_layout")


classes = (
    NODE_MT_compositor_node_switch_all,
    NODE_MT_NWSwitchNodes_category_compositor_input,
    NODE_MT_NWSwitchNodes_category_compositor_input_constant,
    NODE_MT_NWSwitchNodes_category_compositor_input_scene,
    NODE_MT_NWSwitchNodes_category_compositor_output,
    NODE_MT_NWSwitchNodes_category_compositor_color,
    NODE_MT_NWSwitchNodes_category_compositor_color_adjust,
    NODE_MT_NWSwitchNodes_category_compositor_color_mix,
    NODE_MT_NWSwitchNodes_category_compositor_filter,
    NODE_MT_NWSwitchNodes_category_compositor_filter_blur,
    NODE_MT_NWSwitchNodes_category_compositor_keying,
    NODE_MT_NWSwitchNodes_category_compositor_mask,
    NODE_MT_NWSwitchNodes_category_compositor_tracking,
    NODE_MT_NWSwitchNodes_category_compositor_transform,
    NODE_MT_NWSwitchNodes_category_compositor_utilities,
    NODE_MT_NWSwitchNodes_category_compositor_vector,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
