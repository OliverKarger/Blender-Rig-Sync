bl_info = {
    'name': 'Rig Sync Tools',
    'author': 'Oliver Karger',
    'version': (1, 1, 0),
    'blender': (4, 3, 0),
    'location': 'View3D > Tool Panel > Rig Sync Tools',
    'description': 'Simply utility that adds Constraints to copy Transforms from one Rig to another. Bone-by-Bone',
    'category': 'Animation',
    'support': 'COMMUNITY',
}

import bpy
from .rig import *
from .operators import (
    rig_sync_list_bones,
    rig_sync_enable_sync,
    rig_sync_disable_sync,
    rig_sync_select_all_bones,
    rig_sync_select_none_bones
)
from .ui import rig_sync_bones_list, rig_sync_panel
from .properties import rig_sync_bone_item, rig_sync_panel_properties

classes = [
    # Property Groups
    rig_sync_bone_item,
    rig_sync_panel_properties,

    # Operators
    rig_sync_list_bones,
    rig_sync_enable_sync,
    rig_sync_disable_sync,
    rig_sync_select_all_bones,
    rig_sync_select_none_bones,

    # UI Classes
    rig_sync_bones_list,
    rig_sync_panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.rig_sync_props = bpy.props.PointerProperty(type=rig_sync_panel_properties)

def unregister():
    del bpy.types.Scene.rig_sync_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
