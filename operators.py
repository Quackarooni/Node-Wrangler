# SPDX-FileCopyrightText: 2019-2022 Blender Foundation
#

# SPDX-License-Identifier: GPL-2.0-or-later

import itertools
import functools
import bpy

from bpy.types import Operator, PropertyGroup, NodeSocketVirtual
from bpy.props import (
    FloatProperty,
    EnumProperty,
    BoolProperty,
    IntProperty,
    StringProperty,
    FloatVectorProperty,
    IntVectorProperty,
    CollectionProperty,
)
from bpy_extras.io_utils import ImportHelper, ExportHelper
from mathutils import Vector
from os import path
from glob import glob
from copy import copy
from itertools import chain, islice, zip_longest

from .interface import NWConnectionListInputs, NWConnectionListOutputs

from .utils.constants import (
    blend_types, 
    geo_combine_operations, 
    vector_operations,
    boolean_operations,
    shader_operations,
    string_operations,
    operations,
    blend_types_list,
    vector_operations_list,
    bool_operations_list,
    math_operations_list, 
    navs,
    nav_list,
    get_texture_node_types, 
    rl_outputs
    )
from .utils.draw import draw_callback_nodeoutline
from .utils.paths import match_files_to_socket_names, split_into_components
from .utils.nodes import (
    is_virtual_socket,
    n_wise_iter,
    next_in_list,
    prev_in_list,
    filter_nodes_by_type,
    node_mid_pt, 
    get_bounds, 
    autolink, 
    node_at_pos, 
    get_active_tree, 
    get_nodes_links, 
    connect_sockets,
    is_viewer_socket,
    is_viewer_link, 
    get_group_output_node, 
    get_output_location, 
    force_update, 
    get_internal_socket,
    fw_check, 
    NWBase, 
    FinishedAutolink, 
    get_first_enabled_output, 
    is_visible_socket, 
    temporary_unframe, 
    viewer_socket_name
    )

from .addon_utils import fetch_user_preferences, safe_poll
from .sock_utils import get_socket_location

class NodeSetting(bpy.types.PropertyGroup):
    value: StringProperty(
        name="Value",
        description="Python expression to be evaluated as the initial node setting",
        default="",
    )

class NWLazyMix(Operator, NWBase):
    """Add a Mix RGB/Shader node by interactively drawing lines between nodes"""
    bl_idname = "node.fw_lazy_mix"
    bl_label = "Mix Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        context.area.tag_redraw()
        nodes, links = get_nodes_links(context)
        cont = True

        start_pos = [event.mouse_region_x, event.mouse_region_y]

        node1 = None
        if not context.scene.NWBusyDrawing:
            node1 = node_at_pos(nodes, context, event)
            if node1:
                context.scene.NWBusyDrawing = node1.name
        else:
            if context.scene.NWBusyDrawing != 'STOP':
                node1 = nodes[context.scene.NWBusyDrawing]

        context.scene.NWLazySource = node1.name
        context.scene.NWLazyTarget = node_at_pos(nodes, context, event).name

        if event.type == 'MOUSEMOVE':
            self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        elif event.type == 'RIGHTMOUSE' and event.value == 'RELEASE':
            end_pos = [event.mouse_region_x, event.mouse_region_y]
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')

            node2 = None
            node2 = node_at_pos(nodes, context, event)
            if node2:
                context.scene.NWBusyDrawing = node2.name

            if node1 == node2:
                cont = False

            if cont:
                if node1 and node2:
                    for node in nodes:
                        node.select = False
                    node1.select = True
                    node2.select = True

                    bpy.ops.node.fw_merge_nodes(mode="MIX", merge_type="AUTO")

            context.scene.NWBusyDrawing = ""
            return {'FINISHED'}

        elif event.type == 'ESC':
            print('cancelled')
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'NODE_EDITOR':
            # the arguments we pass the the callback
            args = (self, context, 'MIX')
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceNodeEditor.draw_handler_add(
                draw_callback_nodeoutline, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


class NWLazyConnect(Operator, NWBase):
    """Connect two nodes without clicking a specific socket (automatically determined"""
    bl_idname = "node.fw_lazy_connect"
    bl_label = "Lazy Connect"
    bl_options = {'REGISTER', 'UNDO'}
    with_menu: BoolProperty()

    def modal(self, context, event):
        context.area.tag_redraw()
        nodes, links = get_nodes_links(context)
        cont = True

        start_pos = [event.mouse_region_x, event.mouse_region_y]

        node1 = None
        if not context.scene.NWBusyDrawing:
            node1 = node_at_pos(nodes, context, event)
            if node1:
                context.scene.NWBusyDrawing = node1.name
        else:
            if context.scene.NWBusyDrawing != 'STOP':
                node1 = nodes[context.scene.NWBusyDrawing]

        context.scene.NWLazySource = node1.name
        context.scene.NWLazyTarget = node_at_pos(nodes, context, event).name

        if event.type == 'MOUSEMOVE':
            self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        elif event.type == 'RIGHTMOUSE' and event.value == 'RELEASE':
            end_pos = [event.mouse_region_x, event.mouse_region_y]
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')

            node2 = None
            node2 = node_at_pos(nodes, context, event)
            if node2:
                context.scene.NWBusyDrawing = node2.name

            if node1 == node2:
                cont = False

            link_success = False
            if cont:
                if node1 and node2:
                    original_sel = []
                    original_unsel = []
                    for node in nodes:
                        if node.select:
                            node.select = False
                            original_sel.append(node)
                        else:
                            original_unsel.append(node)
                    node1.select = True
                    node2.select = True

                    # link_success = autolink(node1, node2, links)
                    if self.with_menu:
                        if len(node1.outputs) > 1 and node2.inputs:
                            bpy.ops.wm.call_menu("INVOKE_DEFAULT", name=NWConnectionListOutputs.bl_idname)
                        elif len(node1.outputs) == 1:
                            bpy.ops.node.fw_call_inputs_menu(from_socket=0)
                    else:
                        try:
                            link_success = autolink(node1, node2, links)
                        except FinishedAutolink:
                            link_success = True

                    for node in original_sel:
                        node.select = True
                    for node in original_unsel:
                        node.select = False

            if link_success:
                force_update(context)
            context.scene.NWBusyDrawing = ""
            return {'FINISHED'}

        elif event.type == 'ESC':
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'NODE_EDITOR':
            nodes, links = get_nodes_links(context)
            node = node_at_pos(nodes, context, event)
            if node:
                context.scene.NWBusyDrawing = node.name

            # the arguments we pass the the callback
            mode = "LINK"
            if self.with_menu:
                mode = "LINKMENU"
            args = (self, context, mode)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceNodeEditor.draw_handler_add(
                draw_callback_nodeoutline, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


class NWDeleteUnused(Operator, NWBase):
    """Delete all nodes whose output is not used"""
    bl_idname = 'node.fw_del_unused'
    bl_label = 'Delete Unused Nodes'
    bl_options = {'REGISTER', 'UNDO'}

    delete_muted: BoolProperty(
        name="Delete Muted",
        description="Delete (but reconnect, like Ctrl-X) all muted nodes",
        default=True)
    delete_frames: BoolProperty(
        name="Delete Empty Frames",
        description="Delete all frames that have no nodes inside them",
        default=True)

    def is_unused_node(self, node):
        end_types = ['OUTPUT_MATERIAL', 'OUTPUT', 'VIEWER', 'COMPOSITE',
                     'SPLITVIEWER', 'OUTPUT_FILE', 'LEVELS', 'OUTPUT_LIGHT',
                     'OUTPUT_WORLD', 'GROUP_INPUT', 'GROUP_OUTPUT', 'FRAME']
        if node.type in end_types:
            return False

        for output in node.outputs:
            if output.links:
                return False
        return True

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context):
            if context.space_data.node_tree.nodes:
                valid = True
        return valid

    def execute(self, context):
        nodes, links = get_nodes_links(context)

        # Store selection
        selection = []
        for node in nodes:
            if node.select:
                selection.append(node.name)

        for node in nodes:
            node.select = False

        deleted_nodes = []
        temp_deleted_nodes = []
        del_unused_iterations = len(nodes)
        for it in range(0, del_unused_iterations):
            temp_deleted_nodes = list(deleted_nodes)  # keep record of last iteration
            for node in nodes:
                if self.is_unused_node(node):
                    node.select = True
                    deleted_nodes.append(node.name)
                    bpy.ops.node.delete()

            if temp_deleted_nodes == deleted_nodes:  # stop iterations when there are no more nodes to be deleted
                break

        if self.delete_frames:
            repeat = True
            while repeat:
                frames_in_use = []
                frames = []
                repeat = False
                for node in nodes:
                    if node.parent:
                        frames_in_use.append(node.parent)
                for node in nodes:
                    if node.type == 'FRAME' and node not in frames_in_use:
                        frames.append(node)
                        if node.parent:
                            repeat = True  # repeat for nested frames
                for node in frames:
                    if node not in frames_in_use:
                        node.select = True
                        deleted_nodes.append(node.name)
                bpy.ops.node.delete()

        if self.delete_muted:
            for node in nodes:
                if node.mute:
                    node.select = True
                    deleted_nodes.append(node.name)
            bpy.ops.node.delete_reconnect()

        # get unique list of deleted nodes (iterations would count the same node more than once)
        deleted_nodes = list(set(deleted_nodes))
        for n in deleted_nodes:
            self.report({'INFO'}, "Node " + n + " deleted")
        num_deleted = len(deleted_nodes)
        n = ' node'
        if num_deleted > 1:
            n += 's'
        if num_deleted:
            self.report({'INFO'}, "Deleted " + str(num_deleted) + n)
        else:
            self.report({'INFO'}, "Nothing deleted")

        # Restore selection
        nodes, links = get_nodes_links(context)
        for node in nodes:
            if node.name in selection:
                node.select = True
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class NWSwapLinks(Operator, NWBase):
    """Swap the output connections of the two selected nodes, or two similar inputs of a single node"""
    bl_idname = 'node.fw_swap_links'
    bl_label = 'Swap Links'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context):
            if context.selected_nodes:
                valid = len(context.selected_nodes) <= 2
        return valid

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        selected_nodes = context.selected_nodes
        n1 = selected_nodes[0]

        # Swap outputs
        if len(selected_nodes) == 2:
            n2 = selected_nodes[1]
            if n1.outputs and n2.outputs:
                n1_outputs = []
                n2_outputs = []

                out_index = 0
                for output in n1.outputs:
                    if output.links:
                        for link in output.links:
                            n1_outputs.append([out_index, link.to_socket])
                            links.remove(link)
                    out_index += 1

                out_index = 0
                for output in n2.outputs:
                    if output.links:
                        for link in output.links:
                            n2_outputs.append([out_index, link.to_socket])
                            links.remove(link)
                    out_index += 1

                for connection in n1_outputs:
                    try:
                        connect_sockets(n2.outputs[connection[0]], connection[1])
                    except:
                        self.report({'WARNING'},
                                    "Some connections have been lost due to differing numbers of output sockets")
                for connection in n2_outputs:
                    try:
                        connect_sockets(n1.outputs[connection[0]], connection[1])
                    except:
                        self.report({'WARNING'},
                                    "Some connections have been lost due to differing numbers of output sockets")
            else:
                if n1.outputs or n2.outputs:
                    self.report({'WARNING'}, "One of the nodes has no outputs!")
                else:
                    self.report({'WARNING'}, "Neither of the nodes have outputs!")

        # Swap Inputs
        elif len(selected_nodes) == 1:
            if n1.inputs and n1.inputs[0].is_multi_input:
                self.report({'WARNING'}, "Can't swap inputs of a multi input socket!")
                return {'FINISHED'}
            if n1.inputs:
                types = []
                i = 0
                for i1 in n1.inputs:
                    if i1.is_linked and not i1.is_multi_input:
                        similar_types = 0
                        for i2 in n1.inputs:
                            if i1.type == i2.type and i2.is_linked and not i2.is_multi_input:
                                similar_types += 1
                        types.append([i1, similar_types, i])
                    i += 1
                types.sort(key=lambda k: k[1], reverse=True)

                if types:
                    t = types[0]
                    if t[1] == 2:
                        for i2 in n1.inputs:
                            if t[0].type == i2.type == t[0].type and t[0] != i2 and i2.is_linked:
                                pair = [t[0], i2]
                        i1f = pair[0].links[0].from_socket
                        i1t = pair[0].links[0].to_socket
                        i2f = pair[1].links[0].from_socket
                        i2t = pair[1].links[0].to_socket
                        connect_sockets(i1f, i2t)
                        connect_sockets(i2f, i1t)
                    if t[1] == 1:
                        if len(types) == 1:
                            fs = t[0].links[0].from_socket
                            i = t[2]
                            links.remove(t[0].links[0])
                            if i + 1 == len(n1.inputs):
                                i = -1
                            i += 1
                            while n1.inputs[i].is_linked:
                                i += 1
                            connect_sockets(fs, n1.inputs[i])
                        elif len(types) == 2:
                            i1f = types[0][0].links[0].from_socket
                            i1t = types[0][0].links[0].to_socket
                            i2f = types[1][0].links[0].from_socket
                            i2t = types[1][0].links[0].to_socket
                            connect_sockets(i1f, i2t)
                            connect_sockets(i2f, i1t)

                else:
                    self.report({'WARNING'}, "This node has no input connections to swap!")
            else:
                self.report({'WARNING'}, "This node has no inputs to swap!")

        force_update(context)
        return {'FINISHED'}


class NWResetBG(Operator, NWBase):
    """Reset the zoom and position of the background image"""
    bl_idname = 'node.fw_bg_reset'
    bl_label = 'Reset Backdrop'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if fw_check(context):
            return context.space_data.tree_type == 'CompositorNodeTree'
        
        return False

    def execute(self, context):
        space = context.space_data
        space.backdrop_zoom = 1
        space.backdrop_offset = (0, 0)
        return {'FINISHED'}


class NWAddAttrNode(Operator, NWBase):
    """Add an Attribute node with this name"""
    bl_idname = 'node.fw_add_attr_node'
    bl_label = 'Add Attribute Node'
    bl_options = {'REGISTER', 'UNDO'}

    attr_name: StringProperty()
    attr_type: StringProperty(default='GEOMETRY')

    def execute(self, context):
        bpy.ops.node.add_node('INVOKE_DEFAULT', use_transform=True, type="ShaderNodeAttribute")
        context.active_node.attribute_name = self.attr_name
        context.active_node.attribute_type = self.attr_type
        return {'FINISHED'}


class NWAddNamedAttrNode(Operator, NWBase):
    """Add an Named Attribute node with the specified name"""
    bl_idname = 'node.fw_add_named_attr_node'
    bl_label = 'Add Named Attribute Node'
    bl_options = {'REGISTER', 'UNDO'}

    attr_name: StringProperty()
    attr_type: StringProperty()

    attr_map = {
        'BYTE_COLOR' : 'FLOAT_COLOR',
        'FLOAT2' : 'FLOAT_VECTOR',
        }

    def execute(self, context):
        bpy.ops.node.add_node('INVOKE_DEFAULT', use_transform=True, type="GeometryNodeInputNamedAttribute")
        active_node = context.active_node

        attr_type = self.attr_map.get(self.attr_type, self.attr_type)

        active_node.inputs["Name"].default_value = self.attr_name
        active_node.data_type = attr_type

        return {'FINISHED'}


