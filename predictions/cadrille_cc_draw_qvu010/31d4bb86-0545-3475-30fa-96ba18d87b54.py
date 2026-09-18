import cadquery as cq
plate_width = 80.0
plate_height = 40.0
plate_thickness = 15.0
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, 2, 1)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, 2, 1)
    .hole(hole_diameter)
)
result = (
    result.faces("<Z").workplane()
    .rarray(hole_spacing, 0, 2, 1)
    .hole(hole_diameter)
)
result = (
    result.faces("<Z").workplane()
    .rarray(hole_spacing, 0, 2, 1)
    .hole(hole_diameter)
)
