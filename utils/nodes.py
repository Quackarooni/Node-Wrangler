# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from math import hypot
from itertools import zip_longest, filterfalse

def n_wise_iter(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip_longest(*[iter(iterable)]*n)

def filter_nodes_by_type(nodes, types, tree_type=None, *, invert=False):
    if isinstance(types, str):
        types = (types,)

    if tree_type is None:
        tree_type = bpy.context.space_data.tree_type

    if tree_type in ('ShaderNodeTree', 'GeometryNodeTree'):
        if 'MIX_RGB' in types:
            condition = lambda n : (n.type in types) or (n.bl_idname == 'ShaderNodeMix' and n.data_type == 'RGBA')
        else:
            condition = lambda n : (n.type in types)

    elif tree_type in ('CompositorNodeTree', 'TextureNodeTree'):
        condition = lambda n : (n.type in types)
    else:
        raise NotImplementedError(f"Function has no implemented behavior for NodeTree of type {tree_type}")

    if invert:
        return filterfalse(condition, nodes)
    else:
        return filter(condition, nodes)

def next_in_list(items, key, *, wrap=False):
    index = items.index(key)
    max_index = len(items) - 1

    if index == max_index:
        if wrap is True:
            return items[0]
        else:
            return items[max_index]
    else:
        return items[index + 1]

def prev_in_list(items, key, *, wrap=False):
    index = items.index(key)
    max_index = len(items) - 1

    if index == 0:
        if wrap is True:
            return items[max_index]
        else:
            return items[0]
    else:
        return items[index - 1]


def fetch_user_preferences(attr_id=None):
    prefs = bpy.context.preferences.addons["Node Wrangler"].preferences

    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)

def get_sim_output_node(node):
    if node.bl_idname == 'GeometryNodeSimulationInput':
        return node.paired_output
    if node.bl_idname == 'GeometryNodeSimulationOutput':
        return node

def connect_sockets(input, output):
    """
    Connect sockets in a node tree.

    This is useful because the links created through the normal Python API are
    invalid when one of the sockets is a virtual socket (grayed out sockets in
    Group Input and Group Output nodes).

    It replaces node_tree.links.new(input, output)
    """
    import bpy

    # Swap sockets if they are not passed in the proper order
    if input.is_output and not output.is_output:
        input, output = output, input

    input_node = output.node
    output_node = input.node

    if input_node.id_data is not output_node.id_data:
        #print("Sockets do not belong to the same node tree")
        return

    if is_virtual_socket(input) and is_virtual_socket(output):
        #print("Cannot connect two virtual sockets together")
        return
    
    if input.type != output.type and not (is_virtual_socket(input) and is_virtual_socket(output)):
        if 'GEOMETRY' in (input.type, output.type):
            #print("Cannot connect geometry and non-geometry socket together")
            return 

        if ('SHADER' == output.type) and ('SHADER' != input.type):
            #print("Cannot connect shader output to not shader input")
            return 

    if output_node.type in ('SIMULATION_INPUT', 'SIMULATION_OUTPUT') and type(input) == bpy.types.NodeSocketVirtual:
        get_sim_output_node(output_node).state_items.new(output.type, output.name)
        input = output_node.inputs[-2]

    if input_node.type in ('SIMULATION_INPUT', 'SIMULATION_OUTPUT')  and type(output) == bpy.types.NodeSocketVirtual:
        get_sim_output_node(input_node).state_items.new(input.type, input.name)
        output = input_node.outputs[-2]

    if output_node.type in ('GROUP_OUTPUT',) and type(input) == bpy.types.NodeSocketVirtual:
        output_node.id_data.outputs.new(type(output).__name__, output.name)
        input = output_node.inputs[-2]

    if input_node.type in ('GROUP_INPUT',) and type(output) == bpy.types.NodeSocketVirtual:
        input_node.id_data.inputs.new(type(input).__name__, input.name)
        output = input_node.outputs[-2]

    return input_node.id_data.links.new(input, output)


def force_update(context):
    context.space_data.node_tree.update_tag()


def dpi_fac():
    prefs = bpy.context.preferences.system
    return prefs.dpi / 72


def prefs_line_width():
    prefs = bpy.context.preferences.system
    return prefs.pixel_size


def node_mid_pt(node, axis):
    if axis == 'x':
        d = node.location.x + (node.dimensions.x / 2)
    elif axis == 'y':
        d = node.location.y - (node.dimensions.y / 2)
    else:
        d = 0
    return d


