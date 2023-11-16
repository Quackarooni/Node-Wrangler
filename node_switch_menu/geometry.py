# SPDX-FileCopyrightText: 2022-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu
from .utils import switch_node_type 
from bpy.app.translations import (
    pgettext_iface as iface_,
    contexts as i18n_contexts,
)


class NODE_MT_NWSwitchNodes_category_GEO_ATTRIBUTE(Menu):
    bl_label = "Attribute"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeAttributeStatistic")
        switch_node_type(layout, "GeometryNodeAttributeDomainSize")
        layout.separator()
        switch_node_type(layout, "GeometryNodeBlurAttribute")
        switch_node_type(layout, "GeometryNodeCaptureAttribute")
        switch_node_type(layout, "GeometryNodeRemoveAttribute")
        switch_node_type(layout, "GeometryNodeStoreNamedAttribute")


class NODE_MT_NWSwitchNodes_category_GEO_COLOR(Menu):
    bl_label = "Color"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "ShaderNodeValToRGB")
        switch_node_type(layout, "ShaderNodeRGBCurve")
        layout.separator()
        switch_node_type(layout, "FunctionNodeCombineColor")
        props = switch_node_type(layout, "ShaderNodeMix", label=iface_("Mix Color"))
        ops = props.settings.add()
        ops.name = "data_type"
        ops.value = "'RGBA'"
        switch_node_type(layout, "FunctionNodeSeparateColor")


class NODE_MT_NWSwitchNodes_category_GEO_CURVE(Menu):
    bl_label = "Curve"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_CURVE_READ")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_CURVE_SAMPLE")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_CURVE_WRITE")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_CURVE_OPERATIONS")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_PRIMITIVES_CURVE")
        layout.menu("NODE_MT_NWSwitchNodes_category_curve_topology")


class NODE_MT_NWSwitchNodes_category_GEO_CURVE_READ(Menu):
    bl_label = "Read"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeInputCurveHandlePositions")
        switch_node_type(layout, "GeometryNodeCurveLength")
        switch_node_type(layout, "GeometryNodeInputTangent")
        switch_node_type(layout, "GeometryNodeInputCurveTilt")
        switch_node_type(layout, "GeometryNodeCurveEndpointSelection")
        switch_node_type(layout, "GeometryNodeCurveHandleTypeSelection")
        switch_node_type(layout, "GeometryNodeInputSplineCyclic")
        switch_node_type(layout, "GeometryNodeSplineLength")
        switch_node_type(layout, "GeometryNodeSplineParameter")
        switch_node_type(layout, "GeometryNodeInputSplineResolution")


class NODE_MT_NWSwitchNodes_category_GEO_CURVE_SAMPLE(Menu):
    bl_label = "Sample"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSampleCurve")


class NODE_MT_NWSwitchNodes_category_GEO_CURVE_WRITE(Menu):
    bl_label = "Write"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSetCurveNormal")
        switch_node_type(layout, "GeometryNodeSetCurveRadius")
        switch_node_type(layout, "GeometryNodeSetCurveTilt")
        switch_node_type(layout, "GeometryNodeSetCurveHandlePositions")
        switch_node_type(layout, "GeometryNodeCurveSetHandles")
        switch_node_type(layout, "GeometryNodeSetSplineCyclic")
        switch_node_type(layout, "GeometryNodeSetSplineResolution")
        switch_node_type(layout, "GeometryNodeCurveSplineType")


class NODE_MT_NWSwitchNodes_category_GEO_CURVE_OPERATIONS(Menu):
    bl_label = "Operations"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeCurveToMesh")
        switch_node_type(layout, "GeometryNodeCurveToPoints")
        switch_node_type(layout, "GeometryNodeDeformCurvesOnSurface")
        switch_node_type(layout, "GeometryNodeFillCurve")
        switch_node_type(layout, "GeometryNodeFilletCurve")
        switch_node_type(layout, "GeometryNodeInterpolateCurves")
        switch_node_type(layout, "GeometryNodeResampleCurve")
        switch_node_type(layout, "GeometryNodeReverseCurve")
        switch_node_type(layout, "GeometryNodeSubdivideCurve")
        switch_node_type(layout, "GeometryNodeTrimCurve")


