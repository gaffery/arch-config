bl_info = {
        "name":"Edit shotkey add set",
        "author": "gaffey",
        "version": (0,0,1),
        "blender": (2,7,6),
        "location": "Properties",
        "category": "Operator",
        "description": "Edit shotkey add set mode ",
        "wiki_url": "none",
        "tracker_url":"none"
        }



import bpy

class OccludeGeometry(bpy.types.Operator):
    """edit use Occlude Geometry"""
    bl_idname = "occlude.geometry"
    bl_label = "Occlude Ggeometry "
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):
        if bpy.context.space_data.use_occlude_geometry == 1:
            bpy.context.space_data.use_occlude_geometry = 0
        else:
            bpy.context.space_data.use_occlude_geometry = 1
        return {'FINISHED'}




def register():
    bpy.utils.register_class(OccludeGeometry)
def unregister():
    bpy.utils.unregister_class(OccludeGeometry)
if __name__ == "__main__":
    register()
