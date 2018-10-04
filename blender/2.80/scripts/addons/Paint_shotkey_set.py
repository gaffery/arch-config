bl_info = {
        "name":"Paint shotkey add set",
        "author": "gaffey",
        "version": (0,0,1),
        "blender": (2,7,6),
        "location": "Properties",
        "category": "Operator",
        "description": "Paint shotkey add set mode ",
        "wiki_url": "none",
        "tracker_url":"none"
        } 



import bpy

class PaintUseSymmetryX(bpy.types.Operator):
    """paint use symmetry x"""      
    bl_idname = "paint.symmetry_x"  
    bl_label = "paint use symmetry x" 
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):    
        if bpy.context.scene.tool_settings.image_paint.use_symmetry_x ==1:
            bpy.context.scene.tool_settings.image_paint.use_symmetry_x=0
        else:
            bpy.context.scene.tool_settings.image_paint.use_symmetry_x=1
        return {'FINISHED'}      
 


 
def register():
    bpy.utils.register_class(PaintUseSymmetryX)
def unregister():
    bpy.utils.unregister_class(PaintUseSymmetryX)	
if __name__ == "__main__":
    register()