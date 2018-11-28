# Import
import bpy
import bpy.utils.previews
import os


preview_collections = {}


# Add Node Button
class UseCurrentMaterial(bpy.types.Operator):
    bl_idname = "material.use_current_material_node"
    bl_label = "Add Material Node"
    bl_options = {'UNDO'}

    def execute(self, context):
        append_material_node(self, context)
        return {'FINISHED'}


# Panel
class PBRMaterialPanelNode(bpy.types.Panel):
    bl_label = "PBR Material Nodes"
    bl_idname = "pbr_previews_node"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        if bpy.context.object.active_material:
            return context.scene.render.engine == 'CYCLES' and bpy.context.space_data.tree_type == 'ShaderNodeTree' and bpy.context.space_data.shader_type == 'OBJECT' and bpy.context.object.active_material.use_nodes


    # Draw
    def draw(self, context):
        settings = context.scene.pbr_material_settings
        layout = self.layout
        col = layout.column(align=True)
        row = col.row()
        row.prop(settings, 'category_node', text="Category", expand=True)

        # Preview
        row = col.row()
        if settings.category_node == 'm':
            row.template_icon_view(context.scene, "thumbs_mats_metals_node", show_labels=True)

            # Material Name
            material_name = context.scene.thumbs_mats_metals_node
            row = col.row(align=True)
            row.alignment = 'CENTER'
            row.label(material_name)

        else:
            row.template_icon_view(context.scene, "thumbs_mats_dielectrics_node", show_labels=True)

            # Material Name
            material_name = context.scene.thumbs_mats_dielectrics_node
            row = col.row(align=True)
            row.alignment = 'CENTER'
            row.label(material_name)