class NWPreviewNode(Operator, NWBase):
    bl_idname = "node.fw_preview_node"
    bl_label = "Preview Node"
    bl_description = "Connect active node to the Node Group output or the Material Output"
    bl_options = {'REGISTER', 'UNDO'}

    # If false, the operator is not executed if the current node group happens to be a geometry nodes group.
    # This is needed because geometry nodes has its own viewer node that uses the same shortcut as in the compositor.
    run_in_geometry_nodes: BoolProperty(default=True)

    def __init__(self):
        self.shader_output_type = ""
        self.shader_output_ident = ""

    @classmethod
    def poll(cls, context):
        if fw_check(context):
            space = context.space_data
            if space.tree_type == 'ShaderNodeTree' or space.tree_type == 'GeometryNodeTree':
                if context.active_node:
                    if context.active_node.type != "OUTPUT_MATERIAL" or context.active_node.type != "OUTPUT_WORLD":
                        return True
                else:
                    return True
        return False

    @classmethod
    def get_output_sockets(cls, node_tree):
        return [item for item in node_tree.interface.items_tree if item.item_type == 'SOCKET' and item.in_out in {'OUTPUT', 'BOTH'}]

    def ensure_viewer_socket(self, node, socket_type, connect_socket=None):
        # check if a viewer output already exists in a node group otherwise create
        if hasattr(node, "node_tree"):
            viewer_socket = None
            output_sockets = self.get_output_sockets(node.node_tree)
            if len(output_sockets):
                free_socket = None
                for socket in output_sockets:
                    if is_viewer_socket(socket) and socket.socket_type == socket_type:
                        # if viewer output is already used but leads to the same socket we can still use it
                        is_used = self.is_socket_used_other_mats(socket)
                        if is_used:
                            if connect_socket is None:
                                continue
                            groupout = get_group_output_node(node.node_tree)
                            groupout_input = groupout.inputs[i]
                            links = groupout_input.links
                            if connect_socket not in [link.from_socket for link in links]:
                                continue
                            viewer_socket = socket
                            break
                        if not free_socket:
                            free_socket = socket
                if not viewer_socket and free_socket:
                    viewer_socket = free_socket

            if not viewer_socket:
                # create viewer socket
                viewer_socket = node.node_tree.interface.new_socket(viewer_socket_name, in_out='OUTPUT', socket_type=socket_type)
                viewer_socket.NWViewerSocket = True
            return viewer_socket

    def init_shader_variables(self, space, shader_type):
        if shader_type == 'OBJECT':
            if space.id not in [light for light in bpy.data.lights]:  # cannot use bpy.data.lights directly as iterable
                self.shader_output_type = "OUTPUT_MATERIAL"
                self.shader_output_ident = "ShaderNodeOutputMaterial"
            else:
                self.shader_output_type = "OUTPUT_LIGHT"
                self.shader_output_ident = "ShaderNodeOutputLight"

        elif shader_type == 'WORLD':
            self.shader_output_type = "OUTPUT_WORLD"
            self.shader_output_ident = "ShaderNodeOutputWorld"

    def get_shader_output_node(self, tree):
        for node in tree.nodes:
            if node.type == self.shader_output_type and node.is_active_output:
                return node

    @classmethod
    def ensure_group_output(cls, tree):
        # check if a group output node exists otherwise create
        groupout = get_group_output_node(tree)
        if not groupout:
            groupout = tree.nodes.new('NodeGroupOutput')
            loc_x, loc_y = get_output_location(tree)
            groupout.location.x = loc_x
            groupout.location.y = loc_y
            groupout.select = False
            # So that we don't keep on adding new group outputs
            groupout.is_active_output = True
        return groupout

    @classmethod
    def search_sockets(cls, node, sockets, index=None):
        # recursively scan nodes for viewer sockets and store in list
        for i, input_socket in enumerate(node.inputs):
            if index and i != index:
                continue
            if input_socket.is_linked:
                link = input_socket.links[0]
                next_node = link.from_node
                external_socket = link.from_socket
                if hasattr(next_node, "node_tree"):
                    for socket_index, socket in enumerate(next_node.node_tree.interface.items_tree):
                        if socket.identifier == external_socket.identifier:
                            break
                    if is_viewer_socket(socket) and socket not in sockets:
                        sockets.append(socket)
                        # continue search inside of node group but restrict socket to where we came from
                        groupout = get_group_output_node(next_node.node_tree)
                        cls.search_sockets(groupout, sockets, index=socket_index)

    @classmethod
    def scan_nodes(cls, tree, sockets):
        # get all viewer sockets in a material tree
        for node in tree.nodes:
            if hasattr(node, "node_tree"):
                if node.node_tree is None:
                    continue
                for socket in cls.get_output_sockets(node.node_tree):
                    if is_viewer_socket(socket) and (socket not in sockets):
                        sockets.append(socket)
                cls.scan_nodes(node.node_tree, sockets)

    @classmethod
    def remove_socket(cls, tree, socket):
        interface = tree.interface
        interface.remove(socket)
        interface.active_index = min(interface.active_index, len(interface.items_tree) - 1)

    def link_leads_to_used_socket(self, link):
        # return True if link leads to a socket that is already used in this material
        socket = get_internal_socket(link.to_socket)
        return (socket and self.is_socket_used_active_mat(socket))

    def is_socket_used_active_mat(self, socket):
        # ensure used sockets in active material is calculated and check given socket
        if not hasattr(self, "used_viewer_sockets_active_mat"):
            self.used_viewer_sockets_active_mat = []
            materialout = self.get_shader_output_node(bpy.context.space_data.node_tree)
            if materialout:
                self.search_sockets(materialout, self.used_viewer_sockets_active_mat)
        return socket in self.used_viewer_sockets_active_mat

    def is_socket_used_other_mats(self, socket):
        # ensure used sockets in other materials are calculated and check given socket
        if not hasattr(self, "used_viewer_sockets_other_mats"):
            self.used_viewer_sockets_other_mats = []
            for mat in bpy.data.materials:
                if mat.node_tree == bpy.context.space_data.node_tree or not hasattr(mat.node_tree, "nodes"):
                    continue
                # get viewer node
                materialout = self.get_shader_output_node(mat.node_tree)
                if materialout:
                    self.search_sockets(materialout, self.used_viewer_sockets_other_mats)
        return socket in self.used_viewer_sockets_other_mats

    @staticmethod
    def is_valid_socket(socket):
        return not (socket.hide or isinstance(socket, NodeSocketVirtual))

    # TODO - FIX THIS NOT WORKING IN THE COMPOSITOR
    def invoke(self, context, event):
        space = context.space_data
        # Ignore operator when running in wrong context.
        if self.run_in_geometry_nodes != (space.tree_type == "GeometryNodeTree"):
            return {'PASS_THROUGH'}

        shader_type = space.shader_type
        self.init_shader_variables(space, shader_type)
        mlocx = event.mouse_region_x
        mlocy = event.mouse_region_y
        context.space_data.cursor_location_from_region(event.mouse_region_x, event.mouse_region_y)

        # TODO - AVOID USING THIS OPERATOR TO AVOID ADDING TO THE UNDO STACK
        select_node = bpy.ops.node.select(location=(mlocx, mlocy), extend=False)
        if 'FINISHED' in select_node:  # only run if mouse click is on a node
            active_tree, path_to_tree = get_active_tree(context)
            nodes, links = active_tree.nodes, active_tree.links
            base_node_tree = space.node_tree
            active = nodes.active

            region = context.region
            mouse_pos = Vector(region.view2d.region_to_view(mlocx, mlocy))
            distance_from_mouse = lambda sock : (mouse_pos - get_socket_location(sock)).magnitude

            visible_outputs = filter(self.is_valid_socket, active.outputs)
            closest_outputs = sorted(visible_outputs, key=distance_from_mouse)

            # For geometry node trees we just connect to the group output
            if space.tree_type == "GeometryNodeTree":
                valid = False
                if active:
                    for out in active.outputs:
                        if is_visible_socket(out):
                            valid = True
                            break
                # Exit early
                if not valid:
                    return {'FINISHED'}

                delete_sockets = []

                # Scan through all nodes in tree including nodes inside of groups to find viewer sockets
                self.scan_nodes(base_node_tree, delete_sockets)

                # Find (or create if needed) the output of this node tree
                geometryoutput = self.ensure_group_output(base_node_tree)


                make_links = []  # store sockets for new links
                if active.outputs:
                    # If there is no 'GEOMETRY' output type - We can't preview the node

                    try:
                        socket_to_connect = closest_outputs[0]
                    except Exception:
                        return {'FINISHED'}

                    socket_type = 'GEOMETRY'
                    # Find an input socket of the output of type geometry
                    geometryoutindex = None
                    for i, inp in enumerate(geometryoutput.inputs):
                        if inp.type == socket_type:
                            geometryoutindex = i
                            break
                    if geometryoutindex is None:
                        # Create geometry socket
                        geometryoutput.inputs.new(socket_type, 'Geometry')
                        geometryoutindex = len(geometryoutput.inputs) - 1

                    make_links.append((socket_to_connect, geometryoutput.inputs[geometryoutindex]))
                    output_socket = geometryoutput.inputs[geometryoutindex]
                    for li_from, li_to in make_links:
                        connect_sockets(li_from, li_to)
                    tree = base_node_tree
                    link_end = output_socket
                    while tree.nodes.active != active:
                        node = tree.nodes.active
                        viewer_socket = self.ensure_viewer_socket(
                            node, 'NodeSocketGeometry', connect_socket=socket_to_connect if node.node_tree.nodes.active == active else None)
                        link_start = node.outputs[viewer_socket_name]
                        node_socket = viewer_socket
                        if node_socket in delete_sockets:
                            delete_sockets.remove(node_socket)
                        connect_sockets(link_start, link_end)
                        # Iterate
                        link_end = self.ensure_group_output(node.node_tree).inputs[viewer_socket_name]
                        tree = tree.nodes.active.node_tree
                    connect_sockets(socket_to_connect, link_end)

                # Delete sockets
                for socket in delete_sockets:
                    tree = socket.id_data
                    self.remove_socket(tree, socket)

                nodes.active = active
                active.select = True
                force_update(context)
                return {'FINISHED'}

            # What follows is code for the shader editor
            valid = False
            if active:
                for out in active.outputs:
                    if is_visible_socket(out):
                        valid = True
                        break
            if valid:
                # get material_output node
                materialout = None  # placeholder node
                delete_sockets = []
                
                # scan through all nodes in tree including nodes inside of groups to find viewer sockets
                self.scan_nodes(base_node_tree, delete_sockets)

                materialout = self.get_shader_output_node(base_node_tree)
                if not materialout:
                    materialout = base_node_tree.nodes.new(self.shader_output_ident)
                    materialout.location = get_output_location(base_node_tree)
                    materialout.select = False

                make_links = []  # store sockets for new links
                check_links_func = functools.partial(is_viewer_link, output_node=materialout)
                #if any(map(check_links_func, closest_outputs[0].links)):
                #    return {'CANCELLED'}

                if active.outputs:
                    socket_to_connect = closest_outputs[0]
                    socket_type = 'NodeSocketShader'
                    materialout_index = 1 if socket_to_connect.name == "Volume" else 0
                    make_links.append((socket_to_connect, materialout.inputs[materialout_index]))
                    output_socket = materialout.inputs[materialout_index]
                    for li_from, li_to in make_links:
                        connect_sockets(li_from, li_to)

                    # Create links through node groups until we reach the active node
                    tree = base_node_tree
                    link_end = output_socket
                    while tree.nodes.active != active:
                        node = tree.nodes.active
                        viewer_socket = self.ensure_viewer_socket(
                            node, socket_type, connect_socket=socket_to_connect if node.node_tree.nodes.active == active else None)
                        link_start = node.outputs[viewer_socket_name]
                        node_socket = viewer_socket
                        if node_socket in delete_sockets:
                            delete_sockets.remove(node_socket)
                        connect_sockets(link_start, link_end)
                        # Iterate
                        link_end = self.ensure_group_output(node.node_tree).inputs[viewer_socket_name]
                        tree = tree.nodes.active.node_tree
                    connect_sockets(socket_to_connect, link_end)

                # Delete sockets
                for socket in delete_sockets:
                    if not self.is_socket_used_other_mats(socket):
                        tree = socket.id_data
                        self.remove_socket(tree, socket)

                nodes.active = active
                active.select = True

                force_update(context)

            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class NWFrameSelected(Operator, NWBase):
    bl_idname = "node.fw_frame_selected"
    bl_label = "Frame Selected"
    bl_description = "Add a frame node and parent the selected nodes to it"
    bl_options = {'REGISTER', 'UNDO'}

    label_prop: StringProperty(
        name='Label',
        description='The visual name of the frame node',
        default=' '
    )
    use_custom_color_prop: BoolProperty(
        name="Custom Color",
        description="Use custom color for the frame node",
        default=False
    )
    color_prop: FloatVectorProperty(
        name="Color",
        description="The color of the frame node",
        default=(0.604, 0.604, 0.604),
        min=0, max=1, step=1, precision=3,
        subtype='COLOR_GAMMA', size=3
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'label_prop')
        layout.prop(self, 'use_custom_color_prop')
        col = layout.column()
        col.active = self.use_custom_color_prop
        col.prop(self, 'color_prop', text="")

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        selected = []
        for node in nodes:
            if node.select:
                selected.append(node)

        bpy.ops.node.add_node(type='NodeFrame')
        frm = nodes.active
        frm.label = self.label_prop
        frm.use_custom_color = self.use_custom_color_prop
        frm.color = self.color_prop

        for node in selected:
            node.parent = frm

        return {'FINISHED'}


class NWReloadImages(Operator):
    bl_idname = "node.fw_reload_images"
    bl_label = "Reload Images"
    bl_description = "Update all the image nodes to match their files on disk"

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context) and context.space_data.tree_type != 'GeometryNodeTree':
            if context.active_node is not None:
                for out in context.active_node.outputs:
                    if is_visible_socket(out):
                        valid = True
                        break
        return valid

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        image_types = ["IMAGE", "TEX_IMAGE", "TEX_ENVIRONMENT", "TEXTURE"]
        num_reloaded = 0
        for node in nodes:
            if node.type in image_types:
                if node.type == "TEXTURE":
                    if node.texture:  # node has texture assigned
                        if node.texture.type in ['IMAGE', 'ENVIRONMENT_MAP']:
                            if node.texture.image:  # texture has image assigned
                                node.texture.image.reload()
                                num_reloaded += 1
                else:
                    if node.image:
                        node.image.reload()
                        num_reloaded += 1

        if num_reloaded:
            self.report({'INFO'}, "Reloaded images")
            print("Reloaded " + str(num_reloaded) + " images")
            force_update(context)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No images found to reload in this node tree")
            return {'CANCELLED'}


