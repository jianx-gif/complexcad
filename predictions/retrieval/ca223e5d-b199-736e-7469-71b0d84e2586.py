import cadquery as cq

# Dimensions
enclosure_height = 50.0
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
top_fillet_radius = 2.0
rib_width = 4.0
rib_height = enclosure_height - 10.0
rib_count = 4
hole_diameter = 3.0
hole_pitch = 20.0
hole_rows = 2
hole_columns = 3

# Base revolved enclosure (outer and inner walls)
profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, enclosure_height - top_fillet_radius)
    .threePointArc((inner_radius + top_fillet_radius, enclosure_height - top_fillet_radius/2), (outer_radius, enclosure_height - top_fillet_radius))
    .lineTo(outer_radius, enclosure_height)
    .lineTo(outer_radius, 0)
    .close()
)
base = profile.revolve(360)

# Interior ribs (radial fins attached to inner wall)
rib = (
    cq.Workplane('XY')
    .box(wall_thickness, rib_width, rib_height)
    .translate((inner_radius, 0, enclosure_height/2 - rib_height/2))
)
# Pattern ribs around circumference
ribs = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))
base_with_ribs = base.union(ribs)

# Add top surface mounting holes pattern using offset workplane
with_holes = (
    base_with_ribs.workplane(offset=enclosure_height)
    .rarray(hole_pitch, hole_pitch, hole_columns, hole_rows, center=True)
    .hole(hole_diameter)
)
# Fillet top outer edge
result = with_holes.faces('>Z').edges().fillet(top_fillet_radius)
