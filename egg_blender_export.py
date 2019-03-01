import traceback

import bpy

from .egg import Egg, Entry


def save(context, export_settings):
    _start(context)

    try:
        egg = Egg()
        exporter = EggExporter(egg, export_settings)
        exporter.export_globals()
        exporter.export_scenes()
        # exporter.export_animations()
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print('cannot complete Egg Export: {}'.format(err))
    else:
        _write(egg, export_settings)
    finally:
        _end(context)


def _start(context):
    pass


class EggExporter():
    """
    Extract necessary information from the blender file.
    """
    def __init__(self, egg, export_settings):
        self.egg = egg
        self.export_settings = export_settings

    def export_globals(self):
        coordinate_entry = Entry('CoordinateSystem', content='Z-up')
        self.egg.append(coordinate_entry)

    def export_scenes(self):
        for scene in bpy.data.scenes:
            self._export_scene(scene)

    def _export_scene(self, scene):
        for blend_object in scene.objects:
            self._export_blend_object(blend_object)

    def _export_blend_object(self, blend_object):
        # if blend_object.type == 'MESH':
        # if blend_object.type == bpy.types.MESH:
        if blend_object.type == 'MESH':
            self._export_mesh_data(blend_object)

    def _export_mesh_data(self, blend_object):
        """
        TODO: The polygon entries for each mesh must be the triangles, not quads or n-gons.
        """
        mesh_entry = Entry('Group', name=blend_object.name)
        for polygon in blend_object.data.polygons:
            vertex_indices = tuple([v for v in polygon.vertices])
            vertex_ref_entry = Entry('VertexRef', content=vertex_indices)
            vertex_ref_entry.append(Entry("Ref", content=blend_object.data.name))
            mesh_entry.append(Entry('Polygon', content=vertex_ref_entry))

        self.egg.append(mesh_entry)

        vertex_pool_entry = Entry('VertexPool', name=blend_object.data.name)
        for vertex in blend_object.data.vertices:
            vertex_attributes = [(blend_object.matrix_world * vertex.co).to_tuple()]
            vertex_pool_entry.append(
                Entry('Vertex', name=vertex.index, content=vertex_attributes),
            )

        self.egg.append(vertex_pool_entry)

    def export_animations(self):
        animation_entries = []

        return animation_entries


def _write(egg, export_settings):
    with open(export_settings['egg_filepath'], 'wb') as eggfile:
        output = [bytes(line + '\n', export_settings['egg_file_format']) for line in egg.format_output()]
        eggfile.writelines(output)


def _end(context):
    pass