def get_bounds(nodes):
    weird_offset = 10
    min_x, max_x, min_y, max_y = None, None, None, None

    for index, node in enumerate(nodes):
        x_curr_min = node.location.x
        x_curr_max = node.location.x + node.dimensions.x
        y_curr_min = (node.location.y - node.dimensions.y) if not node.hide else (node.location.y - weird_offset - 0.5*node.dimensions.y)
        y_curr_max = (node.location.y) if not node.hide else (node.location.y - weird_offset + 0.5*node.dimensions.y)

        if not index:
            min_x = x_curr_min
            max_x = x_curr_max
            min_y = y_curr_min
            max_y = y_curr_max
        else:
            min_x = min(x_curr_min, min_x)
            max_x = max(x_curr_max, max_x)
            min_y = min(y_curr_min, min_y)
            max_y = max(y_curr_max, max_y)

    return min_x, max_x, min_y, max_y

class FinishedAutolink(Exception):
    def __init__(self, *args):
        pass

def is_virtual_socket(socket):
    return isinstance(socket, bpy.types.NodeSocketVirtual)

def autolink(node1, node2, links):
    available_inputs = [inp for inp in node2.inputs if inp.enabled]
    available_outputs = [outp for outp in node1.outputs if outp.enabled]
    visible_inputs = [inp for inp in node2.inputs if (inp.enabled and not inp.hide)]
    visible_outputs = [outp for outp in node1.outputs if (outp.enabled and not outp.hide)]

    def autolink_iter(inputs, outputs, condition=(lambda a,b: True)):
        for outp in outputs:
            for inp in inputs:
                if condition(inp, outp):
                    new_link = connect_sockets(outp, inp)

                    if new_link is not None:
                        raise FinishedAutolink


    autolink_iter(visible_inputs, visible_outputs, 
        condition=(lambda inp, outp: (not inp.is_linked and not outp.is_linked) and inp.name == outp.name))
    autolink_iter(visible_inputs, visible_outputs, 
        condition=(lambda inp, outp: (not inp.is_linked and not outp.is_linked) 
            and len(set(inp.name.split(" ")) & set(outp.name.split(" "))) > 0 ))
    
    autolink_iter(available_inputs, available_outputs, 
        condition=(lambda inp, outp: (not inp.is_linked and not outp.is_linked) and inp.name == outp.name))
    autolink_iter(visible_inputs, visible_outputs, 
        condition=(lambda inp, outp: not inp.is_linked and inp.name == outp.name))
    autolink_iter(available_inputs, available_outputs, 
        condition=(lambda inp, outp: not inp.is_linked and inp.name == outp.name))

    autolink_iter(visible_inputs, visible_outputs, 
        condition=(lambda inp, outp: (not inp.is_linked and not outp.is_linked) and inp.type == outp.type))
    autolink_iter(visible_inputs, visible_outputs, 
        condition=(lambda inp, outp: not inp.is_linked and inp.type == outp.type))
    autolink_iter(visible_inputs, visible_outputs, 
        condition=(lambda inp, outp: not inp.is_linked))
    autolink_iter(visible_inputs, visible_outputs, 
        condition=(lambda inp, outp: inp.type == outp.type))

    autolink_iter(available_inputs, available_outputs, 
        condition=(lambda inp, outp: not inp.is_linked))
    autolink_iter(available_inputs, available_outputs, 
        condition=(lambda inp, outp: not inp.is_linked and inp.type == outp.type))
    autolink_iter(visible_inputs, visible_outputs)

    print("Could not make a link from " + node1.name + " to " + node2.name)


def abs_node_location(node):
    abs_location = node.location
    if node.parent is None:
        return abs_location
    return abs_location + abs_node_location(node.parent)


def node_at_pos(nodes, context, event):
    nodes_under_mouse = []
    target_node = None

    store_mouse_cursor(context, event)
    x, y = context.space_data.cursor_location

    # Make a list of each corner (and middle of border) for each node.
    # Will be sorted to find nearest point and thus nearest node
    node_points_with_dist = []
    for node in nodes:
        skipnode = False
        if node.type != 'FRAME':  # no point trying to link to a frame node
            dimx = node.dimensions.x / dpi_fac()
            dimy = node.dimensions.y / dpi_fac()
            locx, locy = abs_node_location(node)

            if not skipnode:
                node_points_with_dist.append([node, hypot(x - locx, y - locy)])  # Top Left
                node_points_with_dist.append([node, hypot(x - (locx + dimx), y - locy)])  # Top Right
                node_points_with_dist.append([node, hypot(x - locx, y - (locy - dimy))])  # Bottom Left
                node_points_with_dist.append([node, hypot(x - (locx + dimx), y - (locy - dimy))])  # Bottom Right

                node_points_with_dist.append([node, hypot(x - (locx + (dimx / 2)), y - locy)])  # Mid Top
                node_points_with_dist.append([node, hypot(x - (locx + (dimx / 2)), y - (locy - dimy))])  # Mid Bottom
                node_points_with_dist.append([node, hypot(x - locx, y - (locy - (dimy / 2)))])  # Mid Left
                node_points_with_dist.append([node, hypot(x - (locx + dimx), y - (locy - (dimy / 2)))])  # Mid Right

    nearest_node = sorted(node_points_with_dist, key=lambda k: k[1])[0][0]

    for node in nodes:
        if node.type != 'FRAME' and skipnode == False:
            locx, locy = abs_node_location(node)
            dimx = node.dimensions.x / dpi_fac()
            dimy = node.dimensions.y / dpi_fac()
            if (locx <= x <= locx + dimx) and \
               (locy - dimy <= y <= locy):
                nodes_under_mouse.append(node)

    if len(nodes_under_mouse) == 1:
        if nodes_under_mouse[0] != nearest_node:
            target_node = nodes_under_mouse[0]  # use the node under the mouse if there is one and only one
        else:
            target_node = nearest_node  # else use the nearest node
    else:
        target_node = nearest_node
    return target_node


