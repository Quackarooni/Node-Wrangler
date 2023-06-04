import bpy
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

node_tree_group_type = {
    'CompositorNodeTree': 'CompositorNodeGroup',
    'ShaderNodeTree': 'ShaderNodeGroup',
    'TextureNodeTree': 'TextureNodeGroup',
    'GeometryNodeTree': 'GeometryNodeGroup',
}       
  
def contains_tree(nodetree, group, level=0):
    if nodetree == group and level == 0:
        return True
    else:
        for node in nodetree.nodes:
            if node.type != 'GROUP':
                continue

            if node.bl_idname in node_tree_group_type.values() and node.node_tree is not None:
                if contains_tree(node.node_tree, group, level=level + 1):
                    return True
    return False      


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

        #if node_tree in all_node_groups.values():
        layout.separator()
        switch_node_type(layout, "NodeGroupInput")
        switch_node_type(layout, "NodeGroupOutput")

        if node_tree:
            from nodeitems_builtins import node_tree_group_type

            groups = [
                group for group in context.blend_data.node_groups
                if (group.bl_idname == node_tree.bl_idname and
                    not contains_tree(node_tree, group) and
                    not group.name.startswith('.'))
            ]
            if groups:
                layout.separator()
                for group in groups:
                    props = switch_node_type(layout, node_tree_group_type[group.bl_idname], label=group.name)
                    ops = props.settings.add()
                    ops.name = "node_tree"
                    ops.value = "bpy.data.node_groups[%r]" % group.name

classes = (
        NODE_MT_NWSwitchNodes_GN_group,
        )

def register():  
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


