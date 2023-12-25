# SPDX-FileCopyrightText: 2019-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty, IntVectorProperty

from .keymap_defs import kmi_defs
from . import interface

from .utils.constants import nice_hotkey_name
from rna_keymap_ui import _indented_layout as indented_layout
from itertools import groupby


# Principled prefs
class NWPrincipledPreferences(bpy.types.PropertyGroup):
    base_color: StringProperty(
        name='Base Color',
        default='diffuse diff albedo base col color basecolor',
        description='Naming Components for Base Color maps')
    metallic: StringProperty(
        name='Metallic',
        default='metallic metalness metal mtl',
        description='Naming Components for metallness maps')
    specular: StringProperty(
        name='Specular',
        default='specularity specular spec spc',
        description='Naming Components for Specular maps')
    normal: StringProperty(
        name='Normal',
        default='normal nor nrm nrml norm',
        description='Naming Components for Normal maps')
    bump: StringProperty(
        name='Bump',
        default='bump bmp',
        description='Naming Components for bump maps')
    rough: StringProperty(
        name='Roughness',
        default='roughness rough rgh',
        description='Naming Components for roughness maps')
    gloss: StringProperty(
        name='Gloss',
        default='gloss glossy glossiness',
        description='Naming Components for glossy maps')
    displacement: StringProperty(
        name='Displacement',
        default='displacement displace disp dsp height heightmap',
        description='Naming Components for displacement maps')
    transmission: StringProperty(
        name='Transmission',
        default='transmission transparency',
        description='Naming Components for transmission maps')
    emission: StringProperty(
        name='Emission',
        default='emission emissive emit',
        description='Naming Components for emission maps')
    alpha: StringProperty(
        name='Alpha',
        default='alpha opacity',
        description='Naming Components for alpha maps')
    ambient_occlusion: StringProperty(
        name='Ambient Occlusion',
        default='ao ambient occlusion',
        description='Naming Components for AO maps')