def append_material_node(self, context):
    settings = context.scene.pbr_material_settings
    path = os.path.join(os.path.dirname(__file__), "blends" + os.sep + "dielectrics.blend")

    if settings.category_node == 'd':
        node_name = context.scene.thumbs_mats_dielectrics_node
        if node_name in ("Atmosphere", "Blood", "Cloud", "Curtain", "Fire", "Grass", "Hair", "Leaf", "Ocean", "Paper", "Particles", "Satin", "Transparent"):
            with bpy.data.libraries.load(path, False) as (data_from, data_to):
                if not node_name in bpy.data.node_groups:
                    data_to.node_groups = [node_name]
    else:
        node_name = context.scene.thumbs_mats_metals_node

    bpy.ops.node.select_all(action='DESELECT')
    active_mat = bpy.context.active_object.active_material

    # Dielectrics
    if node_name=="Dielectric":
        princi = principled(node_name, active_mat)
        princi.inputs[7].default_value = (0)
    elif node_name=="Acrylic Paint Black":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.05, 0.05, 0.05, 1)
        princi.inputs[5].default_value = (0.488)
        princi.inputs[7].default_value = (0)
    elif node_name=="Acrylic Paint White":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
        princi.inputs[5].default_value = (0.488)
        princi.inputs[7].default_value = (0)
    elif node_name=="Asphalt New":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.05, 0.05, 0.05, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.55)
    elif node_name=="Asphalt Old":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.12, 0.12, 0.12, 1)
        princi.inputs[5].default_value = (0.25)
        princi.inputs[7].default_value = (0.55)
    elif node_name=="Bark":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.168, 0.136, 0.105, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.6)
    elif node_name=="Brick":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.227, 0.147, 0.109, 1)
        princi.inputs[5].default_value = (0.588)
        princi.inputs[7].default_value = (0.78)
    elif node_name=="Car Paint":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0, 0.083, 0.457, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.25)
        princi.inputs[12].default_value = (1)
    elif node_name=="Carbon":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.015, 0.015, 0.015, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.4)
        princi.inputs[12].default_value = (1)
    elif node_name=="Ceramic":
        princi = principled(node_name, active_mat)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0.898, 0.716, 1)
        princi.inputs[0].default_value = (0.6, 0.6, 0.6, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.6, 0.6, 0.6, 1)
        princi.inputs[5].default_value = (0.525)
        princi.inputs[7].default_value = (0)
    elif node_name=="Chalk":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.179, 0.7, 0.39, 1)
        princi.inputs[5].default_value = (0.563)
        princi.inputs[7].default_value = (0.65)
    elif node_name=="Cloth":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.065, 0.08, 0.254, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.8)
        princi.inputs[10].default_value = (1)
        princi.inputs[11].default_value = (0)
    elif node_name=="Coal":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.04, 0.04, 0.04, 1)
        princi.inputs[5].default_value = (0.425)
        princi.inputs[7].default_value = (0.66)
    elif node_name=="Concrete":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.231, 0.231, 0.202, 1)
        princi.inputs[5].default_value = (1.2)
        princi.inputs[7].default_value = (0.74)
    elif node_name=="Dirt":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.258, 0.162, 0.109, 1)
        princi.inputs[5].default_value = (0.75)
        princi.inputs[7].default_value = (0.78)
    elif node_name=="Light":
        emission = active_mat.node_tree.nodes.new("ShaderNodeEmission")
        blackbody = active_mat.node_tree.nodes.new("ShaderNodeBlackbody")
        blackbody.location = (-200, 0)
        blackbody.inputs[0].default_value = (3000)
        active_mat.node_tree.links.new(blackbody.outputs[0], emission.inputs[0])
        active_mat.node_tree.links.new(emission.outputs[0].inputs[0])
    elif node_name=="Mud":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.342, 0.246, 0.165, 1)
        princi.inputs[5].default_value = (2.225)
        princi.inputs[7].default_value = (0.62)
    elif node_name=="Plaster":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.275, 0.262, 0.235, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.86)
    elif node_name=="Plastic":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.448, 0.013, 0.007, 1)
        princi.inputs[5].default_value = (0.375)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Rock":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.328, 0.287, 0.227, 1)
        princi.inputs[5].default_value = (0.625)
        princi.inputs[7].default_value = (0.81)
    elif node_name=="Rubber":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.022, 0.022, 0.022, 1)
        princi.inputs[5].default_value = (0.425)
        princi.inputs[7].default_value = (0.79)
    elif node_name=="Rust":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.184, 0.032, 0.007, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.82)
    elif node_name=="Sand":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.44, 0.386, 0.231, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.8)
        princi.inputs[10].default_value = (1)
        princi.inputs[11].default_value = (0)
    elif node_name=="Skin":
        princi = principled(node_name, active_mat)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0, 0, 1)
        princi.inputs[0].default_value = (0.523, 0.251, 0.19, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.523, 0.251, 0.19, 1)
        princi.inputs[5].default_value = (0.413)
        princi.inputs[7].default_value = (0.5)
    elif node_name=="Snow":
        princi = principled(node_name, active_mat)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0.97, 0.95, 1)
        princi.inputs[0].default_value = (0.9, 0.9, 0.9, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.9, 0.9, 0.9, 1)
        princi.inputs[5].default_value = (1.25)
        princi.inputs[7].default_value = (0.5)
    elif node_name=="Wax":
        princi = principled(node_name, active_mat)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0.397, 0.16, 1)
        princi.inputs[0].default_value = (0.263, 0.084, 0.222, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.263, 0.084, 0.222, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.3)
    elif node_name=="Wood":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.402, 0.319, 0.231, 1)
        princi.inputs[5].default_value = (1)
        princi.inputs[7].default_value = (0.68)

    # Translucent and Volume
    if node_name in ("Atmosphere", "Blood", "Cloud", "Curtain", "Fire", "Grass", "Hair", "Leaf", "Ocean", "Paper", "Particles", "Satin", "Transparent"):
        group = bpy.data.materials[active_mat.name].node_tree.nodes.new("ShaderNodeGroup")
        group.node_tree = bpy.data.node_groups[node_name]
        group.location = bpy.context.space_data.edit_tree.view_center

    # Metals
    if node_name=="Aluminium":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.815, 0.831, 0.839, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Brass":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.956, 0.791, 0.305, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Bronze":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.973, 0.429, 0.15, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Chromium":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.262, 0.258, 0.283, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Cobalt":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.392, 0.386, 0.361, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Copper":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.973, 0.356, 0.246, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Gallium":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.479, 0.604, 0.578, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Gold":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.973, 0.539, 0.109, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Iron":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.552, 0.571, 0.571, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Lead":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.591, 0.591, 0.591, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Mercury":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.584, 0.571, 0.571, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0)
    elif node_name=="Molybdenum":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.429, 0.445, 0.361, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Nickel":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.392, 0.323, 0.235, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Pewter":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.515, 0.456, 0.392, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Platinum":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.429, 0.381, 0.314, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Pot":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.815, 0.831, 0.839, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.3)
        princi.inputs[8].default_value = (1)
        princi.inputs[9].default_value = (0.25)
    elif node_name=="Rhodium":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.468, 0.381, 0.392, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Silver":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.93, 0.913, 0.831, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Tin":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.776, 0.776, 0.776, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Titanium":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.262, 0.209, 0.165, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Tungsten":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.319, 0.319, 0.309, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Vanadium":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.407, 0.451, 0.429, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Zinc":
        princi = principled(node_name, active_mat)
        princi.inputs[0].default_value = (0.591, 0.546, 0.462, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)


