# SPDX-FileCopyrightText: 2022-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu
from .utils import switch_node_type 
from bpy.app.translations import (
    pgettext_iface as iface_,
)


# only show input/output nodes when editing line style node trees
def line_style_shader_nodes_poll(context):
    snode = context.space_data
    return (snode.tree_type == 'ShaderNodeTree' and
            snode.shader_type == 'LINESTYLE')


# only show nodes working in world node trees
def world_shader_nodes_poll(context):
    snode = context.space_data
    return (snode.tree_type == 'ShaderNodeTree' and
            snode.shader_type == 'WORLD')


# only show nodes working in object node trees
def object_shader_nodes_poll(context):
    snode = context.space_data
    return (snode.tree_type == 'ShaderNodeTree' and
            snode.shader_type == 'OBJECT')


def cycles_shader_nodes_poll(context):
    return context.engine == 'CYCLES'


def eevee_shader_nodes_poll(context):
    return context.engine == 'BLENDER_EEVEE'


def object_cycles_shader_nodes_poll(context):
    return (object_shader_nodes_poll(context) and
            cycles_shader_nodes_poll(context))


def object_not_eevee_shader_nodes_poll(context):
    return (object_shader_nodes_poll(context) and
            not eevee_shader_nodes_poll(context))


def object_eevee_shader_nodes_poll(context):
    return (object_shader_nodes_poll(context) and
            eevee_shader_nodes_poll(context))


class NODE_MT_NWSwitchNodes_category_shader_input(Menu):
    bl_label = "Input"

    def draw(self, context):
        layout = self.layout

        switch_node_type(layout, "ShaderNodeAmbientOcclusion")
        switch_node_type(layout, "ShaderNodeAttribute")
        switch_node_type(layout, "ShaderNodeBevel")
        switch_node_type(layout, "ShaderNodeCameraData")
        switch_node_type(layout, "ShaderNodeVertexColor")
        switch_node_type(layout, "ShaderNodeHairInfo")
        switch_node_type(layout, "ShaderNodeFresnel")
        switch_node_type(layout, "ShaderNodeNewGeometry")
        switch_node_type(layout, "ShaderNodeLayerWeight")
        switch_node_type(layout, "ShaderNodeLightPath")
        switch_node_type(layout, "ShaderNodeObjectInfo")
        switch_node_type(layout, "ShaderNodeParticleInfo")
        switch_node_type(layout, "ShaderNodePointInfo")
        switch_node_type(layout, "ShaderNodeRGB")
        switch_node_type(layout, "ShaderNodeTangent")
        switch_node_type(layout, "ShaderNodeTexCoord")
        switch_node_type(layout, "ShaderNodeUVAlongStroke", poll=line_style_shader_nodes_poll(context))
        switch_node_type(layout, "ShaderNodeUVMap")
        switch_node_type(layout, "ShaderNodeValue")
        switch_node_type(layout, "ShaderNodeVolumeInfo")
        switch_node_type(layout, "ShaderNodeWireframe")


class NODE_MT_NWSwitchNodes_category_shader_output(Menu):
    bl_label = "Output"

    def draw(self, context):
        layout = self.layout

        switch_node_type(
            layout,
            "ShaderNodeOutputMaterial",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeOutputLight",
            poll=object_not_eevee_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeOutputAOV",
        )
        switch_node_type(
            layout,
            "ShaderNodeOutputWorld",
            poll=world_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeOutputLineStyle",
            poll=line_style_shader_nodes_poll(context),
        )


class NODE_MT_NWSwitchNodes_category_shader_shader(Menu):
    bl_label = "Shader"

    def draw(self, context):
        layout = self.layout

        switch_node_type(
            layout,
            "ShaderNodeAddShader",
        )
        switch_node_type(
            layout,
            "ShaderNodeBackground",
            poll=world_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfDiffuse",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeEmission",
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfGlass",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfGlossy",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfHair",
            poll=object_not_eevee_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeHoldout",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeMixShader",
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfPrincipled",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfHairPrincipled",
            poll=object_not_eevee_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeVolumePrincipled"
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfRefraction",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfSheen",
            poll=object_not_eevee_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeEeveeSpecular",
            poll=object_eevee_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeSubsurfaceScattering",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfToon",
            poll=object_not_eevee_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfTranslucent",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeBsdfTransparent",
            poll=object_shader_nodes_poll(context),
        )
        switch_node_type(
            layout,
            "ShaderNodeVolumeAbsorption",
        )
        switch_node_type(
            layout,
            "ShaderNodeVolumeScatter",
        )