class NWSwitchNodeType(Operator, NWBase):
    """Switch type of selected nodes """
    bl_idname = "node.fw_swtch_node_type"
    bl_label = "Switch Node Type"
    bl_options = {'REGISTER', 'UNDO'}

    to_type: StringProperty(
        name="Switch to type",
        default='',
    )

    settings: CollectionProperty(
        name="Settings",
        description="Settings to be applied on the newly created node",
        type=NodeSetting,
        options={'SKIP_SAVE'},
    )

    def execute(self, context):
        to_type = self.to_type
        if len(to_type) == 0:
            return {'CANCELLED'}

        nodes, links = get_nodes_links(context)
        # Those types of nodes will not swap.
        src_excludes = ('NodeFrame')
        # Those attributes of nodes will be copied if possible
        attrs_to_pass = ('color', 'hide', 'label', 'mute', 'parent',
                         'show_options', 'show_preview', 'show_texture',
                         'use_alpha', 'use_clamp', 'use_custom_color', 'location'
                         )
        selected = [n for n in nodes if n.select]
        reselect = []
        for node in [n for n in selected if
                     n.rna_type.identifier not in src_excludes and
                     (n.rna_type.identifier != to_type or (n.rna_type.identifier in 
                     ("ShaderNodeMix", "GeometryNodeGroup", "CompositorNodeGroup", "ShaderNodeGroup", "TextureNodeGroup")))]:
                     
            new_node = nodes.new(to_type)
            for attr in attrs_to_pass:
                if hasattr(node, attr) and hasattr(new_node, attr):
                    try:
                        setattr(new_node, attr, getattr(node, attr))
                    except ValueError:
                        pass

            for setting in self.settings:
                value = eval(setting.value)
                node_data = new_node
                node_attr_name = setting.name

                # Support path to nested data.
                if '.' in node_attr_name:
                    node_data_path, node_attr_name = node_attr_name.rsplit(".", 1)
                    node_data = node.path_resolve(node_data_path)

                try:
                    setattr(node_data, node_attr_name, value)
                except AttributeError as e:
                    self.report(
                        {'ERROR_INVALID_INPUT'},
                        "Node has no attribute " + setting.name)
                    print(str(e))

            # set image datablock of dst to image of src
            if hasattr(node, 'image') and hasattr(new_node, 'image'):
                if node.image:
                    new_node.image = node.image
            # Special cases
            if new_node.type == 'SWITCH':
                new_node.hide = True


            # Dictionaries: src_sockets and dst_sockets:
            # 'INPUTS': input sockets ordered by type (entry 'MAIN' main type of inputs).
            # 'OUTPUTS': output sockets ordered by type (entry 'MAIN' main type of outputs).
            # in 'INPUTS' and 'OUTPUTS':
            # 'SHADER', 'RGBA', 'VECTOR', 'VALUE' - sockets of those types.
            # socket entry:
            # (index_in_type, socket_index, socket_name, socket_default_value, socket_links)
            src_sockets = {
                'INPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
                'OUTPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
            }
            dst_sockets = {
                'INPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
                'OUTPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
            }
            types_order_one = 'SHADER', 'RGBA', 'VECTOR', 'VALUE'
            types_order_two = 'SHADER', 'VECTOR', 'RGBA', 'VALUE'
            # check src node to set src_sockets values and dst node to set dst_sockets dict values
            for sockets, nd in ((src_sockets, node), (dst_sockets, new_node)):
                # Check node's inputs and outputs and fill proper entries in "sockets" dict
                for in_out, in_out_name in ((nd.inputs, 'INPUTS'), (nd.outputs, 'OUTPUTS')):
                    # enumerate in inputs, then in outputs
                    # find name, default value and links of socket
                    for i, socket in enumerate(in_out):
                        the_name = socket.name
                        dval = None
                        # Not every socket, especially in outputs has "default_value"
                        if hasattr(socket, 'default_value'):
                            dval = socket.default_value
                        socket_links = []
                        for lnk in socket.links:
                            socket_links.append(lnk)
                        # check type of socket to fill proper keys.
                        for the_type in types_order_one:
                            if socket.type == the_type:
                                # create values for sockets['INPUTS'][the_type] and sockets['OUTPUTS'][the_type]
                                # entry structure: (index_in_type, socket_index, socket_name,
                                # socket_default_value, socket_links)
                                sockets[in_out_name][the_type].append(
                                    (len(sockets[in_out_name][the_type]), i, the_name, dval, socket_links))
                    # Check which of the types in inputs/outputs is considered to be "main".
                    # Set values of sockets['INPUTS']['MAIN'] and sockets['OUTPUTS']['MAIN']
                    for type_check in types_order_one:
                        if sockets[in_out_name][type_check]:
                            sockets[in_out_name]['MAIN'] = type_check
                            break

            matches = {
                'INPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE_NAME': [], 'VALUE': [], 'MAIN': []},
                'OUTPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE_NAME': [], 'VALUE': [], 'MAIN': []},
            }

            for inout, soctype in (
                    ('INPUTS', 'MAIN',),
                    ('INPUTS', 'SHADER',),
                    ('INPUTS', 'RGBA',),
                    ('INPUTS', 'VECTOR',),
                    ('INPUTS', 'VALUE',),
                    ('OUTPUTS', 'MAIN',),
                    ('OUTPUTS', 'SHADER',),
                    ('OUTPUTS', 'RGBA',),
                    ('OUTPUTS', 'VECTOR',),
                    ('OUTPUTS', 'VALUE',),
            ):
                if src_sockets[inout][soctype] and dst_sockets[inout][soctype]:
                    if soctype == 'MAIN':
                        sc = src_sockets[inout][src_sockets[inout]['MAIN']]
                        dt = dst_sockets[inout][dst_sockets[inout]['MAIN']]
                    else:
                        sc = src_sockets[inout][soctype]
                        dt = dst_sockets[inout][soctype]
                    # start with 'dt' to determine number of possibilities.
                    for i, soc in enumerate(dt):
                        # if src main has enough entries - match them with dst main sockets by indexes.
                        if len(sc) > i:
                            matches[inout][soctype].append(((sc[i][1], sc[i][3]), (soc[1], soc[3])))
                        # add 'VALUE_NAME' criterion to inputs.
                        if inout == 'INPUTS' and soctype == 'VALUE':
                            for s in sc:
                                if s[2] == soc[2]:  # if names match
                                    # append src (index, dval), dst (index, dval)
                                    matches['INPUTS']['VALUE_NAME'].append(((s[1], s[3]), (soc[1], soc[3])))

            # When src ['INPUTS']['MAIN'] is 'VECTOR' replace 'MAIN' with matches VECTOR if possible.
            # This creates better links when relinking textures.
            if src_sockets['INPUTS']['MAIN'] == 'VECTOR' and matches['INPUTS']['VECTOR']:
                matches['INPUTS']['MAIN'] = matches['INPUTS']['VECTOR']

            # Pass default values and RELINK:
            for tp in ('MAIN', 'SHADER', 'RGBA', 'VECTOR', 'VALUE_NAME', 'VALUE'):
                # INPUTS: Base on matches in proper order.
                for (src_i, src_dval), (dst_i, dst_dval) in matches['INPUTS'][tp]:
                    # pass dvals
                    if src_dval and dst_dval and tp in {'RGBA', 'VALUE_NAME'}:
                        new_node.inputs[dst_i].default_value = src_dval
                    # Special case: switch to math
                    if node.type in {'MIX_RGB', 'ALPHAOVER', 'ZCOMBINE'} and\
                            new_node.type == 'MATH' and\
                            tp == 'MAIN':
                        new_dst_dval = max(src_dval[0], src_dval[1], src_dval[2])
                        new_node.inputs[dst_i].default_value = new_dst_dval
                        if node.type == 'MIX_RGB':
                            if node.blend_type in [o[0] for o in operations]:
                                new_node.operation = node.blend_type
                    # Special case: switch from math to some types
                    if node.type == 'MATH' and\
                            new_node.type in {'MIX_RGB', 'ALPHAOVER', 'ZCOMBINE'} and\
                            tp == 'MAIN':
                        for i in range(3):
                            new_node.inputs[dst_i].default_value[i] = src_dval
                        if new_node.type == 'MIX_RGB':
                            if node.operation in [t[0] for t in blend_types]:
                                new_node.blend_type = node.operation
                            # Set Fac of MIX_RGB to 1.0
                            new_node.inputs[0].default_value = 1.0
                    # make link only when dst matching input is not linked already.
                    if node.inputs[src_i].links and not new_node.inputs[dst_i].links:
                        in_src_link = node.inputs[src_i].links[0]
                        in_dst_socket = new_node.inputs[dst_i]
                        connect_sockets(in_src_link.from_socket, in_dst_socket)
                        links.remove(in_src_link)
                # OUTPUTS: Base on matches in proper order.
                for (src_i, src_dval), (dst_i, dst_dval) in matches['OUTPUTS'][tp]:
                    for out_src_link in node.outputs[src_i].links:
                        out_dst_socket = new_node.outputs[dst_i]
                        connect_sockets(out_dst_socket, out_src_link.to_socket)
            # relink rest inputs if possible, no criteria
            for src_inp in node.inputs:
                for dst_inp in new_node.inputs:
                    if src_inp.links and not dst_inp.links:
                        src_link = src_inp.links[0]
                        connect_sockets(src_link.from_socket, dst_inp)
                        links.remove(src_link)
            # relink rest outputs if possible, base on node kind if any left.
            for src_o in node.outputs:
                for out_src_link in src_o.links:
                    for dst_o in new_node.outputs:
                        if src_o.type == dst_o.type:
                            connect_sockets(dst_o, out_src_link.to_socket)
            # relink rest outputs no criteria if any left. Link all from first output.
            for src_o in node.outputs:
                for out_src_link in src_o.links:
                    if new_node.outputs:
                        connect_sockets(new_node.outputs[0], out_src_link.to_socket)
            nodes.remove(node)

        force_update(context)
        return {'FINISHED'}