# Principled
def principled(node_name, active_mat):
    principled = active_mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    principled.name = node_name
    principled.location = bpy.context.space_data.edit_tree.view_center
    return principled

# RGB
def rgb(principled, active_mat):
    rgbnode = active_mat.node_tree.nodes.new("ShaderNodeRGB")
    rgbnode.location.x = principled.location.x-200
    rgbnode.location.y = principled.location.y
    active_mat.node_tree.links.new(rgbnode.outputs[0], principled.inputs[2])
    return rgbnode


# Previews
def generate_previews(metals):
    if metals:
        previews = preview_collections["pbr_materials_metals_node"]
    else:
        previews = preview_collections["pbr_materials_dielectrics_node"]
    image_location = previews.images_location
    enum_items = []
    # Generate the thumbnails
    for i, image in enumerate(os.listdir(image_location)):
        filepath = os.path.join(image_location, image)
        thumb = previews.load(filepath, filepath, 'IMAGE')

        enum_items.append((image, image, "", thumb.icon_id, i))
    enum_items.sort()
    return enum_items


##################################################################################################################


# Register
def register():
    previews_mat_metals = bpy.utils.previews.new()
    previews_mat_metals.images_location = os.path.join(os.path.dirname(__file__), "thumbs" + os.sep + 'm')

    previews_mat_dielectrics = bpy.utils.previews.new()
    previews_mat_dielectrics.images_location = os.path.join(os.path.dirname(__file__), "thumbs" + os.sep + 'd')

    preview_collections['pbr_materials_metals_node'] = previews_mat_metals
    preview_collections['pbr_materials_dielectrics_node'] = previews_mat_dielectrics

    bpy.types.Scene.thumbs_mats_metals_node = bpy.props.EnumProperty(
        items=generate_previews(True),
        description="Choose the material you want to use",
        update=append_material_node,
        default='Gold'
    )
    bpy.types.Scene.thumbs_mats_dielectrics_node = bpy.props.EnumProperty(
        items=generate_previews(False),
        description="Choose the material you want to use",
        update=append_material_node,
        default='Dielectric'
    )

# Unregister
def unregister():
    for preview in preview_collections.values():
        bpy.utils.previews.remove(preview)
    preview_collections.clear()

    del bpy.types.Scene.thumbs_mats_metals_node
    del bpy.types.Scene.thumbs_mats_dielectrics_node