def store_mouse_cursor(context, event):
    space = context.space_data
    v2d = context.region.view2d
    tree = space.edit_tree

    # convert mouse position to the View2D for later node placement
    if context.region.type == 'WINDOW':
        space.cursor_location_from_region(event.mouse_region_x, event.mouse_region_y)
    else:
        space.cursor_location = tree.view_center


def get_active_tree(context):
    tree = context.space_data.node_tree
    path = []
    # Get nodes from currently edited tree.
    # If user is editing a group, space_data.node_tree is still the base level (outside group).
    # context.active_node is in the group though, so if space_data.node_tree.nodes.active is not
    # the same as context.active_node, the user is in a group.
    # Check recursively until we find the real active node_tree:
    if tree.nodes.active:
        while tree.nodes.active != context.active_node:
            tree = tree.nodes.active.node_tree
            path.append(tree)
    return tree, path


def get_nodes_links(context):
    tree, path = get_active_tree(context)
    return tree.nodes, tree.links


viewer_socket_name = "tmp_viewer"


def is_viewer_socket(socket):
    # checks if a internal socket is a valid viewer socket
    return socket.name == viewer_socket_name and socket.NWViewerSocket


def get_internal_socket(socket):
    # get the internal socket from a socket inside or outside the group
    node = socket.node
    if node.type == 'GROUP_OUTPUT':
        source_iterator = node.inputs
        iterator = node.id_data.outputs
    elif node.type == 'GROUP_INPUT':
        source_iterator = node.outputs
        iterator = node.id_data.inputs
    elif hasattr(node, "node_tree"):
        if socket.is_output:
            source_iterator = node.outputs
            iterator = node.node_tree.outputs
        else:
            source_iterator = node.inputs
            iterator = node.node_tree.inputs
    else:
        return None

    for i, s in enumerate(source_iterator):
        if s == socket:
            break
    return iterator[i]


def is_viewer_link(link, output_node):
    if link.to_node == output_node and link.to_socket == output_node.inputs[0]:
        return True
    if link.to_node.type == 'GROUP_OUTPUT':
        socket = get_internal_socket(link.to_socket)
        if is_viewer_socket(socket):
            return True
    return False


def get_group_output_node(tree):
    for node in tree.nodes:
        if node.type == 'GROUP_OUTPUT' and node.is_active_output:
            return node


def get_output_location(tree):
    # get right-most location
    sorted_by_xloc = (sorted(tree.nodes, key=lambda x: x.location.x))
    max_xloc_node = sorted_by_xloc[-1]

    # get average y location
    sum_yloc = 0
    for node in tree.nodes:
        sum_yloc += node.location.y

    loc_x = max_xloc_node.location.x + max_xloc_node.dimensions.x + 80
    loc_y = sum_yloc / len(tree.nodes)
    return loc_x, loc_y


def fw_check(context):
    space = context.space_data
    valid_trees = ["ShaderNodeTree", "CompositorNodeTree", "TextureNodeTree", "GeometryNodeTree"]

    if (space.type == 'NODE_EDITOR'
            and space.node_tree is not None
            and space.node_tree.library is None
            and space.tree_type in valid_trees):
        return True

    return False


def get_first_enabled_output(node):
    for output in node.outputs:
        if output.enabled:
            return output
    else:
        return node.outputs[0]


def is_visible_socket(socket):
    return not socket.hide and socket.enabled and socket.type != 'CUSTOM'


class temporary_unframe():  # Context manager for temporarily unparenting nodes from their frames
    def __init__(self, nodes):
        self.parent_dict = {}
        for node in nodes:
            if node.parent is not None:
                self.parent_dict[node] = node.parent
            node.parent = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for node, parent in self.parent_dict.items():
            node.parent = parent


class NWBase:
    @classmethod
    def poll(cls, context):
        return fw_check(context)