class NWMergeNodes(Operator, NWBase):
    bl_idname = "node.fw_merge_nodes"
    bl_label = "Merge Nodes"
    bl_description = "Merge Selected Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(
        name="mode",
        description="All possible blend types, boolean operations and math operations",
        items=list(set(blend_types + geo_combine_operations + operations + vector_operations))
    )
    merge_type: EnumProperty(
        name="merge type",
        description="Type of Merge to be used",
        items=(
            ('AUTO', 'Auto', 'Automatic Output Type Detection'),
            ('SHADER', 'Shader', 'Merge using ADD or MIX Shader'),
            ('GEOMETRY', 'Geometry', 'Merge using Mesh Boolean or Join Geometry Node'),
            ('MIX', 'Mix Node', 'Merge using Mix Nodes'),
            ('MATH', 'Math Node', 'Merge using Math Nodes'),
            ('VECTOR', 'Vector Math Node', 'Merge using Vector Math Nodes'),
            ('ZCOMBINE', 'Z-Combine Node', 'Merge using Z-Combine Nodes'),
            ('ALPHAOVER', 'Alpha Over Node', 'Merge using Alpha Over Nodes'),
        ),
    )

    # Check if the link connects to a node that is in selected_nodes
    # If not, then check recursively for each link in the nodes outputs.
    # If yes, return True. If the recursion stops without finding a node
    # in selected_nodes, it returns False. The depth is used to prevent
    # getting stuck in a loop because of an already present cycle.
    @staticmethod
    def link_creates_cycle(link, selected_nodes, depth=0) -> bool:
        if depth > 255:
            # We're stuck in a cycle, but that cycle was already present,
            # so we return False.
            # NOTE: The number 255 is arbitrary, but seems to work well.
            return False
        node = link.to_node
        if node in selected_nodes:
            return True
        if not node.outputs:
            return False
        for output in node.outputs:
            if output.is_linked:
                for olink in output.links:
                    if NWMergeNodes.link_creates_cycle(olink, selected_nodes, depth + 1):
                        return True
        # None of the outputs found a node in selected_nodes, so there is no cycle.
        return False

    # Merge the nodes in `nodes_list` with a node of type `node_name` that has a multi_input socket.
    # The parameters `socket_indices` gives the indices of the node sockets in the order that they should
    # be connected. The last one is assumed to be a multi input socket.
    # For convenience the node is returned.
    @staticmethod
    def merge_with_multi_input(nodes_list, merge_position, do_hide, loc_x, links, nodes, node_name, socket_indices):
        # The y-location of the last node
        loc_y = nodes_list[-1][2]
        if merge_position == 'CENTER':
            # Average the y-location
            for i in range(len(nodes_list) - 1):
                loc_y += nodes_list[i][2]
            loc_y = loc_y / len(nodes_list)
        new_node = nodes.new(node_name)
        new_node.hide = do_hide
        new_node.location.x = loc_x
        new_node.location.y = loc_y
        selected_nodes = [nodes[node_info[0]] for node_info in nodes_list]
        prev_links = []
        outputs_for_multi_input = []
        for i, node in enumerate(selected_nodes):
            node.select = False
            # Search for the first node which had output links that do not create
            # a cycle, which we can then reconnect afterwards.
            if prev_links == [] and node.outputs[0].is_linked:
                prev_links = [
                    link for link in node.outputs[0].links if not NWMergeNodes.link_creates_cycle(
                        link, selected_nodes)]
            # Get the index of the socket, the last one is a multi input, and is thus used repeatedly
            # To get the placement to look right we need to reverse the order in which we connect the
            # outputs to the multi input socket.
            if i < len(socket_indices) - 1:
                ind = socket_indices[i]
                connect_sockets(node.outputs[0], new_node.inputs[ind])
            else:
                outputs_for_multi_input.insert(0, node.outputs[0])
        if outputs_for_multi_input != []:
            ind = socket_indices[-1]
            for output in outputs_for_multi_input:
                connect_sockets(output, new_node.inputs[ind])
        if prev_links != []:
            for link in prev_links:
                connect_sockets(new_node.outputs[0], link.to_node.inputs[0])
        return new_node

    def execute(self, context):
        settings = fetch_user_preferences()
        merge_hide = settings.merge_hide
        merge_position = settings.merge_position  # 'center' or 'bottom'

        do_hide = False
        do_hide_shader = False
        if merge_hide == 'ALWAYS':
            do_hide = True
            do_hide_shader = True
        elif merge_hide == 'NON_SHADER':
            do_hide = True

        tree_type = context.space_data.node_tree.type
        if tree_type == 'GEOMETRY':
            node_type = 'GeometryNode'
        if tree_type == 'COMPOSITING':
            node_type = 'CompositorNode'
        elif tree_type == 'SHADER':
            node_type = 'ShaderNode'
        elif tree_type == 'TEXTURE':
            node_type = 'TextureNode'
        nodes, links = get_nodes_links(context)
        mode = self.mode
        merge_type = self.merge_type
        # Prevent trying to add Z-Combine in not 'COMPOSITING' node tree.
        # 'ZCOMBINE' works only if mode == 'MIX'
        # Setting mode to None prevents trying to add 'ZCOMBINE' node.
        if (merge_type == 'ZCOMBINE' or merge_type == 'ALPHAOVER') and tree_type != 'COMPOSITING':
            merge_type = 'MIX'
            mode = 'MIX'
        if (merge_type != 'MATH' and merge_type != 'GEOMETRY') and tree_type == 'GEOMETRY':
            merge_type = 'AUTO'
        # The Mix node and math nodes used for geometry nodes are of type 'ShaderNode'
        if (merge_type == 'MATH' or merge_type == 'MIX') and tree_type == 'GEOMETRY':
            node_type = 'ShaderNode'
        selected_mix = []  # entry = [index, loc]
        selected_shader = []  # entry = [index, loc]
        selected_geometry = []  # entry = [index, loc]
        selected_math = []  # entry = [index, loc]
        selected_vector = []  # entry = [index, loc]
        selected_z = []  # entry = [index, loc]
        selected_alphaover = []  # entry = [index, loc]

        for i, node in enumerate(nodes):
            if node.select and node.outputs:
                if merge_type == 'AUTO':
                    for (type, types_list, dst) in (
                            ('SHADER', ('MIX', 'ADD'), selected_shader),
                            ('GEOMETRY', [t[0] for t in geo_combine_operations], selected_geometry),
                            ('RGBA', [t[0] for t in blend_types], selected_mix),
                            ('VALUE', [t[0] for t in operations], selected_math),
                            ('VECTOR', [], selected_vector),
                    ):
                        output = get_first_enabled_output(node)
                        output_type = output.type
                        valid_mode = mode in types_list
                        # When mode is 'MIX' we have to cheat since the mix node is not used in
                        # geometry nodes.
                        if tree_type == 'GEOMETRY':
                            if mode == 'MIX':
                                if output_type == 'VALUE' and type == 'VALUE':
                                    valid_mode = True
                                elif output_type == 'VECTOR' and type == 'VECTOR':
                                    valid_mode = True
                                elif type == 'GEOMETRY':
                                    valid_mode = True
                        # When mode is 'MIX' use mix node for both 'RGBA' and 'VALUE' output types.
                        # Cheat that output type is 'RGBA',
                        # and that 'MIX' exists in math operations list.
                        # This way when selected_mix list is analyzed:
                        # Node data will be appended even though it doesn't meet requirements.
                        elif output_type != 'SHADER' and mode == 'MIX':
                            output_type = 'RGBA'
                            valid_mode = True
                        if output_type == type and valid_mode:
                            dst.append([i, node.location.x, node.location.y, node.dimensions.x, node.hide])
                else:
                    for (type, types_list, dst) in (
                            ('SHADER', ('MIX', 'ADD'), selected_shader),
                            ('GEOMETRY', [t[0] for t in geo_combine_operations], selected_geometry),
                            ('MIX', [t[0] for t in blend_types], selected_mix),
                            ('MATH', [t[0] for t in operations], selected_math),
                            ('VECTOR', [t[0] for t in vector_operations], selected_vector),
                            ('ZCOMBINE', ('MIX', ), selected_z),
                            ('ALPHAOVER', ('MIX', ), selected_alphaover),
                    ):
                        if merge_type == type and mode in types_list:
                            dst.append([i, node.location.x, node.location.y, node.dimensions.x, node.hide])

        # When nodes with output kinds 'RGBA' and 'VALUE' are selected at the same time
        # use only 'Mix' nodes for merging.
        # For that we add selected_math list to selected_mix list and clear selected_math.
        if selected_mix and selected_math and merge_type == 'AUTO':
            selected_mix += selected_math
            selected_math = []
        for nodes_list in [
                selected_mix,
                selected_shader,
                selected_geometry,
                selected_math,
                selected_vector,
                selected_z,
                selected_alphaover]:
            if not nodes_list:
                continue
            count_before = len(nodes)
            # sort list by loc_x - reversed
            nodes_list.sort(key=lambda k: k[1], reverse=True)
            # get maximum loc_x
            loc_x = nodes_list[0][1] + nodes_list[0][3] + 70
            nodes_list.sort(key=lambda k: k[2], reverse=True)

            # Change the node type for math nodes in a geometry node tree.
            if tree_type == 'GEOMETRY':
                if nodes_list is selected_math or nodes_list is selected_vector or nodes_list is selected_mix:
                    node_type = 'ShaderNode'
                    if mode == 'MIX':
                        mode = 'ADD'
                else:
                    node_type = 'GeometryNode'
            if merge_position == 'CENTER':
                # average yloc of last two nodes (lowest two)
                loc_y = ((nodes_list[len(nodes_list) - 1][2]) + (nodes_list[len(nodes_list) - 2][2])) / 2
                if nodes_list[len(nodes_list) - 1][-1]:  # if last node is hidden, mix should be shifted up a bit
                    if do_hide:
                        loc_y += 40
                    else:
                        loc_y += 80
            else:
                loc_y = nodes_list[len(nodes_list) - 1][2]
            offset_y = 100
            if not do_hide:
                offset_y = 200
            if nodes_list == selected_shader and not do_hide_shader:
                offset_y = 150.0
            the_range = len(nodes_list) - 1
            if len(nodes_list) == 1:
                the_range = 1
            was_multi = False
            for i in range(the_range):
                if nodes_list == selected_mix:
                    mix_name = 'Mix'
                    if tree_type == 'COMPOSITING':
                        mix_name = 'MixRGB'
                    add_type = node_type + mix_name
                    add = nodes.new(add_type)
                    if tree_type != 'COMPOSITING':
                        add.data_type = 'RGBA'
                    add.blend_type = mode
                    if mode != 'MIX':
                        add.inputs[0].default_value = 1.0
                    add.show_preview = False
                    add.hide = do_hide
                    if do_hide:
                        loc_y = loc_y - 50
                    first = 6
                    second = 7
                    if tree_type == 'COMPOSITING':
                        first = 1
                        second = 2
                elif nodes_list == selected_math:
                    add_type = node_type + 'Math'
                    add = nodes.new(add_type)
                    add.operation = mode
                    add.hide = do_hide
                    if do_hide:
                        loc_y = loc_y - 50
                    first = 0
                    second = 1
                elif nodes_list == selected_shader:
                    if mode == 'MIX':
                        add_type = node_type + 'MixShader'
                        add = nodes.new(add_type)
                        add.hide = do_hide_shader
                        if do_hide_shader:
                            loc_y = loc_y - 50
                        first = 1
                        second = 2
                    elif mode == 'ADD':
                        add_type = node_type + 'AddShader'
                        add = nodes.new(add_type)
                        add.hide = do_hide_shader
                        if do_hide_shader:
                            loc_y = loc_y - 50
                        first = 0
                        second = 1
                elif nodes_list == selected_geometry:
                    if mode in ('JOIN', 'MIX'):
                        add_type = node_type + 'JoinGeometry'
                        add = self.merge_with_multi_input(
                            nodes_list, merge_position, do_hide, loc_x, links, nodes, add_type, [0])
                    elif mode == 'INSTANCES':
                        add_type = node_type + 'GeometryToInstance'
                        add = self.merge_with_multi_input(
                            nodes_list, merge_position, do_hide, loc_x, links, nodes, add_type, [0])
                    else:
                        add_type = node_type + 'MeshBoolean'
                        indices = [0, 1] if mode == 'DIFFERENCE' else [1]
                        add = self.merge_with_multi_input(
                            nodes_list, merge_position, do_hide, loc_x, links, nodes, add_type, indices)
                        add.operation = mode
                    was_multi = True
                    break
                elif nodes_list == selected_vector:
                    add_type = node_type + 'VectorMath'
                    add = nodes.new(add_type)
                    add.operation = mode
                    add.hide = do_hide
                    if do_hide:
                        loc_y = loc_y - 50
                    first = 0
                    second = 1
                elif nodes_list == selected_z:
                    add = nodes.new('CompositorNodeZcombine')
                    add.show_preview = False
                    add.hide = do_hide
                    if do_hide:
                        loc_y = loc_y - 50
                    first = 0
                    second = 2
                elif nodes_list == selected_alphaover:
                    add = nodes.new('CompositorNodeAlphaOver')
                    add.show_preview = False
                    add.hide = do_hide
                    if do_hide:
                        loc_y = loc_y - 50
                    first = 1
                    second = 2
                add.location = loc_x, loc_y
                loc_y += offset_y
                add.select = True

            # This has already been handled separately
            if was_multi:
                continue
            count_adds = i + 1
            count_after = len(nodes)
            index = count_after - 1
            first_selected = nodes[nodes_list[0][0]]
            # "last" node has been added as first, so its index is count_before.
            last_add = nodes[count_before]
            # Create list of invalid indexes.
            invalid_nodes = [nodes[n[0]]
                             for n in (selected_mix + selected_math + selected_shader + selected_z + selected_geometry)]

            # Special case:
            # Two nodes were selected and first selected has no output links, second selected has output links.
            # Then add links from last add to all links 'to_socket' of out links of second selected.
            first_selected_output = get_first_enabled_output(first_selected)
            if len(nodes_list) == 2:
                if not first_selected_output.links:
                    second_selected = nodes[nodes_list[1][0]]
                    for ss_link in get_first_enabled_output(second_selected).links:
                        # Prevent cyclic dependencies when nodes to be merged are linked to one another.
                        # Link only if "to_node" index not in invalid indexes list.
                        if not self.link_creates_cycle(ss_link, invalid_nodes):
                            connect_sockets(get_first_enabled_output(last_add), ss_link.to_socket)
            # add links from last_add to all links 'to_socket' of out links of first selected.
            for fs_link in first_selected_output.links:
                # Link only if "to_node" index not in invalid indexes list.
                if not self.link_creates_cycle(fs_link, invalid_nodes):
                    connect_sockets(get_first_enabled_output(last_add), fs_link.to_socket)
            # add link from "first" selected and "first" add node
            node_to = nodes[count_after - 1]
            connect_sockets(first_selected_output, node_to.inputs[first])
            if node_to.type == 'ZCOMBINE':
                for fs_out in first_selected.outputs:
                    if fs_out != first_selected_output and fs_out.name in ('Z', 'Depth'):
                        connect_sockets(fs_out, node_to.inputs[1])
                        break
            # add links between added ADD nodes and between selected and ADD nodes
            for i in range(count_adds):
                if i < count_adds - 1:
                    node_from = nodes[index]
                    node_to = nodes[index - 1]
                    node_to_input_i = first
                    node_to_z_i = 1  # if z combine - link z to first z input
                    connect_sockets(get_first_enabled_output(node_from), node_to.inputs[node_to_input_i])
                    if node_to.type == 'ZCOMBINE':
                        for from_out in node_from.outputs:
                            if from_out != get_first_enabled_output(node_from) and from_out.name in ('Z', 'Depth'):
                                connect_sockets(from_out, node_to.inputs[node_to_z_i])
                if len(nodes_list) > 1:
                    node_from = nodes[nodes_list[i + 1][0]]
                    node_to = nodes[index]
                    node_to_input_i = second
                    node_to_z_i = 3  # if z combine - link z to second z input
                    connect_sockets(get_first_enabled_output(node_from), node_to.inputs[node_to_input_i])
                    if node_to.type == 'ZCOMBINE':
                        for from_out in node_from.outputs:
                            if from_out != get_first_enabled_output(node_from) and from_out.name in ('Z', 'Depth'):
                                connect_sockets(from_out, node_to.inputs[node_to_z_i])
                index -= 1
            # set "last" of added nodes as active
            nodes.active = last_add
            for i, x, y, dx, h in nodes_list:
                nodes[i].select = False

        return {'FINISHED'}

