import cadquery as cq
clamp_length = 80.0
clamp_width = 40.0
clamp_height = 20.0
material_thickness = 4.0
cavity_radius = 8.0
cavity_offset = 10.0
vent_spacing_x = 10.0
vent_spacing_y = 6.0
vent_rows = 2
vent_cols = 3
vent_rows = 2
vent_hole_diameter = 4.0
vent_hole_depth = clamp_height - 2.0
chamfer_dist = 0.8
mount_hole_dia = 3.0
mount_hole_offset = clamp_width/2 - 10.0
base = (
    cq.Workplane("XY")
    .rect(clamp_length, clamp_width)
    .extrude(clamp_height)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(cavity_radius)
    .extrude(clamp_height)
)
rib = rib.translate((0, 0, clamp_height))
rib = rib.translate((0, 0, clamp_height))
rib = rib.translate((0, 0, clamp_height))
rib = rib.translate((0, 0, clamp_height))
vent_cut = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(vent_hole_diameter/2)
    .extrude(vent_hole_depth)
    .translate((0, 0, clamp_height))
)
vent_cut = vent_cut.union(rib)
vent_cut = vent_cut.faces(">Z").edges().chamfer(chamfer_dist)
vent_cut = vent_cut.faces(">Z").workplane().hole(vent_hole_diameter)
vent_cut = vent_cut.faces("<Z").workplane().center(vent_hole_offset, 0).hole(vent_hole_diameter)
vent_cut = vent_cut.faces(">Z").workplane().center(vent_hole_offset, 0).hole(vent_hole_diameter)
rib = rib.translate((0, 0, clamp_height - 2.0))
rib = rib.translate((0, 0, clamp_height - 2.0))
result = vent_cut.union(rib)
