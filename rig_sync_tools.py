import bpy
import re

class rig_sync_panel_properties(bpy.types.PropertyGroup):
    """ This Class contains the Properties in the Rig Sync Panel """
    source_rig: bpy.props.PointerProperty(
        name='Source Rig',
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    target_rig: bpy.props.PointerProperty(
        name='Target Rig',
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )

class rig_sync_panel(bpy.types.Panel):
    """ This Class represents the actual UI Panel """
    bl_label = 'Rig Sync Tools'
    bl_idname = 'VIEW3D_PT_rig_sync_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        props = context.scene.rig_sync_props

        # Source Rig selector
        layout.prop(props, 'source_rig', text='Source Rig')

        # Target Rig selector
        layout.prop(props, 'target_rig', text='Target Rig')

        # Action Buttons
        row = layout.row()
        row.operator('rig_sync.enable_sync', text='Enable Sync')
        row.operator('rig_sync.disable_sync', text='Disable Sync')


def switch_to_pose_mode():
    """Switch to Pose Mode if not already in Pose Mode"""
    if bpy.context.object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')


def switch_to_object_mode():
    """Switch to Object Mode if not already in Object Mode"""
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


def generate_constraint_name(bone_name, source_rig_name):
    """Generate the constraint name based on bone and source rig name"""
    return f'Sync Bone {bone_name} with Rig {source_rig_name}'


class rig_sync_enable_sync(bpy.types.Operator):
    bl_idname = 'rig_sync.enable_sync'
    bl_label = 'Enable Sync'

    def execute(self, context):
        props = context.scene.rig_sync_props

        # Get rigs
        source_rig = props.source_rig
        target_rig = props.target_rig

        if not source_rig or not target_rig:
            self.report({'ERROR'}, 'Please select both Source Rig and Target Rig.')
            return {'CANCELLED'}

        source_rig_name = source_rig.name
        target_rig_name = target_rig.name

        switch_to_pose_mode()

        for bone in source_rig.pose.bones:
            bone_name = bone.name
            if bone_name in target_rig.pose.bones:
                constraint_name = generate_constraint_name(bone_name, source_rig_name)
                target_bone = target_rig.pose.bones[bone_name]

                # Check if the constraint already exists
                constraint_exists = any(
                    re.match(f"^{re.escape(constraint_name)}(\\.\\d{{3}})?$", constraint.name)
                    for constraint in target_bone.constraints
                )

                if constraint_exists:
                    print(f'Constraint for Bone {bone_name} on Rig {target_rig_name} already exists')
                else:
                    # Add the Copy Transforms constraint
                    constraint = target_bone.constraints.new(type='COPY_TRANSFORMS')
                    constraint.name = constraint_name
                    constraint.target = source_rig
                    constraint.subtarget = bone_name
                    constraint.target_space = 'LOCAL'
                    constraint.owner_space = 'LOCAL'
                    print(f'Added Constraint to Bone {bone_name} of Rig {target_rig_name}')

        switch_to_object_mode()
        return {'FINISHED'}


class rig_sync_disable_sync(bpy.types.Operator):
    bl_idname = 'rig_sync.disable_sync'
    bl_label = 'Disable Sync'

    def execute(self, context):
        props = context.scene.rig_sync_props

        # Get rigs
        source_rig = props.source_rig
        target_rig = props.target_rig

        if not source_rig or not target_rig:
            self.report({'ERROR'}, 'Please select both Source Rig and Target Rig.')
            return {'CANCELLED'}

        source_rig_name = source_rig.name
        target_rig_name = target_rig.name

        switch_to_pose_mode()

        for bone in target_rig.pose.bones:
            bone_name = bone.name
            constraint_name = generate_constraint_name(bone_name, source_rig_name)

            # Remove constraints that match the pattern
            constraints_to_remove = [
                constraint for constraint in bone.constraints
                if re.match(f"^{re.escape(constraint_name)}(\\.\\d{{3}})?$", constraint.name)
            ]

            for constraint in constraints_to_remove:
                bone.constraints.remove(constraint)
                print(f'Removed Constraint from Bone {bone_name} of Rig {target_rig_name}')

        switch_to_object_mode()
        return {'FINISHED'}


classes = [
    rig_sync_panel_properties,
    rig_sync_panel,
    rig_sync_enable_sync,
    rig_sync_disable_sync
]


def register():
    for cl in classes:
        bpy.utils.register_class(cl)
    bpy.types.Scene.rig_sync_props = bpy.props.PointerProperty(type=rig_sync_panel_properties)


def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)
    del bpy.types.Scene.rig_sync_props