class NWMergeNodesRefactored(Operator, NWBase):
    bl_idname = "node.fw_merge_nodes_refactored"
    bl_label = "Merge Nodes"
    bl_description = "Merge Selected Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    operation: EnumProperty(
        name="mode",
        description="All possible blend types, boolean operations and math operations",
        default='NONE',
        items=list(set(chain(
            (('NONE', 'NONE', 'NONE',),),
            blend_types,
            geo_combine_operations,
            operations,
            vector_operations,
            boolean_operations,
            shader_operations,
            string_operations
            )))
    )
    merge_type: EnumProperty(
        name="merge type",
        description="Type of Merge to be used",
        items=(
            ('AUTO', 'Auto', 'Automatic Output Type Detection'),
            ('SHADER', 'Shader', 'Merge using ADD or MIX Shader'),
            ('GEOMETRY', 'Geometry', 'Merge using Mesh Boolean or Join Geometry Node'),
            ('MIX_COLOR', 'Mix Color Node', 'Merge using Mix Color Nodes'),
            ('MATH', 'Math Node', 'Merge using Math Nodes'),
            ('VECTOR', 'Vector Math Node', 'Merge using Vector Math Nodes'),
            ('STRING', 'String Node', 'Merge using String Nodes'),
            ('BOOLEAN', 'Boolean Math Node', 'Merge using Boolean Math Nodes'),
            ('Z_COMBINE', 'Z-Combine Node', 'Merge using Z-Combine Nodes'),
            ('ALPHA_OVER', 'Alpha Over Node', 'Merge using Alpha Over Nodes'),
        ),
    )

    @staticmethod
    def get_function_type(operation_name):
        prefs = fetch_user_preferences()
        unary_ops = [
            #Boolean Ops
            'NOT',
            #Vector Ops
            'NORMALIZE','LENGTH','ABSOLUTE','FRACTION', 'SCALE', 'FLOOR','CEIL','SINE','COSINE','TANGENT',
            #Math Ops
            'SQRT','INVERSE_SQRT','ABSOLUTE','EXPONENT','SIGN','ROUND','TRUNC','FRACT',
            'ARCSINE','ARCCOSINE','ARCTANGENT','SINH','COSH','TANH','RADIANS','DEGREES',
            #String Ops
            'SLICE','STRING_LENGTH','STRING_TO_CURVES','VALUE_TO_STRING',
            #Shader Ops
            'SHADER_TO_RGB'
        ]

        batch_ops = [
            #String Ops
            'JOIN',
            #Geometry Ops
            'JOIN_GEOMETRY',
            'INSTANCES',
            'DIFFERENCE',
            'UNION',
            'INTERSECT',
        ]


        binary_merge_ops = [
            #Vector Ops
            'DOT_PRODUCT', 'DISTANCE'
        ]

        ternary_ops = [
            #Math Ops
            'SMOOTH_MIN', 'SMOOTH_MAX', 'COMPARE', 
            #Vector Ops
            'FACEFORWARD',
            #Math & Vector Ops
            'MULTIPLY_ADD', 'WRAP',            
            #String Ops
            'REPLACE',
        ]

        temp_type = 'TERNARY' if operation_name in ternary_ops else 'BINARY'

        if operation_name in unary_ops:
            return 'UNARY'
        elif operation_name in batch_ops:
            return 'BATCH'

        elif operation_name in batch_ops:
            return 'BATCH'

        if temp_type == 'TERNARY':
            merge_mode = prefs.merge_ternary_mode

            if merge_mode == 'AUTO':
                return 'TERNARY_MERGE'
            elif merge_mode == 'CHAIN':
                return 'TERNARY'
            elif merge_mode == 'GROUP':
                return 'TERNARY_MERGE' 


        merge_mode = prefs.merge_binary_mode

        if merge_mode == 'AUTO':
            if operation_name in binary_merge_ops:
                return 'BINARY_MERGE'
            else:
                return 'BINARY'

        elif merge_mode == 'CHAIN':
            return 'BINARY'
        elif merge_mode == 'GROUP':
            return 'BINARY_MERGE'


    @staticmethod
    def get_valid_socket(node, mode, data_types=None, target_index=0):
        if data_types is None:
            sockets = [soc for soc in getattr(node, mode.lower()) 
                if soc.enabled and (not soc.hide)]
        else:
            sockets = [soc for soc in getattr(node, mode.lower()) 
                if soc.enabled and (not soc.hide) and soc.type in data_types]

        return sockets[target_index]

        #TODO - Implement this as an iterator rather than a list
        for index, socket in enumerate(sockets):
            if index == target_index:
                return socket
            else:
                raise IndexError
                

    def arrange_nodes(self, nodes, align_point=(0, 0)):
        current_pos = 0
        margin = 15
        x_spacing_offset = 120

        #TODO - Implement Sizes between different nodes, in both cases of vertical and horizontal alignment
        if self.operation == 'STRING_TO_CURVES':
            offset_size = 50
        else:
            offset_size = 30

        for node in nodes:
            node.location.y = current_pos
            current_pos -= offset_size + margin

        merge_position = fetch_user_preferences("merge_position")
        min_x, max_x, min_y, max_y = get_bounds(nodes)
        target_x, target_y = align_point

        align_offset_x = target_x - max_x + x_spacing_offset
        if merge_position == 'TOP':
            align_offset_y = target_y - max_y - (0.5 * offset_size)
        elif merge_position == 'MIDDLE':
            align_offset_y = target_y - 0.5 * (min_y + max_y)
        elif merge_position == 'BOTTOM':
            align_offset_y = target_y - min_y + (0.5 * offset_size)

        for node in nodes:
            node.location.x = align_offset_x
            node.location.y += align_offset_y

    def group_merge(self, context, selected_nodes, data, group_size):
        nodes, links = get_nodes_links(context)
        operation_type = self.operation

        new_nodes = []
        for group in n_wise_iter(selected_nodes, n=group_size):
            new_node = nodes.new(data.node_to_add)
            new_node.hide = True
            new_node.select = True

            if data.subtype_name is not None:
                setattr(new_node, data.subtype_name, operation_type)

            if data.mix_type is not None:
                new_node.data_type = data.mix_type

            for index, node in enumerate(group):
                if node is not None:
                    from_socket = self.get_valid_socket(node, mode='Outputs', data_types=data.preferred_input_type)
                    to_socket = self.get_valid_socket(new_node, mode='Inputs', data_types=data.socket_data_type, target_index=index)
                    connect_sockets(from_socket, to_socket)

            new_nodes.append(new_node)

        context.space_data.edit_tree.nodes.active = new_node
        return new_nodes

    def chain_merge(self, context, selected_nodes, data, group_size):
        nodes, links = get_nodes_links(context)
        operation_type = self.operation
        max_index = group_size - 1

        if len(selected_nodes) <= group_size:
            new_node = nodes.new(data.node_to_add)
            new_node.hide = True
            new_node.select = True  

            if data.subtype_name is not None:
                setattr(new_node, data.subtype_name, operation_type)

            if data.mix_type is not None:
                new_node.data_type = data.mix_type

            for index, node in enumerate(selected_nodes):
                from_socket = self.get_valid_socket(node, mode='Outputs', data_types=data.preferred_input_type)
                to_socket = self.get_valid_socket(new_node, mode='Inputs', data_types=data.socket_data_type, target_index=index)
                connect_sockets(from_socket, to_socket)

            context.space_data.edit_tree.nodes.active = new_node
            return [new_node, ]

        new_nodes = []
        if data.prefer_first_socket:
            first_node = selected_nodes.pop(0)
        else:
            first_node = selected_nodes.pop(max_index)

        prev_socket = None
        for group in n_wise_iter(selected_nodes, n=max_index):
            new_node = nodes.new(data.node_to_add)
            new_node.hide = True
            new_node.select = True

            if data.subtype_name is not None:
                setattr(new_node, data.subtype_name, operation_type)

            if data.mix_type is not None:
                new_node.data_type = data.mix_type

            for index, node in enumerate(group, start=data.prefer_first_socket):
                if node is not None:
                    from_socket = self.get_valid_socket(node, mode='Outputs', data_types=data.preferred_input_type)
                    to_socket = self.get_valid_socket(new_node, mode='Inputs', data_types=data.socket_data_type, target_index=index)
                    connect_sockets(from_socket, to_socket)

            chain_index = 0 if data.prefer_first_socket else max_index

            if prev_socket is not None:
                from_socket = prev_socket
                to_socket = self.get_valid_socket(new_node, mode='Inputs', data_types=data.socket_data_type, target_index=chain_index)
                connect_sockets(from_socket, to_socket)
            else:
                from_socket = self.get_valid_socket(first_node, mode='Outputs', data_types=data.preferred_input_type)
                to_socket = self.get_valid_socket(new_node, mode='Inputs', data_types=data.socket_data_type, target_index=chain_index)
                connect_sockets(from_socket, to_socket)

            prev_socket = self.get_valid_socket(new_node, mode='Outputs', data_types=data.preferred_input_type)
            new_nodes.append(new_node)

        context.space_data.edit_tree.nodes.active = new_node
        return new_nodes

    def batch_merge(self, context, selected_nodes, data):
        nodes, links = get_nodes_links(context)
        operation_type = self.operation

        new_node = nodes.new(data.node_to_add)
        new_node.hide = True
        new_node.select = True

        if data.subtype_name is not None:
            setattr(new_node, data.subtype_name, operation_type)

        batch_socket = self.get_valid_socket(new_node, mode='Inputs', 
            data_types=data.socket_data_type, target_index=data.batch_socket_index)
        
        if not data.isolate_first_socket:
            for node in reversed(selected_nodes):
                from_socket = self.get_valid_socket(node, mode='Outputs', data_types=data.preferred_input_type)
                connect_sockets(from_socket, batch_socket)
        else:
            first_node = selected_nodes.pop(0)

            for node in reversed(selected_nodes):
                from_socket = self.get_valid_socket(node, mode='Outputs', data_types=data.preferred_input_type)
                connect_sockets(from_socket, batch_socket)

            first_to_socket = self.get_valid_socket(new_node, mode='Inputs', 
                data_types=data.socket_data_type, target_index=data.first_socket_index)
            first_from_socket = self.get_valid_socket(first_node, mode='Outputs', data_types=data.preferred_input_type)

            connect_sockets(first_from_socket, first_to_socket)

        context.space_data.edit_tree.nodes.active = new_node
        return [new_node, ]

    def setup_function_data(self, context, function_type, operation_type):
        tree_type = context.space_data.node_tree.type
        merge_type = self.merge_type

        mix_type = None
        isolate_first_socket = False
        first_socket_index = None
        preferred_input_type = [
            'CUSTOM', 'VALUE', 'INT', 'BOOLEAN', 'VECTOR', 
            'STRING', 'RGBA', 'SHADER', 'OBJECT', 'IMAGE', 
            #'GEOMETRY', #Exclude geometry sockets as inputs by default
            'COLLECTION', 'TEXTURE', 'MATERIAL'
            ]

        if merge_type == 'VECTOR':
            node_to_add = 'ShaderNodeVectorMath'
            subtype_name = "operation"
            socket_data_type = ('VECTOR', )

        elif merge_type == 'BOOLEAN':
            node_to_add = 'FunctionNodeBooleanMath'
            subtype_name = "operation"
            socket_data_type = ('BOOLEAN', )

        elif merge_type == 'MATH':
            if tree_type == 'COMPOSITING':
                node_to_add = 'CompositorNodeMath'
                subtype_name = "operation"
                socket_data_type = ('VALUE', )
            else:
                node_to_add = 'ShaderNodeMath'
                subtype_name = "operation"
                socket_data_type = ('VALUE', )

        elif merge_type == 'MIX_COLOR':
            if tree_type == 'COMPOSITING':
                node_to_add = 'CompositorNodeMixRGB'
                subtype_name = "blend_type"
                socket_data_type = ('RGBA', )
            else:
                mix_type = 'RGBA'
                node_to_add = 'ShaderNodeMix'
                subtype_name = "blend_type"
                socket_data_type = ('RGBA', )

        elif merge_type == 'STRING':
            lookup_dict = {
                'JOIN': 'GeometryNodeStringJoin',
                'REPLACE': 'FunctionNodeReplaceString',
                'SLICE': 'FunctionNodeSliceString',
                'STRING_LENGTH': 'FunctionNodeStringLength',
                'STRING_TO_CURVES': 'GeometryNodeStringToCurves',
                'VALUE_TO_STRING': 'FunctionNodeValueToString',
                }

            node_to_add = lookup_dict[operation_type]
            subtype_name = None
            socket_data_type = ('STRING', 'VALUE')

            if operation_type == 'JOIN':
                batch_socket_index = 1

        elif merge_type == 'GEOMETRY':
            lookup_dict = {
                'JOIN_GEOMETRY': 'GeometryNodeJoinGeometry',
                'INSTANCES': 'GeometryNodeGeometryToInstance',
                'DIFFERENCE': 'GeometryNodeMeshBoolean',
                'UNION': 'GeometryNodeMeshBoolean',
                'INTERSECT': 'GeometryNodeMeshBoolean',
                }

            node_to_add = lookup_dict[operation_type]
            socket_data_type = ('GEOMETRY', )
            preferred_input_type = ('GEOMETRY', )
            subtype_name = None

            if node_to_add == 'GeometryNodeMeshBoolean':
                subtype_name = 'operation'

            if operation_type == 'DIFFERENCE':
                isolate_first_socket = True
                first_socket_index = 0
                batch_socket_index = 1
            else:
                batch_socket_index = 0

        elif merge_type == 'SHADER':
            lookup_dict = {
                'MIX': 'ShaderNodeMixShader',
                'ADD': 'ShaderNodeAddShader',
                'SHADER_TO_RGB': 'ShaderNodeShaderToRGB',
                }

            node_to_add = lookup_dict[operation_type]
            subtype_name = None
            socket_data_type = ('SHADER')

        elif merge_type == 'Z_COMBINE':
            node_to_add = 'CompositorNodeZcombine'
            subtype_name = None
            socket_data_type = ('RGBA', )

        elif merge_type == 'ALPHA_OVER':
            node_to_add = 'CompositorNodeAlphaOver'
            subtype_name = None
            socket_data_type = ('RGBA', )


        prefs = fetch_user_preferences()
        prefer_first_socket_binary = prefs.prefer_first_socket_binary
        prefer_first_socket_ternary = prefs.prefer_first_socket_ternary

        prefer_first_socket = None
        if function_type in ('BINARY', 'BINARY_MERGE'):
            prefer_first_socket = prefer_first_socket_binary
        elif function_type in ('TERNARY', 'TERNARY_MERGE'):
            prefer_first_socket = prefer_first_socket_ternary

        from typing import NamedTuple

        if function_type == 'BATCH':
            class NodeData_Batch(NamedTuple):
                node_to_add : str
                subtype_name : str
                operation_type : str
                preferred_input_type : tuple 
                isolate_first_socket : bool
                socket_data_type : tuple
                first_socket_index : int
                batch_socket_index : int

            data = NodeData_Batch(
                node_to_add=node_to_add, 
                subtype_name=subtype_name, 
                operation_type=operation_type,
                first_socket_index=first_socket_index,
                batch_socket_index=batch_socket_index,
                preferred_input_type=preferred_input_type,
                isolate_first_socket=isolate_first_socket,
                socket_data_type=socket_data_type
                )

        elif function_type in ('UNARY', 'BINARY_MERGE', 'TERNARY_MERGE'):
            class NodeData_Merge(NamedTuple):
                node_to_add : str
                subtype_name : str
                mix_type : str
                operation_type : str
                socket_data_type : tuple
                preferred_input_type : tuple

            data = NodeData_Merge(
                node_to_add=node_to_add, 
                subtype_name=subtype_name, 
                operation_type=operation_type, 
                mix_type=mix_type,
                preferred_input_type=preferred_input_type, 
                socket_data_type=socket_data_type
                )

        elif function_type in ('BINARY', 'TERNARY'):
            class NodeData_Chain(NamedTuple):
                node_to_add : str
                subtype_name : str
                mix_type : str
                operation_type : str
                socket_data_type : tuple
                preferred_input_type : tuple
                prefer_first_socket : bool

            data = NodeData_Chain(
                node_to_add=node_to_add, 
                subtype_name=subtype_name, 
                operation_type=operation_type, 
                mix_type=mix_type,
                prefer_first_socket=prefer_first_socket,
                preferred_input_type=preferred_input_type, 
                socket_data_type=socket_data_type
                )            

        return data

    def execute(self, context):
        prefs = fetch_user_preferences()
        merge_hide = prefs.merge_hide
        merge_position = prefs.merge_position

        nodes, links = get_nodes_links(context)

        #TODO - Fetch operation type and subtype function
        operation_type = self.operation
        function_type = self.get_function_type(operation_type)

        selected_nodes = [node for node in context.selected_nodes if node.type != "FRAME"]
        if not selected_nodes:
            return {'CANCELLED'}

        for node in nodes:
            node.select = False

        min_x, max_x, min_y, max_y = get_bounds(selected_nodes)

        if merge_position == 'TOP':
            align_point = (max_x, max_y)
        elif merge_position == 'MIDDLE':
            align_point = (max_x, 0.5 * (min_y + max_y))
        elif merge_position == 'BOTTOM':
            align_point = (max_x, min_y)
        selected_nodes.sort(key=lambda n: n.location.y - (n.dimensions.y / 2), reverse=True)

        data = self.setup_function_data(context, function_type, operation_type)

        if function_type == 'UNARY':
            new_nodes = self.group_merge(context, selected_nodes, data, group_size=1)

        elif function_type == 'BATCH':
            new_nodes = self.batch_merge(context, selected_nodes, data)

        elif function_type == 'TERNARY_MERGE':
            new_nodes = self.group_merge(context, selected_nodes, data, group_size=3)

        elif function_type == 'BINARY_MERGE':
            new_nodes = self.group_merge(context, selected_nodes, data, group_size=2)
                
        elif function_type == 'TERNARY':
            new_nodes = self.chain_merge(context, selected_nodes, data, group_size=3)

        elif function_type == 'BINARY':
            new_nodes = self.chain_merge(context, selected_nodes, data, group_size=2)
        
        else:
            raise NotImplementedError(f"Function type '{function_type}', does not have a supported implementation")

        self.arrange_nodes(new_nodes, align_point=align_point)
        return {'FINISHED'}


class NWBatchChangeNodes(Operator, NWBase):
    bl_idname = "node.fw_batch_change"
    bl_label = "Batch Change"
    bl_description = "Batch Change Blend Type and Math Operation"
    bl_options = {'REGISTER', 'UNDO'}

    blend_type: EnumProperty(
        name="Blend Type",
        default = 'CURRENT',
        items=blend_types + navs,
    )
    math_operation: EnumProperty(
        name="Operation",
        default = 'CURRENT',
        items=operations + navs,
    )

    vector_operation: EnumProperty(
        name="Vector Operation",
        default = 'CURRENT',
        items=vector_operations + navs,
    )

    bool_operation: EnumProperty(
        name="Boolean Type",
        default = 'CURRENT',
        items=boolean_operations + navs,
    )

    @staticmethod
    def set_node_property(node, property_name, value, prop_list, should_wrap):
        if value == 'CURRENT':
            return

        elif value not in nav_list:
            prop_value = value
        else:
            current_value = getattr(node, property_name)
            
            if value == 'NEXT':
                prop_value = next_in_list(prop_list, key=current_value, wrap=should_wrap)
            if value == 'PREV':
                prop_value = prev_in_list(prop_list, key=current_value, wrap=should_wrap)

        setattr(node, property_name, prop_value)

    def execute(self, context):
        nodes = list(filter_nodes_by_type(context.selected_nodes, 
            types=('MIX_RGB', 'MATH', 'VECT_MATH', 'BOOLEAN_MATH')))

        if len(nodes) <= 0:
            return {'CANCELLED'}

        mode = (fetch_user_preferences("batch_change_behavior") == 'WRAP')

        for node in nodes:
            if node.type in ('MIX', 'MIX_RGB'):
                self.set_node_property(node, "blend_type", 
                    value=self.blend_type, prop_list=blend_types_list, should_wrap=mode)

            if node.type == 'MATH':
                self.set_node_property(node, "operation", 
                    value=self.math_operation, prop_list=math_operations_list, should_wrap=mode)

            if node.type == 'VECT_MATH':
                self.set_node_property(node, "operation", 
                    value=self.vector_operation, prop_list=vector_operations_list, should_wrap=mode)

            if node.type == 'BOOLEAN_MATH':
                self.set_node_property(node, "operation", 
                    value=self.bool_operation, prop_list=bool_operations_list, should_wrap=mode)

        #Somehow the operator stores the state from the last time it's called so a hard reset here was applied
        self.blend_type = 'CURRENT'
        self.math_operation = 'CURRENT'
        self.vector_operation = 'CURRENT'
        self.bool_operation = 'CURRENT'
        return {'FINISHED'}