class NODE_MT_NWSwitchNodes_category_GEO_PRIMITIVES_CURVE(Menu):
    bl_label = "Primitives"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeCurveArc")
        switch_node_type(layout, "GeometryNodeCurvePrimitiveBezierSegment")
        switch_node_type(layout, "GeometryNodeCurvePrimitiveCircle")
        switch_node_type(layout, "GeometryNodeCurvePrimitiveLine")
        switch_node_type(layout, "GeometryNodeCurveSpiral")
        switch_node_type(layout, "GeometryNodeCurveQuadraticBezier")
        switch_node_type(layout, "GeometryNodeCurvePrimitiveQuadrilateral")
        switch_node_type(layout, "GeometryNodeCurveStar")


class NODE_MT_NWSwitchNodes_category_curve_topology(Menu):
    bl_label = "Topology"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeCurveOfPoint")
        switch_node_type(layout, "GeometryNodeOffsetPointInCurve")
        switch_node_type(layout, "GeometryNodePointsOfCurve")


class NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY(Menu):
    bl_label = "Geometry"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_READ")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_SAMPLE")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_WRITE")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_OPERATIONS")
        layout.separator()
        switch_node_type(layout, "GeometryNodeGeometryToInstance")
        switch_node_type(layout, "GeometryNodeJoinGeometry")


class NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_READ(Menu):
    bl_label = "Read"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeInputID")
        switch_node_type(layout, "GeometryNodeInputIndex")
        switch_node_type(layout, "GeometryNodeInputNamedAttribute")
        switch_node_type(layout, "GeometryNodeInputNormal")
        switch_node_type(layout, "GeometryNodeInputPosition")
        switch_node_type(layout, "GeometryNodeInputRadius")
        if context.space_data.geometry_nodes_type == 'TOOL':
            switch_node_type(layout, "GeometryNodeToolSelection")


class NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_WRITE(Menu):
    bl_label = "Write"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSetID")
        switch_node_type(layout, "GeometryNodeSetPosition")
        if context.space_data.geometry_nodes_type == 'TOOL':
            switch_node_type(layout, "GeometryNodeToolSetSelection")


class NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_OPERATIONS(Menu):
    bl_label = "Operations"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeBoundBox")
        switch_node_type(layout, "GeometryNodeConvexHull")
        switch_node_type(layout, "GeometryNodeDeleteGeometry")
        switch_node_type(layout, "GeometryNodeDuplicateElements")
        switch_node_type(layout, "GeometryNodeMergeByDistance")
        switch_node_type(layout, "GeometryNodeTransform")
        layout.separator()
        switch_node_type(layout, "GeometryNodeSeparateComponents")
        switch_node_type(layout, "GeometryNodeSeparateGeometry")
        switch_node_type(layout, "GeometryNodeSplitToInstances")


class NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_SAMPLE(Menu):
    bl_label = "Sample"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeProximity")
        switch_node_type(layout, "GeometryNodeIndexOfNearest")
        switch_node_type(layout, "GeometryNodeRaycast")
        switch_node_type(layout, "GeometryNodeSampleIndex")
        switch_node_type(layout, "GeometryNodeSampleNearest")


class NODE_MT_NWSwitchNodes_category_GEO_INPUT(Menu):
    bl_label = "Input"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_INPUT_CONSTANT")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_INPUT_GROUP")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_INPUT_SCENE")


class NODE_MT_NWSwitchNodes_category_GEO_INPUT_CONSTANT(Menu):
    bl_label = "Constant"
    bl_options = {'SEARCH_ON_KEY_PRESS'}
    bl_translation_context = i18n_contexts.id_nodetree

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "FunctionNodeInputBool")
        switch_node_type(layout, "FunctionNodeInputColor")
        switch_node_type(layout, "GeometryNodeInputImage")
        switch_node_type(layout, "FunctionNodeInputInt")
        switch_node_type(layout, "GeometryNodeInputMaterial")
        switch_node_type(layout, "FunctionNodeInputString")
        switch_node_type(layout, "ShaderNodeValue")
        switch_node_type(layout, "FunctionNodeInputVector")


