# SPDX-FileCopyrightText: 2019-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Panel, Menu
from bpy.props import StringProperty

from . import operators

from .utils.constants import (
    blend_types, 
    blend_types_menu_dict, 
    geo_combine_operations, 
    operations, 
    operations_menu_dict,
    string_operations,
    shader_operations,
    vector_operations,
    vector_operations_menu_dict,
    boolean_operations,
    boolean_operations_menu_dict
    )
from .utils.nodes import get_nodes_links, fw_check, NWBase, fetch_user_preferences
import itertools


def drawlayout(context, layout, mode='non-panel'):
    tree_type = context.space_data.tree_type
    prefs = fetch_user_preferences()

    col = layout.column(align=True)
    col.menu(NWMergeNodesMenu.bl_idname)
    col.separator()

    if mode == 'panel':
        box = col.box()
        show_binary = prefs.merge_binary_mode in ('AUTO', 'CHAIN')
        show_ternary = prefs.merge_ternary_mode in ('AUTO', 'CHAIN')

        box.label(text="Binary Merge Mode:")
        box.prop(prefs, "merge_binary_mode", text="")
        if show_binary:
            box.prop(prefs, "prefer_first_socket_binary")

        box.label(text="Ternary Merge Mode:")
        box.prop(prefs, "merge_ternary_mode", text="")
        if show_ternary:
            box.prop(prefs, "prefer_first_socket_ternary")

    col.separator()

    col = layout.column(align=True)
    #col.menu(NWSwitchNodeTypeMenu.bl_idname, text="Switch Node Type")
    tree_type = context.space_data.tree_type
    if tree_type == 'GeometryNodeTree':
        col.menu("NODE_MT_geometry_node_switch_all")
    elif tree_type == 'CompositorNodeTree':
        col.menu("NODE_MT_compositor_node_switch_all")
    elif tree_type == 'ShaderNodeTree':
        col.menu("NODE_MT_shader_node_switch_all")
    elif tree_type == 'TextureNodeTree':
        col.menu("NODE_MT_texture_node_switch_all")

    col.separator()

    if tree_type == 'ShaderNodeTree':
        col = layout.column(align=True)
        col.operator(operators.NWAddTextureSetup.bl_idname, text="Add Texture Setup", icon='NODE_SEL')
        col.operator(operators.NWAddPrincipledSetup.bl_idname, text="Add Principled Setup", icon='NODE_SEL')
        col.separator()

    col = layout.column(align=True)
    col.operator(operators.NWDetachOutputs.bl_idname, icon='UNLINKED')
    col.operator(operators.NWSwapLinks.bl_idname)
    col.menu(NWAddReroutesMenu.bl_idname, text="Add Reroutes", icon='LAYER_USED')
    col.separator()

    col = layout.column(align=True)
    col.menu(NWLinkActiveToSelectedMenu.bl_idname, text="Link Active To Selected", icon='LINKED')
    if tree_type != 'GeometryNodeTree':
        col.operator(operators.NWLinkToOutputNode.bl_idname, icon='DRIVER')
    col.separator()

    col = layout.column(align=True)
    if mode == 'panel':
        row = col.row(align=True)
        row.operator(operators.NWClearLabel.bl_idname).option = True
        row.operator(operators.NWModifyLabels.bl_idname)
    else:
        col.operator(operators.NWClearLabel.bl_idname).option = True
        col.operator(operators.NWModifyLabels.bl_idname)
    col.menu(NWBatchChangeNodesMenu.bl_idname, text="Batch Change")
    col.separator()
    col.menu(NWCopyToSelectedMenu.bl_idname, text="Copy to Selected")
    col.separator()

    col = layout.column(align=True)
    if tree_type == 'CompositorNodeTree':
        col.operator(operators.NWResetBG.bl_idname, icon='ZOOM_PREVIOUS')
    if tree_type != 'GeometryNodeTree':
        col.operator(operators.NWReloadImages.bl_idname, icon='FILE_REFRESH')
    col.separator()

    col = layout.column(align=True)
    col.operator(operators.NWFrameSelected.bl_idname, icon='STICKY_UVS_LOC')
    col.separator()

    col = layout.column(align=True)
    col.operator(operators.NWAlignNodes.bl_idname, text='Auto-Align Nodes', icon='CENTER_ONLY').mode = 'AUTOMATIC'
    if mode == 'panel':
        row = col.row(align=True)
        row.operator(operators.NWAlignNodes.bl_idname, text='Align X').mode = 'HORIZONTAL'
        row.operator(operators.NWAlignNodes.bl_idname, text='Align Y').mode = 'VERTICAL'
    else:
        col.operator(operators.NWAlignNodes.bl_idname, text='Align X').mode = 'HORIZONTAL'
        col.operator(operators.NWAlignNodes.bl_idname, text='Align Y').mode = 'VERTICAL'

    col.separator()

    col = layout.column(align=True)
    col.operator(operators.NWDeleteUnused.bl_idname, icon='CANCEL')
    col.separator()