# Addon prefs
class NWNodeWrangler(bpy.types.AddonPreferences):
    bl_idname = __package__

    merge_hide: EnumProperty(
        name="Hide Mix nodes",
        items=(
            ("ALWAYS", "Always", "Always collapse the new merge nodes"),
            ("NON_SHADER", "Non-Shader", "Collapse in all cases except for shaders"),
            ("NEVER", "Never", "Never collapse the new merge nodes")
        ),
        default='NON_SHADER',
        description="When merging nodes with the Ctrl+Numpad0 hotkey (and similar) specify whether to collapse them or show the full node with options expanded")

    merge_binary_mode: EnumProperty(
        name="Binary Functions",
        items=(
            ("AUTO", "Automatic", "Automatically determine what is the appropriate merge mode"),
            ("GROUP", "By Group", "Plug the selected nodes in groups of two"),
            ("CHAIN", "Chain Together", "Chain the output of each node one after another"),
        ),
        default='AUTO',
        description="When merging nodes, specify how binary functions are handled")

    merge_ternary_mode: EnumProperty(
        name="Ternary Functions",
        items=(
            ("AUTO", "Automatic", "Automatically determine what is the appropriate merge mode"),
            ("GROUP", "By Group", "Plug the selected nodes in groups of two"),
            ("CHAIN", "Chain Together", "Chain the output of each node one after another"),
            ("AS_BINARY", "Treat as Binary", "Handle ternary functions the same way as binary functions"),
        ),
        default='AUTO',
        description="When merging nodes, specify how ternary functions are handled")
    
    merge_position: EnumProperty(
        name="Mix Node Position",
        items=(
            ("TOP", "Top", "Place the Mix nodes such that the tops align with the original nodes"),
            ("MIDDLE", "Middle", "Place the Mix nodes such that the middle parts align with the original nodes"),
            ("BOTTOM", "Bottom", "Place the Mix nodes such that the bottom align with the original nodes")
        ),
        default='MIDDLE',
        description="When merging nodes with the Ctrl+Numpad0 hotkey (and similar) specify the position of the new nodes")
    
    batch_change_behavior: EnumProperty(
        name="Previous / Next Behavior",
        items=(
            ("CLAMP", "Clamp", "Don't allow moving past the beginning / end of a list"),
            ("WRAP", "Wrap", "When going past the end of a list, wrap back to the beginning, and vice versa"),
        ),
        default='WRAP',
        description="When changing to previous/next option during Batch Change, specify how the operator handles going past the boundaries of the option list")

    prefer_first_socket_binary: BoolProperty(
        name="Prefer First Socket",
        default=True,
        description="When chaining binary nodes together, specify whether the output of the previous node goes in the first or last socket of the next node"
    )

    prefer_first_socket_ternary: BoolProperty(
        name="Prefer First Socket",
        default=True,
        description="When chaining ternary nodes together, specify whether the output of the previous node goes in the first or last socket of the next node"
    )

    show_hotkey_list: BoolProperty(
        name="Show Hotkey List",
        default=False,
        description="Expand this box into a list of all the hotkeys for functions in this addon"
    )
    hotkey_list_filter: StringProperty(
        name="Filter by Name",
        default="",
        description="Show only hotkeys that have this text in their name",
        options={'TEXTEDIT_UPDATE'}
    )
    show_principled_lists: BoolProperty(
        name="Show Principled naming tags",
        default=False,
        description="Expand this box into a list of all naming tags for principled texture setup"
    )
    align_nodes_margin: IntVectorProperty(
        name="Margin",
        default=(50, 15),
        subtype="XYZ",
        size=2,
        min=0,
        soft_min=0,
        soft_max=200,
        description='The amount of space between nodes during when the Align Nodes operator is called'
    )
    principled_tags: bpy.props.PointerProperty(type=NWPrincipledPreferences)

    def draw(self, context):
        layout = self.layout
        col = layout.column(heading="Margin (Align Nodes):")
        col.prop(self, "align_nodes_margin", text="")
        col.separator()

        col.label(text="Merge Node Options:")
        col.prop(self, "merge_position")
        col.prop(self, "merge_hide")
        col.separator()

        col.label(text="Batch Change Options:")
        col.prop(self, "batch_change_behavior")

        box = layout.box()
        col = box.column(align=True)
        col.prop(
            self,
            "show_principled_lists",
            text='Edit tags for auto texture detection in Principled BSDF setup',
            toggle=True)
        if self.show_principled_lists:
            tags = self.principled_tags

            col.prop(tags, "base_color")
            col.prop(tags, "metallic")
            col.prop(tags, "specular")
            col.prop(tags, "rough")
            col.prop(tags, "gloss")
            col.prop(tags, "normal")
            col.prop(tags, "bump")
            col.prop(tags, "displacement")
            col.prop(tags, "transmission")
            col.prop(tags, "emission")
            col.prop(tags, "alpha")
            col.prop(tags, "ambient_occlusion")

        box = layout.box()
        col = box.column(align=True)

        hotkey_button_name = "Show Hotkey List"
        if self.show_hotkey_list:
            hotkey_button_name = "Hide Hotkey List"

        col.prop(self, "show_hotkey_list", text=hotkey_button_name, toggle=True)
        if self.show_hotkey_list:
            col.separator()
            col.prop(self, "hotkey_list_filter", icon="VIEWZOOM")
            col = indented_layout(col, level=1)
            col.separator()

            def get_keystroke(hotkey):
                keystr = nice_hotkey_name(hotkey.key_type)
                if hotkey.shift:
                    keystr = "Shift " + keystr
                if hotkey.alt:
                    keystr = "Alt " + keystr
                if hotkey.ctrl:
                    keystr = "Ctrl " + keystr   

                return f"{keystr}"         

            def keymap_display(hotkey):
                return hotkey.display_name

            original_order = {key.display_name:i for i, key in enumerate(kmi_defs)}
            # Since the grouped hotkeys are iterated through twice(resorting, and display), 
            # the iterators provided by groupby should be turned into tuples
            grouped_hotkeys = ((i, tuple(j)) for i, j in groupby(sorted(kmi_defs, key=keymap_display), key=keymap_display))

            for hotkey_label, entries in sorted(grouped_hotkeys, key=lambda n :original_order[n[0]]):
                if (self.hotkey_list_filter.lower() in hotkey_label.lower()):
                    # Display Name takes up 71.5% of the display width,
                    # while the keystroke takes the remaining 28.5%
                    split = col.split(factor=0.715)
                    split.label(text=hotkey_label)
                
                    subcol = split.column(align=True)
                    for entry in entries:
                        subcol.label(text=get_keystroke(entry))
                        
            return
#
#  REGISTER/UNREGISTER CLASSES AND KEYMAP ITEMS
#
switch_category_menus = []
addon_keymaps = []

classes = (
    NWPrincipledPreferences, NWNodeWrangler
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # keymaps
    addon_keymaps.clear()
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Node Editor', space_type="NODE_EDITOR")
        for entry in kmi_defs:
            kmi = km.keymap_items.new(
                entry.bl_idname, 
                type=entry.key_type, 
                value=entry.input_mode, 
                any=entry.any_modifier,
                shift=entry.shift, 
                ctrl=entry.ctrl, 
                alt=entry.alt, 
                oskey=entry.oskey,
                key_modifier=entry.custom_modifier,
                repeat=entry.repeat,
                direction=entry.direction,
                head=entry.head
                )

            props = entry.props
            if props is not None:
                for prop, value in props.items():
                    setattr(kmi.properties, prop, value)
            
            addon_keymaps.append((km, kmi))


def unregister():
    for cat_types in switch_category_menus:
        bpy.utils.unregister_class(cat_types)
    switch_category_menus.clear()

    # keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
