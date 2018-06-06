import bpy, os
from . icons import get_icon_id, icons
from bpy.props import IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty, PointerProperty
import bpy, os



### fold menues
class Dropdown_HardOps_Props_EDM(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.hardops_window
    """

    display_hops_internal_tools_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Internal Tools", default = False)
    display_hops_meshtools_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Mesh Tools", default = False)
    
    display_hops_add_am_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Asset Manager", default = False)
    display_hops_add_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Hardops Insert", default = True)

    display_hops_ops_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Edit Operators", default = True)
    display_hops_vert_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Edit Operators", default = False)
    display_hops_uv_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Edit Operators", default = False)

    display_hops_material_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Materials", default = True)
    display_hops_mat_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Materials", default = False)
    display_mat_edit_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Material Settings", default = False)

    display_hops_mod_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Modifiers", default = False)

    display_hops_gui_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Display", default = True)
    display_hops_guidpy_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Object Display", default = False)
    display_hops_guiobj_edm = bpy.props.BoolProperty(name = "Open/Close", description = "View Display", default = False)
    
    display_hops_xtras_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Extra Tools", default = True)
    display_hops_ext_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Extra Tools", default = False)
    display_hops_opgl_edm = bpy.props.BoolProperty(name = "Open/Close", description = "OpenGL", default = False)

    display_hops_img_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Image OpenGL Render", default = False)
    display_img_ren_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Render", default = True)
    display_img_dim_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Dimesions", default = False)
    display_img_pfc_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Performance", default = False)
    display_img_color_edm = bpy.props.BoolProperty(name = "Open/Close", description = "Color Managment", default = False)

    display_hops_cam_edm = bpy.props.BoolProperty(name = "Open/Close", description = "fold menu", default = False)

    display_set_material_edm = bpy.props.BoolProperty(name = "Set Material", description = "Assign Materials to selected Faces", default = False)

    #AM additions
    #wm = context.window_manager
    current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    user_preferences = bpy.context.user_preferences
    addon_pref = user_preferences.addons[current_dir].preferences
    
bpy.utils.register_class(Dropdown_HardOps_Props_EDM)
bpy.types.WindowManager.hardops_window_edm = bpy.props.PointerProperty(type = Dropdown_HardOps_Props_EDM)


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
   

class HardOps_Panel_EDM(bpy.types.Panel):
    bl_label = "HardOps 8"
    bl_idname = "HardOps_Panel_ID_EDM"
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
        if context.mode == "EDIT_MESH" or context.mode == "EDIT_CURVE" or context.mode == "EDIT_LATTICE":
            return isNoModelingMode


    def draw(self, context):
        lt = context.window_manager.hardops_window_edm
        layout = self.layout.column(1)   
        obj = context.active_object
        
        #AM additions
        #wm = context.window_manager
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_pref = user_preferences.addons[current_dir].preferences
        

        # Insert Mesh
        if context.mode == "EDIT_MESH":
            box = layout.box().column(1)       

            row = box.row(1) 
            row.alignment = 'CENTER'               
            sub = row.row(1)
            sub.scale_x = 1
            sub.operator("mesh.primitive_plane_add",icon='MESH_PLANE',text="")
            sub.operator("mesh.primitive_cube_add",icon='MESH_CUBE',text="")
            sub.operator("mesh.primitive_circle_add",icon='MESH_CIRCLE',text="")
            sub.operator("mesh.primitive_uv_sphere_add",icon='MESH_UVSPHERE',text="")
            sub.operator("mesh.primitive_ico_sphere_add",icon='MESH_ICOSPHERE',text="")         

            if lt.display_hops_add_edm:              
                sub.prop(lt, "display_hops_add_edm", text="", icon='MOVE_UP_VEC')
            else:               
                sub.prop(lt, "display_hops_add_edm", text="", icon='MOVE_DOWN_VEC')    
                
                      
            row = box.row(1)  
            row.alignment = 'CENTER'                        
            sub = row.row(1)
            sub.scale_x = 1
            sub.operator("mesh.primitive_cylinder_add",icon='MESH_CYLINDER',text="")
            sub.operator("mesh.primitive_torus_add",icon='MESH_TORUS',text="")
            sub.operator("mesh.primitive_cone_add",icon='MESH_CONE',text="")
            sub.operator("mesh.primitive_grid_add",icon='MESH_GRID',text="")
            sub.operator("mesh.primitive_monkey_add",icon='MESH_MONKEY',text="")                                         

            if lt.display_hops_add_am_edm:              
                sub.prop(lt, "display_hops_add_am_edm", text="", icon='MOVE_UP_VEC')
            else:               
                sub.prop(lt, "display_hops_add_am_edm", text="", icon='MOVE_DOWN_VEC')    
           
            row = box.row(1) 
            row.alignment = 'CENTER'  
            row.scale_x = 0.905
                
            row.prop(obj, "name", text="", icon = "COPY_ID")

            sub = row.row(1)
            sub.scale_x = 1.15         
            if lt.display_hops_internal_tools_edm:              
                sub.prop(lt, "display_hops_internal_tools_edm", text="", icon='MOVE_UP_VEC')
            else:               
                sub.prop(lt, "display_hops_internal_tools_edm", text="", icon='MOVE_DOWN_VEC')  


            box.separator()

            if lt.display_hops_add_am_edm:   

                #if context.window_manager.AssetM_previews:
                if any("asset_management" in s for s in bpy.context.user_preferences.addons.keys()):
                    if addon_pref.Asset_Manager_Preview :
                        box = layout.box().column(1)

                        row = box.row(1)
                        row.template_icon_view(context.window_manager, "AssetM_previews")
                        
                        row = box.row(1) 
                        row.menu("menu.am_set", icon = "SCRIPTWIN")

                        box.separator()

                    else:
                        box.separator()
                else:
                    box.separator()


            if lt.display_hops_add_edm: 

                box = layout.box().column(1)       

                row = box.row(1) 
                row.scale_y = 0.7
                row.template_icon_view(context.window_manager , "Hard_Ops_previews")
                #row.template_icon_view(context.window_manager, "sup_preview")

                row = box.row(1) 
                props = row.operator("hops.move_assets_preview_selection", icon = "TRIA_LEFT", text = "")
                props.property_name = "Hard_Ops_previews"
                props.move_amount = -1

                row.operator("hops.insert_asset", text = "Insert").asset_name = context.window_manager.Hard_Ops_previews

                props = row.operator("hops.move_assets_preview_selection", icon = "TRIA_RIGHT", text = "")
                props.property_name = "Hard_Ops_previews"
                props.move_amount = 1

                row = box.row(1) 
                row.operator("view3d.insertpopup", "Asset", icon_value=get_icon_id("HardOps"))
                row.prop(context.window_manager, "choose_primitive", text="", expand=False, icon_value=get_icon_id("Noicon"))     
     
                box.separator()


            #############################  
            # Collapsing Menues   
            
            if lt.display_hops_internal_tools_edm: 
                
                box = layout.box().column(1)

                row = box.row(1)                             
                row.alignment = 'CENTER'
                 
                if lt.display_hops_ops_edm:              
                    row.prop(lt, "display_hops_ops_edm", text="", icon='EDIT')
                else:               
                    row.prop(lt, "display_hops_ops_edm", text="", icon='EDIT')  

                if lt.display_hops_xtras_edm:              
                    row.prop(lt, "display_hops_xtras_edm", text="", icon='MOD_EXPLODE')
                else:               
                    row.prop(lt, "display_hops_xtras_edm", text="", icon='MOD_EXPLODE')   

                if lt.display_hops_vert_edm:              
                    row.prop(lt, "display_hops_vert_edm", text="", icon='GROUP_VERTEX')
                else:               
                    row.prop(lt, "display_hops_vert_edm", text="", icon='GROUP_VERTEX')   
                    
                if lt.display_hops_mod_edm:              
                    row.prop(lt, "display_hops_mod_edm", text="", icon='MODIFIER')
                else:               
                    row.prop(lt, "display_hops_mod_edm", text="", icon='MODIFIER')                

                if lt.display_hops_uv_edm:              
                    row.prop(lt, "display_hops_uv_edm", text="", icon='UV_ISLANDSEL')
                else:               
                    row.prop(lt, "display_hops_uv_edm", text="", icon='UV_ISLANDSEL') 

                row = box.row(1)  
                row.alignment = 'CENTER'

                if lt.display_hops_gui_edm:              
                    row.prop(lt, "display_hops_gui_edm", text="", icon='ZOOM_SELECTED')
                else:               
                    row.prop(lt, "display_hops_gui_edm", text="", icon='ZOOM_SELECTED') 

                if lt.display_hops_material_edm:              
                    row.prop(lt, "display_hops_material_edm", text="", icon='MATERIAL')
                else:               
                    row.prop(lt, "display_hops_material_edm", text="", icon='MATERIAL')   

                if lt.display_hops_opgl_edm:              
                    row.prop(lt, "display_hops_opgl_edm", text="", icon='LAMP_SPOT')
                else:               
                    row.prop(lt, "display_hops_opgl_edm", text="", icon='LAMP_SPOT')    
                
                if lt.display_hops_cam_edm:              
                    row.prop(lt, "display_hops_cam_edm", text="", icon='CAMERA_DATA')
                else:               
                    row.prop(lt, "display_hops_cam_edm", text="", icon='CAMERA_DATA')     
                       
                if lt.display_hops_img_edm:              
                    row.prop(lt, "display_hops_img_edm", text="", icon='SCENE')
                else:               
                    row.prop(lt, "display_hops_img_edm", text="", icon='SCENE')  

                box.separator()


            #############################
            # Tools
            
            if lt.display_hops_ops_edm: 

                box = layout.box().column(1)              
                row = box.row(1)
                row.alignment = 'CENTER'
                row.label("BEVEL & SHARPEN", icon_value=get_icon_id("Noicon"))

                box.separator()

                row = box.column(1) 
                row.operator("bevelandsharp1.objects", text = "Make SSharp", icon_value=get_icon_id("MakeSharpE"))
                row.operator("transform.edge_bevelweight", text = "Bweight", icon_value=get_icon_id("AdjustBevel"))
                row.operator("clean1.objects", text = "Clean SSharps", icon_value=get_icon_id("CleansharpsE"))
                
                box.separator()
                
                box = layout.box().column(1)    
    
                
                #############################
                # MeshTools
                
                row = box.row(1)                                                    
                if lt.display_hops_meshtools_edm: 
                    row = box.row(1)                                             
                    row.prop(lt, "display_hops_meshtools_edm", text="MESHTOOLS", icon_value=get_icon_id("Noicon"))
                else:               
                    row = box.row(1)
                    row.prop(lt, "display_hops_meshtools_edm", text="MeshTools", icon_value=get_icon_id("Noicon"))   
    
                if lt.display_hops_meshtools_edm: 
    
                    box.separator()             
    
                    row = box.row(1)
                    row.operator("circle.setup", text = "Circle", icon_value=get_icon_id("CircleSetup"))
                    row.operator("nth.circle", text = "Circle (Nth)", icon_value=get_icon_id("NthCircle"))
    
                    row = box.row(1)
                    row.operator("fgrate.op", text = "Grate (Face)", icon_value=get_icon_id("FaceGrate"))
                    row.operator("fknurl.op", text = "Knurl (Face)", icon_value=get_icon_id("FaceKnurl"))  
                    
                    row = box.row(1)
                    row.operator("quick.panel", text = "Panel (Face)", icon_value=get_icon_id("EdgeRingPanel"))
                    row.operator("entrench.selection", text = "Panel (Edge)", icon_value=get_icon_id("EdgeRingPanel"))

                    box.separator()
    
                    row = box.column(1) 
                    row.operator("view3d.symmetrize", text = "(X) - Symmetrize", icon_value=get_icon_id("Xslap")).symtype = "NEGATIVE_X"
                    row.operator("view3d.symmetrize", text = "(Y) - Symmetrize", icon_value=get_icon_id("Yslap")).symtype = "NEGATIVE_Y"
                    row.operator("view3d.symmetrize", text = "(Z) - Symmetrize", icon_value=get_icon_id("Zslap")).symtype = "POSITIVE_Z"                 

                    box.separator()
        
                    row = box.row(1) 
                    row.operator("hops.draw_uv", text = "UV Preview", icon_value=get_icon_id("PUnwrap"))                   
                    row.operator("clean1.objects", text = "Demote", icon_value = get_icon_id("Pizzaops")).clearsharps = False
                   
                                        
                    box.separator()
    
                    box = layout.box().column(1)  
                

            #############################
            # Gui
            
            row = box.row(1)                  
            if lt.display_hops_gui_edm:

                # Shading               
                row = box.row(1)                                                    
                if lt.display_hops_guiobj_edm:
                    row = box.row(1)              
                    row.prop(lt, "display_hops_guiobj_edm", text="SHADING", icon_value=get_icon_id("Noicon"))
                else:
                    row = box.row(1)               
                    row.prop(lt, "display_hops_guiobj_edm", text="Shading", icon_value=get_icon_id("Noicon")) 

                if lt.display_hops_guiobj_edm:
                    
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
                            row.operator("object.add_materials", text="Display Ngons/Tris", icon='COLOR') 
                    
                    row = box.row(1) 
                    row.operator("data.facetype_select", text="Ngons", icon ="RESTRICT_SELECT_OFF").face_type = "5"
                    row.operator("data.facetype_select", text="Tris", icon ="RESTRICT_SELECT_OFF").face_type = "3"

                    box.separator()
                    
                    row = box.row(1) 
                    row.operator("mesh.mark_sharp", text="EdgeSharp",icon="SNAP_EDGE")
                    props = row.operator("mesh.mark_sharp", text="VertSharp",icon="SNAP_VERTEX")
                    props.use_verts = True
                    props.clear = True

                    row = box.row(1) 
                    row.operator("mesh.mark_sharp", text="E-SharpClear",icon="PANEL_CLOSE").clear = True
                    row.operator("mesh.mark_sharp", text="V-SharpClear",icon="PANEL_CLOSE").use_verts = True

                    box.separator()

                    row = box.row(1) 
                    row.operator("mesh.normals_make_consistent", text="Normal-Recall",icon="SNAP_NORMAL")
                    row.operator("mesh.flip_normals", text="Normal-Flip",icon="FILE_REFRESH")
                                                             
                    row = box.row(1)
                    sub = row.row(1)
                    sub.active = context.active_object.data.use_auto_smooth
                    sub.prop(context.active_object.data, "auto_smooth_angle", text="Angle")  
                    row.operator("mesh.faces_shade_smooth", text="Smooth", icon="SOLID")                  

                    box.separator()
                       
                    if context.active_object:                
                        
                        row = box.row(1)
                        row.prop(context.space_data, "use_occlude_geometry", text="Limit 2 Visible", icon='ORTHO')  

                        active_xray = bpy.context.object.show_x_ray 
                        if active_xray == True:
                            row.operator("view3d.xray_off", text="X-Ray", icon="META_CUBE")
                        else:
                            row.operator("view3d.xray_on", text="X-Ray", icon="META_PLANE")
                       
                        row = box.row(1)         
                        row.prop(context.space_data, "show_backface_culling", text="Backface", icon ="MOD_LATTICE")   
                        row.prop(context.space_data, "show_occlude_wire", text="Hidden", icon ="OUTLINER_DATA_LATTICE")  

                    else:
                        box.separator()
                        
                        box.label('No object selected as active', icon ="ERROR")    

                    box.separator()

                    box = layout.box().column(1) 


                #############################
                # Display

                if lt.display_hops_guidpy_edm:
                    row = box.row(1)              
                    row.prop(lt, "display_hops_guidpy_edm", text="DISPLAY", icon_value=get_icon_id("Noicon"))
                else:
                    row = box.row(1)               
                    row.prop(lt, "display_hops_guidpy_edm", text="Display", icon_value=get_icon_id("Noicon"))   

                if lt.display_hops_guidpy_edm:  
                
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
            if lt.display_hops_xtras_edm: 

                if lt.display_hops_ext_edm:  
                    row.prop(lt, "display_hops_ext_edm", text="XTRAS", icon_value=get_icon_id("Noicon"))
                    row = box.row(1)
                else:               
                    row = box.row(1)
                    row.prop(lt, "display_hops_ext_edm", text="Xtras", icon_value=get_icon_id("Noicon"))   

            if lt.display_hops_ext_edm: 

                box.separator()                   

                row = box.row(1)   
                if any("AutoMirror" in s for s in bpy.context.user_preferences.addons.keys()):
                    row.operator("view3d.mirrorhelper", text = "Mirror Helper", icon_value=get_icon_id("MHelper"))

                if any("Lattice" in s for s in bpy.context.user_preferences.addons.keys()):
                    row.operator("object.easy_lattice", text = "Easy Lattice", icon_value=get_icon_id("MHelper"))

                if any("relink" in s for s in bpy.context.user_preferences.addons.keys()):
                    row.menu("relink_menu", text = "ReLink", icon_value=get_icon_id("MHelper"))

                row = box.row(1)   
                if any("mira_tools" in s for s in bpy.context.user_preferences.addons.keys()):
                    #row.menu("mira.submenu", text = "Mira (T)", icon="PLUGIN")
                    row.operator("tp_batch.mira", text = "Mira (C)", icon="PLUGIN")
            
                box.separator() 

                row = box.row(1)
                
                Frame = icons.get
                row.operator("view3d.hops_helper_popup", text = "(H) Mod", icon_value=get_icon_id("MHelper"))                

                box.separator() 
                
                box = layout.box().column(1)  


            #############################
            # Materials
            
            if lt.display_hops_material_edm: 
                
                row = box.row(1) 
                if lt.display_hops_mat_edm:
                    row = box.row(1)              
                    row.prop(lt, "display_hops_mat_edm", text="MATERIALS", icon_value=get_icon_id("Noicon") )
                else:
                    row = box.row(1)               
                    row.prop(lt, "display_hops_mat_edm", text="Materials", icon_value=get_icon_id("Noicon") )   

                if lt.display_hops_mat_edm:  
                
                    box.separator()                                      
                    
                    if len(context.selected_objects) >= 1:

                        row = box.row(1) 
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

                        if lt.display_mat_edit_edm:                                                      
                          row.prop(lt, "display_mat_edit_edm", text="", icon='MOVE_DOWN_VEC')
                                        
                        else: 
                          row.prop(lt, "display_mat_edit_edm", text="", icon='MOVE_UP_VEC')     

                        row.separator()
                        
                        row = box.row(1)
                        row.operator("object.material_slot_assign", text="Assign")
                        row.operator("object.material_slot_select", text="Select")
                        row.operator("object.material_slot_deselect", text="Deselect")

                        box.separator()
                                              
                        if lt.display_mat_edit_edm:  
                        
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



            #############################
            # Vertex Groups
            
            if lt.display_hops_vert_edm:         
                box = layout.box().column(1)   

                row = box.row(1)              
                row.alignment = 'CENTER'
                row.label("VERTEX", icon_value=get_icon_id("Noicon"))
                
                box.separator()                                       
                
                row = box.row()
                row.template_list("MESH_UL_vgroups", "", context.object, "vertex_groups", context.object.vertex_groups, "active_index", rows=4)           

                col = row.column()
                sub = col.column(1)
                sub.operator("object.vertex_group_add", icon='ZOOMIN', text="")
                sub.operator("object.vertex_group_remove", icon='ZOOMOUT', text="").all = False
                sub.menu("MESH_MT_vertex_group_specials", icon='DOWNARROW_HLT', text="")
                sub.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
                sub.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'                                

                box.separator()   

                row = box.row(1)
                row.operator("object.vertex_group_assign", text="Assign")
                row.operator("object.vertex_group_remove_from", text="Remove")

                row = box.row(1)
                row.operator("object.vertex_group_select", text="Select")
                row.operator("object.vertex_group_deselect", text="Deselect")

                box.separator()   

                row = box.row(1)  
                row.prop(context.tool_settings, "vertex_group_weight", text="Weight")             

                box.separator()   


            #############################
            # UV
            
            if lt.display_hops_uv_edm: 

                box = layout.box().column(1) 
          
                row = box.row(1)              
                row.alignment = 'CENTER'
                row.label("UV", icon_value=get_icon_id("Noicon"))
              
                box.separator() 

                row = box.row()   
                row.template_list("MESH_UL_uvmaps_vcols", "uvmaps", context.object.data, "uv_textures", context.object.data.uv_textures, "active_index", rows=2)

                row = row.column(1)
                row.operator("mesh.uv_texture_add", icon='ZOOMIN', text="")
                row.operator("mesh.uv_texture_remove", icon='ZOOMOUT', text="")                  

                box.separator() 


            #############################
            # Modifier
            
            if lt.display_hops_mod_edm: 
                                              
                box = layout.box().column(1)                                      
                
                row = box.row(1)
                row.alignment = 'CENTER'
                row.label('MODIFIER STACK', icon_value=get_icon_id("Noicon"))   
                
                box.separator()
                                      
                row = box.row(1)
                row.scale_y = 1.5

                row.operator_menu_enum("object.modifier_add", "type", text ="Modifier", icon ="NLA_PUSHDOWN")

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

                # Modifier Stack   
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
 
  
        #############################
        # Edit Curve
        
        if context.mode == "EDIT_CURVE":
        
            box = layout.box().column(1)
             
            row = box.row(1)              
            row.alignment = 'CENTER'
            row.label("CURVE EDITING")      
            
            box.separator()                                  

            box = layout.box().column(1)
            
            row = box.row(1)         
            row.alignment = 'CENTER'               

            sub = row.row(1)
            sub.scale_x = 1.2     
            sub.operator("curve.primitive_bezier_curve_add",icon='CURVE_BEZCURVE',text="")
            sub.operator("curve.primitive_bezier_circle_add",icon='CURVE_BEZCIRCLE',text="")
            sub.operator("curve.primitive_nurbs_curve_add",icon='CURVE_NCURVE',text="")
            sub.operator("curve.primitive_nurbs_circle_add",icon='CURVE_NCIRCLE',text="")
            sub.operator("curve.primitive_nurbs_path_add",icon='CURVE_PATH',text="") 
            
            row = box.row(1) 
            row.alignment = 'CENTER'  
            row.scale_x = 1.09
                
            row.prop(obj, "name", text="", icon = "COPY_ID")                        

            box.separator() 
            
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
            
            box = layout.box().column(1)

            row = box.column(1)  
            row.operator("curve.spline_type_set", "Set Spline Type", icon="IPO_BEZIER")           

            box.separator()
                                  
            box = layout.box().column(1)

            row = box.row(1)
            row.alignment = 'CENTER'  
            row.label("Handles") 
            
            row = box.row(1)                            
            row.operator("curve.handle_type_set", text="Auto").type = 'AUTOMATIC'
            row.operator("curve.handle_type_set", text="Vector").type = 'VECTOR'

            row = box.row(1)   
            row.operator("curve.handle_type_set", text="Align").type = 'ALIGNED'
            row.operator("curve.handle_type_set", text="Free").type = 'FREE_ALIGN'

            box.separator()
            
            box = layout.box().column(1)

            row = box.row(1)
            row.alignment = 'CENTER' 
            row.label("Subdivide")   
             
            row = box.row(1) 
            row.operator("curve.subdivide", text="1").number_cuts=1        
            row.operator("curve.subdivide", text="2").number_cuts=2
            row.operator("curve.subdivide", text="3").number_cuts=3
            row.operator("curve.subdivide", text="4").number_cuts=4
            row.operator("curve.subdivide", text="5").number_cuts=5        
            row.operator("curve.subdivide", text="6").number_cuts=6  

            box.separator()
            
            box = layout.box().column(1)

            row = box.row(1)  
            row.operator("curve.extrude_move", text="Extrude")
            row.operator("curve.make_segment",  text="Weld") 

            row = box.row(1)             
            row.operator("curve.split",  text="Split")                   
            row.operator("curve.separate",  text="Separate")         

            row = box.row(1) 
            row.operator("transform.tilt", text="Tilt")                                     
            row.operator("curve.radius_set", "Radius")                 

            row = box.row(1) 
            row.operator("transform.vertex_random") 
            row.operator("curve.smooth")  


            box.separator()
            
            box = layout.box().column(1)
                      
            row = box.row(1)                     
            row.operator("curve.normals_make_consistent", icon ="SNAP_NORMAL")

            row = box.row(1)
            row.prop(context.active_object.data, "show_handles", text="Handles")
            row.prop(context.active_object.data, "show_normal_face", text="Normals")
     
            row = box.row(1)
            row.prop(context.scene.tool_settings, "normal_size", text="Normal Size")
                   
            box.separator()
            

        #############################
        # Edit Lattice
        
        if context.mode == "EDIT_LATTICE":
        
            box = layout.box().column(1)
             
            row = box.row(1)              
            row.alignment = 'CENTER'
            row.label("LATTICE EDITING")      
            
            box.separator()                                  

            box = layout.box().column(1)            
            
            row = box.row(1) 
            row.alignment = 'CENTER'  
            row.scale_x = 1    
                
            row.prop(obj, "name", text="", icon = "COPY_ID")                
                      
            box = layout.box().column(1)

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
            
            row = box.row(1)
            row.operator("lattice.make_regular", "Make Regular", icon ="LATTICE_DATA")

            box.separator()


        #############################
        # GUI
        
        if lt.display_hops_opgl_edm: 
            box = layout.box().column(1)   

            row = box.row(1)              

            row = box.row(1)              
            row.alignment = 'CENTER'
            row.label("OpenGL", icon_value=get_icon_id("Noicon"))

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
        
        if lt.display_hops_cam_edm: 

            box = layout.box().column(1)             
            row = box.row(1)
            row.alignment = 'CENTER'
            row.label('CAMERA', icon_value=get_icon_id("Noicon"))   

            box.separator()

            row = box.row(1)     
            row.operator("view3d.camera_to_view", text="C-View")
            row.operator("view3d.camera_to_view_selected", text="C-View Selected")		

            box.separator()
            
            box = layout.box().column(1)             
                  
            row = box.column(1)    
            row.prop(context.space_data, "lock_camera")                                                               
                  
            row = box.row(1)  
            row.prop(context.object, 'location', text="")

            box.separator()  
          
            row = box.row(1)     
            row.prop(context.object.data, "show_passepartout", text="Passepartout")                          
            row.prop(context.object.data, "passepartout_alpha", text="Alpha", slider=True)
            

        #############################
        # Image Render 
        
        if lt.display_hops_img_edm: 

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
            if lt.display_img_dim_edm:                       
                 row.prop(lt, "display_img_dim_edm", text="Scale", icon='MAN_SCALE')                             
            else:            
                 row.prop(lt, "display_img_dim_edm", text="Scale", icon='MAN_SCALE')   

            if lt.display_img_pfc_edm:                       
                 row.prop(lt, "display_img_pfc_edm", text="Power", icon='GRID')                             
            else:            
                 row.prop(lt, "display_img_pfc_edm", text="Power", icon='GRID')

            if lt.display_img_color_edm:                       
                 row.prop(lt, "display_img_color_edm", text="Color", icon='COLOR')                             
            else:            
                 row.prop(lt, "display_img_color_edm", text="Color", icon='COLOR')               
            
            box.separator()

            # Performance
            if lt.display_img_pfc_edm:  

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

            # Dimensions
            if lt.display_img_dim_edm:  

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
            if lt.display_img_color_edm:

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
        # History
        
        box.separator()
                     
        box = layout.box().column(1) 
        
        row = box.row(1) 
        row.operator('wm.url_open',  text = '', icon="INFO").url = "https://masterxeon1001.wordpress.com/hard-ops-intro-guide/"
        row.operator("view3d.ruler", text="Ruler", icon_value=get_icon_id("Ruler"))   
        row.operator("ed.undo_history", text="History", icon_value=get_icon_id("History"))
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
        
        box.separator()

