import bpy
from .rig import (
    switch_to_pose_mode,
    switch_to_object_mode,
    generate_constraint_name,
    add_constraint_to_bone,
    remove_constraint_from_bone,
    get_matching_bones
)

class rig_sync_list_bones(bpy.types.Operator):
    """ Operator to List Bones shared across Source and Target Rig """
    bl_idname = 'rig_sync.list_bones'
    bl_label = 'List Bones'

    def execute(self, context):
        props = context.scene.rig_sync_props
        source_rig = props.source_rig
        target_rig = props.target_rig

        if not source_rig or not target_rig:
            self.report({'ERROR'}, 'Please select both Source Rig and Target Rig.')
            return {'CANCELLED'}

        props.bones.clear()

        for bone_name in get_matching_bones(source_rig, target_rig):
            new_bone = props.bones.add()
            new_bone.name = bone_name
            new_bone.selected = False

        self.report({'INFO'}, f'Listed {len(props.bones)} matching bones.')
        return {'FINISHED'}

class rig_sync_enable_sync(bpy.types.Operator):
    """ Operator to enable Rig Sync """
    bl_idname = 'rig_sync.enable_sync'
    bl_label = 'Enable Sync'

    def execute(self, context):
        props = context.scene.rig_sync_props
        source_rig = props.source_rig
        target_rig = props.target_rig

        if not source_rig or not target_rig:
            self.report({'ERROR'}, 'Please select both Source Rig and Target Rig.')
            return {'CANCELLED'}

        switch_to_pose_mode()

        for bone_item in props.bones:
            if bone_item.selected and bone_item.name in target_rig.pose.bones:
                target_bone = target_rig.pose.bones[bone_item.name]
                constraint_name = generate_constraint_name(bone_item.name, source_rig.name)
                add_constraint_to_bone(target_bone, source_rig, bone_item.name, constraint_name)

        switch_to_object_mode()
        return {'FINISHED'}

class rig_sync_disable_sync(bpy.types.Operator):
    """ Operator to disable Rig Sync """
    bl_idname = 'rig_sync.disable_sync'
    bl_label = 'Disable Sync'

    def execute(self, context):
        props = context.scene.rig_sync_props
        source_rig = props.source_rig
        target_rig = props.target_rig

        if not source_rig or not target_rig:
            self.report({'ERROR'}, 'Please select both Source Rig and Target Rig.')
            return {'CANCELLED'}

        switch_to_pose_mode()

        for bone_item in props.bones:
            if bone_item.selected and bone_item.name in target_rig.pose.bones:
                target_bone = target_rig.pose.bones[bone_item.name]
                constraint_name = generate_constraint_name(bone_item.name, source_rig.name)
                remove_constraint_from_bone(target_bone, constraint_name)

        switch_to_object_mode()
        return {'FINISHED'}

class rig_sync_select_all_bones(bpy.types.Operator):
    """ Operator to select all Bones in the Bone List """
    bl_idname = 'rig_sync.select_all_bones'
    bl_label = 'Select All Bones'

    def execute(self, context):
        props = context.scene.rig_sync_props
        for bone in props.bones:
            bone.selected = True
        return {'FINISHED'}

class rig_sync_select_none_bones(bpy.types.Operator):
    """ Operator to select no Bones in the Bone List """
    bl_idname = 'rig_sync.select_none_bones'
    bl_label = 'Select None Bones'

    def execute(self, context):
        props = context.scene.rig_sync_props
        for bone in props.bones:
            bone.selected = False
        return {'FINISHED'}