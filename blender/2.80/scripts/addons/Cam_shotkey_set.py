bl_info = {
        "name":"Camera Shotkey Add Set",
        "author": "gaffey",
        "version": (0,0,1),
        "blender": (2,7,8),
        "location": "Properties",
        "category": "Operator",
        "description": "camera shotkey add set mode ",
        "wiki_url": "none",
        "tracker_url":"none"
        }



import bpy

class LockCameraView(bpy.types.Operator):
    """lock camera to view"""
    bl_idname = "camera.lock"
    bl_label = "Camera View Lock"
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):
        if bpy.context.space_data.lock_camera == 1:
            bpy.context.space_data.lock_camera = 0
        else:
            bpy.context.space_data.lock_camera = 1
        return {'FINISHED'}




def register():
    bpy.utils.register_class(LockCameraView)
def unregister():
    bpy.utils.unregister_class(LockCameraView)
if __name__ == "__main__":
    register()
