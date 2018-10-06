bl_info = {
        "name":"ParticleBrushSelect",
        "author": "gaffey",
        "version": (0,0,1),
        "blender": (2,7,0),
        "location": "Properties",
        "category": "Operator",
        "description": "Set particle brush select mode ",
        "wiki_url": "none",
        "tracker_url":"none"
        }

import bpy

class ParticleSmoothBrushSelect(bpy.types.Operator):
    """Select the smooth brush"""
    bl_idname = "particle.smooth_select"
    bl_label = "Select smooth particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'SMOOTH'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}



class ParticleCombBrushSelect(bpy.types.Operator):
    """Select the comb brush"""
    bl_idname = "particle.comb_select"
    bl_label = "Select comb particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'COMB'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}



class ParticleNoneBrushSelect(bpy.types.Operator):
    """Select the none brush"""
    bl_idname = "particle.none_select"
    bl_label = "Select none particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'NONE'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}



class ParticleAddBrushSelect(bpy.types.Operator):
    """Select the add brush"""
    bl_idname = "particle.add_select"
    bl_label = "Select add particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'ADD'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}



class ParticleLengthBrushSelect(bpy.types.Operator):
    """Select the length brush"""
    bl_idname = "particle.length_select"
    bl_label = "Select length particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'LENGTH'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}


class ParticlePuffBrushSelect(bpy.types.Operator):
    """Select the puff brush"""
    bl_idname = "particle.puff_select"
    bl_label = "Select puff particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'PUFF'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}




class ParticleCutBrushSelect(bpy.types.Operator):
    """Select the cut brush"""
    bl_idname = "particle.cut_select"
    bl_label = "Select cut particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'CUT'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}



class ParticleWeightBrushSelect(bpy.types.Operator):
    """Select the weight brush"""
    bl_idname = "particle.weight_select"
    bl_label = "Select weight particle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = 'WEIGHT'
        bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ParticleWeightBrushSelect)
    bpy.utils.register_class(ParticleSmoothBrushSelect)
    bpy.utils.register_class(ParticleCombBrushSelect)
    bpy.utils.register_class(ParticleNoneBrushSelect)
    bpy.utils.register_class(ParticleAddBrushSelect)
    bpy.utils.register_class(ParticleLengthBrushSelect)
    bpy.utils.register_class(ParticlePuffBrushSelect)
    bpy.utils.register_class(ParticleCutBrushSelect)
    
def unregister():
    bpy.utils.unregister_class(ParticleWeightBrushSelect)
    bpy.utils.unregister_class(ParticleSmoothBrushSelect)
    bpy.utils.unregister_class(ParticleCombBrushSelect)
    bpy.utils.unregister_class(ParticleNoneBrushSelect)
    bpy.utils.unregister_class(ParticleAddBrushSelect)
    bpy.utils.unregister_class(ParticleLengthBrushSelect)
    bpy.utils.unregister_class(ParticlePuffBrushSelect)
    bpy.utils.unregister_class(ParticleCutBrushSelect)
    
if __name__ == "__main__":
    register()