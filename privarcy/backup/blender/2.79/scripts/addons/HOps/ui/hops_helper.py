import bpy
from bpy.props import *
from .. utils.blender_ui import get_dpi_factor
from bl_ui.properties_data_modifier import DATA_PT_modifiers

def find_node(material, nodetype):
    if material and material.node_tree:
        ntree = material.node_tree

        active_output_node = None
        for node in ntree.nodes:
            if getattr(node, "type", None) == nodetype:
                if getattr(node, "is_active_output", True):
                    return node
                if not active_output_node:
                    active_output_node = node
        return active_output_node
       
    return None

def find_node_input(node, name):
    for input in node.inputs:
        if input.name == name:
            return input
  
    return None


def panel_node_draw(layout, id_data, output_type, input_name):
    if not id_data.use_nodes:
        layout.operator("cycles.use_shading_nodes", icon='NODETREE')
        return False

    ntree = id_data.node_tree

    node = find_node(id_data, output_type)
    if not node:
        layout.label(text="No output node")
    else:
        input = find_node_input(node, input_name)
        layout.template_node_view(ntree, node, input)

    return True    

helper_tabs_items = [
    ("MODIFIERS", "Modifiers", ""),
    ("MATERIALS", "Materials", ""),
    ("MISC", "Misc", "") ]

class HOpsHelperPopup(bpy.types.Operator):
    bl_idname = "view3d.hops_helper_popup"
    bl_label = "HOps Helper"

    tab = EnumProperty(name = "Tab", default = "MODIFIERS",
            options = {"SKIP_SAVE"}, items = helper_tabs_items)

    def execute(self, context):
        return {'FINISHED'}

    def check(self, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 300 * get_dpi_factor())

    def draw(self, context):
        layout = self.layout
        self.draw_tab_bar(layout)

        if self.tab == "MODIFIERS":
            self.draw_modifier_tab(layout)
        elif self.tab == "MATERIALS":
            self.draw_material_tab(layout)
        elif self.tab == "MISC":
            self.draw_misc_tab(layout)

    def draw_tab_bar(self, layout):
        row = layout.row()
        row.prop(self, "tab", expand = True)
        layout.separator()

    def draw_modifier_tab(self, layout):
        row = layout.row()

        object = bpy.context.active_object
        if object is None:
            row.alignment = "CENTER"
            row.label("No active object", icon = "INFO")
            return

        row.operator_menu_enum("object.modifier_add", "type")
        row.operator("object.make_links_data", text = "Copy Modifiers From").type = "MODIFIERS"

        modifiers_panel = DATA_PT_modifiers(bpy.context)
        for modifier in object.modifiers:
            box = layout.template_modifier(modifier)
            if box:
                getattr(modifiers_panel, modifier.type)(box, object, modifier)

    def draw_material_tab(self, layout):
        layout.operator_context = 'INVOKE_REGION_WIN'   

        cobj = bpy.context.object              
        cmat = bpy.context.object.active_material        

        # box = layout.box().column(1) 

        # row = box.row(1)              
        # # row.operator("material.simplify", text="", icon="SPACE3")                               
        # # row.menu("object.material_list_menu", text="Apply...", icon="NLA_PUSHDOWN")      
   
        # box.separator()

        box = layout.box().column(1) 

        row = box.row(1)
        row.template_ID(cobj, "active_material", new="material.new")
       
        box.separator()
       
        #row = box.row(1)                        
        #row.prop(cmat, "use_nodes", icon='NODETREE') 

        #box.separator()

        box = layout.box().column(1) 

        row = box.column(1)  

        mat = bpy.context.object.material_slots[0].material
        if not panel_node_draw(box, mat, 'OUTPUT_MATERIAL', 'Surface'):
            box = layout.box().column(1) 

            row = box.column(1) 
            row.prop(mat, "diffuse_color")

        # box.separator()

        # box = layout.box().column(1) 

        # row = box.column(1)  
        # mat = bpy.context.object.material_slots[0].material
        # panel_node_draw(box, mat, 'OUTPUT_MATERIAL', 'Volume')
      
        # box.separator()

        # box = layout.box().column(1) 

        # row = box.column(1)
        # mat = bpy.context.object.material_slots[0].material  
        # panel_node_draw(box, mat, 'OUTPUT_MATERIAL', 'Displacement') 
        
        box.separator()   

        cobj = bpy.context.object 
        cmat = bpy.context.object.active_material                
        ccmat = bpy.context.object.active_material.cycles 

        box = layout.box().column(1) 

        row = box.row(1)
        row.label(text="Surface:")
      
        # row = box.column(1)
        # row.prop(ccmat, "sample_as_light", text="Multiple Importance")
        # row.prop(ccmat, "use_transparent_shadow")

        # box.separator()
        # box.separator()
        
        # row = box.row(1)
        # row.label(text="Volume:")
       
        # row = box.row(1)
        # row.prop(ccmat, "volume_sampling", text="")
        # row.prop(ccmat, "volume_interpolation", text="")              
      
        # row = box.row(1)               
        # row.prop(ccmat, "homogeneous_volume", text="Homogeneous")

        # box.separator()
        box.separator()
        
        row = box.row(1)
        row.label("Viewport Color:")
        row.label("Viewport Alpha:")
                              
        row = box.row(1)               
        row.prop(cmat, "diffuse_color", text="")
        row.prop(cmat, "specular_color", text="")
     
        row = box.row(1)                   
        row.prop(cmat, "alpha")
        row.prop(cmat, "specular_hardness", text="Hardness")

        box.separator()
        
        row = box.column(1)
        row.prop(cobj, "show_transparent", text = "Transparency")

        row = box.column(1)
        row.label("Viewport Specular:")  
        cgmat = bpy.context.object.active_material.game_settings                           
        row.prop(cgmat, "alpha_blend", text="")

        box.separator()
        box.separator()
        
        row = box.column(1) 

        row.prop(cmat, "pass_index")            

        box.separator()                                               
          

    def draw_misc_tab(self, layout):
        layout.label("Coming To 008!", icon = "INFO")
