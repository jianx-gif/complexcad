import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
thickness = 20.0
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
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = base.edges("|Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().center(0, 0).rect(hole_spacing, hole_offset).cutBlind(-wall_thickness)
base = base.faces(">Z").workplane().center(0, hole_offset).rect(hole_spacing, hole_offset).cutBlind(-wall_thickness)
base = base.faces(">Z").workplane().center(0, hole_offset).rect(hole_spacing, hole_offset).cutBlind(-wall_thickness)
base = base.faces(">Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_spacing, hole_offset).hole(hole_diameter)
result = base
