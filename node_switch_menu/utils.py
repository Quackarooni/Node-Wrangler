
import bpy
from bpy.types import Menu
from .. import operators
from bpy.app.translations import (
    pgettext_iface as iface_,
    contexts as i18n_contexts,
)


def switch_node_type(layout, node_type, *, label=None, poll=None):
    """Add a node type to a menu."""
    bl_rna = bpy.types.Node.bl_rna_get_subclass(node_type)
    if not label:
        label = bl_rna.name if bl_rna else iface_("Unknown")

    if poll is True or poll is None:
        translation_context = bl_rna.translation_context if bl_rna else i18n_contexts.default
        props = layout.operator(operators.NWSwitchNodeType.bl_idname, text=label, text_ctxt=translation_context)
        props.to_type = node_type
        return props


class NODE_MT_NWSwitchNodes_category_layout(Menu):
    bl_label = "Layout"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, _context):
        layout = self.layout
        switch_node_type(layout, "NodeReroute")


class NODE_MT_NWSwitchNodes_category_group(Menu):
    bl_label = "Group"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    @classmethod
    def valid_groups(cls, context):
        node_tree = context.space_data.edit_tree
        valid_groups = tuple(
                group for group in context.blend_data.node_groups
                if (group.bl_idname == node_tree.bl_idname and
                    not group.contains_tree(node_tree) and
                    not group.name.startswith('.')))

        return valid_groups

    @classmethod
    def poll(cls, context):
        is_nodegroup = context.space_data.edit_tree in context.blend_data.node_groups.values()
        has_other_nodegroups = len(cls.valid_groups(context)) > 0
        return is_nodegroup and has_other_nodegroups

    @staticmethod
    def group_node_id(tree):
        return tree.removesuffix("Tree") + "Group"

    def draw(self, context):
        layout = self.layout

        """Add items to the layout used for interacting with node groups."""
        space_node = context.space_data
        node_tree = space_node.edit_tree
        all_node_groups = context.blend_data.node_groups

        if node_tree in all_node_groups.values():
            layout.separator()
            switch_node_type(layout, "NodeGroupInput")
            switch_node_type(layout, "NodeGroupOutput")

        if node_tree is not None:
            groups = self.valid_groups(context)
            if len(groups) > 0:
                layout.separator()
                for group in groups:
                    props = switch_node_type(layout, self.group_node_id(group.bl_idname), label=group.name)
                    ops = props.settings.add()
                    ops.name = "node_tree"
                    ops.value = "bpy.data.node_groups[%r]" % group.name


classes = (
    NODE_MT_NWSwitchNodes_category_layout,
    NODE_MT_NWSwitchNodes_category_group,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)