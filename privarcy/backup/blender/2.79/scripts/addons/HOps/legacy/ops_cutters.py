import os
import bpy
import bmesh
from bpy.props import *
from math import pi, radians
import bpy.utils.previews
from random import choice

#############################
#Reverse Boolean
#############################

class RevBool(bpy.types.Operator):
    """Gives A Reverse Boolean Of Selection"""
    bl_idname = "reverse.boolean"
    bl_label = "ReverseBoolean"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #main(context)
        context = bpy.context
        scene = context.scene

        obj = context.object.copy()

        bool_mods = [m for m in obj.modifiers if m.type == 'BOOLEAN']

        if len(bool_mods):
            mod = bool_mods[-1]
            if mod.operation == 'DIFFERENCE':
                mod.operation = 'INTERSECT'

            elif mod.operation == 'INTERSECT':
                mod.operation = 'DIFFERENCE'

        scene.objects.link(obj)
        bpy.ops.multi.csharp()
        return {'FINISHED'}

#############################
#Reverse Boolean Cstep
#############################

class ReBool(bpy.types.Operator):
    """Gives A Reverse Boolean Of Selection For Sstep"""
    bl_idname = "reverse.bools"
    bl_label = "ReBool-S"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #main(context)
        context = bpy.context
        scene = context.scene

        obj = context.object.copy()

        bool_mods = [m for m in obj.modifiers if m.type == 'BOOLEAN']

        if len(bool_mods):
            mod = bool_mods[-1]
            if mod.operation == 'DIFFERENCE':
                mod.operation = 'INTERSECT'

            elif mod.operation == 'INTERSECT':
                mod.operation = 'DIFFERENCE'

        scene.objects.link(obj)
        bpy.ops.multi.sstep()
        return {'FINISHED'}

#############################
#Multi-SStep
#############################

class multisstepOperator(bpy.types.Operator):
    """Multi SStep"""
    bl_idname = "multi.sstep"
    bl_label = "Multi Object Sstep"

    @classmethod
    def poll(cls, context):

        obj_type = context.object.type
        return(obj_type in {'MESH'})
        return context.active_object is not None

    def execute(self, context):


        sel = bpy.context.selected_objects
        active = bpy.context.scene.objects.active.name

        for ob in sel:
                ob = ob.name
                bpy.context.scene.objects.active = bpy.data.objects[ob]

                #print(context.selected_objects)
                #bpy.ops.csharpen.objects(bevelwidth=0.01)
                bpy.ops.sstep.objects()

        return {'FINISHED'}

#############################
#Multi-CStep
#############################

class multicstepOperator(bpy.types.Operator):
    """Multi CStep"""
    bl_idname = "multi.cstep"
    bl_label = "Multi Object Cstep"

    @classmethod
    def poll(cls, context):

        obj_type = context.object.type
        return(obj_type in {'MESH'})
        return context.active_object is not None

    def execute(self, context):


        sel = bpy.context.selected_objects
        active = bpy.context.scene.objects.active.name

        for ob in sel:
                ob = ob.name
                bpy.context.scene.objects.active = bpy.data.objects[ob]

                #print(context.selected_objects)
                #bpy.ops.csharpen.objects(bevelwidth=0.01)
                bpy.ops.cstep.objects()

        return {'FINISHED'}
