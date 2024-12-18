# Blender Rig Sync

A Simple Utility that syncs two Rigs in Blender using Constraints.<br>
It applies a `CopyTransform` Constraint to the Target Rig based on the Source Rig.<br>
Bones are identified using their Names.

Tested with Blender 4.3 and Rigify Rigs.

## Usage

1. Install Addon
    1. Go to Edit - Preferences - Add-ons
    2. Click the downward-facing Arrow in the top-right Corner and select _Install from Disk_
    3. Select the Zip File
    4. Enable the Addon
2. Go to the 3D Viewport
3. Press `N` to open the right Sidebar and go to `Tool`
4. Open the _Rig Sync Tools_ Area
5. Select your Source and Target Rig
6. Click _Enable Sync_ or _Disable Sync_ to control the Syncing.

The Script automatically checks if such constraint is already present on the Bone and will _not_ add another one.