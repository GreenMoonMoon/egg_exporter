
# built-in
from mathutils import Vector
from collections import defaultdict

# blender
import bpy
import bpy.types


GROUP = 'Group'
VERTEX_POOL = 'VertexPool'
VERTEX = 'Vertex'
POLYGON = 'Polygon'


class Entry():
    def __init__(self, entry_type, name, attributes=None):
        self.entry_type = entry_type
        self.name = name
        self.attributes = attributes


def start(export_settings):
    """
    Start the export process by storing the blender current state.
    """
    pass


def end(export_settings):
    """
    Restore blender state and delete temporary objects.
    """
    pass


def save(context, export_settings):
    # bpy.context.window_manager.process_begin(0, 100)
    # bpy.context.window_manager.process_update(0)

    start(export_settings)

    blender_objects = filter_objects(export_settings)
    egg = generate_egg(blender_objects, export_settings)
    formatted_egg = format_egg(egg)
    write_egg(formatted_egg, export_settings)

    end(export_settings)

    # bpy.context.window_manager.process_end()

    return {'FINISHED'}


# ===========================================================================

def generate_egg(blender_objects, export_settings):
    egg = defaultdict(dict)

    generate_globals_entries(egg, export_settings)

    for obj in blender_objects:
        if type(obj.data) == bpy.types.Mesh:
            add_mesh_entry(obj, egg, export_settings)


def add_mesh_entry(obj, egg, export_settings): 
    vertex_pool_attributes = []

    for vertex in obj.data.vertices:
        vertex_pool_attributes.append(Entry(VERTEX, vertex.index, obj.world_matrix * vertex.co))

    if obj.data.name not in egg['vertex_pools']:
        egg['vertex_pools'][obj.data.name] = Entry(VERTEX_POOL, obj.data.name, vertex_pool_attributes)

    group_attributes = []

    for polygon in obj.data.polygons:
        polygon_attributes = None
        group_attributes.apppend(Entry(POLYGON, polygon.index, polygon_attributes))

    egg['groups'][obj.name] = Entry(GROUP, obj.name, group_attributes)


def generate_globals_entries(export_settings, egg):
    """
    Write the global information entries.
    """
    egg['globals'] = '<CoordinateSystem> {{ Z-up }}\n'


def generate_texture_entries(export_settings, egg):
    pass


def generate_material_entries(export_settings, egg):
    pass


def write_egg(egg_formatted, export_settings):
    egg_file = open(export_settings['file_path'], 'wb')
    egg_file.writelines(egg_formatted)
    egg_file.close()

def format_egg(egg):
    pass


# ======================================================================================================================

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
    else:
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
            polygon_entries.append(entry('Polygon', polygon.index, polygon.vertices))

        egg.append(entry('Group', obj_mesh.name, polygon_entries))


if __name__ == '__main__':
    export_settings = {
        'selected_only': False,
    }
    egg = []

    filtered_objects = filter_objects(export_settings)

    write_meshes(egg, filtered_objects['meshes'])

    print(egg)
