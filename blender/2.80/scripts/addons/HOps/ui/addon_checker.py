import bpy
from .. utils.addons import addon_exists

used_addons = [
    ("BoxCutter",           "BoxCutter",        "https://gumroad.com/l/BoxCutter/iamanoperative"),
    ("BoolTool",            "Bool Tool 0.2",    "https://github.com/vitorbalbio/code/tree/master/BoolTool"),   
    ("mira_tools",          "Mira Tools",       "http://blenderartists.org/forum/showthread.php?366107-MiraTools"),
]

recommended_addons = [
    ("Batch Operations",    "Batch Operations", "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/BatchOperations"),
    ("AutoMirror",          "Auto Mirror",      "http://blenderaddonlist.blogspot.com/2014/07/addon-auto-mirror.html"),
    ("QuickLatticeCreate",  "Easy Lattice",     "http://blenderaddonlist.blogspot.com/2013/10/addon-quick-easy-lattice-object.html"),
    ("Blender Updater",     "Blender Updater",  "https://github.com/tobkum/BlenderUpdater/releases/tag/0.3"),
    ("mesh_edge_equalize",  "Edge Equalizer",  "https://github.com/kroopson/blenderedgeequalize/blob/master/mesh_edge_equalize_operator.py")
]

def draw_addon_diagnostics(layout, columns = 4):
    col = layout.column()
    col.label("Recommended Addons:")
    draw_addon_table(col, used_addons, columns, True)

    col = layout.column()
    col.label("Additional Addons:")
    draw_addon_table(col, recommended_addons, columns, False)

def draw_addon_table(layout, addons, columns, show_existance):
    col = layout.column()
    for i, (identifier, name, url) in enumerate(addons):
        if i % columns == 0: row = col.row()
        icon = addon_icon(identifier, show_existance)
        row.operator("wm.url_open", text = name, icon = icon).url = url

    if len(addons) % columns != 0:
        for i in range(0, columns - len(addons) % columns):
            row.label("")

def addon_icon(addon_identifier, show_existance):
    if show_existance:
        if addon_exists(addon_identifier): return "FILE_TICK"
        else: return "ERROR"
    else:
        return "NONE"