class NODE_MT_NWSwitchNodes_category_GEO_INPUT_GROUP(Menu):
    bl_label = "Group"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "NodeGroupInput")


class NODE_MT_NWSwitchNodes_category_GEO_INPUT_SCENE(Menu):
    bl_label = "Scene"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        if context.space_data.geometry_nodes_type == 'TOOL':
            switch_node_type(layout, "GeometryNodeTool3DCursor")
        switch_node_type(layout, "GeometryNodeCollectionInfo")
        switch_node_type(layout, "GeometryNodeImageInfo")
        switch_node_type(layout, "GeometryNodeIsViewport")
        if context.preferences.experimental.use_grease_pencil_version3:
            switch_node_type(layout, "GeometryNodeInputNamedLayerSelection")
        switch_node_type(layout, "GeometryNodeObjectInfo")
        switch_node_type(layout, "GeometryNodeInputSceneTime")
        switch_node_type(layout, "GeometryNodeSelfObject")


class NODE_MT_NWSwitchNodes_category_GEO_INSTANCE(Menu):
    bl_label = "Instances"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeInstanceOnPoints")
        switch_node_type(layout, "GeometryNodeInstancesToPoints")
        layout.separator()
        switch_node_type(layout, "GeometryNodeRealizeInstances")
        switch_node_type(layout, "GeometryNodeRotateInstances")
        switch_node_type(layout, "GeometryNodeScaleInstances")
        switch_node_type(layout, "GeometryNodeTranslateInstances")
        layout.separator()
        switch_node_type(layout, "GeometryNodeInputInstanceRotation")
        switch_node_type(layout, "GeometryNodeInputInstanceScale")


class NODE_MT_NWSwitchNodes_category_GEO_MATERIAL(Menu):
    bl_label = "Material"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeReplaceMaterial")
        layout.separator()
        switch_node_type(layout, "GeometryNodeInputMaterialIndex")
        switch_node_type(layout, "GeometryNodeMaterialSelection")
        layout.separator()
        switch_node_type(layout, "GeometryNodeSetMaterial")
        switch_node_type(layout, "GeometryNodeSetMaterialIndex")


class NODE_MT_NWSwitchNodes_category_GEO_MESH(Menu):
    bl_label = "Mesh"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_MESH_READ")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_MESH_SAMPLE")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_MESH_WRITE")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_MESH_OPERATIONS")
        layout.menu("NODE_MT_NWSwitchNodes_category_PRIMITIVES_MESH")
        layout.menu("NODE_MT_NWSwitchNodes_category_mesh_topology")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_UV")


class NODE_MT_NWSwitchNodes_category_GEO_MESH_READ(Menu):
    bl_label = "Read"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeInputMeshEdgeAngle")
        switch_node_type(layout, "GeometryNodeInputMeshEdgeNeighbors")
        switch_node_type(layout, "GeometryNodeInputMeshEdgeVertices")
        switch_node_type(layout, "GeometryNodeEdgesToFaceGroups")
        switch_node_type(layout, "GeometryNodeInputMeshFaceArea")
        switch_node_type(layout, "GeometryNodeMeshFaceSetBoundaries")
        switch_node_type(layout, "GeometryNodeInputMeshFaceNeighbors")
        if context.space_data.geometry_nodes_type == 'TOOL':
            switch_node_type(layout, "GeometryNodeToolFaceSet")
        switch_node_type(layout, "GeometryNodeInputMeshFaceIsPlanar")
        switch_node_type(layout, "GeometryNodeInputShadeSmooth")
        switch_node_type(layout, "GeometryNodeInputEdgeSmooth")
        switch_node_type(layout, "GeometryNodeInputMeshIsland")
        switch_node_type(layout, "GeometryNodeInputShortestEdgePaths")
        switch_node_type(layout, "GeometryNodeInputMeshVertexNeighbors")


class NODE_MT_NWSwitchNodes_category_GEO_MESH_SAMPLE(Menu):
    bl_label = "Sample"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSampleNearestSurface")
        switch_node_type(layout, "GeometryNodeSampleUVSurface")