class NodeWranglerPanel(Panel, NWBase):
    bl_idname = "NODE_PT_fw_node_wrangler"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Forked Wrangler"
    bl_region_type = "UI"
    bl_category = "Forked Wrangler"

    prepend: StringProperty(
        name='prepend',
    )
    append: StringProperty()
    remove: StringProperty()

    def draw(self, context):
        self.layout.label(text="(Quick access: Shift+W)")
        drawlayout(context, self.layout, mode='panel')


#
#  M E N U S
#
class NodeWranglerMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_node_wrangler_menu"
    bl_label = "Node Wrangler"

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        drawlayout(context, self.layout)


class NWMergeNodesMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_nodes_menu"
    bl_label = "Merge Selected Nodes"

    def draw(self, context):
        type = context.space_data.tree_type
        layout = self.layout
        if type == 'ShaderNodeTree':
            layout.menu(NWMergeShadersMenu.bl_idname)            
            layout.separator()
            layout.menu(NWMergeMixMenu.bl_idname)
            layout.menu(NWMergeMathMenu.bl_idname)
            layout.menu(NWMergeVectorMathMenu.bl_idname)

        elif type == 'GeometryNodeTree':
            layout.menu(NWMergeGeometryMenu.bl_idname)
            layout.separator()
            layout.menu(NWMergeMixMenu.bl_idname)
            layout.menu(NWMergeMathMenu.bl_idname)
            layout.menu(NWMergeVectorMathMenu.bl_idname)
            layout.separator()
            layout.menu(NWMergeBoolMenu.bl_idname)
            layout.menu(NWMergeStringMenu.bl_idname)
        else:
            layout.menu(NWMergeMixMenu.bl_idname)
            layout.menu(NWMergeMathMenu.bl_idname)

            props = layout.operator(operators.NWMergeNodesRefactored.bl_idname, text="Use Z-Combine Nodes")
            props.merge_type = 'Z_COMBINE'

            props = layout.operator(operators.NWMergeNodesRefactored.bl_idname, text="Use Alpha Over Nodes")
            props.merge_type = 'ALPHA_OVER'

class NWMergeGeometryMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_geometry_menu"
    bl_label = "Use Geometry Nodes"

    def draw(self, context):
        layout = self.layout
        # The boolean node + Join Geometry node
        for operation, name, description in geo_combine_operations:
            props = layout.operator(operators.NWMergeNodesRefactored.bl_idname, text=name)
            props.operation = operation
            props.merge_type = 'GEOMETRY'


class NWMergeShadersMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_shaders_menu"
    bl_label = "Use Shaders"

    def draw(self, context):
        layout = self.layout
        render_engine = context.scene.render.engine

        for operation, name, description in shader_operations:
            if operation == 'SHADER_TO_RGB':
                if render_engine == 'BLENDER_EEVEE':
                    props = layout.operator(operators.NWMergeNodesRefactored.bl_idname, text=name)
            else:
                props = layout.operator(operators.NWMergeNodesRefactored.bl_idname, text=name)
            props.operation = operation
            props.merge_type = 'SHADER'


class NWMergeMixMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_mix_menu"
    bl_label = "Use Mix Color Nodes"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()   

        for key, items in blend_types_menu_dict.items():
            col.separator(factor=1.0)
            for operation, name, description in items:
                props = col.operator(operators.NWMergeNodesRefactored.bl_idname, text=name, icon='NONE')
                props.operation = operation
                props.merge_type = 'MIX_COLOR'   


class NWMergeMathMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_math_menu"
    bl_label = "Use Math Nodes"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        for key, items in operations_menu_dict.items():
            col = row.column()
            col.label(text=key, icon='NONE')
            col.separator(factor=1.0)
            for operation, name, description in items:
                if operation == "LayoutSeparator":
                    col.separator(factor=1.0)
                else:
                    props = col.operator(operators.NWMergeNodesRefactored.bl_idname, text=name, icon='NONE')
                    props.operation = operation
                    props.merge_type = 'MATH'


class NWMergeVectorMathMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_vector_math_menu"
    bl_label = "Use Vector Math Nodes"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        for key, items in vector_operations_menu_dict.items():
            col = row.column()
            col.label(text=key, icon='NONE')
            col.separator(factor=1.0)
            for operation, name, description in items:
                if operation == "LayoutSeparator":
                    col.separator(factor=1.0)
                else:
                    props = col.operator(operators.NWMergeNodesRefactored.bl_idname, text=name, icon='NONE')
                    props.operation = operation
                    props.merge_type = 'VECTOR'


class NWMergeStringMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_string_menu"
    bl_label = "Use String Nodes"

    def draw(self, context):
        layout = self.layout
        for operation, name, description in string_operations:
            props = layout.operator(operators.NWMergeNodesRefactored.bl_idname, text=name)
            props.operation = operation
            props.merge_type = 'STRING'

class NWMergeBoolMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_merge_bool_menu"
    bl_label = "Use Boolean Math Nodes"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()   

        for key, items in boolean_operations_menu_dict.items():
            col.separator(factor=1.0)
            for operation, name, description in items:
                props = col.operator(operators.NWMergeNodesRefactored.bl_idname, text=name)
                props.operation = operation
                props.merge_type = 'BOOLEAN'


class NWConnectionListOutputs(Menu, NWBase):
    bl_idname = "NODE_MT_fw_connection_list_out"
    bl_label = "From:"

    def draw(self, context):
        layout = self.layout
        nodes, links = get_nodes_links(context)

        n1 = nodes[context.scene.NWLazySource]
        for index, output in enumerate(n1.outputs):
            # Only show sockets that are exposed.
            if output.enabled:
                layout.operator(
                    operators.NWCallInputsMenu.bl_idname,
                    text=output.name,
                    icon="RADIOBUT_OFF").from_socket = index


class NWConnectionListInputs(Menu, NWBase):
    bl_idname = "NODE_MT_fw_connection_list_in"
    bl_label = "To:"

    def draw(self, context):
        layout = self.layout
        nodes, links = get_nodes_links(context)

        n2 = nodes[context.scene.NWLazyTarget]

        for index, input in enumerate(n2.inputs):
            # Only show sockets that are exposed.
            # This prevents, for example, the scale value socket
            # of the vector math node being added to the list when
            # the mode is not 'SCALE'.
            if input.enabled:
                op = layout.operator(operators.NWMakeLink.bl_idname, text=input.name, icon="FORWARD")
                op.from_socket = context.scene.NWSourceSocket
                op.to_socket = index

class NWBatchChangeNodesMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_batch_change_nodes_menu"
    bl_label = "Batch Change Selected Nodes"

    def draw(self, context):
        layout = self.layout
        layout.menu(NWBatchChangeBlendTypeMenu.bl_idname)
        layout.menu(NWBatchChangeOperationMenu.bl_idname)
        if context.space_data.tree_type in ('GeometryNodeTree', 'ShaderNodeTree'):
            layout.menu(NWBatchChangeVectorOperationMenu.bl_idname)


        if context.space_data.tree_type == 'GeometryNodeTree':
            layout.separator()
            layout.menu(NWBatchChangeBoolMenu.bl_idname)


class NWBatchChangeBlendTypeMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_batch_change_blend_type_menu"
    bl_label = "Change Mix Blend Type"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        for key, items in blend_types_menu_dict.items():
            col.separator(factor=1.0)
            for operation, name, description in items:
                props = col.operator(operators.NWBatchChangeNodes.bl_idname, text=name, icon='NONE')
                props.blend_type = operation

class NWBatchChangeOperationMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_batch_change_operation_menu"
    bl_label = "Change Math Operation"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        for key, items in operations_menu_dict.items():
            col = row.column()
            col.label(text=key, icon='NONE')
            col.separator(factor=1.0)
            for operation, name, description in items:
                if operation == "LayoutSeparator":
                    col.separator(factor=1.0)
                else:
                    props = col.operator(operators.NWBatchChangeNodes.bl_idname, text=name, icon='NONE')
                    props.operation = operation

class NWBatchChangeBoolMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_batch_change_bool_menu"
    bl_label = "Change Boolean Operation"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()   

        for key, items in boolean_operations_menu_dict.items():
            col.separator(factor=1.0)
            for operation, name, description in items:
                props = col.operator(operators.NWBatchChangeNodes.bl_idname, text=name)
                props.bool_type = operation

class NWBatchChangeVectorOperationMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_batch_change_vector_operation_menu"
    bl_label = "Change Vector Operation"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        for key, items in vector_operations_menu_dict.items():
            col = row.column()
            col.label(text=key, icon='NONE')
            col.separator(factor=1.0)
            for operation, name, description in items:
                if operation == "LayoutSeparator":
                    col.separator(factor=1.0)
                else:
                    props = col.operator(operators.NWBatchChangeNodes.bl_idname, text=name)
                    props.vector_operation = operation


class NWCopyToSelectedMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_copy_node_properties_menu"
    bl_label = "Copy to Selected"

    def draw(self, context):
        layout = self.layout
        layout.operator(operators.NWCopySettings.bl_idname, text="Settings from Active")
        layout.menu(NWCopyLabelMenu.bl_idname)


class NWCopyLabelMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_copy_label_menu"
    bl_label = "Copy Label"

    def draw(self, context):
        layout = self.layout
        layout.operator(operators.NWCopyLabel.bl_idname, text="from Active Node's Label").option = 'FROM_ACTIVE'
        layout.operator(operators.NWCopyLabel.bl_idname, text="from Linked Node's Label").option = 'FROM_NODE'
        layout.operator(operators.NWCopyLabel.bl_idname, text="from Linked Output's Name").option = 'FROM_SOCKET'


class NWAddReroutesMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_add_reroutes_menu"
    bl_label = "Add Reroutes"
    bl_description = "Add Reroute Nodes to Selected Nodes' Outputs"

    def draw(self, context):
        layout = self.layout
        layout.operator(operators.NWAddReroutes.bl_idname, text="to All Outputs").option = 'ALL'
        layout.operator(operators.NWAddReroutes.bl_idname, text="to Loose Outputs").option = 'LOOSE'
        layout.operator(operators.NWAddReroutes.bl_idname, text="to Linked Outputs").option = 'LINKED'


class NWLinkActiveToSelectedMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_link_active_to_selected_menu"
    bl_label = "Link Active to Selected"

    def draw(self, context):
        layout = self.layout
        layout.menu(NWLinkStandardMenu.bl_idname)
        layout.menu(NWLinkUseNodeNameMenu.bl_idname)
        layout.menu(NWLinkUseOutputsNamesMenu.bl_idname)


class NWLinkStandardMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_link_standard_menu"
    bl_label = "To All Selected"

    def draw(self, context):
        layout = self.layout
        props = layout.operator(operators.NWLinkActiveToSelected.bl_idname, text="Don't Replace Links")
        props.replace = False
        props.use_node_name = False
        props.use_outputs_names = False
        props = layout.operator(operators.NWLinkActiveToSelected.bl_idname, text="Replace Links")
        props.replace = True
        props.use_node_name = False
        props.use_outputs_names = False


class NWLinkUseNodeNameMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_link_use_node_name_menu"
    bl_label = "Use Node Name/Label"

    def draw(self, context):
        layout = self.layout
        props = layout.operator(operators.NWLinkActiveToSelected.bl_idname, text="Don't Replace Links")
        props.replace = False
        props.use_node_name = True
        props.use_outputs_names = False
        props = layout.operator(operators.NWLinkActiveToSelected.bl_idname, text="Replace Links")
        props.replace = True
        props.use_node_name = True
        props.use_outputs_names = False


class NWLinkUseOutputsNamesMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_link_use_outputs_names_menu"
    bl_label = "Use Outputs Names"

    def draw(self, context):
        layout = self.layout
        props = layout.operator(operators.NWLinkActiveToSelected.bl_idname, text="Don't Replace Links")
        props.replace = False
        props.use_node_name = False
        props.use_outputs_names = True
        props = layout.operator(operators.NWLinkActiveToSelected.bl_idname, text="Replace Links")
        props.replace = True
        props.use_node_name = False
        props.use_outputs_names = True


class NWAttributeMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_fw_node_attribute_menu"
    bl_label = "Attributes"

    @classmethod
    def poll(cls, context):
        if fw_check(context):
            return context.space_data.tree_type == 'ShaderNodeTree'
        return False

    @staticmethod
    def fetch_attributes(context):
        mat = context.object.active_material
        deps = context.evaluated_depsgraph_get()

        def is_valid(obj):
            mesh = obj.data
            return hasattr(mesh, "materials") and hasattr(mesh, "attributes") and mat.name in mesh.materials
        
        valid_objects = tuple(obj for obj in deps.objects if is_valid(obj))

        for obj in valid_objects:
            for attr in obj.data.attributes:
                yield ("GEOMETRY", attr.name)

        for inst in deps.object_instances:
            if inst.is_instance and inst.parent in valid_objects:
                obj = inst.object
                if is_valid(obj):
                    for attr in obj.data.attributes:
                        yield ("GEOMETRY", attr.name)

        for obj in valid_objects:
            nodetrees = (m.node_group for m in obj.modifiers if m.type == 'NODES')
            for tree in nodetrees:
                for node in tree.nodes:
                    if node.bl_label != "Store Named Attribute" or node.mute is True:
                        continue

                    attr_name = node.inputs["Name"].default_value
                    if attr_name == "":
                        continue
                    
                    domain = "INSTANCER" if node.domain == "INSTANCE" else "GEOMETRY"
                    yield (domain, attr_name)


    def draw(self, context):
        layout = self.layout
        attrs = sorted(list(set(self.fetch_attributes(context))))

        if len(attrs) > 0:
            for attr_type, attr_name in attrs:
                props = layout.operator(operators.NWAddAttrNode.bl_idname, text=attr_name)
                props.attr_name = attr_name
                props.attr_type = attr_type

        else:
            layout.label(text="No attributes on objects with this material")


class NWNamedAttributeMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_fw_node_named_attribute_menu"
    bl_label = "Named Attributes"

    @classmethod
    def poll(cls, context):
        if fw_check(context):
            return context.space_data.tree_type == 'GeometryNodeTree'
        return False

    @staticmethod
    def get_named_attrs(obj, active_tree=None):
        # TODO - If the Active Node is a Store Named Attribute, it affects node ordering
        # TODO - Look into a way to make this order more consistent
        nodetrees = (m.node_group for m in obj.modifiers if m.type == 'NODES')

        for tree in nodetrees:
            for node in tree.nodes:
                if node.bl_label != "Store Named Attribute" or node.mute is True:
                    continue

                attr_name = node.inputs["Name"].default_value
                if attr_name == "":
                    continue

                yield (attr_name, node.data_type)

            if tree == active_tree:
                break

    def draw(self, context):
        layout = self.layout
        active_object = context.active_object
        
        active_tree = context.space_data.edit_tree
        if active_tree is None:
            active_tree = context.space_data.node_tree

        attrs = sorted(tuple(dict(self.get_named_attrs(active_object, active_tree)).items()))

        if len(attrs) > 0:
            for attr_name, attr_type in attrs:
                props = layout.operator(operators.NWAddNamedAttrNode.bl_idname, text=attr_name)
                props.attr_name = attr_name
                props.attr_type = attr_type
        else:
            layout.label(text="No named attributes detected")


class NWSwitchNodeTypeMenu(Menu, NWBase):
    bl_idname = "NODE_MT_fw_switch_node_type_menu"
    bl_label = "Switch Type to..."
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw_search(self, context):
        layout = self.layout

        if layout.operator_context == 'EXEC_REGION_WIN':
            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.operator("WM_OT_search_single_menu", text="Search...", icon='VIEWZOOM').menu_idname = self.bl_idname
            layout.separator()

        layout.operator_context = 'INVOKE_REGION_WIN'

    def draw(self, context):
        layout = self.layout
        self.draw_search(context)

        layout.operator_context = 'INVOKE_REGION_WIN'

        tree_type = context.space_data.tree_type
        if tree_type == 'GeometryNodeTree':
            layout.menu_contents("NODE_MT_geometry_node_switch_all")
        elif tree_type == 'CompositorNodeTree':
            layout.menu_contents("NODE_MT_compositor_node_switch_all")
        elif tree_type == 'ShaderNodeTree':
            layout.menu_contents("NODE_MT_shader_node_switch_all")
        elif tree_type == 'TextureNodeTree':
            layout.menu_contents("NODE_MT_texture_node_switch_all")
        else:
            layout.label(icon='WARNING', text="Switch Nodes not available in this editor.")

#
#  APPENDAGES TO EXISTING UI
#


def select_parent_children_buttons(self, context):
    layout = self.layout
    layout.operator(operators.NWSelectParentChildren.bl_idname,
                    text="Select frame's members (children)").option = 'CHILD'
    layout.operator(operators.NWSelectParentChildren.bl_idname, text="Select parent frame").option = 'PARENT'


def attr_nodes_menu_func(self, context):
    col = self.layout.column(align=True)
    col.menu("NODE_MT_fw_node_attribute_menu")
    col.separator()


