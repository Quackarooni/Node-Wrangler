import bpy
from bl_ui import node_add_menu
from . import operators
from .utils.nodes import get_active_tree
from .utils.nodes import fw_check

menu_classes = []
addon_draw_funcs = []
spacing = 0.65

from bpy.app.translations import (
    pgettext_iface as iface_,
    contexts as i18n_contexts,
)
#taken from https://github.com/blender/blender/blob/master/release/scripts/startup/bl_ui/node_add_menu.py
def switch_node_type(layout, node_type, *, label=None):
    """Add a node type to a menu."""
    bl_rna = bpy.types.Node.bl_rna_get_subclass(node_type)
    if not label:
        label = bl_rna.name if bl_rna else iface_("Unknown")
    translation_context = bl_rna.translation_context if bl_rna else i18n_contexts.default
    #props = layout.operator("node.add_node", text=label, text_ctxt=translation_context)

    props = layout.operator(operators.NWSwitchNodeType.bl_idname, text=label, text_ctxt=translation_context)
    props.to_type = node_type
    return props


class MenuBaseClass(bpy.types.Menu):
    bl_label = "Menu"
    bl_space_type = "NODE_EDITOR"

    items = []

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        return fw_check(context) and (tree_type == 'GeometryNodeTree')

    def draw(self, context):
        pass

class NODE_MT_NWSwitchNodes_GN(MenuBaseClass):
    bl_label = "Add"
    bl_idname = "NODE_MT_NWSwitchNodes_GN"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'

        layout.menu(NODE_MT_NWSwitchNodes_GN_attribute.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_input.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_output.bl_idname)
        layout.separator(factor=spacing)

        layout.menu(NODE_MT_NWSwitchNodes_GN_geometry.bl_idname)
        layout.separator(factor=spacing)
        layout.menu(NODE_MT_NWSwitchNodes_GN_curve.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_instance.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_point.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_volume.bl_idname)
        layout.separator(factor=spacing)
        
        layout.menu(NODE_MT_NWSwitchNodes_GN_material.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_texture.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_utilities.bl_idname)

        layout.separator(factor=spacing)
        layout.menu(NODE_MT_NWSwitchNodes_GN_group.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_layout.bl_idname)

class NODE_MT_NWSwitchNodes_GN_attribute(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_attribute"
    bl_label = "Attribute"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeAttributeStatistic")
        switch_node_type(layout, "GeometryNodeAttributeDomainSize")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeBlurAttribute")
        switch_node_type(layout, "GeometryNodeCaptureAttribute")
        switch_node_type(layout, "GeometryNodeStoreNamedAttribute")
        switch_node_type(layout, "GeometryNodeRemoveAttribute")

class NODE_MT_NWSwitchNodes_GN_input(MenuBaseClass):
    bl_label = "Input"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_input"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.menu(NODE_MT_NWSwitchNodes_GN_input_constant.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_input_group.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_input_scene.bl_idname)

class NODE_MT_NWSwitchNodes_GN_input_group(MenuBaseClass):
    bl_label = "Group"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_input_group"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "NodeGroupInput")

class NODE_MT_NWSwitchNodes_GN_input_scene(MenuBaseClass):
    bl_label = "Scene"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_input_scene"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeCollectionInfo")
        switch_node_type(layout, "GeometryNodeImageInfo")
        switch_node_type(layout, "GeometryNodeIsViewport")
        switch_node_type(layout, "GeometryNodeObjectInfo")
        switch_node_type(layout, "GeometryNodeSelfObject")
        switch_node_type(layout, "GeometryNodeInputSceneTime")

class NODE_MT_NWSwitchNodes_GN_input_constant(MenuBaseClass):
    bl_label = "Constant"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_input_constant"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "FunctionNodeInputBool")
        switch_node_type(layout, "FunctionNodeInputColor")
        switch_node_type(layout, "FunctionNodeInputInt")
        switch_node_type(layout, "GeometryNodeInputMaterial")
        switch_node_type(layout, "FunctionNodeInputString")
        switch_node_type(layout, "ShaderNodeValue")
        switch_node_type(layout, "FunctionNodeInputVector")

class NODE_MT_NWSwitchNodes_GN_output(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_output"
    bl_label = "Output"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "NodeGroupOutput")
        switch_node_type(layout, "GeometryNodeViewer")
        
