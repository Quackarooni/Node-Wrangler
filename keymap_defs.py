from . import operators
from . import interface
from dataclasses import dataclass

@dataclass(frozen=True)
class NWKeymapEntry:
    bl_idname: str
    display_name: str
    key_type: str = 'NONE'
    input_mode: str = 'PRESS'

    ctrl: bool = False
    shift: bool = False
    alt: bool = False
    shift: bool = False
    any_modifier: bool = False
    custom_modifier: str = 'NONE'
    
    direction: str = 'ANY'
    repeat: bool = False
    head: bool = False
    props: dict = None


kmi_defs = (
    # MERGE NODES
    # NWMergeNodes with Ctrl (AUTO).
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Automatic)", ctrl=True, key_type='NUMPAD_0', props={'mode':'MIX', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Automatic)", ctrl=True, key_type='ZERO', props={'mode':'MIX', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Add)", ctrl=True, key_type='NUMPAD_PLUS', props={'mode':'ADD', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Add)", ctrl=True, key_type='EQUAL', props={'mode':'ADD', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Subtract)", ctrl=True, key_type='NUMPAD_MINUS', props={'mode':'SUBTRACT', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Subtract)", ctrl=True, key_type='MINUS', props={'mode':'SUBTRACT', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Multiply)", ctrl=True, key_type='NUMPAD_ASTERIX', props={'mode':'MULTIPLY', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Multiply)", ctrl=True, key_type='EIGHT', props={'mode':'MULTIPLY', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Divide)", ctrl=True, key_type='NUMPAD_SLASH', props={'mode':'DIVIDE', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Divide)", ctrl=True, key_type='SLASH', props={'mode':'DIVIDE', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Less Than)", ctrl=True, key_type='COMMA', props={'mode':'LESS_THAN', 'merge_type':'AUTO'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Greater Than)", ctrl=True, key_type='PERIOD', props={'mode':'GREATER_THAN', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Z-Combine)", ctrl=True, key_type='NUMPAD_PERIOD', props={'mode':'MIX', 'merge_type':'ZCOMBINE'}),
    # NWMergeNodes with Ctrl Alt (MIX or ALPHAOVER)
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Alpha Over)", ctrl=True, alt=True, key_type='NUMPAD_0', props={'mode':'MIX', 'merge_type':'ALPHAOVER'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Alpha Over)", ctrl=True, alt=True, key_type='ZERO', props={'mode':'MIX', 'merge_type':'ALPHAOVER'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Add)", ctrl=True, alt=True, key_type='NUMPAD_PLUS', props={'mode':'ADD', 'merge_type':'MIX'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Add)", ctrl=True, alt=True, key_type='EQUAL', props={'mode':'ADD', 'merge_type':'MIX'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Subtract)", ctrl=True, alt=True, key_type='NUMPAD_MINUS', props={'mode':'SUBTRACT', 'merge_type':'MIX'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Subtract)", ctrl=True, alt=True, key_type='MINUS', props={'mode':'SUBTRACT', 'merge_type':'MIX'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Multiply)", ctrl=True, alt=True, key_type='NUMPAD_ASTERIX', props={'mode':'MULTIPLY', 'merge_type':'MIX'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Multiply)", ctrl=True, alt=True, key_type='EIGHT', props={'mode':'MULTIPLY', 'merge_type':'MIX'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Divide)", ctrl=True, alt=True, key_type='NUMPAD_SLASH', props={'mode':'DIVIDE', 'merge_type':'MIX'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Color, Divide)", ctrl=True, alt=True, key_type='SLASH', props={'mode':'DIVIDE', 'merge_type':'MIX'}),
    # NWMergeNodes with Ctrl Shift (MATH)
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Add)", ctrl=True, shift=True, key_type='NUMPAD_PLUS', props={'mode':'ADD', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Add)", ctrl=True, shift=True, key_type='EQUAL', props={'mode':'ADD', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Subtract)", ctrl=True, shift=True, key_type='NUMPAD_MINUS', props={'mode':'SUBTRACT', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Subtract)", ctrl=True, shift=True, key_type='MINUS', props={'mode':'SUBTRACT', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Multiply)", ctrl=True, shift=True, key_type='NUMPAD_ASTERIX', props={'mode':'MULTIPLY', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Multiply)", ctrl=True, shift=True, key_type='EIGHT', props={'mode':'MULTIPLY', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Divide)", ctrl=True, shift=True, key_type='NUMPAD_SLASH', props={'mode':'DIVIDE', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Divide)", ctrl=True, shift=True, key_type='SLASH', props={'mode':'DIVIDE', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Less Than)", ctrl=True, shift=True, key_type='COMMA', props={'mode':'LESS_THAN', 'merge_type':'MATH'}),
    NWKeymapEntry(operators.NWMergeNodes.bl_idname, "Merge Nodes (Math, Greater Than)", ctrl=True, shift=True, key_type='PERIOD', props={'mode':'GREATER_THAN', 'merge_type':'MATH'}),
    # BATCH CHANGE NODES
    # NWBatchChangeNodes with Alt
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Mix)", key_type='NUMPAD_0', alt=True, props={'blend_type':'MIX'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Mix)", key_type='ZERO', alt=True, props={'blend_type':'MIX'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Add)", key_type='NUMPAD_PLUS', alt=True, props={'blend_type':'ADD', 'math_operation':'ADD', 'vector_operation':'ADD', 'bool_operation':'OR'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Add)", key_type='EQUAL', alt=True, props={'blend_type':'ADD', 'math_operation':'ADD', 'vector_operation':'ADD', 'bool_operation':'OR'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Multiply)", key_type='NUMPAD_ASTERIX', alt=True, props={'blend_type':'MULTIPLY', 'math_operation':'MULTIPLY', 'vector_operation':'MULTIPLY', 'bool_operation':'AND'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Multiply)", key_type='EIGHT', alt=True, props={'blend_type':'MULTIPLY', 'math_operation':'MULTIPLY', 'vector_operation':'MULTIPLY', 'bool_operation':'AND'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Subtract)", key_type='NUMPAD_MINUS', alt=True, props={'blend_type':'SUBTRACT', 'math_operation':'SUBTRACT', 'vector_operation':'SUBTRACT', 'bool_operation':'NIMPLY'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Subtract)", key_type='MINUS', alt=True, props={'blend_type':'SUBTRACT', 'math_operation':'SUBTRACT', 'vector_operation':'SUBTRACT', 'bool_operation':'NIMPLY'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Divide)", key_type='NUMPAD_SLASH', alt=True, props={'blend_type':'DIVIDE', 'math_operation':'DIVIDE', 'vector_operation':'DIVIDE', 'bool_operation':'NOT'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Divide)", key_type='SLASH', alt=True, props={'blend_type':'DIVIDE', 'math_operation':'DIVIDE', 'vector_operation':'DIVIDE', 'bool_operation':'NOT'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Less Than)", key_type='COMMA', alt=True, props={'math_operation':'LESS_THAN'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Greater Than)", key_type='PERIOD', alt=True, props={'math_operation':'GREATER_THAN'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Previous)", key_type='UP_ARROW', repeat=True, alt=True, props={'blend_type':'PREV', 'math_operation':'PREV', 'vector_operation':'PREV', 'bool_operation':'PREV'}),
    NWKeymapEntry(operators.NWBatchChangeNodes.bl_idname, "Batch Change (Next)", key_type='DOWN_ARROW', repeat=True, alt=True, props={'blend_type':'NEXT', 'math_operation':'NEXT', 'vector_operation':'NEXT', 'bool_operation':'NEXT',}),
    # LINK ACTIVE TO SELECTED
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link active to selected (Don't replace links)", key_type='K', shift=False, props={'replace':False, 'use_node_name':False, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link active to selected (Replace links)", key_type='K', shift=True, props={'replace':True, 'use_node_name':False, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link active to selected (Don't replace links, node names)", key_type='QUOTE', shift=False, props={'replace':False, 'use_node_name':True, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link active to selected (Replace links, node names)", key_type='QUOTE', shift=True, props={'replace':True, 'use_node_name':True, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link active to selected (Don't replace links, output names)", key_type='SEMI_COLON', shift=False, props={'replace':False, 'use_node_name':False, 'use_outputs_names':True}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link active to selected (Replace links, output names)", key_type='SEMI_COLON', shift=True, props={'replace':True, 'use_node_name':False, 'use_outputs_names':True}),
    # CHANGE MIX FACTOR
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Reduce Mix Factor by 0.1", key_type='LEFT_ARROW', ctrl=False, shift=False, alt=True, props={'option':-0.1}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Increase Mix Factor by 0.1", key_type='RIGHT_ARROW', ctrl=False, shift=False, alt=True, props={'option':0.1}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Reduce Mix Factor by 0.01", key_type='LEFT_ARROW', ctrl=False, shift=True, alt=True, props={'option':-0.01}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Increase Mix Factor by 0.01", key_type='RIGHT_ARROW', ctrl=False, shift=True, alt=True, props={'option':0.01}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Set Mix Factor to 0.0", key_type='LEFT_ARROW', ctrl=True, shift=True, alt=True, props={'option':0.0}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Set Mix Factor to 1.0", key_type='RIGHT_ARROW', ctrl=True, shift=True, alt=True, props={'option':1.0}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Set Mix Factor to 0.0", key_type='NUMPAD_0', ctrl=True, shift=True, alt=True, props={'option':0.0}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Set Mix Factor to 0.0", key_type='ZERO', ctrl=True, shift=True, alt=True, props={'option':0.0}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Set Mix Factor to 1.0", key_type='NUMPAD_1', ctrl=True, shift=True, alt=True, props={'option':1.0}),
    NWKeymapEntry(operators.NWChangeMixFactor.bl_idname, "Set Mix Factor to 1.0", key_type='ONE', ctrl=True, shift=True, alt=True, props={'option':1.0}),
    # MISC. OPERATORS
    NWKeymapEntry(operators.NWClearLabel.bl_idname, "Clear node labels", key_type='L', alt=True, props={'option':False}),
    NWKeymapEntry(operators.NWModifyLabels.bl_idname, "Modify node labels", key_type='L', shift=True, alt=True),
    NWKeymapEntry(operators.NWCopyLabel.bl_idname, "Copy label from active to selected", key_type='V', shift=True, props={'option':'FROM_ACTIVE'}),
    NWKeymapEntry(operators.NWDetachOutputs.bl_idname, "Detach outputs", key_type='D', shift=True, alt=True),
    NWKeymapEntry(operators.NWLinkToOutputNode.bl_idname, "Link to output node", key_type='O'),
    NWKeymapEntry(operators.NWSelectParentChildren.bl_idname, "Select children", key_type='RIGHT_BRACKET', props={'option':'CHILD'}),
    NWKeymapEntry(operators.NWSelectParentChildren.bl_idname, "Select Parent", key_type='LEFT_BRACKET', props={'option':'PARENT'}),
    NWKeymapEntry(operators.NWAddTextureSetup.bl_idname, "Add texture setup", key_type='T', ctrl=True),
    NWKeymapEntry(operators.NWAddPrincipledSetup.bl_idname, "Add Principled texture setup", key_type='T', ctrl=True, shift=True),
    NWKeymapEntry(operators.NWResetBG.bl_idname, "Reset backdrop image zoom", key_type='Z'),
    NWKeymapEntry(operators.NWDeleteUnused.bl_idname, "Delete unused nodes", key_type='X', alt=True),
    NWKeymapEntry(operators.NWFrameSelected.bl_idname, "Frame selected nodes", key_type='P', shift=True),
    NWKeymapEntry(operators.NWSwapLinks.bl_idname, "Swap Links", key_type='S', alt=True),
    NWKeymapEntry(operators.NWPreviewNode.bl_idname, "Preview node output", key_type='LEFTMOUSE', ctrl=True, shift=True, props={'run_in_geometry_nodes':False}),
    NWKeymapEntry(operators.NWPreviewNode.bl_idname, "Preview node output", key_type='LEFTMOUSE', shift=True, alt=True, props={'run_in_geometry_nodes':True}),
    NWKeymapEntry(operators.NWReloadImages.bl_idname, "Reload images", key_type='R', alt=True),
    NWKeymapEntry(operators.NWLazyMix.bl_idname, "Lazy Mix", key_type='RIGHTMOUSE', ctrl=True, shift=True),
    NWKeymapEntry(operators.NWLazyConnect.bl_idname, "Lazy Connect", key_type='RIGHTMOUSE', alt=True, props={'with_menu':False}),
    NWKeymapEntry(operators.NWLazyConnect.bl_idname, "Lazy Connect with Socket Menu", key_type='RIGHTMOUSE', shift=True, alt=True, props={'with_menu':True}),
    NWKeymapEntry(operators.NWViewerFocus.bl_idname, "Set Viewers Tile Center", key_type='LEFTMOUSE', input_mode='DOUBLE_CLICK'),
    NWKeymapEntry(operators.NWAlignNodes.bl_idname, "Align selected nodes neatly in a row/column", key_type='EQUAL', shift=True),
    NWKeymapEntry(operators.NWResetNodes.bl_idname, "Revert node back to default state, but keep connections", key_type='BACK_SPACE'),
    # MENUS
    NWKeymapEntry('wm.call_menu', "Node Wrangler Context Menu", 'W', shift=True, props={'name':interface.NodeWranglerMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Add Reroutes Menu", 'SLASH', props={'name':interface.NWAddReroutesMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Add Reroutes Menu", 'NUMPAD_SLASH', props={'name':interface.NWAddReroutesMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Link Active to Selected (Menu)", 'BACK_SLASH', props={'name':interface.NWLinkActiveToSelectedMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Copy to Selected (Menu)", 'C',  shift=True, props={'name':interface.NWCopyToSelectedMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Switch Node Type (Menu)", 'S',  shift=True, props={'name':interface.NWSwitchNodeTypeMenu.bl_idname}),
)

# kmi_defs entry: (identifier, key, action, CTRL, SHIFT, ALT, props, nice name)
# props entry: (property name, property value)
kmi_defs_old = (
    # MERGE NODES
    # NWMergeNodes with Ctrl (AUTO).
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_0', 'PRESS', True, False, False, (('mode', 'MIX'), ('merge_type', 'AUTO'),), "Merge Nodes (Automatic)"),
    (operators.NWMergeNodes.bl_idname, 'ZERO', 'PRESS', True, False, False, (('mode', 'MIX'), ('merge_type', 'AUTO'),), "Merge Nodes (Automatic)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_PLUS', 'PRESS', True, False, False, (('mode', 'ADD'), ('merge_type', 'AUTO'),), "Merge Nodes (Add)"),
    (operators.NWMergeNodes.bl_idname, 'EQUAL', 'PRESS', True, False, False, (('mode', 'ADD'), ('merge_type', 'AUTO'),), "Merge Nodes (Add)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_ASTERIX', 'PRESS', True, False, False, (('mode', 'MULTIPLY'), ('merge_type', 'AUTO'),), "Merge Nodes (Multiply)"),
    (operators.NWMergeNodes.bl_idname, 'EIGHT', 'PRESS', True, False, False, (('mode', 'MULTIPLY'), ('merge_type', 'AUTO'),), "Merge Nodes (Multiply)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_MINUS', 'PRESS', True, False, False, (('mode', 'SUBTRACT'), ('merge_type', 'AUTO'),), "Merge Nodes (Subtract)"),
    (operators.NWMergeNodes.bl_idname, 'MINUS', 'PRESS', True, False, False, (('mode', 'SUBTRACT'), ('merge_type', 'AUTO'),), "Merge Nodes (Subtract)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_SLASH', 'PRESS', True, False, False, (('mode', 'DIVIDE'), ('merge_type', 'AUTO'),), "Merge Nodes (Divide)"),
    (operators.NWMergeNodes.bl_idname, 'SLASH', 'PRESS', True, False, False, (('mode', 'DIVIDE'), ('merge_type', 'AUTO'),), "Merge Nodes (Divide)"),
    (operators.NWMergeNodes.bl_idname, 'COMMA', 'PRESS', True, False, False, (('mode', 'LESS_THAN'), ('merge_type', 'MATH'),), "Merge Nodes (Less than)"),
    (operators.NWMergeNodes.bl_idname, 'PERIOD', 'PRESS', True, False, False, (('mode', 'GREATER_THAN'), ('merge_type', 'MATH'),), "Merge Nodes (Greater than)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_PERIOD', 'PRESS', True, False, False, (('mode', 'MIX'), ('merge_type', 'ZCOMBINE'),), "Merge Nodes (Z-Combine)"),
    # NWMergeNodes with Ctrl Alt (MIX or ALPHAOVER)
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_0', 'PRESS', True, False, True,(('mode', 'MIX'), ('merge_type', 'ALPHAOVER'),), "Merge Nodes (Alpha Over)"),
    (operators.NWMergeNodes.bl_idname, 'ZERO', 'PRESS', True, False, True,(('mode', 'MIX'), ('merge_type', 'ALPHAOVER'),), "Merge Nodes (Alpha Over)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_PLUS', 'PRESS', True, False, True,(('mode', 'ADD'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Add)"),
    (operators.NWMergeNodes.bl_idname, 'EQUAL', 'PRESS', True, False, True,(('mode', 'ADD'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Add)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_ASTERIX', 'PRESS', True, False, True,(('mode', 'MULTIPLY'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Multiply)"),
    (operators.NWMergeNodes.bl_idname, 'EIGHT', 'PRESS', True, False, True,(('mode', 'MULTIPLY'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Multiply)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_MINUS', 'PRESS', True, False, True,(('mode', 'SUBTRACT'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Subtract)"),
    (operators.NWMergeNodes.bl_idname, 'MINUS', 'PRESS', True, False, True, (('mode', 'SUBTRACT'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Subtract)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_SLASH', 'PRESS', True, False, True, (('mode', 'DIVIDE'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Divide)"),
    (operators.NWMergeNodes.bl_idname, 'SLASH', 'PRESS', True, False, True, (('mode', 'DIVIDE'), ('merge_type', 'MIX'),), "Merge Nodes (Color, Divide)"),
    # NWMergeNodes with Ctrl Shift (MATH)
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_PLUS', 'PRESS', True, True, False, (('mode', 'ADD'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Add)"),
    (operators.NWMergeNodes.bl_idname, 'EQUAL', 'PRESS', True, True, False, (('mode', 'ADD'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Add)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_ASTERIX', 'PRESS', True, True, False, (('mode', 'MULTIPLY'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Multiply)"),
    (operators.NWMergeNodes.bl_idname, 'EIGHT', 'PRESS', True, True, False, (('mode', 'MULTIPLY'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Multiply)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_MINUS', 'PRESS', True, True, False, (('mode', 'SUBTRACT'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Subtract)"),
    (operators.NWMergeNodes.bl_idname, 'MINUS', 'PRESS', True, True, False, (('mode', 'SUBTRACT'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Subtract)"),
    (operators.NWMergeNodes.bl_idname, 'NUMPAD_SLASH', 'PRESS', True, True, False, (('mode', 'DIVIDE'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Divide)"),
    (operators.NWMergeNodes.bl_idname, 'SLASH', 'PRESS', True, True, False, (('mode', 'DIVIDE'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Divide)"),
    (operators.NWMergeNodes.bl_idname, 'COMMA', 'PRESS', True, True, False, (('mode', 'LESS_THAN'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Less than)"),
    (operators.NWMergeNodes.bl_idname, 'PERIOD', 'PRESS', True, True, False, (('mode', 'GREATER_THAN'), ('merge_type', 'MATH'),), "Merge Nodes (Math, Greater than)"),
    # BATCH CHANGE NODES
    # NWBatchChangeNodes with Alt
    (operators.NWBatchChangeNodes.bl_idname, 'NUMPAD_0', 'PRESS', False, False, True, (('blend_type', 'MIX'),), "Batch Change (Mix)"),
    (operators.NWBatchChangeNodes.bl_idname, 'ZERO', 'PRESS', False, False, True, (('blend_type', 'MIX'),), "Batch Change (Mix)"),
    (operators.NWBatchChangeNodes.bl_idname, 'NUMPAD_PLUS', 'PRESS', False, False, True, (('blend_type', 'ADD'), ('math_operation', 'ADD'), ('vector_operation', 'ADD'), ('bool_operation', 'OR'),), "Batch Change (Add)"),
    (operators.NWBatchChangeNodes.bl_idname, 'EQUAL', 'PRESS', False, False, True, (('blend_type', 'ADD'), ('math_operation', 'ADD'), ('vector_operation', 'ADD'), ('bool_operation', 'OR'),), "Batch Change (Add)"),
    (operators.NWBatchChangeNodes.bl_idname, 'NUMPAD_ASTERIX', 'PRESS', False, False, True, (('blend_type', 'MULTIPLY'), ('math_operation', 'MULTIPLY'), ('vector_operation', 'MULTIPLY'), ('bool_operation', 'AND'),), "Batch Change (Multiply)"),
    (operators.NWBatchChangeNodes.bl_idname, 'EIGHT', 'PRESS', False, False, True, (('blend_type', 'MULTIPLY'), ('math_operation', 'MULTIPLY'), ('vector_operation', 'MULTIPLY'), ('bool_operation', 'AND'),), "Batch Change (Multiply)"),
    (operators.NWBatchChangeNodes.bl_idname, 'NUMPAD_MINUS', 'PRESS', False, False, True, (('blend_type', 'SUBTRACT'), ('math_operation', 'SUBTRACT'), ('vector_operation', 'SUBTRACT'), ('bool_operation', 'NIMPLY'),), "Batch Change (Subtract)"),
    (operators.NWBatchChangeNodes.bl_idname, 'MINUS', 'PRESS', False, False, True, (('blend_type', 'SUBTRACT'), ('math_operation', 'SUBTRACT'), ('vector_operation', 'SUBTRACT'), ('bool_operation', 'NIMPLY'),), "Batch Change (Subtract)"),
    (operators.NWBatchChangeNodes.bl_idname, 'NUMPAD_SLASH', 'PRESS', False, False, True, (('blend_type', 'DIVIDE'), ('math_operation', 'DIVIDE'), ('vector_operation', 'DIVIDE'),  ('bool_operation', 'NOT'),), "Batch Change (Divide)"),
    (operators.NWBatchChangeNodes.bl_idname, 'SLASH', 'PRESS', False, False, True, (('blend_type', 'DIVIDE'), ('math_operation', 'DIVIDE'), ('vector_operation', 'DIVIDE'),  ('bool_operation', 'NOT'),), "Batch Change (Divide)"),
    (operators.NWBatchChangeNodes.bl_idname, 'COMMA', 'PRESS', False, False, True, (('math_operation', 'LESS_THAN'),), "Batch Change (Less Than)"),
    (operators.NWBatchChangeNodes.bl_idname, 'PERIOD', 'PRESS', False, False, True, (('math_operation', 'GREATER_THAN'),), "Batch Change (Greater Than)"),
    (operators.NWBatchChangeNodes.bl_idname, 'UP_ARROW', 'PRESS', False, False, True, (('blend_type', 'PREV'), ('math_operation', 'PREV'), ('vector_operation', 'PREV'), ('bool_operation', 'PREV'),), "Batch Change (Previous)"),
    (operators.NWBatchChangeNodes.bl_idname, 'DOWN_ARROW', 'PRESS', False, False, True, (('blend_type', 'NEXT'), ('math_operation', 'NEXT'), ('vector_operation', 'NEXT'), ('bool_operation', 'NEXT'),), "Batch Change (Next)"),
    # LINK ACTIVE TO SELECTED
    (operators.NWLinkActiveToSelected.bl_idname, 'K', 'PRESS', False, False, False, (('replace', False), ('use_node_name', False), ('use_outputs_names', False),), "Link active to selected (Don't replace links)"), # Don't use names, don't replace links (K)
    (operators.NWLinkActiveToSelected.bl_idname, 'K', 'PRESS', False, True, False, (('replace', True), ('use_node_name', False), ('use_outputs_names', False),), "Link active to selected (Replace links)"), # Don't use names, replace links (Shift K)
    (operators.NWLinkActiveToSelected.bl_idname, 'QUOTE', 'PRESS', False, False, False, (('replace', False), ('use_node_name', True), ('use_outputs_names', False),), "Link active to selected (Don't replace links, node names)"), # Use node name, don't replace links (')
    (operators.NWLinkActiveToSelected.bl_idname, 'QUOTE', 'PRESS', False, True, False, (('replace', True), ('use_node_name', True), ('use_outputs_names', False),), "Link active to selected (Replace links, node names)"), # Use node name, replace links (Shift ')
    (operators.NWLinkActiveToSelected.bl_idname, 'SEMI_COLON', 'PRESS', False, False, False, (('replace', False), ('use_node_name', False), ('use_outputs_names', True),), "Link active to selected (Don't replace links, output names)"), # Don't use names, don't replace links (;)
    (operators.NWLinkActiveToSelected.bl_idname, 'SEMI_COLON', 'PRESS', False, True, False, (('replace', True), ('use_node_name', False), ('use_outputs_names', True),), "Link active to selected (Replace links, output names)"), # Don't use names, replace links (')
    # CHANGE MIX FACTOR
    (operators.NWChangeMixFactor.bl_idname, 'LEFT_ARROW', 'PRESS', False, False, True, (('option', -0.1),), "Reduce Mix Factor by 0.1"),
    (operators.NWChangeMixFactor.bl_idname, 'RIGHT_ARROW', 'PRESS', False, False, True, (('option', 0.1),), "Increase Mix Factor by 0.1"),
    (operators.NWChangeMixFactor.bl_idname, 'LEFT_ARROW', 'PRESS', False, True, True, (('option', -0.01),), "Reduce Mix Factor by 0.01"),
    (operators.NWChangeMixFactor.bl_idname, 'RIGHT_ARROW', 'PRESS', False, True, True, (('option', 0.01),), "Increase Mix Factor by 0.01"),
    (operators.NWChangeMixFactor.bl_idname, 'LEFT_ARROW', 'PRESS', True, True, True, (('option', 0.0),), "Set Mix Factor to 0.0"),
    (operators.NWChangeMixFactor.bl_idname, 'RIGHT_ARROW', 'PRESS', True, True, True, (('option', 1.0),), "Set Mix Factor to 1.0"),
    (operators.NWChangeMixFactor.bl_idname, 'NUMPAD_0', 'PRESS', True, True, True, (('option', 0.0),), "Set Mix Factor to 0.0"),
    (operators.NWChangeMixFactor.bl_idname, 'ZERO', 'PRESS', True, True, True, (('option', 0.0),), "Set Mix Factor to 0.0"),
    (operators.NWChangeMixFactor.bl_idname, 'NUMPAD_1', 'PRESS', True, True, True, (('option', 1.0),), "Mix Factor to 1.0"),
    (operators.NWChangeMixFactor.bl_idname, 'ONE', 'PRESS', True, True, True, (('option', 1.0),), "Set Mix Factor to 1.0"),
    # CLEAR LABEL (Alt L)
    (operators.NWClearLabel.bl_idname, 'L', 'PRESS', False, False, True, (('option', False),), "Clear node labels"),
    # MODIFY LABEL (Alt Shift L)
    (operators.NWModifyLabels.bl_idname, 'L', 'PRESS', False, True, True, None, "Modify node labels"),
    # Copy Label from active to selected
    (operators.NWCopyLabel.bl_idname, 'V', 'PRESS', False, True, False, (('option', 'FROM_ACTIVE'),), "Copy label from active to selected"),
    # DETACH OUTPUTS (Alt Shift D)
    (operators.NWDetachOutputs.bl_idname, 'D', 'PRESS', False, True, True, None, "Detach outputs"),
    # LINK TO OUTPUT NODE (O)
    (operators.NWLinkToOutputNode.bl_idname, 'O', 'PRESS', False, False, False, None, "Link to output node"),
    # SELECT PARENT/CHILDREN
    # Select Children
    (operators.NWSelectParentChildren.bl_idname, 'RIGHT_BRACKET', 'PRESS', False, False, False, (('option', 'CHILD'),), "Select children"),
    # Select Parent
    (operators.NWSelectParentChildren.bl_idname, 'LEFT_BRACKET', 'PRESS', False, False, False, (('option', 'PARENT'),), "Select Parent"),
    # Add Texture Setup
    (operators.NWAddTextureSetup.bl_idname, 'T', 'PRESS', True, False, False, None, "Add texture setup"),
    # Add Principled BSDF Texture Setup
    (operators.NWAddPrincipledSetup.bl_idname, 'T', 'PRESS', True, True, False, None, "Add Principled texture setup"),
    # Reset backdrop
    (operators.NWResetBG.bl_idname, 'Z', 'PRESS', False, False, False, None, "Reset backdrop image zoom"),
    # Delete unused
    (operators.NWDeleteUnused.bl_idname, 'X', 'PRESS', False, False, True, None, "Delete unused nodes"),
    # Frame Selected
    (operators.NWFrameSelected.bl_idname, 'P', 'PRESS', False, True, False, None, "Frame selected nodes"),
    # Swap Links
    (operators.NWSwapLinks.bl_idname, 'S', 'PRESS', False, False, True, None, "Swap Links"),
    # Preview Node
    (operators.NWPreviewNode.bl_idname, 'LEFTMOUSE', 'PRESS', True, True, False, (('run_in_geometry_nodes', False),), "Preview node output"),
    (operators.NWPreviewNode.bl_idname, 'LEFTMOUSE', 'PRESS', False, True, True, (('run_in_geometry_nodes', True),), "Preview node output"),
    # Reload Images
    (operators.NWReloadImages.bl_idname, 'R', 'PRESS', False, False, True, None, "Reload images"),
    # Lazy Mix
    (operators.NWLazyMix.bl_idname, 'RIGHTMOUSE', 'PRESS', True, True, False, None, "Lazy Mix"),
    # Lazy Connect
    (operators.NWLazyConnect.bl_idname, 'RIGHTMOUSE', 'PRESS', False, False, True, (('with_menu', False),), "Lazy Connect"),
    # Lazy Connect with Menu
    (operators.NWLazyConnect.bl_idname, 'RIGHTMOUSE', 'PRESS', False, True, True, (('with_menu', True),), "Lazy Connect with Socket Menu"),
    # Viewer Tile Center
    (operators.NWViewerFocus.bl_idname, 'LEFTMOUSE', 'DOUBLE_CLICK', False, False, False, None, "Set Viewers Tile Center"),
    # Align Nodes
    (operators.NWAlignNodes.bl_idname, 'EQUAL', 'PRESS', False, True, False, None, "Align selected nodes neatly in a row/column"),
    # Reset Nodes (Back Space)
    (operators.NWResetNodes.bl_idname, 'BACK_SPACE', 'PRESS', False, False, False, None, "Revert node back to default state, but keep connections"),
    # MENUS
    ('wm.call_menu', 'W', 'PRESS', False, True, False, (('name', interface.NodeWranglerMenu.bl_idname),), "Node Wrangler menu"),
    ('wm.call_menu', 'SLASH', 'PRESS', False, False, False, (('name', interface.NWAddReroutesMenu.bl_idname),), "Add Reroutes menu"),
    ('wm.call_menu', 'NUMPAD_SLASH', 'PRESS', False, False, False, (('name', interface.NWAddReroutesMenu.bl_idname),), "Add Reroutes menu"),
    ('wm.call_menu', 'BACK_SLASH', 'PRESS', False, False, False, (('name', interface.NWLinkActiveToSelectedMenu.bl_idname),), "Link active to selected (menu)"),
    ('wm.call_menu', 'C', 'PRESS', False, True, False, (('name', interface.NWCopyToSelectedMenu.bl_idname),), "Copy to selected (menu)"),
    ('wm.call_menu', 'S', 'PRESS', False, True, False, (('name', interface.NWSwitchNodeTypeMenu.bl_idname),), "Switch node type menu"),
)