class NWChangeMixFactor(Operator, NWBase):
    bl_idname = "node.fw_factor"
    bl_label = "Change Factor"
    bl_description = "Change Factors of Mix Nodes and Mix Shader Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    # option: Change factor.
    # If option is 1.0 or 0.0 - set to 1.0 or 0.0
    # Else - change factor by option value.
    option: FloatProperty()

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        option = self.option
        selected = []  # entry = index
        for si, node in enumerate(nodes):
            if node.select:
                if node.type in {'MIX_RGB', 'MIX_SHADER'} or node.bl_idname == 'ShaderNodeMix':
                    selected.append(si)

        for si in selected:
            fac = nodes[si].inputs[0]
            nodes[si].hide = False
            if option in {0.0, 1.0}:
                fac.default_value = option
            else:
                fac.default_value += option

        return {'FINISHED'}


class NWCopySettings(Operator, NWBase):
    bl_idname = "node.fw_copy_settings"
    bl_label = "Copy Settings"
    bl_description = "Copy Settings of Active Node to Selected Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context):
            if (
                    context.active_node is not None and
                    context.active_node.type != 'FRAME'
            ):
                valid = True
        return valid

    def execute(self, context):
        node_active = context.active_node
        node_selected = context.selected_nodes

        # Error handling
        if not (len(node_selected) > 1):
            self.report({'ERROR'}, "2 nodes must be selected at least")
            return {'CANCELLED'}

        # Check if active node is in the selection
        selected_node_names = [n.name for n in node_selected]
        if node_active.name not in selected_node_names:
            self.report({'ERROR'}, "No active node")
            return {'CANCELLED'}

        # Get nodes in selection by type
        valid_nodes = [n for n in node_selected if n.type == node_active.type]

        if not (len(valid_nodes) > 1) and node_active:
            self.report({'ERROR'}, "Selected nodes are not of the same type as {}".format(node_active.name))
            return {'CANCELLED'}

        if len(valid_nodes) != len(node_selected):
            # Report nodes that are not valid
            valid_node_names = [n.name for n in valid_nodes]
            not_valid_names = list(set(selected_node_names) - set(valid_node_names))
            self.report(
                {'INFO'},
                "Ignored {} (not of the same type as {})".format(
                    ", ".join(not_valid_names),
                    node_active.name))

        # Reference original
        orig = node_active
        # node_selected_names = [n.name for n in node_selected]

        # Output list
        success_names = []

        # Deselect all nodes
        for i in node_selected:
            i.select = False

        # Code by zeffii from http://blender.stackexchange.com/a/42338/3710
        # Run through all other nodes
        for node in valid_nodes[1:]:

            # Check for frame node
            parent = node.parent if node.parent else None
            node_loc = [node.location.x, node.location.y]

            # Select original to duplicate
            orig.select = True

            # Duplicate selected node
            bpy.ops.node.duplicate()
            new_node = context.selected_nodes[0]

            # Deselect copy
            new_node.select = False

            # Properties to copy
            node_tree = node.id_data
            props_to_copy = 'bl_idname name location height width'.split(' ')

            # Input and outputs
            reconnections = []
            mappings = chain.from_iterable([node.inputs, node.outputs])
            for i in (i for i in mappings if i.is_linked):
                for L in i.links:
                    reconnections.append([L.from_socket.path_from_id(), L.to_socket.path_from_id()])

            # Properties
            props = {j: getattr(node, j) for j in props_to_copy}
            props_to_copy.pop(0)

            for prop in props_to_copy:
                setattr(new_node, prop, props[prop])

            # Get the node tree to remove the old node
            nodes = node_tree.nodes
            nodes.remove(node)
            new_node.name = props['name']

            if parent:
                new_node.parent = parent
                new_node.location = node_loc

            for str_from, str_to in reconnections:
                node_tree.links.new(eval(str_from), eval(str_to))

            success_names.append(new_node.name)

        orig.select = True
        node_tree.nodes.active = orig
        self.report(
            {'INFO'},
            "Successfully copied attributes from {} to: {}".format(
                orig.name,
                ", ".join(success_names)))
        return {'FINISHED'}


class NWCopyLabel(Operator, NWBase):
    bl_idname = "node.fw_copy_label"
    bl_label = "Copy Label"
    bl_options = {'REGISTER', 'UNDO'}

    option: EnumProperty(
        name="option",
        description="Source of name of label",
        items=(
            ('FROM_ACTIVE', 'from active', 'from active node',),
            ('FROM_NODE', 'from node', 'from node linked to selected node'),
            ('FROM_SOCKET', 'from socket', 'from socket linked to selected node'),
        )
    )

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        option = self.option
        active = nodes.active
        if option == 'FROM_ACTIVE':
            if active:
                src_label = active.label
                for node in [n for n in nodes if n.select and nodes.active != n]:
                    node.label = src_label
        elif option == 'FROM_NODE':
            selected = [n for n in nodes if n.select]
            for node in selected:
                for input in node.inputs:
                    if input.links:
                        src = input.links[0].from_node
                        node.label = src.label
                        break
        elif option == 'FROM_SOCKET':
            selected = [n for n in nodes if n.select]
            for node in selected:
                for input in node.inputs:
                    if input.links:
                        src = input.links[0].from_socket
                        node.label = src.name
                        break

        return {'FINISHED'}


class NWClearLabel(Operator, NWBase):
    bl_idname = "node.fw_clear_label"
    bl_label = "Clear Label"
    bl_options = {'REGISTER', 'UNDO'}

    option: BoolProperty()

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        for node in [n for n in nodes if n.select]:
            node.label = ''

        return {'FINISHED'}

    def invoke(self, context, event):
        if self.option:
            return self.execute(context)
        else:
            return context.window_manager.invoke_confirm(self, event)


class NWModifyLabels(Operator, NWBase):
    """Modify Labels of all selected nodes"""
    bl_idname = "node.fw_modify_labels"
    bl_label = "Modify Labels"
    bl_options = {'REGISTER', 'UNDO'}

    prepend: StringProperty(
        name="Add to Beginning"
    )
    append: StringProperty(
        name="Add to End"
    )
    replace_from: StringProperty(
        name="Text to Replace"
    )
    replace_to: StringProperty(
        name="Replace with"
    )

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        for node in [n for n in nodes if n.select]:
            node.label = self.prepend + node.label.replace(self.replace_from, self.replace_to) + self.append

        return {'FINISHED'}

    def invoke(self, context, event):
        self.prepend = ""
        self.append = ""
        self.remove = ""
        return context.window_manager.invoke_props_dialog(self)


class NWAddTextureSetup(Operator, NWBase):
    bl_idname = "node.fw_add_texture"
    bl_label = "Texture Setup"
    bl_description = "Add Texture Node Setup to Selected Shaders"
    bl_options = {'REGISTER', 'UNDO'}

    add_mapping: BoolProperty(
        name="Add Mapping Nodes",
        description="Create coordinate and mapping nodes for the texture (ignored for selected texture nodes)",
        default=True)

    @classmethod
    def poll(cls, context):
        if fw_check(context):
            space = context.space_data
            if space.tree_type == 'ShaderNodeTree':
                return True
        return False

    def execute(self, context):
        nodes, links = get_nodes_links(context)

        texture_types = get_texture_node_types()
        selected_nodes = [n for n in nodes if n.select]

        for node in selected_nodes:
            if not node.inputs:
                continue

            input_index = 0
            target_input = node.inputs[0]
            for input in node.inputs:
                if input.enabled:
                    input_index += 1
                    if not input.is_linked:
                        target_input = input
                        break
            else:
                self.report({'WARNING'}, "No free inputs for node: " + node.name)
                continue

            x_offset = 0
            padding = 40.0
            locx = node.location.x
            locy = node.location.y - (input_index * padding)

            is_texture_node = node.rna_type.identifier in texture_types
            use_environment_texture = node.type == 'BACKGROUND'

            # Add an image texture before normal shader nodes.
            if not is_texture_node:
                image_texture_type = 'ShaderNodeTexEnvironment' if use_environment_texture else 'ShaderNodeTexImage'
                image_texture_node = nodes.new(image_texture_type)
                x_offset = x_offset + image_texture_node.width + padding
                image_texture_node.location = [locx - x_offset, locy]
                nodes.active = image_texture_node
                connect_sockets(image_texture_node.outputs[0], target_input)

                # The mapping setup following this will connect to the first input of this image texture.
                target_input = image_texture_node.inputs[0]

            node.select = False

            if is_texture_node or self.add_mapping:
                # Add Mapping node.
                mapping_node = nodes.new('ShaderNodeMapping')
                x_offset = x_offset + mapping_node.width + padding
                mapping_node.location = [locx - x_offset, locy]
                connect_sockets(mapping_node.outputs[0], target_input)

                # Add Texture Coordinates node.
                tex_coord_node = nodes.new('ShaderNodeTexCoord')
                x_offset = x_offset + tex_coord_node.width + padding
                tex_coord_node.location = [locx - x_offset, locy]

                is_procedural_texture = is_texture_node and node.type != 'TEX_IMAGE'
                use_generated_coordinates = is_procedural_texture or use_environment_texture
                tex_coord_output = tex_coord_node.outputs[0 if use_generated_coordinates else 2]
                connect_sockets(tex_coord_output, mapping_node.inputs[0])

        return {'FINISHED'}