class NODE_MT_NWSwitchNodes_category_GEO_MESH_WRITE(Menu):
    bl_label = "Write"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        if context.space_data.geometry_nodes_type == 'TOOL':
            switch_node_type(layout, "GeometryNodeToolSetFaceSet")
        switch_node_type(layout, "GeometryNodeSetShadeSmooth")


class NODE_MT_NWSwitchNodes_category_GEO_MESH_OPERATIONS(Menu):
    bl_label = "Operations"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeDualMesh")
        switch_node_type(layout, "GeometryNodeEdgePathsToCurves")
        switch_node_type(layout, "GeometryNodeEdgePathsToSelection")
        switch_node_type(layout, "GeometryNodeExtrudeMesh")
        switch_node_type(layout, "GeometryNodeFlipFaces")
        switch_node_type(layout, "GeometryNodeMeshBoolean")
        switch_node_type(layout, "GeometryNodeMeshToCurve")
        switch_node_type(layout, "GeometryNodeMeshToPoints")
        if context.preferences.experimental.use_new_volume_nodes:
            switch_node_type(layout, "GeometryNodeMeshToSDFVolume")
        switch_node_type(layout, "GeometryNodeMeshToVolume")
        switch_node_type(layout, "GeometryNodeScaleElements")
        switch_node_type(layout, "GeometryNodeSplitEdges")
        switch_node_type(layout, "GeometryNodeSubdivideMesh")
        switch_node_type(layout, "GeometryNodeSubdivisionSurface")
        switch_node_type(layout, "GeometryNodeTriangulate")


class NODE_MT_NWSwitchNodes_category_PRIMITIVES_MESH(Menu):
    bl_label = "Primitives"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeMeshCone")
        switch_node_type(layout, "GeometryNodeMeshCube")
        switch_node_type(layout, "GeometryNodeMeshCylinder")
        switch_node_type(layout, "GeometryNodeMeshGrid")
        switch_node_type(layout, "GeometryNodeMeshIcoSphere")
        switch_node_type(layout, "GeometryNodeMeshCircle")
        switch_node_type(layout, "GeometryNodeMeshLine")
        switch_node_type(layout, "GeometryNodeMeshUVSphere")


class NODE_MT_NWSwitchNodes_category_mesh_topology(Menu):
    bl_label = "Topology"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeCornersOfEdge")
        switch_node_type(layout, "GeometryNodeCornersOfFace")
        switch_node_type(layout, "GeometryNodeCornersOfVertex")
        switch_node_type(layout, "GeometryNodeEdgesOfCorner")
        switch_node_type(layout, "GeometryNodeEdgesOfVertex")
        switch_node_type(layout, "GeometryNodeFaceOfCorner")
        switch_node_type(layout, "GeometryNodeOffsetCornerInFace")
        switch_node_type(layout, "GeometryNodeVertexOfCorner")


class NODE_MT_NWSwitchNodes_category_GEO_OUTPUT(Menu):
    bl_label = "Output"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "NodeGroupOutput")
        switch_node_type(layout, "GeometryNodeViewer")


class NODE_MT_NWSwitchNodes_category_GEO_POINT(Menu):
    bl_label = "Point"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeDistributePointsInVolume")
        switch_node_type(layout, "GeometryNodeDistributePointsOnFaces")
        layout.separator()
        switch_node_type(layout, "GeometryNodePoints")
        switch_node_type(layout, "GeometryNodePointsToCurves")
        switch_node_type(layout, "GeometryNodePointsToVertices")
        if context.preferences.experimental.use_new_volume_nodes:
            switch_node_type(layout, "GeometryNodePointsToSDFVolume")
        switch_node_type(layout, "GeometryNodePointsToVolume")
        layout.separator()
        switch_node_type(layout, "GeometryNodeSetPointRadius")


class NODE_MT_NWSwitchNodes_category_simulation(Menu):
    bl_label = "Simulation"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        #add_simulation_zone(layout, label="Simulation Zone")


class NODE_MT_NWSwitchNodes_category_GEO_TEXT(Menu):
    bl_label = "Text"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeStringJoin")
        switch_node_type(layout, "FunctionNodeReplaceString")
        switch_node_type(layout, "FunctionNodeSliceString")
        layout.separator()
        switch_node_type(layout, "FunctionNodeStringLength")
        switch_node_type(layout, "GeometryNodeStringToCurves")
        switch_node_type(layout, "FunctionNodeValueToString")
        layout.separator()
        switch_node_type(layout, "FunctionNodeInputSpecialCharacters")