class NODE_MT_NWSwitchNodes_GN_geometry(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_geometry"
    bl_label = "Geometry"

    def draw(self, _context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.menu(NODE_MT_NWSwitchNodes_GN_geometry_read.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_geometry_sample.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_geometry_write.bl_idname)
        layout.separator(factor=spacing)
        layout.menu(NODE_MT_NWSwitchNodes_GN_geometry_operations.bl_idname)
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeJoinGeometry")
        switch_node_type(layout, "GeometryNodeGeometryToInstance")

class NODE_MT_NWSwitchNodes_GN_geometry_read(MenuBaseClass):
    bl_label = "Read"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_geometry_read"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeInputID")
        switch_node_type(layout, "GeometryNodeInputIndex")
        switch_node_type(layout, "GeometryNodeInputNamedAttribute")
        switch_node_type(layout, "GeometryNodeInputNormal")
        switch_node_type(layout, "GeometryNodeInputPosition")
        switch_node_type(layout, "GeometryNodeInputRadius")

class NODE_MT_NWSwitchNodes_GN_geometry_sample(MenuBaseClass):
    bl_label = "Sample"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_geometry_sample"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeProximity")
        switch_node_type(layout, "GeometryNodeRaycast")
        switch_node_type(layout, "GeometryNodeSampleIndex")
        switch_node_type(layout, "GeometryNodeSampleNearest")

class NODE_MT_NWSwitchNodes_GN_geometry_write(MenuBaseClass):
    bl_label = "Write"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_geometry_write"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSetID")
        switch_node_type(layout, "GeometryNodeSetPosition")

class NODE_MT_NWSwitchNodes_GN_geometry_operations(MenuBaseClass):
    bl_label = "Operations"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_geometry_operations"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeBoundBox")
        switch_node_type(layout, "GeometryNodeConvexHull")
        switch_node_type(layout, "GeometryNodeDeleteGeometry")
        switch_node_type(layout, "GeometryNodeDuplicateElements")
        switch_node_type(layout, "GeometryNodeMergeByDistance")
        switch_node_type(layout, "GeometryNodeTransform")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeSeparateComponents")
        switch_node_type(layout, "GeometryNodeSeparateGeometry")
        
class NODE_MT_NWSwitchNodes_GN_mesh(MenuBaseClass):
    bl_label = "Mesh"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh_read.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh_sample.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh_write.bl_idname)
        layout.separator(factor=spacing)
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh_operations.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh_primitives.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh_topology.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_mesh_UV.bl_idname)
        
class NODE_MT_NWSwitchNodes_GN_mesh_read(MenuBaseClass):
    bl_label = "Read"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh_read"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeInputMeshEdgeAngle")
        switch_node_type(layout, "GeometryNodeInputMeshEdgeNeighbors")
        switch_node_type(layout, "GeometryNodeInputMeshEdgeVertices")
        switch_node_type(layout, "GeometryNodeEdgesToFaceGroups")
        switch_node_type(layout, "GeometryNodeInputMeshFaceArea")
        switch_node_type(layout, "GeometryNodeInputMeshFaceNeighbors")
        switch_node_type(layout, "GeometryNodeMeshFaceSetBoundaries")
        switch_node_type(layout, "GeometryNodeInputMeshFaceIsPlanar")
        switch_node_type(layout, "GeometryNodeInputShadeSmooth")
        switch_node_type(layout, "GeometryNodeInputMeshIsland")
        switch_node_type(layout, "GeometryNodeInputShortestEdgePaths")
        switch_node_type(layout, "GeometryNodeInputMeshVertexNeighbors")

class NODE_MT_NWSwitchNodes_GN_mesh_operations(MenuBaseClass):
    bl_label = "Operations"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh_operations"

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
        switch_node_type(layout, "GeometryNodeMeshToVolume")
        switch_node_type(layout, "GeometryNodeScaleElements")
        switch_node_type(layout, "GeometryNodeSplitEdges")
        switch_node_type(layout, "GeometryNodeSubdivideMesh")
        switch_node_type(layout, "GeometryNodeSubdivisionSurface")
        switch_node_type(layout, "GeometryNodeTriangulate")

class NODE_MT_NWSwitchNodes_GN_mesh_write(MenuBaseClass):
    bl_label = "Write"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh_write"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSetShadeSmooth")

class NODE_MT_NWSwitchNodes_GN_mesh_sample(MenuBaseClass):
    bl_label = "Sample"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh_sample"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSampleNearestSurface")
        switch_node_type(layout, "GeometryNodeSampleUVSurface")

