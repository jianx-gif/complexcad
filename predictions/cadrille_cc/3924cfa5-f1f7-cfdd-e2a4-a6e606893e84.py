import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
height = 30.0
wall_thickness = 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(outer_radius, outer_radius)
    .extrude(height)
)
inner = (
    cq.Workplane("XY")
    .rect(inner_radius, inner_radius)
    .extrude(height)
)
base = base.cut(inner)
base = base.edges("|Z").fillet(fillet_radius)
base = base.edges("|Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
result = base
