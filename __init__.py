bl_info = {
    'name': 'Rig Sync Tools',
    'author': 'Oliver Karger',
    'version': (1, 0, 0),
    'blender': (4, 3, 0),
    'location': 'View3D > Tool Panel > Rig Sync Tools',
    'description': 'Simply utility that adds Constraints to copy Transforms from one Rig to another. Bone-by-Bone',
    'category': 'Animation',
    'support': 'COMMUNITY',
}

import bpy
from . import rig_sync_tools

def register():
    rig_sync_tools.register()

def unregister():
    rig_sync_tools.unregister()

if __name__ == '__main__':
    register()