class NODE_MT_NWSwitchNodes_category_GEO_TEXTURE(Menu):
    bl_label = "Texture"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "ShaderNodeTexBrick")
        switch_node_type(layout, "ShaderNodeTexChecker")
        switch_node_type(layout, "ShaderNodeTexGradient")
        switch_node_type(layout, "GeometryNodeImageTexture")
        switch_node_type(layout, "ShaderNodeTexMagic")
        switch_node_type(layout, "ShaderNodeTexMusgrave")
        switch_node_type(layout, "ShaderNodeTexNoise")
        switch_node_type(layout, "ShaderNodeTexVoronoi")
        switch_node_type(layout, "ShaderNodeTexWave")
        switch_node_type(layout, "ShaderNodeTexWhiteNoise")


class NODE_MT_NWSwitchNodes_category_GEO_UTILITIES(Menu):
    bl_label = "Utilities"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_COLOR")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_TEXT")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_VECTOR")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_FIELD")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_MATH")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_ROTATION")
        layout.separator()
        switch_node_type(layout, "FunctionNodeRandomValue")
        #add_repeat_zone(layout, label="Repeat Zone")
        switch_node_type(layout, "GeometryNodeSwitch")


class NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_FIELD(Menu):
    bl_label = "Field"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeAccumulateField")
        switch_node_type(layout, "GeometryNodeFieldAtIndex")
        switch_node_type(layout, "GeometryNodeFieldOnDomain")


class NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_ROTATION(Menu):
    bl_label = "Rotation"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "FunctionNodeAlignEulerToVector")
        switch_node_type(layout, "FunctionNodeAxisAngleToRotation")
        switch_node_type(layout, "FunctionNodeEulerToRotation")
        switch_node_type(layout, "FunctionNodeInvertRotation")
        switch_node_type(layout, "FunctionNodeRotateEuler")
        switch_node_type(layout, "FunctionNodeRotateVector")
        switch_node_type(layout, "FunctionNodeRotationToAxisAngle")
        switch_node_type(layout, "FunctionNodeRotationToEuler")
        switch_node_type(layout, "FunctionNodeRotationToQuaternion")
        switch_node_type(layout, "FunctionNodeQuaternionToRotation")


class NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_MATH(Menu):
    bl_label = "Math"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "FunctionNodeBooleanMath")
        switch_node_type(layout, "ShaderNodeClamp")
        switch_node_type(layout, "FunctionNodeCompare")
        switch_node_type(layout, "ShaderNodeFloatCurve")
        switch_node_type(layout, "FunctionNodeFloatToInt")
        switch_node_type(layout, "ShaderNodeMapRange")
        switch_node_type(layout, "ShaderNodeMath")
        switch_node_type(layout, "ShaderNodeMix")


class NODE_MT_NWSwitchNodes_category_GEO_UV(Menu):
    bl_label = "UV"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeUVPackIslands")
        switch_node_type(layout, "GeometryNodeUVUnwrap")


class NODE_MT_NWSwitchNodes_category_GEO_VECTOR(Menu):
    bl_label = "Vector"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "ShaderNodeVectorCurve")
        switch_node_type(layout, "ShaderNodeVectorMath")
        switch_node_type(layout, "ShaderNodeVectorRotate")
        layout.separator()
        switch_node_type(layout, "ShaderNodeCombineXYZ")
        props = switch_node_type(layout, "ShaderNodeMix", label=iface_("Mix Vector"))
        ops = props.settings.add()
        ops.name = "data_type"
        ops.value = "'VECTOR'"
        switch_node_type(layout, "ShaderNodeSeparateXYZ")


