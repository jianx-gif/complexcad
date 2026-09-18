import cadquery as cq

outer_length = 80.0
outer_width = 50.0
outer_height = 30.0
wall_thickness = 2.0
front_fillet_radius = 3.0
rib_thickness = 2.0
rib_height = 15.0
num_ribs = 4
boss_diameter = 10.0
boss_height = 8.0
boss_margin = 5.0

inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness
rib_spacing = (inner_length - rib_thickness) / (num_ribs - 1)

result = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .rect(inner_length, inner_width)
    .cutBlind(-inner_height)
    .faces("<X")
    .edges("|Z")
    .fillet(front_fillet_radius)
    .faces("<Z")
    .workplane()
    .rect(rib_thickness, inner_width)
    .rarray(rib_spacing, 0, num_ribs, 1)
    .extrude(rib_height)
    .faces("<Y")
    .workplane()
    .center(0, inner_height/2)
    .circle(boss_diameter/2)
    .extrude(boss_height)
)
