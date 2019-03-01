# built-in
import os

# blender
import bpy
from bpy import props
from bpy_extras.io_utils import ExportHelper

# internal
from .egg_blender_export import save

bl_info = {
    'name': 'Panda3D EGG format',
    'author': 'Josue (GreenMoonMoon) Boisvert',
    'blender': (2, 68, 0),
    'location': 'File > Export',
    'description': 'Export as EGG(Panda3D)',
    'warning': '',
    'category': 'Import-Export',
}


# class ExportEGGScenePreferences(bpy.types.Operator):
#     """
#     Store relevant preferences within the scene. Toggling off save preferences
#     will delete current scene preferences.
#     """
#     bl_label = 'Scene Preferences'
#     bl_idname = 'scene.yabee_preferences'

#     def execute(self, context):
#         operator = context.active_operator
#         operator.save_scene_pref = not operator.save_scene_pref
#         if not operator.save_scene_pref and context.scene.get(
#             operator.scene_key, False,
#         ):
#             del context.scene[operator.scene_key]
#         return {'FINISHED'}


class ExportEGGPreferences(bpy.types.AddonPreferences):
    """
    Preferences class for saving addon preferences.
    """
    bl_idname = __name__

    test = props.StringProperty(name='Test property', description='for testing purposes', default='this is default')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "test")


class ExportEGG(bpy.types.Operator, ExportHelper):
    """
    Export selected to the Panda3D EGG format
    """
    bl_idname = "export.panda3d_egg"
    bl_label = "Export to Panda3D EGG"

    filename_ext = ".egg"
    filter_glob = props.StringProperty(default="*.egg", options={'HIDDEN'},)
    export_format = 'ASCII'

    scene_key = 'exportpanda3deggsetting'

    def execute(self, context):
        # TODO: Gather export settings
        export_settings = {}

        export_settings['egg_file_format'] = 'UTF-8'

        export_settings['egg_filepath'] = bpy.path.ensure_ext(self.filepath, self.filename_ext)
        export_settings['egg_exportdir'] = os.path.dirname(export_settings['egg_filepath']) + '/'

        save(context, export_settings)

        return {'FINISHED'}

    def invoke(self, context, event):
        return ExportHelper.invoke(self, context, event)

    def draw(self, context):
        pass


def menu_func_export(self, context):
    self.layout.operator(ExportEGG.bl_idname, text='Panda3D EGG (.egg)')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
