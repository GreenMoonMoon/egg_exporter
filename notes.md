# General notes

* Setttings can be divided in two category, scene and user. Scene preferences like the type of export should be saved in the scene itself. For example a scene used for storing animation always export AnimationOnly, this setting should not be saved as user since not all scene are made for animation. User preferences are general user prefs for exporting. For example the type of texture, normals or the use of pView are setting that seldom change within the same project.
* The general goal of an exporter is to reproduce the content of the scene within the receiver of the format we export to.

## Format

### Global Information Entries
* CoordinateSystem : Y-up, Z-up, Y-up-right(same as Y-up), Z-up-right(same as Z-up), Y-up-left, Z-up-left
* Texture : (Declared here to enable specifiying more than the default attributes)
* Material
* VertexPool: ()

## TODOs
### Baking Procedural textures.