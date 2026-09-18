import cadquery as cq
outer_radius = 40
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base_radius = outer_radius - wall_thickness
base_height = 100
base_chamfer = 2
hole_diameter = 4
hole_spacing = 30
hole_offset = 10
chamfer_size = 1
base = (
    cq.Workplane("XY")
    .rect(outer_radius, outer_radius)
    .extrude(base_height)
)
inner_cyl = (
    cq.Workplane("XY")
    .center(outer_radius - wall_thickness/2, 0)
    .rect(inner_radius, inner_radius)
    .extrude(base_height)
)
base = base.cut(inner_cyl)
base = base.edges("|Z").chamfer(chamfer_size)
base = base.edges("|Z").chamfer(chamfer_size)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces("<Z").edges().fillet(base_chamfer)
result = base
