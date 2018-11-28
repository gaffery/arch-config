bl_info = {
        "name":"Sculpt shotkey add set",
        "author": "gaffey",
        "version": (0,0,1),
        "blender": (2,7,6),
        "location": "Properties",
        "category": "Operator",
        "description": "Sculpt shotkey add set mode ",
        "wiki_url": "none",
        "tracker_url":"none"
        } 



import bpy

class SculptUseSymmetryX(bpy.types.Operator):
    """sculpt use symmetry x"""      
    bl_idname = "sculpt.symmetry_x"  
    bl_label = "sculpt use symmetry x" 
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):    
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_x ==1:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x=0
        else:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x=1
        return {'FINISHED'}      
 


 
def register():
    bpy.utils.register_class(SculptUseSymmetryX)
def unregister():
    bpy.utils.unregister_class(SculptUseSymmetryX)	
if __name__ == "__main__":
    register()