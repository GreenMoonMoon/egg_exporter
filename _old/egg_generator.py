
import bpy
import bpy.types
from mathutils import Vector


class EggEntry():
    """
    Basic represetation of an Egg Entry.
    """
    def __init__(self, entry_type, name, data):
        self.entry_type = entry_type
        self.name = name
        self.data = data

    def __str__(self):
        """
        Used to generate the final document.
        """
        formatted_data = _format_data(self.data)
        return '<{}> {} {{{}}}'.format(self.entry_type, self.name, formatted_data)


def filter_objects(export_settings):
    """
    Get and filter objects.
    """
    # objects = bpy.data.objects

    filtered_objects = {
        'meshes': [],
    }

    for obj in bpy.data.objects:
        # Remove unused objects
        if obj.users == 0:
            continue

        if export_settings['selected_only'] and not obj.select:
            continue

        # Filter layers ???

        # filtered_objects.append(obj)
        if type(obj.data) == bpy.types.Mesh:
            filtered_objects['meshes'].append(obj)            

    print(filtered_objects)

    return filtered_objects


def entry(type, name, data):
    """
    Create egg entries from type, name and data.
    TODO: Handle line separations.
    """
    formatted_data = _format_data(data)
    return '<{}> {} {{{}}}'.format(type, name, formatted_data)


def _format_data(data):
    if isinstance(data, Vector):
        return ' '.join([str(f) for f in data])
    if isinstance(data, list):
        return '\n'.join([str(e) for e in data])

    return data


def write_meshes(egg, obj_meshes):
    """
    TODO: This function adresses two concerns, both getting data and formatting the
    output.
    """
    for obj_mesh in obj_meshes:
        mesh = obj_mesh.data
        world_matrix = obj_mesh.matrix_world

        # a vertex entry is only valid within a vertex pool.
        # this function might be split
        vertice_entries = []
        for vertex in mesh.vertices:
            vertice_entries.append(entry('Vertex', vertex.index, world_matrix * vertex.co))

        egg.append(entry('VertexPool', mesh.name, vertice_entries))

        polygon_entries = []
        for polygon in mesh.polygons:
            polygon_entries.append(entry('Polygon', polygon.index, [p for p in polygon.vertices]))

        egg.append(entry('Group', obj_mesh.name, polygon_entries))