class NODE_MT_NWSwitchNodes_category_GEO_VOLUME(Menu):
    bl_label = "Volume"
    bl_options = {'SEARCH_ON_KEY_PRESS'}
    bl_translation_context = i18n_contexts.id_id

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeVolumeCube")
        switch_node_type(layout, "GeometryNodeVolumeToMesh")
        if context.preferences.experimental.use_new_volume_nodes:
            layout.separator()
            switch_node_type(layout, "GeometryNodeMeanFilterSDFVolume")
            switch_node_type(layout, "GeometryNodeOffsetSDFVolume")
            switch_node_type(layout, "GeometryNodeSampleVolume")
            switch_node_type(layout, "GeometryNodeSDFVolumeSphere")
            switch_node_type(layout, "GeometryNodeInputSignedDistance")


class NODE_MT_geometry_node_switch_all(Menu):
    bl_label = "Switch Node Type"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        snode = context.space_data
        layout = self.layout
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_ATTRIBUTE")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_INPUT")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_OUTPUT")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_CURVE")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_INSTANCE")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_MESH")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_POINT")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_VOLUME")
        #layout.separator()
        #layout.menu("NODE_MT_NWSwitchNodes_category_simulation")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_MATERIAL")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_TEXTURE")
        layout.menu("NODE_MT_NWSwitchNodes_category_GEO_UTILITIES")
        layout.separator()
        layout.menu("NODE_MT_NWSwitchNodes_category_group")
        layout.menu("NODE_MT_NWSwitchNodes_category_layout")


classes = (
    NODE_MT_geometry_node_switch_all,
    NODE_MT_NWSwitchNodes_category_GEO_ATTRIBUTE,
    NODE_MT_NWSwitchNodes_category_GEO_INPUT,
    NODE_MT_NWSwitchNodes_category_GEO_INPUT_CONSTANT,
    NODE_MT_NWSwitchNodes_category_GEO_INPUT_GROUP,
    NODE_MT_NWSwitchNodes_category_GEO_INPUT_SCENE,
    NODE_MT_NWSwitchNodes_category_GEO_OUTPUT,
    NODE_MT_NWSwitchNodes_category_GEO_CURVE,
    NODE_MT_NWSwitchNodes_category_GEO_CURVE_READ,
    NODE_MT_NWSwitchNodes_category_GEO_CURVE_SAMPLE,
    NODE_MT_NWSwitchNodes_category_GEO_CURVE_WRITE,
    NODE_MT_NWSwitchNodes_category_GEO_CURVE_OPERATIONS,
    NODE_MT_NWSwitchNodes_category_GEO_PRIMITIVES_CURVE,
    NODE_MT_NWSwitchNodes_category_curve_topology,
    NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY,
    NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_READ,
    NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_WRITE,
    NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_OPERATIONS,
    NODE_MT_NWSwitchNodes_category_GEO_GEOMETRY_SAMPLE,
    NODE_MT_NWSwitchNodes_category_GEO_INSTANCE,
    NODE_MT_NWSwitchNodes_category_GEO_MESH,
    NODE_MT_NWSwitchNodes_category_GEO_MESH_READ,
    NODE_MT_NWSwitchNodes_category_GEO_MESH_SAMPLE,
    NODE_MT_NWSwitchNodes_category_GEO_MESH_WRITE,
    NODE_MT_NWSwitchNodes_category_GEO_MESH_OPERATIONS,
    NODE_MT_NWSwitchNodes_category_GEO_UV,
    NODE_MT_NWSwitchNodes_category_PRIMITIVES_MESH,
    NODE_MT_NWSwitchNodes_category_mesh_topology,
    NODE_MT_NWSwitchNodes_category_GEO_POINT,
    #NODE_MT_NWSwitchNodes_category_simulation,
    NODE_MT_NWSwitchNodes_category_GEO_VOLUME,
    NODE_MT_NWSwitchNodes_category_GEO_MATERIAL,
    NODE_MT_NWSwitchNodes_category_GEO_TEXTURE,
    NODE_MT_NWSwitchNodes_category_GEO_UTILITIES,
    NODE_MT_NWSwitchNodes_category_GEO_COLOR,
    NODE_MT_NWSwitchNodes_category_GEO_TEXT,
    NODE_MT_NWSwitchNodes_category_GEO_VECTOR,
    NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_FIELD,
    NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_MATH,
    NODE_MT_NWSwitchNodes_category_GEO_UTILITIES_ROTATION,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)