def named_attr_nodes_menu_func(self, context):
    # TODO - Make the configurable by user preference
    if fw_check(context):
        col = self.layout.column(align=True)
        col.separator()
        col.menu("NODE_MT_fw_node_named_attribute_menu")


def multipleimages_menu_func(self, context):
    col = self.layout.column(align=True)
    col.operator(operators.NWAddMultipleImages.bl_idname, text="Multiple Images")
    col.operator(operators.NWAddSequence.bl_idname, text="Image Sequence")
    col.separator()


def bgreset_menu_func(self, context):
    self.layout.operator(operators.NWResetBG.bl_idname)


def save_viewer_menu_func(self, context):
    if fw_check(context):
        if context.space_data.tree_type == 'CompositorNodeTree':
            if context.scene.node_tree.nodes.active:
                if context.scene.node_tree.nodes.active.type == "VIEWER":
                    self.layout.operator(operators.NWSaveViewer.bl_idname, icon='FILE_IMAGE')


def reset_nodes_button(self, context):
    node_active = context.active_node
    node_selected = context.selected_nodes
    node_ignore = ["FRAME", "REROUTE", "GROUP", "SIMULATION_INPUT", "SIMULATION_OUTPUT"]

    # Check if active node is in the selection and respective type
    if (len(node_selected) == 1) and node_active and node_active.select and node_active.type not in node_ignore:
        row = self.layout.row()
        row.operator(operators.NWResetNodes.bl_idname, text="Reset Node", icon="FILE_REFRESH")
        self.layout.separator()

    elif (len(node_selected) == 1) and node_active and node_active.select and node_active.type == "FRAME":
        row = self.layout.row()
        row.operator(operators.NWResetNodes.bl_idname, text="Reset Nodes in Frame", icon="FILE_REFRESH")
        self.layout.separator()


classes = (
    NodeWranglerPanel,
    NodeWranglerMenu,
    NWMergeNodesMenu,
    NWMergeGeometryMenu,
    NWMergeShadersMenu,
    NWMergeMixMenu,
    NWMergeMathMenu,
    NWMergeVectorMathMenu,
    NWMergeStringMenu,
    NWMergeBoolMenu,
    NWConnectionListOutputs,
    NWConnectionListInputs,
    NWBatchChangeNodesMenu,
    NWBatchChangeBlendTypeMenu,
    NWBatchChangeOperationMenu,
    NWBatchChangeVectorOperationMenu,
    NWBatchChangeBoolMenu,
    NWCopyToSelectedMenu,
    NWCopyLabelMenu,
    NWAddReroutesMenu,
    NWLinkActiveToSelectedMenu,
    NWLinkStandardMenu,
    NWLinkUseNodeNameMenu,
    NWLinkUseOutputsNamesMenu,
    NWAttributeMenu,
    NWNamedAttributeMenu,
    NWSwitchNodeTypeMenu,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # menu items
    bpy.types.NODE_MT_select.append(select_parent_children_buttons)
    bpy.types.NODE_MT_category_shader_input.prepend(attr_nodes_menu_func)
    bpy.types.NODE_MT_geometry_node_GEO_INPUT.append(named_attr_nodes_menu_func)
    bpy.types.NODE_PT_backdrop.append(bgreset_menu_func)
    bpy.types.NODE_PT_active_node_generic.append(save_viewer_menu_func)
    bpy.types.NODE_MT_category_shader_texture.prepend(multipleimages_menu_func)
    bpy.types.NODE_MT_category_compositor_input.prepend(multipleimages_menu_func)
    bpy.types.NODE_PT_active_node_generic.prepend(reset_nodes_button)
    bpy.types.NODE_MT_node.prepend(reset_nodes_button)


def unregister():
    # menu items
    bpy.types.NODE_MT_select.remove(select_parent_children_buttons)
    bpy.types.NODE_MT_category_shader_input.remove(attr_nodes_menu_func)
    bpy.types.NODE_MT_geometry_node_GEO_INPUT.remove(named_attr_nodes_menu_func)
    bpy.types.NODE_PT_backdrop.remove(bgreset_menu_func)
    bpy.types.NODE_PT_active_node_generic.remove(save_viewer_menu_func)
    bpy.types.NODE_MT_category_shader_texture.remove(multipleimages_menu_func)
    bpy.types.NODE_MT_category_compositor_input.remove(multipleimages_menu_func)
    bpy.types.NODE_PT_active_node_generic.remove(reset_nodes_button)
    bpy.types.NODE_MT_node.remove(reset_nodes_button)

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
