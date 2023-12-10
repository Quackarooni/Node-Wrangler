from . import operators
from . import interface
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class NWKeymapEntry:
    bl_idname: str
    display_name: str
    key_type: str = 'NONE'
    input_mode: str = 'PRESS'

    ctrl: bool = False
    shift: bool = False
    alt: bool = False
    oskey: bool = False
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
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link Active to Selected", key_type='K', shift=False, props={'replace':False, 'use_node_name':False, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link Active to Selected (Replace Links)", key_type='K', shift=True, props={'replace':True, 'use_node_name':False, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link Active to Selected (Use Node Names)", key_type='QUOTE', shift=False, props={'replace':False, 'use_node_name':True, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link Active to Selected (Replace Links, Use Node Names)", key_type='QUOTE', shift=True, props={'replace':True, 'use_node_name':True, 'use_outputs_names':False}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link Active to Selected (Use Output Names)", key_type='SEMI_COLON', shift=False, props={'replace':False, 'use_node_name':False, 'use_outputs_names':True}),
    NWKeymapEntry(operators.NWLinkActiveToSelected.bl_idname, "Link Active to Selected (Replace Links, Use Output Names)", key_type='SEMI_COLON', shift=True, props={'replace':True, 'use_node_name':False, 'use_outputs_names':True}),
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
    NWKeymapEntry(operators.NWClearLabel.bl_idname, "Clear Node Labels", key_type='L', alt=True, props={'option':False}),
    NWKeymapEntry(operators.NWModifyLabels.bl_idname, "Modify Node Labels", key_type='L', shift=True, alt=True),
    NWKeymapEntry(operators.NWCopyLabel.bl_idname, "Copy Label from Active to Selected", key_type='V', shift=True, props={'option':'FROM_ACTIVE'}),
    NWKeymapEntry(operators.NWDetachOutputs.bl_idname, "Detach Outputs", key_type='D', shift=True, alt=True),
    NWKeymapEntry(operators.NWLinkToOutputNode.bl_idname, "Connect to Output", key_type='O'),
    NWKeymapEntry(operators.NWSelectParentChildren.bl_idname, "Select Children", key_type='RIGHT_BRACKET', props={'option':'CHILD'}),
    NWKeymapEntry(operators.NWSelectParentChildren.bl_idname, "Select Parent", key_type='LEFT_BRACKET', props={'option':'PARENT'}),
    NWKeymapEntry(operators.NWAddTextureSetup.bl_idname, "Add Texture Setup", key_type='T', ctrl=True),
    NWKeymapEntry(operators.NWAddPrincipledSetup.bl_idname, "Add Principled Texture Setup", key_type='T', ctrl=True, shift=True),
    NWKeymapEntry(operators.NWResetBG.bl_idname, "Reset Backdrop Image Zoom", key_type='Z'),
    NWKeymapEntry(operators.NWDeleteUnused.bl_idname, "Delete Unused Nodes", key_type='X', alt=True),
    NWKeymapEntry(operators.NWFrameSelected.bl_idname, "Frame Selected Nodes", key_type='P', shift=True),
    NWKeymapEntry(operators.NWSwapLinks.bl_idname, "Swap Links", key_type='S', alt=True),
    NWKeymapEntry(operators.NWPreviewNode.bl_idname, "Preview Output", key_type='LEFTMOUSE', ctrl=True, shift=True, props={'run_in_geometry_nodes':False}),
    NWKeymapEntry(operators.NWPreviewNode.bl_idname, "Preview Output (Geometry Nodes)", key_type='LEFTMOUSE', shift=True, alt=True, props={'run_in_geometry_nodes':True}),
    NWKeymapEntry(operators.NWReloadImages.bl_idname, "Reload Images", key_type='R', alt=True),
    NWKeymapEntry(operators.NWLazyMix.bl_idname, "Lazy Mix", key_type='RIGHTMOUSE', ctrl=True, shift=True),
    NWKeymapEntry(operators.NWLazyConnect.bl_idname, "Lazy Connect", key_type='RIGHTMOUSE', alt=True, props={'with_menu':False}),
    NWKeymapEntry(operators.NWLazyConnect.bl_idname, "Lazy Connect (with Socket Menu)", key_type='RIGHTMOUSE', shift=True, alt=True, props={'with_menu':True}),
    NWKeymapEntry(operators.NWViewerFocus.bl_idname, "Set Viewer's Tile Center", key_type='LEFTMOUSE', input_mode='DOUBLE_CLICK'),
    NWKeymapEntry(operators.NWAlignNodes.bl_idname, "Auto-Align Nodes", key_type='EQUAL', shift=True),
    NWKeymapEntry(operators.NWResetNodes.bl_idname, "Reset Nodes", key_type='BACK_SPACE'),
    # MENUS
    NWKeymapEntry('wm.call_menu', "Spawn Context Menu", 'W', shift=True, props={'name':interface.NodeWranglerMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Spawn Menu (Add Reroutes)", 'SLASH', props={'name':interface.NWAddReroutesMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Spawn Menu (Add Reroutes)", 'NUMPAD_SLASH', props={'name':interface.NWAddReroutesMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Spawn Menu (Link Active to Selected)", 'BACK_SLASH', props={'name':interface.NWLinkActiveToSelectedMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Spawn Menu (Copy to Selected)", 'C',  shift=True, props={'name':interface.NWCopyToSelectedMenu.bl_idname}),
    NWKeymapEntry('wm.call_menu', "Spawn Menu (Switch Node Type)", 'S',  shift=True, props={'name':interface.NWSwitchNodeTypeMenu.bl_idname}),
)