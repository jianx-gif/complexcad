import cadquery as cq

# Parameters
channel_width = 60.0
channel_height = 30.0
wall_thickness = 5.0
length = 100.0
lip_thickness = 2.0
fillet_radius_inner = 2.0
weld_plate_width = 30.0
weld_plate_height = 20.0
weld_plate_thickness = 4.0
blind_hole_diameter = 8.0
blind_hole_depth = 12.0
blind_hole_offset_along = 30.0
blind_hole_offset_from_top = 5.0
rib_thickness = 3.0
rib_width = 10.0
rib_spacing = 20.0

# Outer dimensions
outer_width = channel_width + 2 * wall_thickness
outer_height = channel_height + wall_thickness + lip_thickness

# Sketch outer profile with lip on top
points = [
    (-outer_width/2, -outer_height/2),
    ( outer_width/2, -outer_height/2),
    ( outer_width/2,  outer_height/2 - lip_thickness),
    ( channel_width/2 + wall_thickness, outer_height/2 - lip_thickness),
    ( channel_width/2 + wall_thickness, outer_height/2),
    (-channel_width/2 - wall_thickness, outer_height/2),
    (-outer_width/2,  outer_height/2 - lip_thickness),
    (-outer_width/2, -outer_height/2)
]
outer_sketch = cq.Sketch().polygon(points)

# Extrude outer shape
outer_solid = (
    cq.Workplane("XY")
    .placeSketch(outer_sketch)
    .extrude(length)
)

# Inner channel cut
inner_sketch = cq.Sketch().rect(channel_width, channel_height)
inner_cut = (
    cq.Workplane("XY")
    .placeSketch(inner_sketch)
    .extrude(length)
)
base = outer_solid.cut(inner_cut)

# Fillet inner corners (inner wall edges)
base = base.edges("<<Z and >Y").fillet(fillet_radius_inner)

# Weld splice plate added on outer +Y side (no additional fillet)
splice = (
    base.faces(">Y")
    .workplane(offset=0)
    .rect(weld_plate_width, weld_plate_height)
    .extrude(weld_plate_thickness)
)
base = base.union(splice)

# Blind hole drilled into side wall near top interior
hole_center_y = channel_height/2 - blind_hole_offset_from_top
hole_center_z = -length/2 + blind_hole_offset_along
hole_center_x = -channel_width/2 + blind_hole_depth/2
cylinder = (
    cq.Workplane("YZ")
    .circle(blind_hole_diameter/2)
    .extrude(blind_hole_depth)
    .translate((hole_center_x, hole_center_y, hole_center_z))
)
base = base.cut(cylinder)

# Exterior ribs on +Y face, spaced along length
rib = (
    base.faces(">Y")
    .workplane(offset=0)
    .rect(rib_width, rib_width)
    .extrude(rib_thickness)
)
num_ribs = int(length / rib_spacing)
for i in range(num_ribs):
    offset_z = -length/2 + rib_spacing/2 + i * rib_spacing
    rib_instance = rib.translate((0, 0, offset_z))
    base = base.union(rib_instance)

result = base