class NODE_MT_NWSwitchNodes_GN_mesh_primitives(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh_primitives"
    bl_label = "Primitives"

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

class NODE_MT_NWSwitchNodes_GN_mesh_topology(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh_topology"
    bl_label = "Topology"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeCornersOfFace"),
        switch_node_type(layout, "GeometryNodeCornersOfVertex"),
        switch_node_type(layout, "GeometryNodeEdgesOfCorner"),
        switch_node_type(layout, "GeometryNodeEdgesOfVertex"),
        switch_node_type(layout, "GeometryNodeFaceOfCorner"),
        switch_node_type(layout, "GeometryNodeOffsetCornerInFace"),
        switch_node_type(layout, "GeometryNodeVertexOfCorner")
        
class NODE_MT_NWSwitchNodes_GN_curve(MenuBaseClass):
    bl_label = "Curve"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_curve"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.menu(NODE_MT_NWSwitchNodes_GN_curve_read.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_curve_sample.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_curve_write.bl_idname)
        layout.separator(factor=spacing)
        layout.menu(NODE_MT_NWSwitchNodes_GN_curve_operations.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_curve_primitives.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_curve_topology.bl_idname)
        
class NODE_MT_NWSwitchNodes_GN_curve_read(MenuBaseClass):
    bl_label = "Read"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_curve_read"

    def draw(self, context):
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

class NODE_MT_NWSwitchNodes_GN_curve_sample(MenuBaseClass):
    bl_label = "Sample"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_curve_sample"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSampleCurve")

class NODE_MT_NWSwitchNodes_GN_curve_operations(MenuBaseClass):
    bl_label = "Operations"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_curve_operations"

    def draw(self, context):
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

class NODE_MT_NWSwitchNodes_GN_curve_write(MenuBaseClass):
    bl_label = "Write"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_curve_write"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeSetCurveNormal")
        switch_node_type(layout, "GeometryNodeSetCurveRadius")
        switch_node_type(layout, "GeometryNodeSetCurveTilt")
        switch_node_type(layout, "GeometryNodeSetCurveHandlePositions")
        switch_node_type(layout, "GeometryNodeCurveSetHandles")
        switch_node_type(layout, "GeometryNodeSetSplineCyclic")
        switch_node_type(layout, "GeometryNodeSetSplineResolution")
        switch_node_type(layout, "GeometryNodeCurveSplineType")