class NWAddPrincipledSetup(Operator, NWBase, ImportHelper):
    bl_idname = "node.fw_add_textures_for_principled"
    bl_label = "Principled Texture Setup"
    bl_description = "Add Texture Node Setup for Principled BSDF"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(
        name='Directory',
        subtype='DIR_PATH',
        default='',
        description='Folder to search in for image files'
    )
    files: CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
    )

    relative_path: BoolProperty(
        name='Relative Path',
        description='Set the file path relative to the blend file, when possible',
        default=True
    )

    order = [
        "filepath",
        "files",
    ]

    def draw(self, context):
        layout = self.layout
        layout.alignment = 'LEFT'

        layout.prop(self, 'relative_path')

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context):
            space = context.space_data
            if space.tree_type == 'ShaderNodeTree':
                valid = True
        return valid

    def execute(self, context):
        # Check if everything is ok
        if not self.directory:
            self.report({'INFO'}, 'No Folder Selected')
            return {'CANCELLED'}
        if not self.files[:]:
            self.report({'INFO'}, 'No Files Selected')
            return {'CANCELLED'}

        nodes, links = get_nodes_links(context)
        active_node = nodes.active
        if not (active_node and active_node.bl_idname == 'ShaderNodeBsdfPrincipled'):
            self.report({'INFO'}, 'Select Principled BSDF')
            return {'CANCELLED'}

        # Filter textures names for texturetypes in filenames
        # [Socket Name, [abbreviations and keyword list], Filename placeholder]
        tags = fetch_user_preferences().principled_tags
        normal_abbr = tags.normal.split(' ')
        bump_abbr = tags.bump.split(' ')
        gloss_abbr = tags.gloss.split(' ')
        rough_abbr = tags.rough.split(' ')
        socketnames = [
            ['Displacement', tags.displacement.split(' '), None],
            ['Base Color', tags.base_color.split(' '), None],
            ['Metallic', tags.metallic.split(' '), None],
            ['Specular IOR Level', tags.specular.split(' '), None],
            ['Roughness', rough_abbr + gloss_abbr, None],
            ['Normal', normal_abbr + bump_abbr, None],
            ['Transmission Weight', tags.transmission.split(' '), None],
            ['Emission Color', tags.emission.split(' '), None],
            ['Alpha', tags.alpha.split(' '), None],
            ['Ambient Occlusion', tags.ambient_occlusion.split(' '), None],
        ]

        match_files_to_socket_names(self.files, socketnames)
        # Remove socketnames without found files
        socketnames = [s for s in socketnames if s[2]
                       and path.exists(self.directory + s[2])]
        if not socketnames:
            self.report({'INFO'}, 'No matching images found')
            print('No matching images found')
            return {'CANCELLED'}

        # Don't override path earlier as os.path is used to check the absolute path
        import_path = self.directory
        if self.relative_path:
            if bpy.data.filepath:
                try:
                    import_path = bpy.path.relpath(self.directory)
                except ValueError:
                    pass

        # Add found images
        print('\nMatched Textures:')
        texture_nodes = []
        disp_texture = None
        ao_texture = None
        normal_node = None
        roughness_node = None
        for i, sname in enumerate(socketnames):
            print(i, sname[0], sname[2])

            # DISPLACEMENT NODES
            if sname[0] == 'Displacement':
                disp_texture = nodes.new(type='ShaderNodeTexImage')
                img = bpy.data.images.load(path.join(import_path, sname[2]))
                disp_texture.image = img
                disp_texture.label = 'Displacement'
                if disp_texture.image:
                    disp_texture.image.colorspace_settings.is_data = True

                # Add displacement offset nodes
                disp_node = nodes.new(type='ShaderNodeDisplacement')
                # Align the Displacement node under the active Principled BSDF node
                disp_node.location = active_node.location + Vector((100, -700))
                link = connect_sockets(disp_node.inputs[0], disp_texture.outputs[0])

                # TODO Turn on true displacement in the material
                # Too complicated for now

                # Find output node
                output_node = [n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial']
                if output_node:
                    if not output_node[0].inputs[2].is_linked:
                        link = connect_sockets(output_node[0].inputs[2], disp_node.outputs[0])

                continue

            # AMBIENT OCCLUSION TEXTURE
            if sname[0] == 'Ambient Occlusion':
                ao_texture = nodes.new(type='ShaderNodeTexImage')
                img = bpy.data.images.load(path.join(import_path, sname[2]))
                ao_texture.image = img
                ao_texture.label = sname[0]
                if ao_texture.image:
                    ao_texture.image.colorspace_settings.is_data = True

                continue

            if not active_node.inputs[sname[0]].is_linked:
                # No texture node connected -> add texture node with new image
                texture_node = nodes.new(type='ShaderNodeTexImage')
                img = bpy.data.images.load(path.join(import_path, sname[2]))
                texture_node.image = img

                # NORMAL NODES
                if sname[0] == 'Normal':
                    # Test if new texture node is normal or bump map
                    fname_components = split_into_components(sname[2])
                    match_normal = set(normal_abbr).intersection(set(fname_components))
                    match_bump = set(bump_abbr).intersection(set(fname_components))
                    if match_normal:
                        # If Normal add normal node in between
                        normal_node = nodes.new(type='ShaderNodeNormalMap')
                        link = connect_sockets(normal_node.inputs[1], texture_node.outputs[0])
                    elif match_bump:
                        # If Bump add bump node in between
                        normal_node = nodes.new(type='ShaderNodeBump')
                        link = connect_sockets(normal_node.inputs[2], texture_node.outputs[0])

                    link = connect_sockets(active_node.inputs[sname[0]], normal_node.outputs[0])
                    normal_node_texture = texture_node

                elif sname[0] == 'Roughness':
                    # Test if glossy or roughness map
                    fname_components = split_into_components(sname[2])
                    match_rough = set(rough_abbr).intersection(set(fname_components))
                    match_gloss = set(gloss_abbr).intersection(set(fname_components))

                    if match_rough:
                        # If Roughness nothing to to
                        link = connect_sockets(active_node.inputs[sname[0]], texture_node.outputs[0])

                    elif match_gloss:
                        # If Gloss Map add invert node
                        invert_node = nodes.new(type='ShaderNodeInvert')
                        link = connect_sockets(invert_node.inputs[1], texture_node.outputs[0])

                        link = connect_sockets(active_node.inputs[sname[0]], invert_node.outputs[0])
                        roughness_node = texture_node

                else:
                    # This is a simple connection Texture --> Input slot
                    link = connect_sockets(active_node.inputs[sname[0]], texture_node.outputs[0])

                # Use non-color except for color inputs
                if sname[0] not in {'Base Color', 'Emission Color'} and texture_node.image:
                    texture_node.image.colorspace_settings.is_data = True

            else:
                # If already texture connected. add to node list for alignment
                texture_node = active_node.inputs[sname[0]].links[0].from_node

            # This are all connected texture nodes
            texture_nodes.append(texture_node)
            texture_node.label = sname[0]

        if disp_texture:
            texture_nodes.append(disp_texture)

        if ao_texture:
            # We want the ambient occlusion texture to be the top most texture node
            texture_nodes.insert(0, ao_texture)

        # Alignment
        for i, texture_node in enumerate(texture_nodes):
            offset = Vector((-550, (i * -280) + 200))
            texture_node.location = active_node.location + offset

        if normal_node:
            # Extra alignment if normal node was added
            normal_node.location = normal_node_texture.location + Vector((300, 0))

        if roughness_node:
            # Alignment of invert node if glossy map
            invert_node.location = roughness_node.location + Vector((300, 0))

        # Add texture input + mapping
        mapping = nodes.new(type='ShaderNodeMapping')
        mapping.location = active_node.location + Vector((-1050, 0))
        if len(texture_nodes) > 1:
            # If more than one texture add reroute node in between
            reroute = nodes.new(type='NodeReroute')
            texture_nodes.append(reroute)
            tex_coords = Vector((texture_nodes[0].location.x,
                                 sum(n.location.y for n in texture_nodes) / len(texture_nodes)))
            reroute.location = tex_coords + Vector((-50, -120))
            for texture_node in texture_nodes:
                link = connect_sockets(texture_node.inputs[0], reroute.outputs[0])
            link = connect_sockets(reroute.inputs[0], mapping.outputs[0])
        else:
            link = connect_sockets(texture_nodes[0].inputs[0], mapping.outputs[0])

        # Connect texture_coordiantes to mapping node
        texture_input = nodes.new(type='ShaderNodeTexCoord')
        texture_input.location = mapping.location + Vector((-200, 0))
        link = connect_sockets(mapping.inputs[0], texture_input.outputs[2])

        # Create frame around tex coords and mapping
        frame = nodes.new(type='NodeFrame')
        frame.label = 'Mapping'
        mapping.parent = frame
        texture_input.parent = frame
        frame.update()

        # Create frame around texture nodes
        frame = nodes.new(type='NodeFrame')
        frame.label = 'Textures'
        for tnode in texture_nodes:
            tnode.parent = frame
        frame.update()

        # Just to be sure
        active_node.select = False
        nodes.update()
        links.update()
        force_update(context)
        return {'FINISHED'}


class NWAddReroutes(Operator, NWBase):
    """Add Reroute Nodes and link them to outputs of selected nodes"""
    bl_idname = "node.fw_add_reroutes"
    bl_label = "Add Reroutes"
    bl_description = "Add Reroutes to Outputs"
    bl_options = {'REGISTER', 'UNDO'}

    option: EnumProperty(
        name="option",
        items=[
            ('ALL', 'to All Outputs', 'Add to all outputs'),
            ('LOOSE', 'to Loose Outputs', 'Add only to loose outputs'),
            ('LINKED', 'to Linked Outputs', 'Add only to linked outputs'),
        ]
    )

    # TODO - Move this to user-preferences so that it'll stay consistent across operator instances
    x_offset: FloatProperty(name='offset', default=20.0, min=0)
    y_offset: FloatProperty(name='spacing', default=-22.0, max=0)
    
    @staticmethod
    def has_outputs(nodes):
        return (node for node in nodes if len(node.outputs) > 0)

    @staticmethod
    def filter_sockets(sockets):
        for socket in sockets:
            if socket.enabled and not socket.hide and not is_virtual_socket(socket):
                yield socket

    def is_valid(self, socket):
        option = self.option
        return ((option == 'ALL') or
                (option == 'LOOSE' and not socket.is_linked) or
                (option == 'LINKED' and socket.is_linked))

    def execute(self, context):
        tree = context.space_data.edit_tree
        added_reroutes = [] 

        for node in self.has_outputs(context.selected_nodes):   
            # unhide 'REROUTE' nodes to avoid issues with location.y
            if node.type == 'REROUTE':
                node.hide = False

            x = node.location.x + node.width + self.x_offset
            sockets = tuple(self.filter_sockets(node.outputs))

            if node.hide:
                y_init = node.location.y - (len(sockets)/ 2.0 - 1) * self.y_offset
            elif node.type == 'REROUTE':
                y_init = node.location.y
            else:
                node_header = 35.0
                y_init = node.location.y - node_header
            y_locs = itertools.accumulate((self.y_offset for _ in sockets), initial=y_init)

            for output, y_loc in zip(sockets, y_locs):
                # Add reroutes only if valid, but offset location in all cases.
                if self.is_valid(output):
                    reroute = tree.nodes.new('NodeReroute')

                    for link in output.links:
                        tree.links.new(reroute.outputs[0], link.to_socket)
                    tree.links.new(output, reroute.inputs[0])

                    reroute.location = (x, y_loc)
                    added_reroutes.append(reroute)
                    
        if len(added_reroutes) <= 0:
            return {'CANCELLED'}

        bpy.ops.node.select_all(action='DESELECT')
        for node in added_reroutes:
            node.select = True
        tree.nodes.active = node

        return {'FINISHED'}


class NWLinkActiveToSelected(Operator, NWBase):
    """Link active node to selected nodes basing on various criteria"""
    bl_idname = "node.fw_link_active_to_selected"
    bl_label = "Link Active Node to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    replace: BoolProperty()
    use_node_name: BoolProperty()
    use_outputs_names: BoolProperty()

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context):
            if context.active_node is not None:
                if context.active_node.select:
                    valid = True
        return valid

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        replace = self.replace
        use_node_name = self.use_node_name
        use_outputs_names = self.use_outputs_names
        active = nodes.active
        selected = [node for node in nodes if node.select and node != active]
        outputs = []  # Only usable outputs of active nodes will be stored here.
        for out in active.outputs:
            if active.type != 'R_LAYERS':
                outputs.append(out)
            else:
                # 'R_LAYERS' node type needs special handling.
                # outputs of 'R_LAYERS' are callable even if not seen in UI.
                # Only outputs that represent used passes should be taken into account
                # Check if pass represented by output is used.
                # global 'rl_outputs' list will be used for that
                for rlo in rl_outputs:
                    pass_used = False  # initial value. Will be set to True if pass is used
                    if out.name == 'Alpha':
                        # Alpha output is always present. Doesn't have representation in render pass. Assume it's used.
                        pass_used = True
                    elif out.name in {rlo.output_name, rlo.exr_output_name}:
                        # example 'render_pass' entry: 'use_pass_uv' Check if True in scene render layers
                        pass_used = getattr(active.scene.view_layers[active.layer], rlo.render_pass)
                        break
                if pass_used:
                    outputs.append(out)
        doit = True  # Will be changed to False when links successfully added to previous output.
        for out in outputs:
            if doit:
                for node in selected:
                    dst_name = node.name  # Will be compared with src_name if needed.
                    # When node has label - use it as dst_name
                    if node.label:
                        dst_name = node.label
                    valid = True  # Initial value. Will be changed to False if names don't match.
                    src_name = dst_name  # If names not used - this assignment will keep valid = True.
                    if use_node_name:
                        # Set src_name to source node name or label
                        src_name = active.name
                        if active.label:
                            src_name = active.label
                    elif use_outputs_names:
                        src_name = (out.name, )
                        for rlo in rl_outputs:
                            if out.name in {rlo.output_name, rlo.exr_output_name}:
                                src_name = (rlo.output_name, rlo.exr_output_name)
                    if dst_name not in src_name:
                        valid = False
                    if valid:
                        for input in node.inputs:
                            if input.type == out.type or node.type == 'REROUTE':
                                if replace or not input.is_linked:
                                    connect_sockets(out, input)
                                    if not use_node_name and not use_outputs_names:
                                        doit = False
                                    break

        return {'FINISHED'}


class NWAlignNodes(Operator, NWBase):
    '''Align the selected nodes neatly in a row/column'''
    bl_idname = "node.fw_align_nodes"
    bl_label = "Align Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(
        name='Align Mode',
        default='AUTOMATIC',
        items=(
            ('AUTOMATIC', 'Auto-Align', ''),
            ('HORIZONTAL', 'Align X', ''),
            ('VERTICAL', 'Align Y', ''),
        )
    )

    @classmethod
    def description(cls, context, props):
        if props.mode == 'AUTOMATIC':
            return "Aligns nodes horizontally/vertically based on which direction takes more space"
        elif props.mode == 'HORIZONTAL':
            return "Aligns nodes in a row from left to right"
        elif props.mode == 'VERTICAL':
            return "Aligns nodes in a column from top to bottom"

    @classmethod
    @safe_poll
    def poll(cls, context):
        selection = (node for node in context.selected_nodes if node.type != 'FRAME')
        for index, _ in enumerate(selection):
            if index >= 1:
                return fw_check(context)

        return False

    @staticmethod
    def get_midpoint(node, axis):
        reroute_width = 10
        weird_offset = 10

        if axis == 'X':
            width = reroute_width if (node.type == 'REROUTE') else node.dimensions.x
            return node.location.x + (0.5 * width)

        elif axis == 'Y':
            if (node.type == 'REROUTE'):
                return node.location.y - (0.5 * reroute_width)
            elif node.hide:
                return node.location.y - weird_offset
            else:
                return node.location.y - (0.5 * node.dimensions.y)

    def execute(self, context):
        selection = [node for node in context.selected_nodes if node.type != 'FRAME']
        active_node = context.active_node
        prefs = fetch_user_preferences()
        margin_x, margin_y = prefs.align_nodes_margin

        # Somehow hidden nodes would come out 10 units higher that non-hidden nodes when aligned, so this offset has to exist
        weird_offset = 10

        # node.dimensions for reroutes indicate (16.0, 16.0) but using that in calculations puts reroutes off-center
        # At least on a purely visual basis, the dimensions of a reroute node seem to be closer to 10 units. (At least for 1.0 unit scale)
        reroute_width = 10

        with temporary_unframe(nodes=selection):
            active_loc = None
            if active_node in selection:
                active_loc = copy(active_node.location)  # make a copy, not a reference

            x_locs = [self.get_midpoint(n, axis='X') for n in selection]
            y_locs = [self.get_midpoint(n, axis='Y') for n in selection]

            x_range = max(x_locs) - min(x_locs)
            y_range = max(y_locs) - min(y_locs)
            horizontal = x_range > y_range

            mid_x = 0.5 * (max(x_locs) + min(x_locs))
            mid_y = 0.5 * (max(y_locs) + min(y_locs))

            # Sort selection by location of node mid-point
            if horizontal:
                selection.sort(key=lambda n: n.location.x + (n.dimensions.x / 2))
            else:
                selection.sort(key=lambda n: n.location.y - (n.dimensions.y / 2), reverse=True)

            if self.mode != 'AUTOMATIC':
                horizontal = (self.mode == 'HORIZONTAL')

            # Alignment
            current_pos = 0

            if horizontal:
                for node in selection:
                    if node.type != 'REROUTE':
                        node.location.x = current_pos
                        node.location.y = (mid_y + weird_offset) if node.hide else mid_y + (0.5 * node.dimensions.y)

                        current_pos += margin_x + node.dimensions.x
                    else:
                        node.location.x = current_pos + (0.5 * reroute_width)
                        node.location.y = mid_y

                        current_pos += margin_x + reroute_width

            else:
                for node in selection:
                    if node.type != 'REROUTE':
                        node.location.x = mid_x - (0.5 * node.dimensions.x)
                        node.location.y = (current_pos - (0.5 * node.dimensions.y) +
                                           weird_offset) if node.hide else current_pos

                        current_pos -= margin_y + node.dimensions.y
                    else:
                        node.location.x = mid_x
                        node.location.y = current_pos - (0.5 * reroute_width)

                        current_pos -= margin_y + reroute_width

            # If active node is selected, center nodes around it
            if active_loc is not None:
                active_loc_diff = (active_loc - active_node.location)
                for node in selection:
                    node.location += active_loc_diff
            else:
                new_x_locs = [self.get_midpoint(n, axis='X') for n in selection]
                new_y_locs = [self.get_midpoint(n, axis='Y') for n in selection]

                new_x_mid = 0.5 * (max(new_x_locs) + min(new_x_locs))
                new_y_mid = 0.5 * (max(new_y_locs) + min(new_y_locs))

                x_diff = mid_x - new_x_mid
                y_diff = mid_y - new_y_mid

                for node in selection:
                    node.location.x += x_diff
                    node.location.y += y_diff

        return {'FINISHED'}


class NWSelectParentChildren(Operator, NWBase):
    bl_idname = "node.fw_select_parent_child"
    bl_label = "Select Parent or Children"
    bl_options = {'REGISTER', 'UNDO'}

    option: EnumProperty(
        name="option",
        items=(
            ('PARENT', 'Select Parent', 'Select Parent Frame'),
            ('CHILD', 'Select Children', 'Select members of selected frame'),
        )
    )

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        option = self.option
        selected = [node for node in nodes if node.select]
        if option == 'PARENT':
            for sel in selected:
                parent = sel.parent
                if parent:
                    parent.select = True
        else:  # option == 'CHILD'
            for sel in selected:
                children = [node for node in nodes if node.parent == sel]
                for kid in children:
                    kid.select = True

        return {'FINISHED'}


class NWDetachOutputs(Operator, NWBase):
    """Detach outputs of selected node leaving inputs linked"""
    bl_idname = "node.fw_detach_outputs"
    bl_label = "Detach Outputs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        selected = context.selected_nodes
        bpy.ops.node.duplicate_move_keep_inputs()
        new_nodes = context.selected_nodes
        bpy.ops.node.select_all(action="DESELECT")
        for node in selected:
            node.select = True
        bpy.ops.node.delete_reconnect()
        for new_node in new_nodes:
            new_node.select = True
        bpy.ops.transform.translate('INVOKE_DEFAULT')

        return {'FINISHED'}


class NWLinkToOutputNode(Operator):
    """Link to Composite node or Material Output node"""
    bl_idname = "node.fw_link_out"
    bl_label = "Connect to Output"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context):
            if context.active_node is not None:
                for out in context.active_node.outputs:
                    if is_visible_socket(out):
                        valid = True
                        break
        return valid

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        active = nodes.active
        output_index = None
        tree_type = context.space_data.tree_type
        shader_outputs = {'OBJECT': 'ShaderNodeOutputMaterial',
                          'WORLD': 'ShaderNodeOutputWorld',
                          'LINESTYLE': 'ShaderNodeOutputLineStyle'}
        output_type = {
            'ShaderNodeTree': shader_outputs[context.space_data.shader_type],
            'CompositorNodeTree': 'CompositorNodeComposite',
            'TextureNodeTree': 'TextureNodeOutput',
            'GeometryNodeTree': 'NodeGroupOutput',
        }[tree_type]
        for node in nodes:
            # check whether the node is an output node and,
            # if supported, whether it's the active one
            if node.rna_type.identifier == output_type \
               and (node.is_active_output if hasattr(node, 'is_active_output')
                    else True):
                output_node = node
                break
        else:  # No output node exists
            bpy.ops.node.select_all(action="DESELECT")
            output_node = nodes.new(output_type)
            output_node.location.x = active.location.x + active.dimensions.x + 80
            output_node.location.y = active.location.y

        if active.outputs:
            for i, output in enumerate(active.outputs):
                if is_visible_socket(output):
                    output_index = i
                    break
            for i, output in enumerate(active.outputs):
                if output.type == output_node.inputs[0].type and is_visible_socket(output):
                    output_index = i
                    break

            out_input_index = 0
            if tree_type == 'ShaderNodeTree':
                if active.outputs[output_index].name == 'Volume':
                    out_input_index = 1
                elif active.outputs[output_index].name == 'Displacement':
                    out_input_index = 2
            elif tree_type == 'GeometryNodeTree':
                if active.outputs[output_index].type != 'GEOMETRY':
                    return {'CANCELLED'}
            connect_sockets(active.outputs[output_index], output_node.inputs[out_input_index])

        force_update(context)  # viewport render does not update

        return {'FINISHED'}


