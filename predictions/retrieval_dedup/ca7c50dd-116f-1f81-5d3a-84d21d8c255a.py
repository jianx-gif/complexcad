import cadquery as cq

# Parameters
outer_width = 60.0
outer_height = 40.0
housing_thickness = 10.0
wall_thickness = 2.0
vent_diameter = 4.0
vent_rows = 2
vent_columns = 5
vent_spacing_x = 8.0
vent_spacing_y = 6.0
rim_chamfer = 1.0
rib_width = 5.0
rib_height = 3.0
rib_length = 20.0
rib_spacing = 12.0
rib_count = 2
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
corner_circle_dia = 10.0

# Base profile: outer rectangle with a decorative corner circle (subtractive mode for vent hole later)
base_sketch = (
    cq.Sketch()
    .rect(outer_width, outer_height)
    .circle(corner_circle_dia, mode="s")
)

# Extrude base solid
solid = (
    cq.Workplane("XY")
    .placeSketch(base_sketch)
    .extrude(housing_thickness)
)

# Shell to create thin walls
solid = solid.shell(-wall_thickness)

# Add chamfered rim on outer vertical edges
solid = solid.edges("|Z").chamfer(rim_chamfer)

# Add external stiffening ribs on the top face
rib_face = solid.faces(">Z")
rib_pattern = (
    rib_face.workplane()
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
solid = solid.union(rib_pattern)

# Add vent apertures on the right side wall
vent_face = solid.faces(">X")
vent_pattern = (
    vent_face.workplane(centerOption="CenterOfBoundBox")
    .rarray(vent_spacing_x, vent_spacing_y, vent_columns, vent_rows)
    .circle(vent_diameter/2)
    .cutBlind(-wall_thickness)
)
solid = solid.union(vent_pattern)

# Add mounting holes on left and right side walls
mount_face_left = solid.faces("<X")
mount_face_right = solid.faces(">X")
mount_points = [(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)]
solid = (
    mount_face_left.workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
    .faces(">X")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

result = solid