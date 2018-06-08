bl_info = {
        "name":"TransformGroup",
        "author": "gaffey",
        "version": (0,0,1),
        "blender": (2,7,8),
        "location": "Properties",
        "category": "Operator",
        "description": "transform group operator ",
        "wiki_url": "none",
        "tracker_url":"none"
        }

import bpy

class TransformGroup(bpy.types.Operator):
    """transform group operator"""
    bl_idname = "transform.group"
    bl_label = "transform group operator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        shape = bpy.data.meshes.new('transform')
        transform = bpy.data.objects.new('transform', shape)
    
        bpy.context.scene.objects.link(transform)
        bpy.context.scene.objects.active = transform
        bpy.ops.object.parent_set(keep_transform=True)
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.select_hierarchy(direction='PARENT', extend=False)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        bpy.data.objects[transform.name].hide = True
        return {'FINISHED'}    

def register():
    bpy.utils.register_class(TransformGroup)

def unregister():
    bpy.utils.unregister_class(TransformGroup)


    
if __name__ == "__main__":
    register()
