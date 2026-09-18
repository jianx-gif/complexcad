import cadquery as cq
outer_radius = 50.0
inner_radius = 15.0
thickness = 8.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(outer_radius, outer_radius)
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = base.edges("|Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().center(0, 0).rect(hole_spacing, hole_offset).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(0, 0).rect(hole_spacing, hole_offset).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(0, 0).circle(hole_diameter/2).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(0, 0).circle(hole_diameter/2).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(0, 0).circle(hole_diameter/2).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(h