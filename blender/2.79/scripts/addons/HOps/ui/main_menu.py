import bpy
import os
from .. icons import get_icon_id
from .. utils.addons import addon_exists
from .. preferences import use_asset_manager, get_preferences, pro_mode_enabled
from .. utils.objects import get_inactive_selected_objects

class HOpsMainMenu(bpy.types.Menu):
    bl_idname = "hops_main_menu"
    bl_label = "Hard Ops 8"

    def draw(self, context):
        layout = self.layout
        active_object = context.active_object

        if active_object is None:
            self.draw_without_active_object(layout)
            layout.separator()
            layout.menu("renderSet.submenu", text="RenderSets", icon_value=get_icon_id("Gui"))
            layout.menu("viewport.submenu", text="ViewPort", icon_value=get_icon_id("Viewport"))
        elif active_object.mode == "OBJECT":
            if active_object.type == "LATTICE":
                self.draw_lattice_menu(layout)
            elif active_object.type == "CURVE":
                self.draw_curve_menu(layout)
                self.draw_always(layout)
            elif active_object.hops.status == "BOOLSHAPE":
                self.draw_boolshape_menu(layout)
                self.draw_always(layout)
            else:
                self.draw_object_mode_menu(layout)
        elif active_object.mode == "EDIT":
            self.draw_edit_mode_menu(layout, active_object)
        elif active_object.mode == "POSE":
            self.draw_rigging_menu(layout)

        self.draw_always(layout)



    # Without Selection
    ############################################################################

    def draw_without_active_object(self, layout):
        wm = bpy.context.window_manager
        if use_asset_manager():
            asset_manager = wm.asset_m
            layout.prop(asset_manager, "libraries", text = "")
            layout.prop(asset_manager, "categories", text = "")
            layout.template_icon_view(wm, "AssetM_previews", show_labels = True)
            layout.separator()
        layout.operator("view3d.asset_scroller_window", "Asset Scroller", icon_value=get_icon_id("HardOps"))
        layout.template_icon_view(wm, "Hard_Ops_previews")
        layout.template_icon_view(wm, "sup_preview")




    # Always
    ############################################################################

    def draw_always(self, layout):
        '''layout.separator()
        layout.menu("protomenu.submenu", text = "Operations", icon_value=get_icon_id("Noicon"))
        layout.separator()
        layout.menu("view3d.mstool_submenu", text = "MeshTools", icon_value=get_icon_id("Noicon"))
        layout.menu("inserts.objects", text="Insert", icon_value=get_icon_id("Noicon"))
        layout.menu("settings.submenu", text="Settings", icon_value=get_icon_id("Noicon"))'''



    # Object Mode
    ############################################################################

    def draw_object_mode_menu(self, layout):
        active_object, other_objects, other_object = get_current_selected_status()
        only_meshes_selected = all(object.type == "MESH" for object in bpy.context.selected_objects)

        object = bpy.context.active_object

        if len(bpy.context.selected_objects) == 1:  
            if object.hops.status in ("CSHARP", "SUBSHARP"):
                if active_object is not None and other_object is None and only_meshes_selected:
                        self.draw_only_with_active_object_is_csharpen(layout, active_object)

            if object.hops.status == "CSTEP":
                if active_object is not None and other_object is None and only_meshes_selected:
                    self.draw_only_with_active_object_is_cstep(layout, active_object)

            if object.hops.status == "UNDEFINED":
                if active_object is not None and other_object is None and only_meshes_selected:
                    if active_object.name.startswith("AP_"):
                        self.draw_only_with_AP_as_active_object(layout, active_object)
                    else:
                        self.draw_only_with_active_object(layout, active_object)
                    
            self.draw_options(layout)


        elif len(bpy.context.selected_objects) == 2:  
            
            selected = bpy.context.selected_objects
            active = bpy.context.active_object
            selected.remove(active)
            object = selected[0]

            if object.hops.is_for_merge:
                if active_object is not None and other_object is not None and only_meshes_selected:
                    self.draw_with_active_object_and_other_mesh_for_merge(layout, active_object, other_object)

            elif object.hops.is_for_softmerge:
                if active_object is not None and other_object is not None and only_meshes_selected:
                    self.draw_with_active_object_and_other_mesh_for_softmerge(layout, active_object, other_object)

            else:
                if active_object is not None and other_object is not None and only_meshes_selected:
                    self.draw_with_active_object_and_other_mesh(layout, active_object, other_object)

            self.draw_options(layout)

        elif len(bpy.context.selected_objects) > 2:

            self.draw_with_active_object_and_other_mesh(layout, active_object, other_object)
            self.draw_options(layout)

        else:
            self.draw_without_active_object(layout)
            layout.separator()
            layout.menu("settings.submenu", text="Settings", icon_value=get_icon_id("Gui"))


    def draw_only_with_AP_as_active_object(self, layout, object):
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("hops.copy_merge", text = "copy merge", icon_value=get_icon_id("Merge"))
        layout.operator("hops.remove_merge", text = "coming soon", icon_value=get_icon_id("Merge"))
        layout.operator("hops.remove_merge", text = "(R) merge", icon_value=get_icon_id("Merge"))

    def draw_only_with_active_object(self, layout, object):
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("hops.soft_sharpen", text = "(S) Sharpen", icon_value=get_icon_id("Ssharpen"))
        layout.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))
        object = bpy.context.active_object
        if object.hops.is_pending_boolean:
            layout.operator("reverse.boolean", text = "(Re)Bool", icon_value=get_icon_id("ReBool"))
        else:
            layout.operator("hops.adjust_tthick", text = "(T)Thick", icon_value=get_icon_id("Tthick"))

    def draw_only_with_active_object_is_csharpen(self, layout, object):
        object = bpy.context.active_object
        layout.operator_context = "INVOKE_DEFAULT"
        if object.hops.is_pending_boolean:
            layout.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))
            layout.operator("hops.adjust_bevel", text = "(B)Width", icon_value=get_icon_id("AdjustBevel"))
            layout.operator("reverse.boolean", text = "(Re)Bool", icon_value=get_icon_id("ReBool"))
        else:
            layout.operator("hops.soft_sharpen", text = "(S) Sharpen", icon_value=get_icon_id("Ssharpen"))
            layout.operator("hops.adjust_bevel", text = "(B)Width", icon_value=get_icon_id("AdjustBevel"))
            layout.operator("step.cstep", text = "(C) Step", icon_value=get_icon_id("Cstep"))

        
    def draw_only_with_active_object_is_cstep(self, layout, object):
        object = bpy.context.active_object
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("step.sstep", text = "(S) Step", icon_value=get_icon_id("Sstep"))
        if object.hops.is_pending_boolean:
            layout.operator("reverse.bools", text = "(Re)Bool-Sstep", icon_value=get_icon_id("ReBool"))
        else:
            layout.operator("hops.adjust_bevel", text = "(B)Width", icon_value=get_icon_id("AdjustBevel"))
        layout.operator("step.cstep", text = "(C) Step", icon_value=get_icon_id("Cstep"))

    def draw_with_active_object_and_other_mesh(self, layout, active_object, other_object):
        object = bpy.context.active_object
        layout.operator_context = "INVOKE_DEFAULT" 
        if object.hops.status == "CSTEP":
            layout.operator("step.sstep", text = "(S) Step", icon_value=get_icon_id("Sstep"))
        else:
            layout.operator("hops.complex_sharpen", text = "(C) Sharpen", icon_value=get_icon_id("CSharpen"))
        layout.operator("hops.complex_split_boolean", text = "(C)Slice", icon_value=get_icon_id("Csplit"))
        layout.operator("step.cstep", text = "(C) Step", icon_value=get_icon_id("Cstep"))

    def draw_with_active_object_and_other_mesh_for_merge(self, layout, active_object, other_object):
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("hops.parent_merge", text = "(C) merge", icon_value = get_icon_id("Merge"))
        layout.operator("hops.simple_parent_merge", text = "(S) merge", icon_value=get_icon_id("Merge"))
        layout.operator("hops.remove_merge", text = "(R) merge", icon_value=get_icon_id("Merge"))

    def draw_with_active_object_and_other_mesh_for_softmerge(self, layout, active_object, other_object):
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("hops.parent_merge_soft", text = "(C) merge(soft)", icon_value = get_icon_id("CSharpen"))
        layout.operator("hops.complex_split_boolean", text = "(C)Slice", icon_value=get_icon_id("Csplit"))
        layout.operator("hops.remove_merge", text = "(R) merge", icon_value=get_icon_id("CSharpen"))

    def draw_options(self, layout):
        layout.separator()
        layout.menu("protomenu.submenu", text = "Operations", icon_value=get_icon_id("Noicon"))
        layout.separator()
        layout.menu("view3d.mstool_submenu", text = "MeshTools", icon_value=get_icon_id("Noicon"))
        layout.menu("inserts.objects", text="Insert", icon_value=get_icon_id("Noicon"))
        layout.menu("settings.submenu", text="Settings", icon_value=get_icon_id("Noicon"))



    # Edit Mode
    ############################################################################

    def draw_edit_mode_menu(self, layout, object):
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("bevelandsharp1.objects", text = "Make SSharp", icon_value = get_icon_id("MakeSharpE"))
        if pro_mode_enabled():
            layout.operator("transform.edge_bevelweight", text = "Bweight", icon_value = get_icon_id("AdjustBevel"))
        layout.operator("clean1.objects", text = "Clean SSharps", icon_value = get_icon_id("CleansharpsE")).clearsharps = True
        layout.separator()
        if pro_mode_enabled():
            layout.operator("clean1.objects", text = "Demote", icon_value = get_icon_id("Pizzaops")).clearsharps = False
        layout.separator()
        layout.menu("view3d.emstool_submenu", text = "MeshTools", icon_value = get_icon_id("Noicon"))

        layout.separator()
        if pro_mode_enabled():
            if addon_exists("mira_tools"):
                layout.menu("mira.submenu", text = "Mira (T)", icon="PLUGIN")

        #layout.operator("ehalfslap.object", text = "(X+) Symmetrize", icon_value = get_icon_id("Xslap"))
        layout.menu("view3d.symmetry_submenu", text = "Symmetrize", icon_value = get_icon_id("Xslap"))
        layout.separator()
                
        """if object.data.show_edge_crease == False:
            layout.operator("object.showoverlays", text = "Show Overlays", icon = "RESTRICT_VIEW_ON")
        else :
            layout.operator("object.hide_overlays", text = "Hide Overlays", icon = "RESTRICT_VIEW_OFF")"""
        
        if bpy.context.object and bpy.context.object.type == 'MESH':
            layout.menu("object.material_list_menu", text = "Material", icon_value=get_icon_id("Noicon"))
        
        layout.separator()
        layout.menu("inserts.objects", text = "Insert", icon_value = get_icon_id("Noicon"))

    # Lattice Mode
    ############################################################################

    def draw_lattice_menu(self, layout):
        layout.prop(bpy.context.object.data, "points_u", text="X")
        layout.prop(bpy.context.object.data, "points_v", text="Y")
        layout.prop(bpy.context.object.data, "points_w", text="Z")
        layout.prop(bpy.context.object.data, "use_outside")
        layout.operator("hops.simplify_lattice", text = "Simplify")
        #self.draw_options(layout)
        layout.separator()
        layout.menu("settings.submenu", text="Settings", icon_value=get_icon_id("Noicon"))

     # BoolShape Menu
    ############################################################################

    def draw_boolshape_menu(self, layout):
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("hops.adjust_bevel", text = "(B)Width", icon_value=get_icon_id("AdjustBevel"))
        layout.operator("hops.adjust_tthick", text = "(T)Thick", icon_value=get_icon_id("Tthick"))
        layout.operator("nw.a_rray", text = "(Q)Array", icon_value=get_icon_id("Qarray"))
        layout.separator()
        #layout.menu("protomenu.submenu", text = "Operations", icon_value=get_icon_id("Noicon"))
        #layout.separator()
        layout.menu("view3d.mstool_submenu", text = "MeshTools", icon_value=get_icon_id("Noicon"))
        layout.menu("settings.submenu", text="Settings", icon_value=get_icon_id("Noicon"))
        

    def draw_curve_menu(self, layout):
        layout.operator("hops.curve_bevel", text = "Curve bevel")
        
    def draw_rigging_menu(self, layout):
        layout.operator("object.create_driver_constraint", text = "Driver Constraint")

def get_current_selected_status():
    active_object = bpy.context.active_object
    other_objects = get_inactive_selected_objects()
    other_object = None
    if len(other_objects) == 1:
            other_object = other_objects[0]

    return active_object, other_objects, other_object
