import bpy, os
from . icons import get_icon_id, icons
from . utils.addons import addon_exists
from . utils.objects import get_inactive_selected_objects
#from . preferences import use_asset_manager, get_preferences, right_handed_enabled, pro_mode_enabled, Relink_options_enabled, BC_unlock_enabled
from bpy.props import IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty, PointerProperty
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)


class Dropdown_HardOps_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.hardops_window
    """

    display_hops_internal_tools = bpy.props.BoolProperty(name = "Open/Close", description = "Internal Tools", default = False)
 
    display_hops_operations = bpy.props.BoolProperty(name = "Open/Close", description = "Operations Tools", default = False)
    display_hops_meshtools = bpy.props.BoolProperty(name = "Open/Close", description = "Mesh Tools", default = False)
    
    display_hops_add = bpy.props.BoolProperty(name = "Open/Close", description = "Hardops Insert", default = True)
    display_hops_add_am = bpy.props.BoolProperty(name = "Open/Close", description = "Asset Manager", default = False)

    display_hops_ops = bpy.props.BoolProperty(name = "Open/Close", description = "Edit Operators", default = True)

    display_hops_material = bpy.props.BoolProperty(name = "Open/Close", description = "Materials", default = True)
    display_hops_mat = bpy.props.BoolProperty(name = "Open/Close", description = "Materials", default = False)
    display_mat_edit = bpy.props.BoolProperty(name = "Open/Close", description = "Material Settings", default = False)

    display_hops_stk = bpy.props.BoolProperty(name = "Open/Close", description = "Stack", default = False)
    display_hops_mod = bpy.props.BoolProperty(name = "Open/Close", description = "Modifiers", default = True)
    display_hops_con = bpy.props.BoolProperty(name = "Open/Close", description = "Contraints", default = False)
    display_hops_gui = bpy.props.BoolProperty(name = "Open/Close", description = "Display", default = True)

    display_hops_guidpy = bpy.props.BoolProperty(name = "Open/Close", description = "Object Display", default = False)
    display_hops_guiobj = bpy.props.BoolProperty(name = "Open/Close", description = "View Display", default = False)

    display_hops_ext = bpy.props.BoolProperty(name = "Open/Close", description = "Extra Tools", default = True)
    display_hops_xtras = bpy.props.BoolProperty(name = "Open/Close", description = "Extra Tools", default = False)
    display_hops_opgl = bpy.props.BoolProperty(name = "Open/Close", description = "OpenGL", default = False)

    display_hops_img = bpy.props.BoolProperty(name = "Open/Close", description = "Image OpenGL Render", default = False)
    display_img_ren = bpy.props.BoolProperty(name = "Open/Close", description = "Render", default = True)
    display_img_dim = bpy.props.BoolProperty(name = "Open/Close", description = "Dimesions", default = False)
    display_img_pfc = bpy.props.BoolProperty(name = "Open/Close", description = "Performance", default = False)
    display_img_color = bpy.props.BoolProperty(name = "Open/Close", description = "Color Managment", default = False)

    display_hops_anim = bpy.props.BoolProperty(name = "Open/Close", description = "Sequence Render", default = False)

    display_hops_cam = bpy.props.BoolProperty(name = "Open/Close", description = "fold menu", default = False)
    display_cam_display = bpy.props.BoolProperty(name = "Open/Close", description = "Display", default = False)
    display_cam_lens = bpy.props.BoolProperty(name = "Open/Close", description = "Lens & Presets", default = False)
    display_cam_sphere = bpy.props.BoolProperty(name = "Open/Close", description = "Depth of Field", default = False)
    display_cam_save = bpy.props.BoolProperty(name = "Open/Close", description = "Safe Areas", default = False)

    display_hops_cycles = bpy.props.BoolProperty(name = "Open/Close", description = "Cycle Setup", default = True)
    display_hops_cyc = bpy.props.BoolProperty(name = "Open/Close", description = "Cycle Setup", default = False)

    display_set_material = bpy.props.BoolProperty(name = "Set Material", description = "Assign Materials to selected Faces", default = True)


    #AM additions
    current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    user_preferences = bpy.context.user_preferences
    addon_pref = user_preferences.addons[current_dir].preferences
    
bpy.utils.register_class(Dropdown_HardOps_Props)
bpy.types.WindowManager.hardops_window = bpy.props.PointerProperty(type = Dropdown_HardOps_Props)


######################################################################################################

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

######################################################################################################

   
class HardOps_Panel_OBM(bpy.types.Panel):
    bl_label = "HardOps 8"
    bl_idname = "HardOps_Panel_ID_OBM"
    bl_category = "HardOps"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'


    @classmethod
    def poll(cls, context):
        isNoModelingMode = not (
        context.sculpt_object or
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        if context.mode == "OBJECT":
            return isNoModelingMode


    def draw(self, context):
        lt = context.window_manager.hardops_window
        layout = self.layout.column(1)   
        obj = context.active_object
        
        #AM additions
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_pref = user_preferences.addons[current_dir].preferences
        
        obj = context.active_object     
        if obj:
           obj_type = obj.type

           box = layout.box()
           row = box.row(1)   
           row.alignment = "CENTER"
                          
           if obj_type in {'MESH'}:
              row.label("MESH EDITING") 
                                  
           if obj_type in {'LATTICE'}:
              row.label("LATTICE DEFORM") 

           if obj_type in {'CURVE'}:
               row.label("CURVE EDITING")               
               
           if obj_type in {'SURFACE'}:
               row.label("SURFACE EDITING")                 
               
           if obj_type in {'META'}:
               row.label("META EDITING")                 
               
           if obj_type in {'FONT'}:
               row.label("FONT EDITING")  
                                              
           if obj_type in {'ARMATURE'}:
               row.label("FONT EDITING") 

           if obj_type in {'EMPTY'}:
               row.label("FONT EDITING") 

           if obj_type in {'CAMERA'}:
              row.label("CAMERA EDITING") 

           if obj_type in {'LAMP'}:
               row.label("LAMP EDITING") 

           if obj_type in {'SPEAKER'}:
               row.label("SPEAKER EDITING") 
                        

        #Add 
        box = layout.box().column(1)       
        
        row = box.row(1) 
        row.alignment = 'CENTER'               
        sub = row.row(1)
        sub.scale_x = 1
        sub.menu("INFO_MT_mesh_add",text="",icon='OUTLINER_OB_MESH')              
        sub.menu("INFO_MT_curve_add",text="",icon='OUTLINER_OB_CURVE')
        sub.menu("INFO_MT_surface_add",text="",icon='OUTLINER_OB_SURFACE')
        sub.menu("INFO_MT_metaball_add",text="",icon="OUTLINER_OB_META")
        sub.operator("object.camera_add",icon='OUTLINER_OB_CAMERA',text="")   
        sub.menu("INFO_MT_armature_add",text="",icon="OUTLINER_OB_ARMATURE")            
        
        if lt.display_hops_add:              
            sub.prop(lt, "display_hops_add", text="", icon='MOVE_UP_VEC')
        else:               
            sub.prop(lt, "display_hops_add", text="", icon='MOVE_DOWN_VEC')  


        row = box.row(1)
        row.alignment = 'CENTER'               
        sub = row.row(1)
        sub.scale_x = 1
        sub.operator("object.empty_add",text="",icon="OUTLINER_OB_EMPTY")          
        sub.operator("object.add",text="",icon="OUTLINER_OB_LATTICE").type="LATTICE"
        sub.operator("object.text_add",text="",icon="OUTLINER_OB_FONT")
        sub.operator("object.lamp_add",icon='OUTLINER_OB_LAMP',text="")
        sub.operator("object.speaker_add",icon='OUTLINER_OB_SPEAKER',text="")
        sub.operator_menu_enum("object.effector_add", "type", text="",icon="SOLO_ON")                
       
        if lt.display_hops_add_am:              
            sub.prop(lt, "display_hops_add_am", text="", icon='MOVE_UP_VEC')
        else:               
            sub.prop(lt, "display_hops_add_am", text="", icon='MOVE_DOWN_VEC')  

        
        if len(context.selected_objects) == 1:                        
            row = box.row(1) 
            row.alignment = 'CENTER'  

            sub = row.row(1)
            sub.scale_x = 0.6 
            sub.prop(obj, "name", text="", icon = "COPY_ID")

            sub1 = row.row(1)
            sub1.scale_x = 1          
            if lt.display_hops_internal_tools:              
                sub1.prop(lt, "display_hops_internal_tools", text="", icon='MOVE_UP_VEC')
            else:               
                sub1.prop(lt, "display_hops_internal_tools", text="", icon='MOVE_DOWN_VEC')  


        box.separator()
        
        if lt.display_hops_add_am:   

            #if context.window_manager.AssetM_previews:
            if any("asset_management" in s for s in bpy.context.user_preferences.addons.keys()):
                if addon_pref.Asset_Manager_Preview :
                    box = layout.box().column(1)

                    row = box.row(1)
                    row.scale_y = 0.7
                    row.template_icon_view(context.window_manager, "AssetM_previews")
                    
                    row = box.row(1) 
                    row.menu("menu.am_set", icon = "SCRIPTWIN")

                    box.separator()

                else:
                    box.separator()
            else:
                box.separator()


        if lt.display_hops_add:   

            box = layout.box().column(1)       

            row = box.row(1) 
            row.scale_y = 0.7
            row.template_icon_view(context.window_manager , "Hard_Ops_previews")
            row.template_icon_view(context.window_manager, "sup_preview")

            row = box.row(1) 
            props = row.operator("hops.move_assets_preview_selection", icon = "TRIA_LEFT", text = "")
            props.property_name = "Hard_Ops_previews"
            props.move_amount = -1

            row.operator("hops.insert_asset", text = "Insert").asset_name = context.window_manager.Hard_Ops_previews

            props = row.operator("hops.move_assets_preview_selection", icon = "TRIA_RIGHT", text = "")
            props.property_name = "Hard_Ops_previews"
            props.move_amount = 1

            props = row.operator("hops.move_assets_preview_selection", icon = "TRIA_LEFT", text = "")
            props.property_name = "sup_preview"
            props.move_amount = -1

            row.operator("hops.insert_subset", text = "Insert").subset_name = context.window_manager.sup_preview

            props = row.operator("hops.move_assets_preview_selection", icon = "TRIA_RIGHT", text = "")
            props.property_name = "sup_preview"
            props.move_amount = 1

            row = box.row(1) 
            row.operator("view3d.insertpopup", "Asset", icon_value=get_icon_id("HardOps"))
            row.prop(context.window_manager, "choose_primitive", text="", expand=False, icon_value=get_icon_id("Noicon"))        
                     
            box.separator()

            if obj:
                obj_type = obj.type
                
                if obj_type in {'MESH', 'CURVE', 'SURFACE', 'META','FONT'}:

                    row = box.row(1)
                    row.operator("object.to_selection", text="Object To Selection", icon="MOD_MULTIRES")                     

                    row = box.row(1)                                     
                    row.operator("make.link", text = "Link", icon='CONSTRAINT' )                           
                    row.operator("unlink.objects", text = "Unlink", icon='UNLINKED' )                    

                    box.separator()
 
 
        if lt.display_hops_internal_tools:   
            
            box = layout.box().column(1)

            row = box.row(1)                             
            row.alignment = 'CENTER'

            if lt.display_hops_ops:              
                row.prop(lt, "display_hops_ops", text="", icon='EDIT')
            else:               
                row.prop(lt, "display_hops_ops", text="", icon='EDIT')  

            if lt.display_hops_ext:              
                row.prop(lt, "display_hops_ext", text="", icon='MOD_EXPLODE')
            else:               
                row.prop(lt, "display_hops_ext", text="", icon='MOD_EXPLODE')                   

            if lt.display_hops_stk:              
                row.prop(lt, "display_hops_stk", text="", icon='MODIFIER')
            else:               
                row.prop(lt, "display_hops_stk", text="", icon='MODIFIER')                

            if lt.display_hops_opgl:              
                row.prop(lt, "display_hops_opgl", text="", icon='LAMP_SPOT')
            else:               
                row.prop(lt, "display_hops_opgl", text="", icon='LAMP_SPOT')    

            if lt.display_hops_img:              
                row.prop(lt, "display_hops_img", text="", icon='SCENE')
            else:               
                row.prop(lt, "display_hops_img", text="", icon='SCENE')  

            row = box.row(1)  
            row.alignment = 'CENTER'

            if lt.display_hops_gui:              
                row.prop(lt, "display_hops_gui", text="", icon='ZOOM_SELECTED')
            else:               
                row.prop(lt, "display_hops_gui", text="", icon='ZOOM_SELECTED') 

            if lt.display_hops_material:              
                row.prop(lt, "display_hops_material", text="", icon='MATERIAL')
            else:               
                row.prop(lt, "display_hops_material", text="", icon='MATERIAL')   
            
            if lt.display_hops_cycles:              
                row.prop(lt, "display_hops_cycles", text="", icon='NODETREE')
            else:               
                row.prop(lt, "display_hops_cycles", text="", icon='NODETREE')  

            if lt.display_hops_cam:              
                row.prop(lt, "display_hops_cam", text="", icon='CAMERA_DATA')
            else:               
                row.prop(lt, "display_hops_cam", text="", icon='CAMERA_DATA')     
                   
            if lt.display_hops_anim:              
                row.prop(lt, "display_hops_anim", text="", icon='CLIP')
            else:               
                row.prop(lt, "display_hops_anim", text="", icon='CLIP')  



        # Tools
        if len(context.selected_objects) > 0:  

            is_bevel = False
            is_bool = False
            is_bevel_3 = False
            is_solidify = False
            is_multiselected = False
            is_notselected = False
            is_noactiveobject = False
            multislist = bpy.context.selected_objects
            activeobject = bpy.context.scene.objects.active
            is_formerge = False

            if len(multislist) > 1:
                is_multiselected = True
            if len(multislist) < 1:
                is_notselected = True
            if activeobject == None:
                is_noactiveobject = True

            for obj in bpy.context.selected_objects:
                if obj.name.startswith("AP"):
                    is_formerge = True
                    pass

           
            for mode in bpy.context.object.modifiers :
                if mode.type == 'BEVEL' :
                    is_bevel = True
                if mode.type == "BEVEL":
                    if mode.profile > 0.70 and mode.profile < 0.72:
                        is_bevel_3 = True
                if mode.type == 'BOOLEAN' :
                    is_bool = True
                if mode.type == 'SOLIDIFY':
                    is_solidify = True

                   
            box.separator()
            
            if lt.display_hops_ops: 
            
                if obj:
                  
                    obj_type = obj.type                
                                
                    if obj_type in {'MESH'}:

                        box = layout.box().column(1)              
                        row = box.row(1)
                        row.alignment = 'CENTER'
                        row.label('DYNAMIC TOOLS', icon_value=get_icon_id("Noicon"))

                        box.separator()
                        
                        row = box.column(1)
                        object = bpy.context.active_object    
                        if is_multiselected == True:
                            
                            if is_formerge == True:
                                row.operator_context = 'INVOKE_DEFAULT'  
                                row.operator("hops.parent_merge", text = "Merge", icon_value=get_icon_id("Merge"))                                    

                                if any("BoolTool" in s for s in bpy.context.user_preferences.addons.keys()):
                                    row.operator_context = 'INVOKE_DEFAULT'
                                    row.operator("hops.complex_split_boolean", text = "(C)Split", icon_value=get_icon_id("Csplit"))
                                else:
                                    row.operator("none.ops", text = "Install BoolTool to unlock")

                                row.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))
                       
                                #if is_bool == True:
                                    #row.operator_context = 'INVOKE_DEFAULT'
                                    #row.operator("hops.finish_setup", text = "Finish Merge", icon_value=get_icon_id("Merge"))
 
                            else:

                                if is_bevel == False and is_bool == True:
                                    row.operator_context = 'INVOKE_DEFAULT'
                                    row.operator("hops.parent_merge_soft", text = "Merge(soft)", icon_value=get_icon_id("Merge"))
                              
                                if is_bevel == False and is_bool == False:
                                    row.operator_context = 'INVOKE_DEFAULT'
                                    
                                    if object.hops.is_for_softmerge and is_solidify == False:
                                        row.operator("hops.parent_merge_soft", text = "Merge(soft)", icon_value=get_icon_id("Merge"))
                                    else:
                                        row.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))

                                elif is_bevel == True and is_bool == False and object.hops.status != "CSTEP":
                                    row.operator_context = 'INVOKE_DEFAULT'
                                    row.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))

                                elif is_bevel == True and is_bool == False and object.hops.status == "CSTEP":
                                    row.operator_context = 'INVOKE_DEFAULT'
                                    row.operator("step.sstep", text = "(S) Step", icon_value=get_icon_id("Sstep"))
                                        
                                if any("BoolTool" in s for s in bpy.context.user_preferences.addons.keys()):
                                    row.operator_context = 'INVOKE_DEFAULT'
                                    if is_bevel == True and object.hops.status == "CSTEP":
                                        row.operator("step.sstep", text = "(S) Step", icon_value=get_icon_id("Sstep"))

                                    row.operator("hops.complex_split_boolean", text = "(C)Split", icon_value=get_icon_id("Csplit"))
                                else:
                                    row.operator("none.ops", text = "Install BoolTool to unlock")

                                if is_bool == False:
                                    row.operator_context = 'INVOKE_DEFAULT'
                                    row.operator("step.cstep", text = "(C) Step", icon_value=get_icon_id("Cstep"))
                                else:
                                    row.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))                                              

                        #Adjust Bevel                                                
                        row = box.column(1)
                        
                        object = bpy.context.active_object    
                        if is_multiselected == False:

                            if is_bevel == True and is_bool == True and not object.hops.status == "CSTEP":
                                row.operator("hops.soft_sharpen", text = "(S) Sharpen", icon_value=get_icon_id("Ssharpen"))   

                            if is_bevel == True and is_bool == True and object.hops.status == "CSTEP":
                                row.operator_context = 'INVOKE_DEFAULT'
                                row.operator("step.sstep", text = "(S) Step", icon_value=get_icon_id("Sstep"))
                            
                            elif is_bevel == True and is_bool == True and object.hops.status != "CSTEP":
                                row.operator_context = 'INVOKE_DEFAULT'
                                row.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))

                            elif is_bevel == True and is_bool == False and object.hops.status != "CSTEP":
                                row.operator_context = 'INVOKE_DEFAULT'
                                row.operator("hops.soft_sharpen", text = "(S) Sharpen", icon_value=get_icon_id("Ssharpen"))

                            elif is_bevel == True and is_bool == False and object.hops.status == "CSTEP":
                                row.operator_context = 'INVOKE_DEFAULT'
                                row.operator("step.sstep", text = "(S) Step", icon_value=get_icon_id("Sstep"))

                            elif is_bevel == True and is_bool == False and object.hops.status == "CSTEP":
                                row.operator_context = 'INVOKE_DEFAULT'
                                row.operator("step.sstep", text = "(S) Step", icon_value=get_icon_id("Sstep"))


                            if is_bool == False:
                            
                                if is_bevel == True:
                                    row.operator_context = 'INVOKE_DEFAULT'                              
                                    row.operator("hops.adjust_bevel", text = "(B)Width", icon_value=get_icon_id("AdjustBevel"))
                                    row.operator("step.cstep", text = "(C) Step", icon_value=get_icon_id("Cstep"))                                                       
                                
                                else:
                                    row.operator("hops.soft_sharpen", text = "(S) Sharpen", icon_value=get_icon_id("Ssharpen"))                                                                                        
                                    row.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))
                                    row.operator("hops.adjust_tthick", text = "(T)Thick", icon_value=get_icon_id("Tthick"))                        
                               
                            else:
                                row.operator("reverse.boolean", text = "(Re)Bool", icon_value=get_icon_id("ReBool"))
                                row.operator("step.cstep", text = "(C) Step", icon_value=get_icon_id("Cstep"))  
                                

                        box.separator()

                        box = layout.box().column(1)
                        row = box.row(1)
                        row.alignment = 'CENTER'

                        box.separator()

                        if lt.display_hops_operations: 
                            row = box.row(1)                                             
                            row.prop(lt, "display_hops_operations", text="OPERATIONS", icon_value=get_icon_id("Noicon"))
                        else:               
                            
                            row = box.row(1)
                            row.prop(lt, "display_hops_operations", text="Operations", icon_value=get_icon_id("Noicon"))   
                        
                        if lt.display_hops_operations:

                            box.separator()
                            
                            row = box.row(1)                           
                            row.operator("ssharpen.objects", text = "(S)Sharpen", icon_value=get_icon_id("Ssharpen"))
                            row.operator("csharpen.objects", text = "(C)Sharpen", icon_value=get_icon_id("CSharpen"))
                            
                            row = box.row(1)    
                            row.operator("clean.objects", text = "Clear Sharps", icon_value=get_icon_id("ClearSharps"))
                            row.operator("solidify.objects", text = "(T)Sharpen", icon_value=get_icon_id("Tsharpen"))

                            box.separator()
                                             
                            row = box.row(1)
                            row.operator("step.sstep", text = "(S)Step", icon_value=get_icon_id("Sstep")) 
                            row.operator("step.cstep", text = "(C)Step", icon_value=get_icon_id("Cstep"))  
                           
                            row = box.row(1)                            
                            if is_bevel == True and len(context.selected_objects) <= 1:
                                row.prop(obj.modifiers['Bevel'], "segments", icon_value=get_icon_id("CSharpen"))                                  
                            row.operator("hops.adjust_bevel", text = "(B)Width", icon_value=get_icon_id("AdjustBevel"))                                                         
                            
                            box.separator()
                            
                            row = box.row(1)  
                            row.operator("hops.adjust_tthick", text = "(T)Thick", icon_value=get_icon_id("Tthick"))                                              
                            row.operator("nw.a_rray", text = "(Q)Array", icon_value=get_icon_id("Qarray"))   
                        
                            row = box.row(1)                    
                            
                            if len(context.selected_objects) > 1:
                                
                                box.separator()
                                
                                row = box.row(1) 
                                
                                row.operator("multi.sstep", text = "(S)Multi-Step", icon_value=get_icon_id("sstep"))
                                row.operator("multi.cstep", text = "(C)Multi-Step", icon_value=get_icon_id("Cstep"))
                                
                                row = box.row(1)                            
                                row.operator("multi.csharp", text = "(C)Multi", icon_value=get_icon_id("CSharpen"))
                                row.operator("multi.ssharp", text = "(S)Multi", icon_value=get_icon_id("Ssharpen")) 
                                
                                row = box.row(1)
                                row.operator("multi.clear", text = "Multi Clear", icon_value=get_icon_id("ClearSharps"))

                            box.separator()
                                 
                            row = box.row(1)                            
                            row.operator("hops.draw_uv", text = "UV Preview", icon_value=get_icon_id("CUnwrap"))                              
                            
                            box.separator()
                            
                            box = layout.box().column(1)  


                    if obj_type in {'MESH'}:
                        
                        row = box.row(1)                                                    
                        if lt.display_hops_meshtools: 
                            row = box.row(1)                                             
                            row.prop(lt, "display_hops_meshtools", text="MESHTOOLS", icon_value=get_icon_id("Noicon"))
                        else:               
                            row = box.row(1)
                            row.prop(lt, "display_hops_meshtools", text="Meshtools", icon_value=get_icon_id("Noicon"))   

                        if lt.display_hops_meshtools: 

                            box.separator()                             
                                                        
                            row = box.row(1) 
                            if addon_exists("BoxCutter"):
                                row.operator("boxcutter.draw_boolean_layout", text = "BoxCutter", icon_value=get_icon_id("BoxCutter"))
                            else: 
                                #layout.operator.wm.url_open(url="https://gum.co/BoxCutter/iamanoperative")
                                row.operator("wm.url_open", text="Get BoxCutter!", icon_value=get_icon_id("BoxCutter")).url = "https://gum.co/BoxCutter/iamanoperative"

                            box.separator() 
                            
                            row = box.row(1)                                 
                            row.operator("array.twist", text = "ATwist360", icon_value=get_icon_id("ATwist360"))
                            row.operator("halfslap.object", text = "(X+) Sym", icon_value=get_icon_id("Xslap"))                                            

                            row = box.row(1)                                                
                            row.operator("clean.recenter", text = "SC-Recenter", icon_value=get_icon_id("SCleanRecenter"))
                            row.operator("yhalfslap.object", text = "(Y+) Sym", icon_value=get_icon_id("Yslap"))                   

                            row = box.row(1)
                            row.operator("stomp2.object", text = "ApplyAll(-L)", icon_value=get_icon_id("Applyall"))
                            row.operator("zhalfslap.object", text = "(Z+) Sym", icon_value=get_icon_id("Zslap")) 

                            box.separator() 
                            
                            row = box.row(1) 
                            row.operator("hops.xunwrap", text = "(X)Unwrap", icon_value=get_icon_id("PUnwrap"))
                            
                            box.separator() 
                            
                            row = box.row(1)                                          
                            row.operator("object.convert",text="Convert > Curve ", icon = "CURVE_DATA").target="CURVE"
                           
                            box.separator() 

                            box = layout.box().column(1)    


                    if obj_type in {'CURVE'}:

                        box = layout.box().column(1)
                         
                        row = box.row(1)              
                        row.alignment = 'CENTER'
                        row.label("Curve Shape", icon = "MOD_CURVE")    
                        
                        box.separator()
                        
                        row = box.row(1)
                        sub = row.row(1)
                        sub.scale_x = 0.25           
                        sub.prop(context.object.data, "dimensions", expand=True)

                        row = box.row(1)        
                        row.prop(context.object.data, "fill_mode", text="")                                               
                        row.prop(context.object.data, "bevel_depth", text="Bevel")
                         
                        row = box.row(1)
                        row.prop(context.object.data, "resolution_u", text="Ring")          
                        row.prop(context.object.data, "bevel_resolution", text="Loop")

                        row = box.row(1)
                        row.prop(context.object.data, "offset", "Offset")
                        row.prop(context.object.data, "extrude","Height")
                        
                        row = box.row(1) 
                        row.prop(context.object.data, "bevel_factor_start", text="Start") 
                        row.prop(context.object.data, "bevel_factor_end", text="End")  

                        row = box.row(1) 
                        row.prop(context.object.data, "bevel_factor_mapping_start", text="")
                        row.prop(context.object.data, "bevel_factor_mapping_end", text="")     

                        box.separator()                                    
                   
                    if obj_type in {'CURVE', 'SURFACE', 'META', 'FONT'}:
                        
                        box.separator() 
                        
                        row = box.row(1)                                       
                        row.operator("object.convert",text="Convert > Mesh ", icon = "OUTLINER_DATA_MESH").target="MESH"                       
                        
                        box.separator() 

                        box = layout.box().column(1)    

                    if obj_type in {'LATTICE'}:

                        box = layout.box().column(1)
                         
                        row = box.row(1)              
                        row.alignment = 'CENTER'
                        row.label("Lattice Cage", icon = "MOD_LATTICE")    
                     
                        box.separator()
                     
                        row = box.row(1)
                        row.prop(context.object.data, "points_u", text="X")
                        row.prop(context.object.data, "points_v", text="Y")
                        row.prop(context.object.data, "points_w", text="Z")
             
                        row = box.row(1)
                        row.prop(context.object.data, "interpolation_type_u", text="")
                        row.prop(context.object.data, "interpolation_type_v", text="")
                        row.prop(context.object.data, "interpolation_type_w", text="")               

                        box.separator() 
                                                
                        row = box.row(1)                     
                        row.prop(context.object.data, "use_outside")
                        row.prop_search(context.object.data, "vertex_group", context.object, "vertex_groups", text="")   
                       
                        box.separator() 

                        box = layout.box().column(1)                       


                    if obj_type in {'EMPTY'}:#, 'CURVE', 'SURFACE', 'META','FONT'}:

                        box = layout.box().column(1)
                         
                        row = box.row(1)              
                        row.alignment = 'CENTER'
                        row.label("Empty", icon = "OUTLINER_OB_EMPTY")    
                        
                        box.separator()
                        
                        row = box.column(1)

                        row.prop(context.object, "empty_draw_type", text="Display")

                        if context.object.empty_draw_type == 'IMAGE':
                            row.template_ID(context.object, "data", open="image.open", unlink="object.unlink_data")
                            row.template_image(context.object, "data", context.object.image_user, compact=True)

                            row = box.row(1)
                            row.prop(context.object, "color", text="Transparency", index=3, slider=True)
                            
                            row = box.row(1)
                            row.prop(context.object, "empty_image_offset", text="Offset X", index=0)
                            row.prop(context.object, "empty_image_offset", text="Offset Y", index=1)

                        row.prop(context.object, "empty_draw_size", text="Size")

                        box.separator() 

                        box = layout.box().column(1)    


                    if obj_type in {'LAMP'}:    

                        box = layout.box().column(1)
                         
                        row = box.row(1)              
                        row.alignment = 'CENTER'
                        row.label("Lights", icon = "LAMP")    
                        
                        box.separator()
                        
                        if context.object.data.type in {'POINT', 'SUN', 'SPOT', 'HEMI', 'AREA'}:
                          
                           row = box.row(1)
                           row.prop(context.object.data, "type", expand=True)
                          
                           box.separator() 
                         
                           if bpy.context.scene.render.engine == 'CYCLES':
                              lamp = context.object.data
                              clamp = context.object.data.cycles
                              cscene = context.scene.cycles

                              row = box.column(1)
                             
                              if context.object.data.type in {'POINT', 'SUN', 'SPOT'}:
                                  row.prop(context.object.data, "shadow_soft_size", text="Size")
                           
                              elif context.object.data.type == 'AREA':
                                  row.prop(context.object.data, "shape", text="")

                                  if context.object.data.shape == 'SQUARE':
                                      row.prop(context.object.data, "size")
                                
                                  elif context.object.data.shape == 'RECTANGLE':
                                      row.prop(context.object.data, "size", text="Size X")
                                      row.prop(context.object.data, "size_y", text="Size Y")

                              if not (context.object.data.type == 'AREA' and context.object.data.cycles.is_portal):
                                  sub = box.column(1)
                                 
                                  if bpy.context.scene.cycles.progressive == 'BRANCHED_PATH':
                                      sub.prop(context.object.data.cycles, "samples")
                                  sub.prop(context.object.data.cycles, "max_bounces")


                              row = box.column(1)
                              row.active = not (context.object.data.type == 'AREA' and context.object.data.cycles.is_portal)
                              row.prop(context.object.data.cycles, "cast_shadow")
                              row.prop(context.object.data.cycles, "use_multiple_importance_sampling", text="Multiple Importance")

                              if context.object.data.type == 'AREA':
                                  row.prop(context.object.data.cycles, "is_portal", text="Portal")

                              if context.object.data.type == 'HEMI':
                                  row.label(text="Not supported, interpreted as sun lamp")
                              
                              box = layout.box().column(1)  

                              if not panel_node_draw(box, context.object.data, 'OUTPUT_LAMP', 'Surface'):
                                                                   
                                  row = box.column(1)
                                  row.prop(context.object.data, "color")
                                 
                              box.separator() 
                                  
                              if context.object.data.type == 'SPOT':                          

                                box = layout.box().column(1)  
                                 
                                row = box.row(1)
                                row.alignment = "CENTER"
                                row.label("Spot Shape", icon ="MESH_CONE")               
                                 
                                row = box.row(1) 
                                          
                                row = box.column(1)
                                row.prop(context.object.data, "spot_size", text="Size")
                                row.prop(context.object.data, "spot_blend", text="Blend", slider=True)

                                row.prop(context.object.data, "show_cone")
  
                           else:
                                row = box.column(1)
                                row.label("Use Cycles render for Setting!", icon = "RADIO")  


                        box.separator() 
                        box = layout.box().column(1)       

            
            #############################
            # Shading
            
            row = box.row(1)                  
            if lt.display_hops_gui:

                row = box.row(1)                                                    
                if lt.display_hops_guiobj:
                    row = box.row(1)              
                    row.prop(lt, "display_hops_guiobj", text="SHADING", icon_value=get_icon_id("Noicon"))
                else:
                    row = box.row(1)               
                    row.prop(lt, "display_hops_guiobj", text="Shading", icon_value=get_icon_id("Noicon")) 
               
                if lt.display_hops_guiobj:    
                    
                    if not obj_type in {'LATTICE'}:
                        box.separator() 

                        row = box.row(1)
                 
                        if context.object.draw_type == 'WIRE':
                            row.operator("object.solid_all", text="Solid Mode", icon='MESH_CUBE')
                        else:
                            row.operator("showwire.objects", text = "Wire Mode", icon='OUTLINER_OB_LATTICE') 

                        active_wire = bpy.context.object.show_wire 
                        if active_wire == True:
                            row.operator("object.wire_off", text="Show Overlays", icon='RESTRICT_VIEW_ON')             
                        else:                       
                            row.operator("object.wire_on", text="Hide Overlays", icon='RESTRICT_VIEW_OFF')   

                        box.separator()

                        row = box.row(1) 
                        m_check = context.window_manager.m_check
                        if bpy.context.object and bpy.context.object.type == 'MESH':
                        
                            if m_check.meshcheck_enabled:
                                row.operator("object.remove_materials", text="Hide Ngons/Tris", icon='RESTRICT_VIEW_OFF')
                            else:
                                row.operator("object.add_materials", text="Display Ngons/Tris", icon_value=get_icon_id("ShowNgonsTris")) 
                    
                        row = box.row(1) 
                        row.operator("data.facetype_select", text="Ngons", icon_value=get_icon_id("Ngons")).face_type = "5"
                        row.operator("data.facetype_select", text="Tris", icon_value=get_icon_id("Tris")).face_type = "3"

                        box.separator()

                        row = box.row(1) 
                        row.prop(context.active_object.data, "use_auto_smooth",icon="AUTO")
                        row.operator("object.shade_flat", text="Flat", icon="MESH_CIRCLE") 
                                                             
                        row = box.row(1)
                        sub = row.row(1)
                        sub.active = context.active_object.data.use_auto_smooth
                        sub.prop(context.active_object.data, "auto_smooth_angle", text="Angle")  
                        row.operator("object.shade_smooth", text="Smooth", icon="SOLID")                  

                    box.separator()
                       
                    if context.active_object:                
                        row = box.row(1)
                        active_xray = bpy.context.object.show_x_ray 
                        if active_xray == True:
                            row.operator("view3d.xray_off", text="X-Ray", icon="META_CUBE")
                        else:
                            row.operator("view3d.xray_on", text="X-Ray", icon="META_PLANE")

                        row.prop(context.space_data, "show_backface_culling", text="Backface", icon="MOD_LATTICE")
                    else:
                        box.separator()
                        
                        box.label('No object selected as active', icon ="ERROR")    
                    
                    box.separator()
                                        
                    box = layout.box().column(1)                                           


                #############################
                # Display
                
                if lt.display_hops_guidpy:
                    row = box.row(1)              
                    row.prop(lt, "display_hops_guidpy", text="DISPLAY", icon_value=get_icon_id("Noicon"))
                else:
                    row = box.row(1)               
                    row.prop(lt, "display_hops_guidpy", text="Display", icon_value=get_icon_id("Noicon"))   

                if lt.display_hops_guidpy:  
                    
                    box.separator() 

                    row = box.row(1)
                    row.operator("ui.reg", text = "Normal", icon_value=get_icon_id("NGui"))
                    row.operator("ui.red", text = "Red Mode", icon_value=get_icon_id("RGui"))
                    
                    row = box.row(1)            
                    row.operator("ui.clean", text = "Quiet", icon_value=get_icon_id("QGui"))

                    box.separator()

                    row = box.row(1) 
                    row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="MESH_UVSPHERE")
                    row.prop(context.space_data, "use_matcap", icon_value=get_icon_id("RGui"))

                    if context.space_data.fx_settings.use_ssao:
                        row = box.row(1)
                        row.prop(context.space_data.fx_settings.ssao, "color","")
                        row.prop(context.space_data.fx_settings.ssao, "factor")
                        
                        row = box.row(1)
                        row.prop(context.space_data.fx_settings.ssao, "distance_max")
                        row.prop(context.space_data.fx_settings.ssao, "attenuation")
                        row.prop(context.space_data.fx_settings.ssao, "samples")

                        box.separator()
                        
                    if context.space_data.use_matcap:
                        row = box.row(1)
                        row.scale_y = 0.2
                        row.scale_x = 0.5
                        row.template_icon_view(context.space_data, "matcap_icon") 

                        box.separator()

                    row = box.row(1)
                    row.prop(context.space_data, "show_world", "World", icon="WORLD")
                    
                    sub = row.row(1)
                    sub.scale_x = 0.25
                    sub.prop(context.space_data, "show_floor", text=" ", icon ="GRID") 
                    sub.prop(context.space_data, "show_axis_x", text="X", toggle=True)
                    sub.prop(context.space_data, "show_axis_y", text="Y", toggle=True)
                    sub.prop(context.space_data, "show_axis_z", text="Z", toggle=True)                    

                    if context.space_data.show_world:
                        row = box.row(1)
                        row.prop(context.scene.world, "horizon_color", "")
                        
                        row = box.row(1)
                        row.prop(context.scene.world, "exposure")
                        row.prop(context.scene.world, "color_range")
                    
                    box.separator()
                                        
                    box = layout.box().column(1)                                            


            #############################
            # Xtras
            
            row = box.row(1)             
            if lt.display_hops_ext: 
                
                if lt.display_hops_xtras:  
                                
                    row.prop(lt, "display_hops_xtras", text="XTRAS", icon_value=get_icon_id("Noicon"))
                    row = box.row(1)
                else:               
                    row = box.row(1)
                    row.prop(lt, "display_hops_xtras", text="Xtras", icon_value=get_icon_id("Noicon"))   
               
                if lt.display_hops_xtras: 
                    
                    box.separator()   
                                                       
                    row = box.row(1)                                     
                    row.operator("view3d.addoncheckerpopup", text = "Diagnostic", icon="SCRIPTPLUGINS")  
                    row.operator("view3d.pizzapopup", text = "Pizza Ops", icon_value=get_icon_id("Pizzaops")) 
                    
                    box.separator()                   

                    row = box.row(1)   
                        
                    if any("AutoMirror" in s for s in bpy.context.user_preferences.addons.keys()):
                        row.operator("view3d.mirrorhelper", text = "Mirror Helper", icon_value=get_icon_id("Xslap"))

                    if any("Lattice" in s for s in bpy.context.user_preferences.addons.keys()):
                        row.operator("object.easy_lattice", text = "Easy Lattice", icon_value=get_icon_id("MHelper"))

                    if any("relink" in s for s in bpy.context.user_preferences.addons.keys()):
                        layout.menu("relink_menu", text = "ReLink")
                
                    box.separator()  

                    row = box.row(1)
                    row.operator("view3d.hops_helper_popup", text = "(H) Mod", icon="SCRIPTPLUGINS")                

                    box.separator() 
                    
                    box = layout.box().column(1)                     
                    

            #############################
            # Material
            
            if lt.display_hops_material: 
                
                row = box.row(1)
                if lt.display_hops_mat:
                    row = box.row(1)              
                    row.prop(lt, "display_hops_mat", text="MATERIALS", icon_value=get_icon_id("Noicon"))
                else:
                    row = box.row(1)               
                    row.prop(lt, "display_hops_mat", text="Materials", icon_value=get_icon_id("Noicon"))   

                if lt.display_hops_mat:

                    box.separator()                                      
                                    
                    if len(context.selected_objects) >= 1:

                        row = box.row(1)
                        row.operator("material.simplify", text="", icon="SPACE3")                               
                        row.menu("object.material_list_menu", text="Apply...", icon="NLA_PUSHDOWN")                                               
                        row.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")        
                        
                        box.separator()   
                                                
                        row = box.row()                
                        row.template_list("MATERIAL_UL_matslots", "", context.object, "material_slots", context.object, "active_material_index", rows=3)             
                       
                        split = row.split(1)
                        row = split.column(1)
                        row.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
                        row.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
                        row.operator("purge.unused_material_data", text="", icon="PANEL_CLOSE") 

                        if lt.display_mat_edit:                                                      
                          row.prop(lt, "display_mat_edit", text="", icon='MOVE_DOWN_VEC')
                        else: 
                          row.prop(lt, "display_mat_edit", text="", icon='MOVE_UP_VEC')     

                        box.separator()

                        if lt.display_mat_edit:  
                                       
                            if bpy.context.scene.render.engine == 'CYCLES':

                                obj = context.active_object  
                                if obj:
                                    obj_type = obj.type

                                    if obj.type in {'MESH','FONT','META','CURVE', 'SURFACE'}:

                                       box = layout.box().column(1) 

                                       row = box.row(1)              
                                       row.alignment = 'CENTER'
                                       row.label("___Cycles Material Properties___")

                                       box.separator()

                                       row = box.row(1)                        
                                       row.template_ID(context.object, "active_material", new="material.new")
                                       
                                       if len(context.object.material_slots) >= 0:                                        

                                           box.separator()

                                           row = box.row(1)                        
                                           row.prop(context.object.active_material, "use_nodes", icon='NODETREE') 
                                           if context.object.material_slots[context.object.active_material_index]:
                                               row.prop(context.object.material_slots[context.object.active_material_index], "link", text="")  
                                           else:
                                               row.label()
                                                                  
                                           row = box.row(1)                         
                                           row.template_ID(context.space_data, "pin_id")

                                           row = box.row(1)  

                                           if context.object.active_material.use_nodes:
                                               row = box.row()
                                                                             
                                               if context.object.active_material.active_node_material:
                                                   row.prop(context.object.active_material.active_node_material, "name", text="")   

                                               else:
                                                   box.separator()
                                                   
                                                   row = box.row(1)
                                                   row.alignment = 'CENTER'
                                                   row.label(text="Material Nodes active!")

                                                   box = layout.box().column(1) 

                                                   row = box.column(1)    
                                                   mat = bpy.context.object.material_slots[0].material
                                                   if not panel_node_draw(box, mat, 'OUTPUT_MATERIAL', 'Surface'):
                                                       row.prop(mat, "diffuse_color")
                                               
                                                   box.separator()

                                                   box = layout.box().column(1) 

                                                   row = box.column(1)  
                                                   mat = bpy.context.object.material_slots[0].material
                                                   panel_node_draw(box, mat, 'OUTPUT_MATERIAL', 'Volume')
                                                  
                                                   box.separator()

                                                   box = layout.box().column(1) 

                                                   row = box.column(1)
                                                   mat = bpy.context.object.material_slots[0].material  
                                                   panel_node_draw(box, mat, 'OUTPUT_MATERIAL', 'Displacement') 
                 
                                                   box.separator()

                                           else:
                                               box.separator()
                                                                       
                                               row = box.row(1)  
                                               row.prop(context.object.active_material, "diffuse_color")                                     

                                               box.separator()


                                           box = layout.box().column(1) 

                                           row = box.row(1)
                                           row.label(text="Cycle Settings:")
                                           
                                           box.separator() 
                                           box.separator() 

                                           row = box.row(1)
                                           row.label(text="Surface:")
                                          
                                           row = box.column(1)
                                           row.prop(context.object.active_material.cycles, "sample_as_light", text="Multiple Importance")
                                           row.prop(context.object.active_material.cycles, "use_transparent_shadow")

                                           box.separator() 
                                           box.separator() 
                                            
                                           row = box.row(1)
                                           row.label(text="Volume:")
                                           
                                           row = box.row(1)
                                           #sub.active = use_cpu(context)
                                           row.prop(context.object.active_material.cycles, "volume_sampling", text="")
                                           row.prop(context.object.active_material.cycles, "volume_interpolation", text="")              
                                          
                                           row = box.row(1)               
                                           row.prop(context.object.active_material.cycles, "homogeneous_volume", text="Homogeneous")
                                         
                                           box.separator()                                 
                                           box.separator() 
                                            
                                           row = box.row(1)
                                           row.label("Viewport Color:")
                                           row.label("Viewport Alpha:")
                                                          
                                           row = box.row(1)               
                                           row.prop(context.object.active_material, "diffuse_color", text="")
                                           row.prop(context.object.active_material, "specular_color", text="")
                                         
                                           row = box.row(1)                   
                                           row.prop(context.object.active_material, "alpha")
                                           row.prop(context.object.active_material, "specular_hardness", text="Hardness")
                                         
                                           box.separator() 
                                           box.separator() 
                                            
                                           row = box.row(1)                                                                      
                                           row.prop(context.object.active_material, "pass_index")   
                                          
                                           box.separator()                                          
                                           
                                           row = box.column(1)
                                           row.label("Viewport Specular:")  
                                           row.prop(context.object.active_material.game_settings, "alpha_blend", text="")                                                         

                            else:
                                box = layout.box().column(1)       
                                
                                row = box.row(1)                                                      
                                row.label(text="Use Cycles Render for Settings!", icon = "RADIO")
                                
                    
                    box.separator()                     
                    box = layout.box().column(1)  

            #############################
            # Cycles Settings

            if lt.display_hops_cycles: 
                
                row = box.row(1)
                if lt.display_hops_cyc:              
                    row.prop(lt, "display_hops_cyc", text="CYCLESRENDER", icon_value=get_icon_id("Noicon"))
                else:               
                    row.prop(lt, "display_hops_cyc", text="CyclesRender", icon_value=get_icon_id("Noicon"))  

                if lt.display_hops_cyc: 
                    
                    box.separator()              
                                    
                    row = box.row(1)
                    row.operator("render.setup", text = "Render(1)", icon="RESTRICT_RENDER_OFF")
                    row.operator("renderb.setup", text = "Render(2)", icon="RESTRICT_RENDER_OFF")
                   
                    row = box.row(1)
                    row.prop(context.scene.cycles, "preview_samples")
                                        
                    box.separator()

                    row = box.row(1)
                    row.operator("setframe.end", text =  "Set FrameEnd", icon_value=get_icon_id("SetFrame")) 
                    
                    row = box.row(1)
                    row.prop(context.scene, 'frame_start')            		
                    row.prop(context.scene, 'frame_end')

                    box.separator()




            #############################
            # Stack Tools
            
            if lt.display_hops_stk:                            

                box.separator()  
                
                box = layout.box().column(1)                                                   

                row = box.row(1)
                
                if lt.display_hops_mod:                       
                     row.prop(lt, "display_hops_mod", text="MODSTACK", icon_value=get_icon_id("Noicon"))                             
                else:            
                     row.prop(lt, "display_hops_mod", text="ModStack", icon_value=get_icon_id("Noicon"))

                if lt.display_hops_con:                       
                     row.prop(lt, "display_hops_con", text="CONSTACK", icon_value=get_icon_id("Noicon"))                             
                else:            
                     row.prop(lt, "display_hops_con", text="ConStack", icon_value=get_icon_id("Noicon"))
                       
                box.separator()


                # Modifiers
                if lt.display_hops_mod: 
                
                    box = layout.box().column(1)                                      
                    
                    row = box.row(1)
                    row.alignment = 'CENTER'                                        
                    row.label('MODIFIER STACK', icon_value=get_icon_id("Noicon"))
                    
                    box.separator()                             

                    row = box.row(1)
                    row.scale_y = 1.5

                    row.operator_menu_enum("object.modifier_add", "type", text ="Modifier", icon ="NLA_PUSHDOWN")
                    row.menu("hrdops_booltool", text ="Boolean", icon ="NLA_PUSHDOWN")

                    mod_list = context.active_object.modifiers
                                  
                    if mod_list:
                                              
                        for mod in mod_list: 
                            if("BTool_" in mod.name):
                                row = box.row(1)                                                                       
                                
                                Rem = row.operator("btool.remove", icon = "CANCEL", text="Remove BT")                    
                                Rem.thisObj = ""
                                Rem.Prop = "CANVAS"   
                                
                                row.operator("btool.to_mesh", icon = "MOD_LATTICE", text="Apply BT")

                        box.separator()                                                                                                         
                    
                    if not mod_list:
                        box.separator()  
                        
                        row = box.row(1) 
                        box.label('No modifier active', icon ="LAMP_DATA") 

                    else:                                                   
                        mod_list = context.active_object.modifiers

                        for mod in mod_list:                                                                                                             
                            
                            #icon = ""
                            #mod.object.name
                            if("BTool_" in mod.name):
                                
                                box = layout.box().column(1)                       
                                row = box.row(1)  

                                if(mod.operation == "UNION"):
                                    icon ="ROTATECOLLECTION"
                                if(mod.operation == "DIFFERENCE"):
                                    icon ="ROTACTIVE"
                                if(mod.operation == "INTERSECT"):
                                    icon ="ROTATECENTER"

                                objSelect = row.operator("btool.find_brush",text=mod.object.name, icon = icon, emboss = False)
                                objSelect.obj = mod.object.name
                                
                                EnableIcon = "RESTRICT_VIEW_ON"
                                if (mod.show_viewport):                                    
                                    EnableIcon = "RESTRICT_VIEW_OFF"
                                Enable = row.operator("btool.enable_brush", icon=EnableIcon,emboss = False)
                                Enable.thisObj = mod.object.name
                                
                                Remove = row.operator("btool.remove", icon="CANCEL",emboss = False)
                                Remove.thisObj = mod.object.name
                                Remove.Prop = "THIS"
                                
                                #Stack Changer
                                Up = row.operator("btool.move_stack",icon ="TRIA_UP",emboss = False)
                                Up.modif = mod.name
                                Up.direction = "UP"
                                
                                Dw = row.operator("btool.move_stack",icon ="TRIA_DOWN",emboss = False)
                                Dw.modif = mod.name
                                Dw.direction = "DOWN"                            

                    # modifier stack   
                    for md in context.active_object.modifiers: 
                        box = layout.box().column(1)                                                                                                 

                        row = box.row(1)                                                                             
                        row.template_modifier(md)                    

                    box = layout.box().column(1)      
                                     
                    row = box.row(1)  
                    row.operator("hops.expand_mod","Exp", icon = 'TRIA_DOWN_BAR')
                    row.operator("hops.collapse_mod","Col", icon = 'TRIA_RIGHT_BAR')   
                    row.operator("hops.remove_mod","Rem", icon = 'X')
                    row.operator("hops.apply_mod","Set",  icon = 'FILE_TICK')     

                    box.separator()


                # Constraints
                if lt.display_hops_con: 
                
                    box = layout.box().column(1)                                      
                    
                    row = box.row(1)
                    row.alignment = 'CENTER'
                    
                    row.label('CONSTRAINTS', icon_value=get_icon_id("Noicon"))
                    
                    box.separator()
                   
                    row = box.row(1)
                    row.scale_y = 1.5              
                    row.operator_menu_enum("object.constraint_add", "type", text="Constraint", icon ="NLA_PUSHDOWN")                

                    box.separator()  

                    con_list = context.active_object.constraints
                    
                    if con_list:
                     
                        for con in con_list:
                            box = layout.box().column(1)                                                                                              
                            
                            row = box.column(1)   
                            row.template_constraint(con)  

                    else: 
                        box.separator()  
                        
                        row = box.row(1)
                        row.label('No contraints active', icon ="ERROR")
                        
                        box.separator()  

                    box = layout.box().column(1)      
                                     
                    row = box.row(1)  
                    row.operator("hops.expand_con","Exp", icon = 'TRIA_DOWN_BAR')
                    row.operator("hops.collapse_con","Col", icon = 'TRIA_RIGHT_BAR')    

                    box.separator()



            #############################
            # OpenGL
            
            if lt.display_hops_opgl: 

                box.separator()  

                box = layout.box().column(1)   

                row = box.row(1)              

                row = box.row(1)              
                row.alignment = 'CENTER'
                row.label("OPENGL", icon_value=get_icon_id("Noicon"))  

                box.separator()                

                row = box.row(1)
                row.prop(context.space_data, "show_textured_solid","Enable Textured Solid", icon_value=get_icon_id("Noicon"))        
                  
                box.separator()              
                             
                system = bpy.context.user_preferences.system
                
                def opengl_lamp_buttons(column, lamp):
                   
                    split = column.split(percentage=0.1)
                    split.prop(lamp, "use", text="", icon='OUTLINER_OB_LAMP' if lamp.use else 'LAMP_DATA')
                    
                    col = split.column()
                    col.active = lamp.use
                    
                    row = col.row()
                    row.label(text="Diffuse:")
                    row.prop(lamp, "diffuse_color", text="")
                    
                    row = col.row()
                    row.label(text="Specular:")
                    row.prop(lamp, "specular_color", text="")
                    
                    col = split.column()           
                    col.active = lamp.use
                    col.prop(lamp, "direction", text="")
                
                row = box.row(1) 

                box.separator()   
                
                column = box.column()
                
                split = column.split(percentage=0.1)
                split.label()
                split.label(text="Colors:")
                split.label(text="Direction:")
                
                lamp = system.solid_lights[0]
                opengl_lamp_buttons(column, lamp)
                
                lamp = system.solid_lights[1]
                opengl_lamp_buttons(column, lamp)
                
                lamp = system.solid_lights[2]
                opengl_lamp_buttons(column, lamp)
                
                box.separator()   

                row = box.row(1)  
                row.menu("VIEW3D_MT_opengl_lights_presets", text=bpy.types.VIEW3D_MT_opengl_lights_presets.bl_label, icon = "COLLAPSEMENU")
                row.operator("scene.opengl_lights_preset_add", text="", icon='ZOOMIN')
                row.operator("scene.opengl_lights_preset_add", text="", icon='ZOOMOUT').remove_active = True
                
                box.separator()   


            #############################
            # Camera
            
            if lt.display_hops_cam: 
                
                box.separator()  
                
                box = layout.box().column(1)             

                row = box.row(1)
                row.alignment = 'CENTER'                                
                row.label('CAMERA', icon_value=get_icon_id("Noicon"))
                    
                box.separator()

                row = box.row(1)                 
                row.operator("object.camera_add")
                row.operator("camera.tp_set")         

                box.separator()
                
                box = layout.box().column(1) 

                row = box.row(1)          
                row.operator("view3d.viewnumpad", text="Active Cam").type = 'CAMERA'  
                row.operator("view3d.object_as_camera", "Obj as Cam")

                row = box.row(1)     
                row.operator("view3d.camera_to_view", text="C-View")
                row.operator("view3d.camera_to_view_selected", text="C-View Selected")		

                box.separator()
                                
                obj = context.active_object
                if obj:
                    obj_type = obj.type
                    
                    if obj.type in {'CAMERA'}:            
                        box = layout.box().column(1) 

                        row = box.row(1)              
                        row.alignment = 'CENTER'
                        row.label("CAMERA DATA", icon_value=get_icon_id("Noicon"))

                        box.separator()

                        row = box.row(1)   

                        if lt.display_cam_display:                       
                             row.prop(lt, "display_cam_display", text="DISPLAY", icon='RENDER_REGION')                             
                        else:            
                             row.prop(lt, "display_cam_display", text="DISPLAY", icon='RENDER_REGION')   

                        if lt.display_cam_lens:                       
                             row.prop(lt, "display_cam_lens", text="LENS", icon='PROP_ON')                             
                        else:            
                             row.prop(lt, "display_cam_lens", text="LENS", icon='PROP_ON')                   

                        if lt.display_cam_sphere:                       
                             row.prop(lt, "display_cam_sphere", text="DOF", icon='WORLD')                             
                        else:            
                             row.prop(lt, "display_cam_sphere", text="DOF", icon='WORLD')   

                        if lt.display_cam_save:                       
                             row.prop(lt, "display_cam_save", text="AREAS", icon='BORDER_RECT')                             
                        else:            
                             row.prop(lt, "display_cam_save", text="AREAS", icon='BORDER_RECT')  

                             
                        box.separator()
                        
                        box = layout.box().column(1)             
                              
                        row = box.column(1)    
                        row.prop(context.space_data, "lock_camera")                                                               
                        row.prop(context.object.data, "draw_size", text="Size")                          
                        row = box.row(1)  
                        row.prop(context.object, 'location', text="")

                        box.separator()  
                            
                        if lt.display_cam_display:
                            box = layout.box().column(1) 

                            row = box.row(1)              
                            row.alignment = 'CENTER'
                            row.label("Composition Guides")

                            box.separator()

                            row = box.column_flow(2)       
                            row.prop(context.object.data, "show_guide", text="Composition guides")           
                            row.prop(context.object.data, "show_limits", text="Limits")
                            row.prop(context.object.data, "show_mist", text="Mist")
                            row.prop(context.object.data, "show_sensor", text="Sensor")
                            row.prop(context.object.data, "show_name", text="Name")      
                            row.prop(context.object.data, "show_passepartout", text="Passepartout")                          
                            row.prop(context.object.data, "passepartout_alpha", text="Alpha", slider=True)

                            box.separator()
                        
                        # Camera Lens           
                        if lt.display_cam_lens:
                            box = layout.box().column(1) 

                            row = box.row(1)              
                            row.alignment = 'CENTER'
                            row.label("Lens & Presets")

                            box.separator()

                            row = box.row(1)                         
                            row.prop(context.object.data, "type", expand=True)

                        
                            box.separator()
                                                  
                            row = box.row(1) 
                            if context.object.data.type == 'PERSP':
                              
                                if context.object.data.lens_unit == 'MILLIMETERS':
                                    row.prop(context.object.data, "lens")
                              
                                elif context.object.data.lens_unit == 'FOV':
                                    row.prop(context.object.data, "angle")
                                    
                                row.prop(context.object.data, "lens_unit", text="")

                            elif context.object.data.type == 'ORTHO':
                                row.prop(context.object.data, "ortho_scale")

                            elif context.object.data.type == 'PANO':
                                
                                if  context.scene.render.engine == 'CYCLES':

                                    row.prop(context.object.data.cycles, "panorama_type", text="Type")
                                   
                                    if context.object.data.cycles.panorama_type == 'FISHEYE_EQUIDISTANT':
                                        row.prop(context.object.data.cycles, "fisheye_fov")
                                   
                                    elif context.object.data.cycles.panorama_type == 'FISHEYE_EQUISOLID':
                                        
                                        row = box.row()
                                        row.prop(context.object.data.cycles, "fisheye_lens", text="Lens")
                                        row.prop(context.object.data.cycles, "fisheye_fov")
                                  
                                    elif context.object.data.cycles.panorama_type == 'EQUIRECTANGULAR':
                                    
                                        row = box.row()
                                      
                                        sub = row.column(1)
                                        sub.prop(context.object.data.cycles, "latitude_min")
                                        sub.prop(context.object.data.cycles, "latitude_max")
                                      
                                        sub = row.column(1)
                                        sub.prop(context.object.data.cycles, "longitude_min")
                                        sub.prop(context.object.data.cycles, "longitude_max")
                                
                                elif context.scene.render.engine == 'BLENDER_RENDER':
                                    row = box.row()
                                 
                                    if context.object.data.lens_unit == 'MILLIMETERS':
                                        row.prop(context.object.data, "lens")
                                 
                                    elif context.object.data.lens_unit == 'FOV':
                                        row.prop(context.object.data, "angle")
                                  
                                    row.prop(context.object.data, "lens_unit", text="")

                            split = box.split()

                            col = split.column(align=True)
                            col.label(text="Shift:")
                            col.prop(context.object.data, "shift_x", text="X")
                            col.prop(context.object.data, "shift_y", text="Y")

                            col = split.column(align=True)
                            col.label(text="Clipping:")
                            col.prop(context.object.data, "clip_start", text="Start")
                            col.prop(context.object.data, "clip_end", text="End")
                                                                    
                            box = layout.box().column(1) 

                            row = box.row(1)  
                            row.menu("CAMERA_MT_presets", text=bpy.types.CAMERA_MT_presets.bl_label)
                            row.operator("camera.preset_add", text="", icon='ZOOMIN')
                            row.operator("camera.preset_add", text="", icon='ZOOMOUT').remove_active = True

                            box.label(text="Sensor:")

                            split = box.split()

                            col = split.column(align=True)
                            if context.object.data.sensor_fit == 'AUTO':
                                col.prop(context.object.data, "sensor_width", text="Size")
                            
                            else:
                                sub = col.column(align=True)
                                sub.active = context.object.data.sensor_fit == 'HORIZONTAL'
                                sub.prop(context.object.data, "sensor_width", text="Width")
                                sub = col.column(align=True)
                                sub.active = context.object.data.sensor_fit == 'VERTICAL'
                                sub.prop(context.object.data, "sensor_height", text="Height")

                            col = split.column(align=True)
                            col.prop(context.object.data, "sensor_fit", text="")
                            
                            box.separator

                        # Depth of Field
                        if lt.display_cam_sphere: 
                            box = layout.box().column(1) 

                            row = box.row(1)              
                            row.alignment = 'CENTER'
                            row.label("Dept of Field")

                            box.separator()

                            row = box.row(1) 
                            row.prop(context.space_data.fx_settings, "use_dof", "Enable")

                            row = box.row(1) 
                            split = box.split()

                            col = split.column()
                            col.label(text="Focus:")
                            col.prop(context.object.data, "dof_object", text="")
                           
                            sub = col.column()
                            sub.active = (context.object.data.dof_object is None)
                            sub.prop(context.object.data, "dof_distance", text="Distance")

                            hq_support = context.object.data.gpu_dof.is_hq_supported
                           
                            row = box.row(1)                           
                           
                            sub = col.column()
                            sub.label("Viewport:")
                            sub.active = hq_support
                            sub.prop(context.object.data.gpu_dof, "use_high_quality")
                            col.prop(context.object.data.gpu_dof, "fstop")
                           
                            if context.object.data.gpu_dof.use_high_quality and hq_support:
                                col.prop(context.object.data.gpu_dof, "blades")

                            box.separator()
                            
                        # Safe Areas
                        if lt.display_cam_save:  
                            box = layout.box().column(1) 

                            row = box.row(1)              
                            row.alignment = 'CENTER'
                            row.label("Safe Areas")

                            box.separator()
                                                    
                            row = box.row(1)
                            row.prop(context.object.data, "show_safe_areas", text="Enable")
                             
                            row = box.row(1) 
                            row.menu("SAFE_AREAS_MT_presets", text=bpy.types.SAFE_AREAS_MT_presets.bl_label)
                            row.operator("safe_areas.preset_add", text="", icon='ZOOMIN')

                            row.operator("safe_areas.preset_add", text="", icon='ZOOMOUT').remove_active = True
                            
                            row = box.row(1) 
                            row.prop(context.object.data, "show_safe_center", text="Center-Cut Safe Areas")

                            split = box.split()
                            col = split.column()

                            col.prop(context.scene.safe_areas, "title", slider=True)
                            col.prop(context.scene.safe_areas, "action", slider=True)

                            col = split.column()
                            col.prop(context.scene.safe_areas, "title_center", slider=True)
                            col.prop(context.scene.safe_areas, "action_center", slider=True)

                            box.separator()


            #############################
            # Image Render
            
            if lt.display_hops_img: 

                box.separator()  

                box = layout.box().column(1)   

                row = box.row(1)           
                row.alignment = 'CENTER'
                row.label("IMAGE RENDER", icon_value=get_icon_id("Noicon"))    
                  
                box.separator()

                row = box.row(1)               
                row.scale_y = 3
                row.operator("render.render", text="Render#")
                row.operator("render.opengl", text="OpenGL#")

                row = box.row(1)
                row.prop(context.scene.render, "display_mode", text="")                                                                 
                row.menu("INFO_MT_opengl_render", "OpenGl Opt.")                 
                
                box.separator()
                 
                row = box.row(1)
                if lt.display_img_dim:                       
                     row.prop(lt, "display_img_dim", text="Size", icon='MAN_SCALE')                             
                else:            
                     row.prop(lt, "display_img_dim", text="Size", icon='MAN_SCALE')   

                if lt.display_img_pfc:                       
                     row.prop(lt, "display_img_pfc", text="Power", icon='GRID')                             
                else:            
                     row.prop(lt, "display_img_pfc", text="Power", icon='GRID')

                if lt.display_img_color:                       
                     row.prop(lt, "display_img_color", text="Color", icon='COLOR')                             
                else:            
                     row.prop(lt, "display_img_color", text="Color", icon='COLOR')

                box.separator()
                
                # Performance
                if lt.display_img_pfc:  

                    box = layout.box().column(1)   

                    row = box.row(1)           
                    row.alignment = 'CENTER'
                    row.label("Performance", icon='GRID')    
                      
                    box.separator()

                    row = box.row(1)    
                    split = box.split()

                    col = split.column(align=True)
                    col.label(text="Threads:")
                    col.row(align=True).prop(context.scene.render, "threads_mode", expand=True)
                    sub = col.column(align=True)
                    sub.enabled = context.scene.render.threads_mode == 'FIXED'
                    sub.prop(context.scene.render, "threads")

                    col.label(text="Tile Size:")
                    col.prop(context.scene.render, "tile_x", text="X")
                    col.prop(context.scene.render, "tile_y", text="Y")

                    col.separator()
                    col.prop(context.scene.render, "preview_start_resolution")

                    col = split.column()
                    col.label(text="Memory:")
                    sub = col.column()
                    sub.enabled = not (context.scene.render.use_border or context.scene.render.use_full_sample)
                    sub.prop(context.scene.render, "use_save_buffers")
                    sub = col.column()
                    sub.active = context.scene.render.use_compositing
                    sub.prop(context.scene.render, "use_free_image_textures")
                    sub.prop(context.scene.render, "use_free_unused_nodes")
                    sub = col.column()
                    sub.active = context.scene.render.use_raytrace
                    sub.label(text="Acceleration structure:")
                    sub.prop(context.scene.render, "raytrace_method", text="")
                    if context.scene.render.raytrace_method == 'OCTREE':
                        sub.prop(context.scene.render, "octree_resolution", text="Resolution")
                    else:
                        sub.prop(context.scene.render, "use_instances", text="Instances")
                    sub.prop(context.scene.render, "use_local_coords", text="Local Coordinates")

                    box.separator()

                # Dimension
                if lt.display_img_dim:  

                    box = layout.box().column(1)   

                    row = box.row(1)           
                    row.alignment = 'CENTER'
                    row.label("Dimensions", icon='MAN_SCALE')    
                      
                    box.separator()

                    row = box.row(1)                 
                    row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
                    row.operator("render.preset_add", text="", icon='ZOOMIN')
                    row.operator("render.preset_add", text="", icon='ZOOMOUT').remove_active = True
                    
                    box.separator()
                   
                    row = box.row(1)               
                    row.prop(context.scene, "Render_Setup", text="")
                    row.operator("object.instances_res_apply", text="Apply Resolution")

                    row = box.row(1)
                    row.label(text="Resolution:")
                    
                    row = box.row(1)                  
                    row.prop(context.scene.render, "resolution_x", text="X")
                    row.prop(context.scene.render, "resolution_y", text="Y")
                 
                    row = box.row(1)
                    row.prop(context.scene.render, "resolution_percentage", text="")

                    box.separator()

                    row = box.row(1)
                    row.label(text="Aspect Ratio:")

                    row = box.row(1)
                    row.prop(context.scene.render, "pixel_aspect_x", text="X")
                    row.prop(context.scene.render, "pixel_aspect_y", text="Y")

                    row = box.row(1)
                    row.prop(context.space_data, "use_render_border")
                    row.prop(context.scene.render, "use_border", text="Border")
                   
                    sub = row.row(1)
                    sub.active = context.scene.render.use_border
                    sub.prop(context.scene.render, "use_crop_to_border", text="Crop")

                    box = layout.box().column(1)   

                    row = box.row(1)           
                    row.alignment = 'CENTER'
                    row.label("Anti-Aliasing", icon='MOD_ARRAY')    
                      
                    box.separator()

                    row = box.row(1)               
                    row.prop(context.scene.render, "use_antialiasing", text="Activation")
                    
                    box.separator()  
                                     
                    row = box.row(1)   
                    split = box.split()

                    col = split.column()
                    col.row().prop(context.scene.render, "antialiasing_samples", expand=True)
                    sub = col.row()
                    sub.enabled = not context.scene.render.use_border
                    sub.prop(context.scene.render, "use_full_sample")

                    col = split.column()
                    col.prop(context.scene.render, "pixel_filter_type", text="")
                    col.prop(context.scene.render, "filter_size", text="Size")
                      
                    box.separator()

                # Color Managment
                if lt.display_img_color:

                    box = layout.box().column(1)   

                    row = box.row(1)           
                    row.alignment = 'CENTER'
                    row.label("Color Managment", icon='COLOR')    
                      
                    box.separator()

                    row = box.row(1)              
                    row.label(text="Display Device...", icon='DISCLOSURE_TRI_RIGHT_VEC')
                    
                    row = box.row(1)                 
                    row.prop(context.scene.display_settings, "display_device", "")

                    box.separator()  

                    row = box.row(1)                             
                    row.label(text="Render...", icon='DISCLOSURE_TRI_RIGHT_VEC')

                    row = box.column(1)                 
                    row.template_colormanaged_view_settings(context.scene, "view_settings")

                    box.separator() 

                    row = box.row(1)                              
                    row.label(text="Sequencer / Color Space...", icon='DISCLOSURE_TRI_RIGHT_VEC')

                    row = box.row(1)                   
                    row.prop(context.scene.sequencer_colorspace_settings, "name", "")
                    
                    box.separator()


            #############################
            # Animation Render
            
            if lt.display_hops_anim:
                
                box.separator()  

                box = layout.box().column(1) 

                row = box.row(1)              
                row.alignment = 'CENTER'
                row.label("ANIMATION RENDER", icon_value=get_icon_id("Noicon"))     

                box.separator()        
                box.separator()

                row = box.row(1) 
                row.alignment = 'CENTER'             
                row.operator("screen.frame_jump", text="", icon='REW').end = False
                row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
                 
                if not context.screen.is_animation_playing:
                    if context.scene.sync_mode == 'AUDIO_SYNC' and context.user_preferences.system.audio_device == 'JACK':
                        row.operator("screen.animation_play", text="", icon='PLAY')
                    else:
                        row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
                        row.operator("screen.animation_play", text="", icon='PLAY')
                else:
                    row.operator("screen.animation_play", text="", icon='PAUSE')  
      
                row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
                row.operator("screen.frame_jump", text="", icon='FF').end = True                                                
        
                box.separator()
                
                box = layout.box().column(1) 

                if context.mode=="OBJECT" or context.mode=="POSE":
             
                    if context.active_object and context.active_object.type in {'MESH', 'CURVE', 'SURFACE', 'ARMATURE', 'META', 'LATTICE'}:

                        row = box.row(1)  
                        row.label(text="Keyframes:")
                        
                        row = box.row(1)
                        row.operator("anim.keyframe_insert_menu", icon='ZOOMIN', text="")
                        row.operator("anim.keyframe_delete_v3d", icon='ZOOMOUT', text="")
                        row.prop_search(context.scene.keying_sets_all, "active", context.scene, "keying_sets_all", text="")
                        row.operator("anim.keyframe_insert", text="", icon='KEY_HLT')
                        row.operator("anim.keyframe_delete", text="", icon='KEY_DEHLT')

                row = box.row(1) 
                row.prop(context.scene, "use_preview_range", text="", toggle=True)
                row.prop(context.scene, "frame_current", text="")            
                row.prop(context.scene, "lock_frame_selection_to_range", text="", toggle=True)

                box.separator()
              
                box = layout.box().column(1) 
             
                row = box.row(1) 
                row.label(text="Frame Range:")
                
                row = box.row(1) 
                if not context.scene.use_preview_range:
                    row.prop(context.scene, "frame_start", text="Start")
                    row.prop(context.scene, "frame_end", text="End")
                else:
                    row.prop(context.scene, "frame_preview_start", text="Start")
                    row.prop(context.scene, "frame_preview_end", text="End")

                row = box.row(1)                
                row.prop(context.scene, "frame_step")
                row.menu("RENDER_MT_framerate_presets", text="Frame Rate")
               
                box.separator()
              
                row = box.row(1)  
                row.label(text="Time Remapping:")
                
                row = box.row(1)  
                row.prop(context.scene.render, "frame_map_old", text="Old")
                row.prop(context.scene.render, "frame_map_new", text="New")

                box.separator() 
              
                box = layout.box().column(1) 
                
                row = box.row()
                row.prop(context.scene.render, "use_motion_blur", text="Enable Motion Blur")
               
                row = box.row()
                row.prop(context.scene.render, "motion_blur_samples")
                row.prop(context.scene.render, "motion_blur_shutter")    

                box.separator() 
              
                box = layout.box().column(1) 
                
                row = box.row(1)
                row.scale_y = 3
                row.operator("render.render", text="SeqRender#").animation = True
                row.operator("render.opengl", text="SeqOpenGL#").animation = True

                row = box.row(1)
                row.prop(context.scene.render, "display_mode", text="")                                                                 
                row.menu("INFO_MT_opengl_render", "OpenGl Opt.") 

                box.separator() 
               
                box = layout.box().column(1) 
               
                row = box.row(1)
                row.scale_y = 2    
                row.operator("render.play_rendered_anim", "Play Sequence#")
     
                box.separator() 

                row = box.row(1)
                row.prop(context.scene.render, "filepath", text="", icon ="NLA_PUSHDOWN")
                
                box.separator()
                
                row = box.row(1)               
                row.template_image_settings(context.scene.render.image_settings, color_management=False)             

                box.separator()      
                    

        # Non Active 
        else:                      
            box = layout.box().column(1)              
            row = box.column(1)
            row.label("Please select an object as active!", icon = "ERROR") 


        # History
  
        box.separator()
                     
        box = layout.box().column(1) 
        
        row = box.row(1)
        row.operator('wm.url_open',  text = '', icon="INFO").url = "https://masterxeon1001.com/2016/05/28/hard-ops-8-release-notes/"
        row.operator("view3d.ruler", text="Ruler", icon_value=get_icon_id("Ruler"))   
        row.operator("ed.undo_history", text="History", icon_value=get_icon_id("History"))
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
        
        box.separator()
        



# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "https://masterxeon1001.wordpress.com/hard-ops-intro-guide/"
    url_manual_mapping = (
        ("sstep.objects", "HardOps Guide"),


        )
    return url_manual_prefix, url_manual_mapping


class Purge_Materials(bpy.types.Operator):
    '''Purge orphaned materials'''
    bl_idname="purge.unused_material_data"
    bl_label="Purge Materials"
    
    def execute(self, context):

        target_coll = eval("bpy.data.materials")

        for item in target_coll:
            if item.users == 0:
                target_coll.remove(item)

        return {'FINISHED'}



class BoolToolMenu(bpy.types.Menu):
    bl_label = "BoolTool"
    bl_idname = "hrdops_booltool"

    def draw(self, context):
        layout = self.layout

        layout.operator("btool.boolean_union", text = "Union Brush",icon = "ROTATECOLLECTION")
        layout.operator("btool.boolean_inters", text ="Intersection Brush",icon = "ROTATECENTER")
        layout.operator("btool.boolean_diff", text ="Difference Brush",icon = "ROTACTIVE")

        layout.separator()

        layout.operator("btool.boolean_union_direct", text = "Union Brush",icon = "ROTATECOLLECTION")
        layout.operator("btool.boolean_inters_direct", text ="Intersection Brush",icon = "ROTATECENTER")
        layout.operator("btool.boolean_diff_direct", text ="Difference Brush",icon = "ROTACTIVE")

        layout.separator()

        layout.operator("btool.draw_polybrush",icon = "LINE_DATA")

bpy.utils.register_class(BoolToolMenu)



class Display_Wire_on(bpy.types.Operator):
    """Enable Wire / Draw All Edges"""
    bl_idname = "object.wire_on"
    bl_label = "Wire on"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.object.show_wire = True
        bpy.context.object.show_all_edges = True

        return {'FINISHED'}

bpy.utils.register_class(Display_Wire_on)


class Display_Wire_off(bpy.types.Operator):
    """Disable Wire / Draw All Edges"""
    bl_idname = "object.wire_off"
    bl_label = "Wire off"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        bpy.context.object.show_wire = False
        bpy.context.object.show_all_edges = False
        return {'FINISHED'}


class Display_AM(bpy.types.Menu):
    """Asset Manager Libary / Category"""
    bl_idname = "menu.am_set"
    bl_label = "AM > Libary / Category"
    bl_options = {'REGISTER', 'UNDO'}


    def draw(self, context):
        layout = self.layout

        if any("asset_management" in s for s in bpy.context.user_preferences.addons.keys()):
            layout.prop(context.window_manager.asset_m, "libraries", text="")
            layout.prop(context.window_manager.asset_m, "categories", text="")
            layout.prop(context.window_manager.asset_m, "favorites_enabled", text="Show Favorites")
        return {'FINISHED'}



class Expand_Mod_Stack(bpy.types.Operator):
    '''Expand modifier stack'''
    bl_idname = "hops.expand_mod"
    bl_label = "Expand"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not(bpy.context.selected_objects):
            for obj in bpy.data.objects:
                for mod in obj.modifiers:
                    mod.show_expanded = True
        else:
            for obj in bpy.context.selected_objects:
                for mod in obj.modifiers:
                    mod.show_expanded = True

        return {'FINISHED'}


class Collapse_Mod_Stack(bpy.types.Operator):
    '''Collapse modifier stack'''
    bl_idname = "hops.collapse_mod"
    bl_label = "Collapse"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not(bpy.context.selected_objects):
            for obj in bpy.data.objects:
                for mod in obj.modifiers:
                    mod.show_expanded = False
        else:
            for obj in bpy.context.selected_objects:
                for mod in obj.modifiers:
                    mod.show_expanded = False

        return {'FINISHED'}


class Mod_Apply(bpy.types.Operator):
    '''apply modifiers'''
    bl_idname = "hops.apply_mod"
    bl_label = "Apply All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if context.mode == 'OBJECT':
            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
        else:
            bpy.ops.object.editmode_toggle()

            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

            bpy.ops.object.editmode_toggle()

        return {"FINISHED"}

bpy.utils.register_class(Mod_Apply)


class Mod_Remove(bpy.types.Operator):
    '''remove modifiers'''
    bl_idname = "hops.remove_mod"
    bl_label = "Remove All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if context.mode == 'OBJECT':
            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_remove(modifier=mod.name)
        else:
            bpy.ops.object.editmode_toggle()

            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_remove(modifier=mod.name)

            bpy.ops.object.editmode_toggle()

        return {"FINISHED"}

bpy.utils.register_class(Mod_Remove)



class Expand_Con_Stack(bpy.types.Operator):
    '''Expand constraint stack'''
    bl_idname = "hops.expand_con"
    bl_label = "Expand"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not(bpy.context.selected_objects):
            for con in obj.constraints:
                con.show_expanded = True
        else:
            for obj in bpy.context.selected_objects:
                for con in obj.constraints:
                    con.show_expanded = True

        return {'FINISHED'}


#constraint
class Collapse_Con_Stack(bpy.types.Operator):
    '''Collapse constraint stack'''
    bl_idname = "hops.collapse_con"
    bl_label = "Collapse"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not(bpy.context.selected_objects):
            for con in obj.constraints:
                con.show_expanded = False
        else:
            for obj in bpy.context.selected_objects:
                for con in obj.constraints:
                    con.show_expanded = False

        return {'FINISHED'}





class tp_batch_Mira(bpy.types.Operator):
    """Edit MiraTools"""
    bl_idname = "tp_batch.mira"
    bl_label = "MiraTools"
    #bl_context = "edit_mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        box = layout.box().column(1)

        row = box.row(1)
        row.prop(context.scene.mi_settings, "surface_snap", text='Snap', icon="SNAP_SURFACE")
        row.prop(context.scene.mi_settings, "snap_objects", text='', icon="VISIBLE_IPO_ON")
        row.prop(context.scene.mi_settings, "convert_instances", text='i-Convert', icon="BOIDS")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("wm.url_open", text="", icon='QUESTION').url = "https://lh3.googleusercontent.com/-0fzOvLD4EM8/Vb5CdYy5qKI/AAAAAAAAIVk/EkiLDYzwtVk/w780-h840-no/%25233_Poly_Loop.png"
        row.operator("mira.poly_loop", text="Poly Loop", icon="MESH_GRID")

        row = box.row(1)
        row.operator("wm.url_open", text="", icon='QUESTION').url = "https://lh5.googleusercontent.com/-o3W-ypmbxI8/Vb5gyXLJ4tI/AAAAAAAAIXc/ZsNqJR5WiWw/w746-h840-no/%25234_Curve_Surface.png"
        row.operator("mira.curve_surfaces", text="CurveSurfaces", icon="SURFACE_NCURVE")

        box.separator()

        row = box.row(1)
        row.prop(context.scene.mi_cur_surfs_settings, "spread_loops_type", text='Points')


        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mira.curve_stretch", text="CurveStretch", icon="STYLUS_PRESSURE")
        row.prop(context.scene.mi_cur_stretch_settings, "points_number", text='PointsNumber')

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mira.curve_guide", text="CurveGuide", icon="RNA")
        row.prop(context.scene.mi_curguide_settings, "points_number", text='LoopSpread')

        box.separator()

        row = box.row(1)
        row.prop(context.scene.mi_curguide_settings, "deform_type", text='DeformType')

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("wm.url_open", text="", icon='QUESTION').url = "https://lh4.googleusercontent.com/-GTuGp92YHvc/VbruOKWUTTI/AAAAAAAAIUk/LbjhscUtqHI/w611-h840-no/%25232_Deform_Mesh.png"
        row.operator("mira.linear_deformer", text="LinearDeformer", icon="OUTLINER_OB_MESH")

        row = box.row(1)
        row.prop(context.scene.mi_ldeformer_settings, "manual_update", text='ManualUpdate')

        row = box.row(1)
        row.operator("mira.noise", text="NoiseDeform", icon="RNDCURVE")
        row.operator("mira.deformer", text="Deformer")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("wm.url_open", text="", icon='QUESTION').url = "https://lh5.googleusercontent.com/-tIDzK8yFnjU/VbhVbn2cfSI/AAAAAAAAIPo/mYRzdjqOki0/w595-h840-no/%25231_Draw_Extrude.png"
        row.operator("mira.draw_extrude", text="Draw Extrude", icon="VPAINT_HLT")
        #row.prop(context.scene.mi_extrude_settings, "extrude_mode", text='Mode')

        box.separator()

        row = box.row(1)
        row.prop(context.scene.mi_extrude_settings, "extrude_step_type", text='Step')

        if context.scene.mi_extrude_settings.extrude_step_type == 'Asolute':
            row.prop(context.scene.mi_extrude_settings, "absolute_extrude_step", text='')
        else:
            row.prop(context.scene.mi_extrude_settings, "relative_extrude_step", text='')

        row = box.row(1)
        if context.scene.mi_settings.surface_snap is False:
            row.prop(context.scene.mi_extrude_settings, "do_symmetry", text='Symmetry')

            if context.scene.mi_extrude_settings.do_symmetry:
                row.prop(context.scene.mi_extrude_settings, "symmetry_axys", text='Axys')


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 250)

bpy.utils.register_class(tp_batch_Mira)




def register():

    bpy.utils.register_manual_map(add_object_manual_map)


def unregister():

    bpy.utils.unregister_manual_map(add_object_manual_map)


if __name__ == "__main__":
    register()