class NODE_MT_NWSwitchNodes_category_shader_color(Menu):
    bl_label = "Color"

    def draw(self, _context):
        layout = self.layout

        switch_node_type(layout, "ShaderNodeBrightContrast")
        switch_node_type(layout, "ShaderNodeGamma")
        switch_node_type(layout, "ShaderNodeHueSaturation")
        switch_node_type(layout, "ShaderNodeInvert")
        switch_node_type(layout, "ShaderNodeLightFalloff")
        props = switch_node_type(layout, "ShaderNodeMix", label=iface_("Mix Color"))
        ops = props.settings.add()
        ops.name = "data_type"
        ops.value = "'RGBA'"
        switch_node_type(layout, "ShaderNodeRGBCurve")


class NODE_MT_NWSwitchNodes_category_shader_converter(Menu):
    bl_label = "Converter"

    def draw(self, context):
        layout = self.layout

        switch_node_type(layout, "ShaderNodeBlackbody")
        switch_node_type(layout, "ShaderNodeClamp")
        switch_node_type(layout, "ShaderNodeValToRGB")
        switch_node_type(layout, "ShaderNodeCombineColor")
        switch_node_type(layout, "ShaderNodeCombineXYZ")
        switch_node_type(layout, "ShaderNodeFloatCurve")
        switch_node_type(layout, "ShaderNodeMapRange")
        switch_node_type(layout, "ShaderNodeMath")
        switch_node_type(layout, "ShaderNodeMix")
        switch_node_type(layout, "ShaderNodeRGBToBW")
        switch_node_type(layout, "ShaderNodeSeparateColor")
        switch_node_type(layout, "ShaderNodeSeparateXYZ")
        switch_node_type(layout, "ShaderNodeShaderToRGB", poll=object_eevee_shader_nodes_poll(context))
        switch_node_type(layout, "ShaderNodeVectorMath")
        switch_node_type(layout, "ShaderNodeWavelength")


class NODE_MT_NWSwitchNodes_category_shader_texture(Menu):
    bl_label = "Texture"

    def draw(self, _context):
        layout = self.layout

        switch_node_type(layout, "ShaderNodeTexBrick")
        switch_node_type(layout, "ShaderNodeTexChecker")
        switch_node_type(layout, "ShaderNodeTexEnvironment")
        switch_node_type(layout, "ShaderNodeTexGradient")
        switch_node_type(layout, "ShaderNodeTexIES")
        switch_node_type(layout, "ShaderNodeTexImage")
        switch_node_type(layout, "ShaderNodeTexMagic")
        switch_node_type(layout, "ShaderNodeTexMusgrave")
        switch_node_type(layout, "ShaderNodeTexNoise")
        switch_node_type(layout, "ShaderNodeTexPointDensity")
        switch_node_type(layout, "ShaderNodeTexSky")
        switch_node_type(layout, "ShaderNodeTexVoronoi")
        switch_node_type(layout, "ShaderNodeTexWave")
        switch_node_type(layout, "ShaderNodeTexWhiteNoise")


class NODE_MT_NWSwitchNodes_category_shader_vector(Menu):
    bl_label = "Vector"

    def draw(self, _context):
        layout = self.layout

        switch_node_type(layout, "ShaderNodeBump")
        switch_node_type(layout, "ShaderNodeDisplacement")
        switch_node_type(layout, "ShaderNodeMapping")
        switch_node_type(layout, "ShaderNodeNormal")
        switch_node_type(layout, "ShaderNodeNormalMap")
        switch_node_type(layout, "ShaderNodeVectorCurve")
        switch_node_type(layout, "ShaderNodeVectorDisplacement")
        switch_node_type(layout, "ShaderNodeVectorRotate")
        switch_node_type(layout, "ShaderNodeVectorTransform")


class NODE_MT_NWSwitchNodes_category_shader_script(Menu):
    bl_label = "Script"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "ShaderNodeScript")


class NODE_MT_shader_node_switch_all(Menu):
    bl_label = "Add"

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_shader_input")
        layout.menu("NODE_MT_NWSwitchNodes_category_shader_output")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_shader_color")
        layout.menu("NODE_MT_NWSwitchNodes_category_shader_converter")
        layout.menu("NODE_MT_NWSwitchNodes_category_shader_shader")
        layout.menu("NODE_MT_NWSwitchNodes_category_shader_texture")
        layout.menu("NODE_MT_NWSwitchNodes_category_shader_vector")
        #layout.separator()
        #layout.menu("NODE_MT_NWSwitchNodes_category_shader_script")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_group")
        layout.menu("NODE_MT_NWSwitchNodes_category_layout")


classes = (
    NODE_MT_shader_node_switch_all,
    NODE_MT_NWSwitchNodes_category_shader_input,
    NODE_MT_NWSwitchNodes_category_shader_output,
    NODE_MT_NWSwitchNodes_category_shader_color,
    NODE_MT_NWSwitchNodes_category_shader_converter,
    NODE_MT_NWSwitchNodes_category_shader_shader,
    NODE_MT_NWSwitchNodes_category_shader_texture,
    NODE_MT_NWSwitchNodes_category_shader_vector,
    #NODE_MT_NWSwitchNodes_category_shader_script,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
