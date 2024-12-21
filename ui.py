import bpy

class rig_sync_bones_list(bpy.types.UIList):
    """ Custom List for Bones """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "selected", text="")
            row.label(text=item.name, icon='BONE_DATA')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='BONE_DATA')

class rig_sync_panel(bpy.types.Panel):
    """ Main UI Panel """
    bl_label = 'Rig Sync Tools'
    bl_idname = 'VIEW3D_PT_rig_sync_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig Sync'

    def draw(self, context):
        layout = self.layout
        props = context.scene.rig_sync_props

        layout.prop(props, 'source_rig', text='Source Rig')
        layout.prop(props, 'target_rig', text='Target Rig')

        row = layout.row()
        row.operator('rig_sync.enable_sync', text='Enable Sync')
        row.operator('rig_sync.disable_sync', text='Disable Sync')

        row = layout.row()
        row.operator('rig_sync.list_bones', text='List Bones')

        row = layout.row()
        row.template_list('rig_sync_bones_list', 'custom_list', props, 'bones', props, 'bones_active_index')

        row = layout.row()
        row.operator('rig_sync.select_all_bones', text='Select All')
        row.operator('rig_sync.select_none_bones', text='Select None')