class NODE_MT_NWSwitchNodes_GN_curve_primitives(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_curve_primitives"
    bl_label = "Primitives"

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
        
class NODE_MT_NWSwitchNodes_GN_curve_topology(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_curve_topology"
    bl_label = "Topology"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeOffsetPointInCurve")
        switch_node_type(layout, "GeometryNodeCurveOfPoint")
        switch_node_type(layout, "GeometryNodePointsOfCurve")
        
class NODE_MT_NWSwitchNodes_GN_instance(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_instance"
    bl_label = "Instances"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeInstanceOnPoints")
        switch_node_type(layout, "GeometryNodeInstancesToPoints")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeRealizeInstances")
        switch_node_type(layout, "GeometryNodeRotateInstances")
        switch_node_type(layout, "GeometryNodeScaleInstances")
        switch_node_type(layout, "GeometryNodeTranslateInstances")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeInputInstanceRotation")
        switch_node_type(layout, "GeometryNodeInputInstanceScale")
        
class NODE_MT_NWSwitchNodes_GN_point(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_point"
    bl_label = "Point"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeDistributePointsInVolume")
        switch_node_type(layout, "GeometryNodeDistributePointsOnFaces")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodePoints")
        switch_node_type(layout, "GeometryNodePointsToVertices")
        switch_node_type(layout, "GeometryNodePointsToVolume")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeSetPointRadius")
        
class NODE_MT_NWSwitchNodes_GN_volume(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_volume"
    bl_label = "Volume"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeVolumeCube")
        switch_node_type(layout, "GeometryNodeVolumeToMesh")
        
class NODE_MT_NWSwitchNodes_GN_material(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_material"
    bl_label = "Material"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeReplaceMaterial")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeInputMaterialIndex")
        switch_node_type(layout, "GeometryNodeMaterialSelection")
        layout.separator(factor=spacing)
        switch_node_type(layout, "GeometryNodeSetMaterial")
        switch_node_type(layout, "GeometryNodeSetMaterialIndex")
        
class NODE_MT_NWSwitchNodes_GN_texture(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_texture"
    bl_label = "Texture"

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
        
class NODE_MT_NWSwitchNodes_GN_utilities(MenuBaseClass):
    bl_label = "Utilities"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_utilities"

    def draw(self, context):
        layout = self.layout
        layout.menu(NODE_MT_NWSwitchNodes_GN_utilities_color.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_utilities_text.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_utilities_vector.bl_idname)
        layout.separator(factor=spacing)
        layout.menu(NODE_MT_NWSwitchNodes_GN_utilities_field.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_utilities_math.bl_idname)
        layout.menu(NODE_MT_NWSwitchNodes_GN_utilities_rotation.bl_idname)
        layout.separator(factor=spacing)
        switch_node_type(layout, "FunctionNodeRandomValue")
        switch_node_type(layout, "GeometryNodeSwitch")

class NODE_MT_NWSwitchNodes_GN_utilities_color(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_utilities_color"
    bl_label = "Color"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "ShaderNodeValToRGB", label='Color Ramp')
        switch_node_type(layout, "ShaderNodeRGBCurve")
        layout.separator(factor=spacing)
        switch_node_type(layout, "FunctionNodeCombineColor")
        props = switch_node_type(layout, "ShaderNodeMix", label=iface_("Mix Color"))
        ops = props.settings.add()
        ops.name = "data_type"
        ops.value = "'RGBA'"
        switch_node_type(layout, "FunctionNodeSeparateColor")
        
        
class NODE_MT_NWSwitchNodes_GN_utilities_text(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_utilities_text"
    bl_label = "Text"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeStringJoin")
        switch_node_type(layout, "FunctionNodeReplaceString")
        switch_node_type(layout, "FunctionNodeSliceString")
        layout.separator(factor=spacing)
        switch_node_type(layout, "FunctionNodeStringLength")
        switch_node_type(layout, "GeometryNodeStringToCurves")
        switch_node_type(layout, "FunctionNodeValueToString")
        layout.separator(factor=spacing)
        switch_node_type(layout, "FunctionNodeInputSpecialCharacters")
        

class NODE_MT_NWSwitchNodes_GN_utilities_vector(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_utilities_vector"
    bl_label = "Vector"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "ShaderNodeVectorCurve")
        switch_node_type(layout, "ShaderNodeVectorMath")
        switch_node_type(layout, "ShaderNodeVectorRotate")
        layout.separator(factor=spacing)
        switch_node_type(layout, "ShaderNodeCombineXYZ")
        props = switch_node_type(layout, "ShaderNodeMix", label=iface_("Mix Vector"))
        ops = props.settings.add()
        ops.name = "data_type"
        ops.value = "'VECTOR'"
        switch_node_type(layout, "ShaderNodeSeparateXYZ")
        

class NODE_MT_NWSwitchNodes_GN_utilities_field(MenuBaseClass):
    bl_label = "Field"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_utilities_field"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeAccumulateField")
        switch_node_type(layout, "GeometryNodeFieldAtIndex")
        switch_node_type(layout, "GeometryNodeFieldOnDomain")

class NODE_MT_NWSwitchNodes_GN_utilities_rotation(MenuBaseClass):
    bl_label = "Rotation"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_utilities_rotation"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "FunctionNodeAlignEulerToVector")
        switch_node_type(layout, "FunctionNodeRotateEuler")

class NODE_MT_NWSwitchNodes_GN_utilities_math(MenuBaseClass):
    bl_label = "Math"
    bl_idname = "NODE_MT_NWSwitchNodes_GN_utilities_math"

    def draw(self, context):
        layout = self.layout
        switch_node_type(layout, "FunctionNodeBooleanMath")
        switch_node_type(layout, "ShaderNodeClamp")
        switch_node_type(layout, "FunctionNodeCompare")
        switch_node_type(layout, "ShaderNodeFloatCurve")
        switch_node_type(layout, "FunctionNodeFloatToInt")
        switch_node_type(layout, "ShaderNodeMapRange")
        switch_node_type(layout, "ShaderNodeMath")

        props = switch_node_type(layout, "ShaderNodeMix")
        ops = props.settings.add()
        ops.name = "data_type"
        ops.value = "'FLOAT'"


class NODE_MT_NWSwitchNodes_GN_mesh_UV(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_mesh_UV"
    bl_label = "UV"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "GeometryNodeUVPackIslands")
        switch_node_type(layout, "GeometryNodeUVUnwrap")
        
        
class NODE_MT_NWSwitchNodes_GN_group(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_group"
    bl_label = "Group"

    @classmethod
    def poll(cls, context):
        return fw_check(context)

    def draw(self, context):
        layout = self.layout
        space_node = context.space_data
        node_tree = space_node.edit_tree
        all_node_groups = context.blend_data.node_groups

        if node_tree in all_node_groups.values():
            layout.separator()
            switch_node_type(layout, "NodeGroupInput")
            switch_node_type(layout, "NodeGroupOutput")

        if node_tree:
            from nodeitems_builtins import node_tree_group_type

            groups = [
                group for group in context.blend_data.node_groups
                if (group.bl_idname == node_tree.bl_idname and
                    not group.contains_tree(node_tree) and
                    not group.name.startswith('.'))
            ]
            if groups:
                layout.separator()
                for group in groups:
                    props = switch_node_type(layout, node_tree_group_type[group.bl_idname], label=group.name)
                    ops = props.settings.add()
                    ops.name = "node_tree"
                    ops.value = "bpy.data.node_groups[%r]" % group.name
        
        
class NODE_MT_NWSwitchNodes_GN_layout(MenuBaseClass):
    bl_idname = "NODE_MT_NWSwitchNodes_GN_layout"
    bl_label = "Layout"

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "NodeFrame")
        switch_node_type(layout, "NodeReroute")

classes = (
        NODE_MT_NWSwitchNodes_GN,
        NODE_MT_NWSwitchNodes_GN_attribute,
        NODE_MT_NWSwitchNodes_GN_input,
        NODE_MT_NWSwitchNodes_GN_input_constant,
        NODE_MT_NWSwitchNodes_GN_input_group,
        NODE_MT_NWSwitchNodes_GN_input_scene,
        NODE_MT_NWSwitchNodes_GN_output,
        NODE_MT_NWSwitchNodes_GN_geometry,
        NODE_MT_NWSwitchNodes_GN_geometry_read,
        NODE_MT_NWSwitchNodes_GN_geometry_sample,
        NODE_MT_NWSwitchNodes_GN_geometry_write,
        NODE_MT_NWSwitchNodes_GN_geometry_operations,
        NODE_MT_NWSwitchNodes_GN_mesh,
        NODE_MT_NWSwitchNodes_GN_mesh_read,
        NODE_MT_NWSwitchNodes_GN_mesh_sample,
        NODE_MT_NWSwitchNodes_GN_mesh_write,
        NODE_MT_NWSwitchNodes_GN_mesh_operations,
        NODE_MT_NWSwitchNodes_GN_mesh_primitives,
        NODE_MT_NWSwitchNodes_GN_mesh_topology,
        NODE_MT_NWSwitchNodes_GN_curve,
        NODE_MT_NWSwitchNodes_GN_curve_read,
        NODE_MT_NWSwitchNodes_GN_curve_sample,
        NODE_MT_NWSwitchNodes_GN_curve_operations,
        NODE_MT_NWSwitchNodes_GN_curve_write,
        NODE_MT_NWSwitchNodes_GN_curve_primitives,
        NODE_MT_NWSwitchNodes_GN_curve_topology,
        NODE_MT_NWSwitchNodes_GN_instance,
        NODE_MT_NWSwitchNodes_GN_point,
        NODE_MT_NWSwitchNodes_GN_volume,
        NODE_MT_NWSwitchNodes_GN_material,
        NODE_MT_NWSwitchNodes_GN_texture,
        NODE_MT_NWSwitchNodes_GN_utilities,
        NODE_MT_NWSwitchNodes_GN_utilities_color,
        NODE_MT_NWSwitchNodes_GN_utilities_text,
        NODE_MT_NWSwitchNodes_GN_utilities_vector,
        NODE_MT_NWSwitchNodes_GN_utilities_field,
        NODE_MT_NWSwitchNodes_GN_utilities_rotation,
        NODE_MT_NWSwitchNodes_GN_utilities_math,
        NODE_MT_NWSwitchNodes_GN_mesh_UV,
        NODE_MT_NWSwitchNodes_GN_group,
        NODE_MT_NWSwitchNodes_GN_layout,
        )

def register():  
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