class NWMakeLink(Operator, NWBase):
    """Make a link from one socket to another"""
    bl_idname = 'node.fw_make_link'
    bl_label = 'Make Link'
    bl_options = {'REGISTER', 'UNDO'}
    from_socket: IntProperty()
    to_socket: IntProperty()

    def execute(self, context):
        nodes, links = get_nodes_links(context)

        n1 = nodes[context.scene.NWLazySource]
        n2 = nodes[context.scene.NWLazyTarget]

        connect_sockets(n1.outputs[self.from_socket], n2.inputs[self.to_socket])

        force_update(context)

        return {'FINISHED'}


class NWCallInputsMenu(Operator, NWBase):
    """Link from this output"""
    bl_idname = 'node.fw_call_inputs_menu'
    bl_label = 'Make Link'
    bl_options = {'REGISTER', 'UNDO'}
    from_socket: IntProperty()

    def execute(self, context):
        nodes, links = get_nodes_links(context)

        context.scene.NWSourceSocket = self.from_socket

        n1 = nodes[context.scene.NWLazySource]
        n2 = nodes[context.scene.NWLazyTarget]
        if len(n2.inputs) > 1:
            bpy.ops.wm.call_menu("INVOKE_DEFAULT", name=NWConnectionListInputs.bl_idname)
        elif len(n2.inputs) == 1:
            connect_sockets(n1.outputs[self.from_socket], n2.inputs[0])
        return {'FINISHED'}


class NWAddSequence(Operator, NWBase, ImportHelper):
    """Add an Image Sequence"""
    bl_idname = 'node.fw_add_sequence'
    bl_label = 'Import Image Sequence'
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(
        subtype="DIR_PATH"
    )
    filename: StringProperty(
        subtype="FILE_NAME"
    )
    files: CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
    )
    relative_path: BoolProperty(
        name='Relative Path',
        description='Set the file path relative to the blend file, when possible',
        default=True
    )

    def draw(self, context):
        layout = self.layout
        layout.alignment = 'LEFT'

        layout.prop(self, 'relative_path')

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        directory = self.directory
        filename = self.filename
        files = self.files
        tree = context.space_data.node_tree

        # DEBUG
        # print ("\nDIR:", directory)
        # print ("FN:", filename)
        # print ("Fs:", list(f.name for f in files), '\n')

        if tree.type == 'SHADER':
            node_type = "ShaderNodeTexImage"
        elif tree.type == 'COMPOSITING':
            node_type = "CompositorNodeImage"
        else:
            self.report({'ERROR'}, "Unsupported Node Tree type!")
            return {'CANCELLED'}

        if not files[0].name and not filename:
            self.report({'ERROR'}, "No file chosen")
            return {'CANCELLED'}
        elif files[0].name and (not filename or not path.exists(directory + filename)):
            # User has selected multiple files without an active one, or the active one is non-existent
            filename = files[0].name

        if not path.exists(directory + filename):
            self.report({'ERROR'}, filename + " does not exist!")
            return {'CANCELLED'}

        without_ext = '.'.join(filename.split('.')[:-1])

        # if last digit isn't a number, it's not a sequence
        if not without_ext[-1].isdigit():
            self.report({'ERROR'}, filename + " does not seem to be part of a sequence")
            return {'CANCELLED'}

        extension = filename.split('.')[-1]
        reverse = without_ext[::-1]  # reverse string

        count_numbers = 0
        for char in reverse:
            if char.isdigit():
                count_numbers += 1
            else:
                break

        without_num = without_ext[:count_numbers * -1]

        files = sorted(glob(directory + without_num + "[0-9]" * count_numbers + "." + extension))

        num_frames = len(files)

        nodes_list = [node for node in nodes]
        if nodes_list:
            nodes_list.sort(key=lambda k: k.location.x)
            xloc = nodes_list[0].location.x - 220  # place new nodes at far left
            yloc = 0
            for node in nodes:
                node.select = False
                yloc += node_mid_pt(node, 'y')
            yloc = yloc / len(nodes)
        else:
            xloc = 0
            yloc = 0

        name_with_hashes = without_num + "#" * count_numbers + '.' + extension

        bpy.ops.node.add_node('INVOKE_DEFAULT', use_transform=True, type=node_type)
        node = nodes.active
        node.label = name_with_hashes

        filepath = directory + (without_ext + '.' + extension)
        if self.relative_path:
            if bpy.data.filepath:
                try:
                    filepath = bpy.path.relpath(filepath)
                except ValueError:
                    pass

        img = bpy.data.images.load(filepath)
        img.source = 'SEQUENCE'
        img.name = name_with_hashes
        node.image = img
        image_user = node.image_user if tree.type == 'SHADER' else node
        # separate the number from the file name of the first  file
        image_user.frame_offset = int(files[0][len(without_num) + len(directory):-1 * (len(extension) + 1)]) - 1
        image_user.frame_duration = num_frames

        return {'FINISHED'}


class NWAddMultipleImages(Operator, NWBase, ImportHelper):
    """Add multiple images at once"""
    bl_idname = 'node.fw_add_multiple_images'
    bl_label = 'Open Selected Images'
    bl_options = {'REGISTER', 'UNDO'}
    directory: StringProperty(
        subtype="DIR_PATH"
    )
    files: CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
    )

    def execute(self, context):
        nodes, links = get_nodes_links(context)

        xloc, yloc = context.region.view2d.region_to_view(context.area.width / 2, context.area.height / 2)

        if context.space_data.node_tree.type == 'SHADER':
            node_type = "ShaderNodeTexImage"
        elif context.space_data.node_tree.type == 'COMPOSITING':
            node_type = "CompositorNodeImage"
        else:
            self.report({'ERROR'}, "Unsupported Node Tree type!")
            return {'CANCELLED'}

        new_nodes = []
        for f in self.files:
            fname = f.name

            node = nodes.new(node_type)
            new_nodes.append(node)
            node.label = fname
            node.hide = True
            node.location.x = xloc
            node.location.y = yloc
            yloc -= 40

            img = bpy.data.images.load(self.directory + fname)
            node.image = img

        # shift new nodes up to center of tree
        list_size = new_nodes[0].location.y - new_nodes[-1].location.y
        for node in nodes:
            if node in new_nodes:
                node.select = True
                node.location.y += (list_size / 2)
            else:
                node.select = False
        return {'FINISHED'}


class NWViewerFocus(bpy.types.Operator):
    """Set the viewer tile center to the mouse position"""
    bl_idname = "node.fw_viewer_focus"
    bl_label = "Viewer Focus"

    x: bpy.props.IntProperty()
    y: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return fw_check(context) and context.space_data.tree_type == 'CompositorNodeTree'

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        render = context.scene.render
        space = context.space_data
        percent = render.resolution_percentage * 0.01

        nodes, links = get_nodes_links(context)
        viewers = [n for n in nodes if n.type == 'VIEWER']

        if viewers:
            mlocx = event.mouse_region_x
            mlocy = event.mouse_region_y
            select_node = bpy.ops.node.select(location=(mlocx, mlocy), extend=False)

            if 'FINISHED' not in select_node:  # only run if we're not clicking on a node
                region_x = context.region.width
                region_y = context.region.height

                region_center_x = context.region.width / 2
                region_center_y = context.region.height / 2

                bd_x = render.resolution_x * percent * space.backdrop_zoom
                bd_y = render.resolution_y * percent * space.backdrop_zoom

                backdrop_center_x = (bd_x / 2) - space.backdrop_offset[0]
                backdrop_center_y = (bd_y / 2) - space.backdrop_offset[1]

                margin_x = region_center_x - backdrop_center_x
                margin_y = region_center_y - backdrop_center_y

                abs_mouse_x = (mlocx - margin_x) / bd_x
                abs_mouse_y = (mlocy - margin_y) / bd_y

                for node in viewers:
                    node.center_x = abs_mouse_x
                    node.center_y = abs_mouse_y
            else:
                return {'PASS_THROUGH'}

        return self.execute(context)

def region_to_view(context, location):
    region = context.region
    x, y = region.view2d.view_to_region(*location, clip=False)

class NWSaveViewer(bpy.types.Operator, ExportHelper):
    """Save the current viewer node to an image file"""
    bl_idname = "node.fw_save_viewer"
    bl_label = "Save This Image"
    filepath: StringProperty(subtype="FILE_PATH")
    filename_ext: EnumProperty(
        name="Format",
        description="Choose the file format to save to",
        items=(('.bmp', "BMP", ""),
               ('.rgb', 'IRIS', ""),
               ('.png', 'PNG', ""),
               ('.jpg', 'JPEG', ""),
               ('.jp2', 'JPEG2000', ""),
               ('.tga', 'TARGA', ""),
               ('.cin', 'CINEON', ""),
               ('.dpx', 'DPX', ""),
               ('.exr', 'OPEN_EXR', ""),
               ('.hdr', 'HDR', ""),
               ('.tif', 'TIFF', "")),
        default='.png',
    )

    @classmethod
    def poll(cls, context):
        valid = False
        if fw_check(context):
            if context.space_data.tree_type == 'CompositorNodeTree':
                if "Viewer Node" in [i.name for i in bpy.data.images]:
                    if sum(bpy.data.images["Viewer Node"].size) > 0:  # False if not connected or connected but no image
                        valid = True
        return valid

    def execute(self, context):
        fp = self.filepath
        if fp:
            formats = {
                '.bmp': 'BMP',
                '.rgb': 'IRIS',
                '.png': 'PNG',
                '.jpg': 'JPEG',
                '.jpeg': 'JPEG',
                '.jp2': 'JPEG2000',
                '.tga': 'TARGA',
                '.cin': 'CINEON',
                '.dpx': 'DPX',
                '.exr': 'OPEN_EXR',
                '.hdr': 'HDR',
                '.tiff': 'TIFF',
                '.tif': 'TIFF'}
            basename, ext = path.splitext(fp)
            old_render_format = context.scene.render.image_settings.file_format
            context.scene.render.image_settings.file_format = formats[self.filename_ext]
            context.area.type = "IMAGE_EDITOR"
            context.area.spaces[0].image = bpy.data.images['Viewer Node']
            context.area.spaces[0].image.save_render(fp)
            context.area.type = "NODE_EDITOR"
            context.scene.render.image_settings.file_format = old_render_format
            return {'FINISHED'}


class NWResetNodes(bpy.types.Operator):
    """Reset Nodes in Selection"""
    bl_idname = "node.fw_reset_nodes"
    bl_label = "Reset Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):
        node_active = context.active_node
        node_selected = context.selected_nodes
        node_ignore = ["FRAME", "REROUTE", "GROUP", "SIMULATION_INPUT", "SIMULATION_OUTPUT"]

        # Check if one node is selected at least
        if not (len(node_selected) > 0):
            self.report({'ERROR'}, "1 node must be selected at least")
            return {'CANCELLED'}

        active_node_name = node_active.name if node_active.select else None
        valid_nodes = [n for n in node_selected if n.type not in node_ignore]

        # Create output lists
        selected_node_names = [n.name for n in node_selected]
        success_names = []

        # Reset all valid children in a frame
        node_active_is_frame = False
        if len(node_selected) == 1 and node_active.type == "FRAME":
            node_tree = node_active.id_data
            children = [n for n in node_tree.nodes if n.parent == node_active]
            if children:
                valid_nodes = [n for n in children if n.type not in node_ignore]
                selected_node_names = [n.name for n in children if n.type not in node_ignore]
                node_active_is_frame = True

        # Check if valid nodes in selection
        if not (len(valid_nodes) > 0):
            # Check for frames only
            frames_selected = [n for n in node_selected if n.type == "FRAME"]
            if (len(frames_selected) > 1 and len(frames_selected) == len(node_selected)):
                self.report({'ERROR'}, "Please select only 1 frame to reset")
            else:
                self.report({'ERROR'}, "No valid node(s) in selection")
            return {'CANCELLED'}

        # Report nodes that are not valid
        if len(valid_nodes) != len(node_selected) and node_active_is_frame is False:
            valid_node_names = [n.name for n in valid_nodes]
            not_valid_names = list(set(selected_node_names) - set(valid_node_names))
            self.report({'INFO'}, "Ignored {}".format(", ".join(not_valid_names)))

        # Deselect all nodes
        for i in node_selected:
            i.select = False

        # Run through all valid nodes
        for node in valid_nodes:

            parent = node.parent if node.parent else None
            node_loc = [node.location.x, node.location.y]

            node_tree = node.id_data
            props_to_copy = 'bl_idname name location height width'.split(' ')

            reconnections = []
            mappings = chain.from_iterable([node.inputs, node.outputs])
            for i in (i for i in mappings if i.is_linked):
                for L in i.links:
                    reconnections.append([L.from_socket.path_from_id(), L.to_socket.path_from_id()])

            props = {j: getattr(node, j) for j in props_to_copy}

            new_node = node_tree.nodes.new(props['bl_idname'])
            props_to_copy.pop(0)

            for prop in props_to_copy:
                setattr(new_node, prop, props[prop])

            nodes = node_tree.nodes
            nodes.remove(node)
            new_node.name = props['name']

            if parent:
                new_node.parent = parent
                new_node.location = node_loc

            for str_from, str_to in reconnections:
                node_tree.links.new(eval(str_from), eval(str_to))

            new_node.select = False
            success_names.append(new_node.name)

        # Reselect all nodes
        if selected_node_names and node_active_is_frame is False:
            for i in selected_node_names:
                node_tree.nodes[i].select = True

        if active_node_name is not None:
            node_tree.nodes[active_node_name].select = True
            node_tree.nodes.active = node_tree.nodes[active_node_name]

        self.report({'INFO'}, "Successfully reset {}".format(", ".join(success_names)))
        return {'FINISHED'}


classes = (
    NodeSetting,
    NWLazyMix,
    NWLazyConnect,
    NWDeleteUnused,
    NWSwapLinks,
    NWResetBG,
    NWAddAttrNode,
    NWAddNamedAttrNode,
    NWPreviewNode,
    NWFrameSelected,
    NWReloadImages,
    NWSwitchNodeType,
    NWMergeNodes,
    NWMergeNodesRefactored,
    NWBatchChangeNodes,
    NWChangeMixFactor,
    NWCopySettings,
    NWCopyLabel,
    NWClearLabel,
    NWModifyLabels,
    NWAddTextureSetup,
    NWAddPrincipledSetup,
    NWAddReroutes,
    NWLinkActiveToSelected,
    NWAlignNodes,
    NWSelectParentChildren,
    NWDetachOutputs,
    NWLinkToOutputNode,
    NWMakeLink,
    NWCallInputsMenu,
    NWAddSequence,
    NWAddMultipleImages,
    NWViewerFocus,
    NWSaveViewer,
    NWResetNodes,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
