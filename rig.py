import bpy
import re

def switch_to_pose_mode():
    """Switch to Pose Mode if an armature is selected and not already in Pose Mode."""
    obj = bpy.context.object
    if obj and obj.type == 'ARMATURE':
        if obj.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
    else:
        raise TypeError("No armature selected. Please select an armature to switch to Pose Mode.")

def switch_to_object_mode():
    """Switch to Object Mode if not already in Object Mode."""
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

def generate_constraint_name(bone_name, source_rig_name):
    """Generate the constraint name based on bone and source rig name."""
    return f'Sync Bone {bone_name} with Rig {source_rig_name}'

def get_matching_bones(source_rig, target_rig):
    """Get a list of bones that exist in both source and target rigs."""
    return [bone.name for bone in source_rig.pose.bones if bone.name in target_rig.pose.bones]

def add_constraint_to_bone(target_bone, source_rig, bone_name, constraint_name):
    """Add a Copy Transforms constraint to a target bone."""
    constraint_exists = any(
        re.match(f"^{re.escape(constraint_name)}(\\.\\d{{3}})?$", constraint.name)
        for constraint in target_bone.constraints
    )

    if not constraint_exists:
        constraint = target_bone.constraints.new(type='COPY_TRANSFORMS')
        constraint.name = constraint_name
        constraint.target = source_rig
        constraint.subtarget = bone_name
        constraint.target_space = 'LOCAL'
        constraint.owner_space = 'LOCAL'
        print(f'Added Constraint to Bone {bone_name}')

def remove_constraint_from_bone(target_bone, constraint_name):
    """Remove constraints that match the generated constraint name."""
    constraints_to_remove = [
        constraint.name for constraint in target_bone.constraints
        if re.match(f"^{re.escape(constraint_name)}(\\.\\d{{3}})?$", constraint.name)
    ]

    for name in constraints_to_remove:
        constraint = target_bone.constraints.get(name)
        if constraint:
            target_bone.constraints.remove(constraint)
            print(f'Removed Constraint: {name}')
