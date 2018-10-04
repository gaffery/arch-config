# Info
bl_info = {
    "name": "PBR Materials",
    "description": "PBR Materials and Procedural Textures",
    "version": (3, 1),
    "blender": (2, 79, 0),
    "author": "Wolf & Nathan Craddock",
    "location": "Material Properties and Node Editor",
	"wiki_url": "https://www.3d-wolf.com/materials.html",
    "tracker_url": "https://www.3d-wolf.com/materials.html",
    "support": "COMMUNITY",
    "category": "Material"
}


if "bpy" in locals():
    import importlib
    importlib.reload(materials)
    importlib.reload(textures)
    importlib.reload(material_nodes)
else:
    from . import materials
    from . import textures
    from . import material_nodes
import bpy
from . import addon_updater_ops


# Toggle
def addon_toggle(self, context):
    settings = context.scene.pbr_material_settings

    # If the Checkbox is OFF, add basic Principled
    if not settings.enabled:
        # Delete active material
        active_mat = context.active_object.active_material
        active_mat.use_nodes = True
        active_mat.node_tree.nodes.clear()
        preview_type = active_mat.preview_render_type
        # Create nodes
        output = active_mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
        principled = active_mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        output.location = (200, 0)
        # Link nodes
        active_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
        # Hack to refresh the preview
        active_mat.preview_render_type = preview_type

    else:
        # Select the Dielectric Preview
        bpy.context.scene.pbr_material_settings.category = 'd'
        bpy.context.scene.thumbs_mats_dielectrics = 'Dielectric'
        # Add material
        materials.add_material(self, context)


# Settings
class PBRMaterialSettings(bpy.types.PropertyGroup):
    category = bpy.props.EnumProperty(
        items=[('d', 'Dielectric', 'Dielectric Materials'),
               ('m', 'Metal', 'Metal Materials')],
        description="Type of Material",
        default='d'
    )
    
    category_node = bpy.props.EnumProperty(
        items=[('d', 'Dielectric', 'Show dielectric materials'),
               ('m', 'Metal', 'Show metallic materials')],
        description="Choose the category for materials",
        default='d'
    )
    
    enabled = bpy.props.BoolProperty(
        name="Enabled",
        description="Use PBR Materials Addon",
        default=False,
        update=addon_toggle
    )


# Preferences
class PBRMaterialsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # addon updater preferences
    auto_check_update = bpy.props.BoolProperty(
        name = "Auto-check for Update",
        description = "If enabled, auto-check for updates using an interval",
        default = True,
        )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description = "Number of months between checking for updates",
        default=0,
        min=0
        )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description = "Number of days between checking for updates",
        default=1,
        min=0,
        )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description = "Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
        )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description = "Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
        )

    def draw(self, context):
		
        layout = self.layout
        # updater draw function
        addon_updater_ops.update_settings_ui(self,context)


# Register
def register():
    addon_updater_ops.register(bl_info)
    bpy.utils.register_module(__name__)
    materials.register()
    textures.register()
    material_nodes.register()
    bpy.types.Scene.pbr_material_settings = bpy.props.PointerProperty(type=PBRMaterialSettings)

def unregister():
    
    bpy.utils.unregister_module(__name__)
    materials.unregister()
    textures.unregister()
    material_nodes.unregister()
    del bpy.types.Scene.pbr_material_settings
