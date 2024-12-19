import bpy

class rig_sync_bone_item(bpy.types.PropertyGroup):
    """ Property for the Bone List Elements """
    name: bpy.props.StringProperty(name="Bone Name")
    selected: bpy.props.BoolProperty(name="Select", default=False)

class rig_sync_panel_properties(bpy.types.PropertyGroup):
    """ Main Panel Properties """
    source_rig: bpy.props.PointerProperty(name='Source Rig', type=bpy.types.Object)
    target_rig: bpy.props.PointerProperty(name='Target Rig', type=bpy.types.Object)
    bones: bpy.props.CollectionProperty(type=rig_sync_bone_item)
    bones_active_index: bpy.props.IntProperty()
