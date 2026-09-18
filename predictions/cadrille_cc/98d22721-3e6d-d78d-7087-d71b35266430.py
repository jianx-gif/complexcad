import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 15.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length, 0),
        (leg_length, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_width),
        (0, leg_width),
    ])
    .close()
    .extrude(thickness)
)
rib = (
    base.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.faces(">Z").workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.union(rib)
result = rib
