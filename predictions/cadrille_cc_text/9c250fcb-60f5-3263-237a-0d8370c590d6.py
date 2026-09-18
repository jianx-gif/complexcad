import cadquery as cq
base_length = 80.0
base_width = 30.0
base_thickness = 8.0
lip_height = 12.0
lip_thickness = 4.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 50.0
hole_offset = 10.0
rib_width = 5.0
rib_depth = 2.0
rib_height = 3.0
rib_spacing = 20.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(base_length - 2 * lip_thickness, base_width - 2 * lip_thickness)
    .cutBlind(-lip_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(base_length - 2 * lip_thickness, base_width - 2 * lip_thickness)
    .cutBlind(-lip_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(base_length - 2 * lip_thickness, rib_width)
    .extrude(rib_height)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_depth)
    .extrude(rib_height)
)
base = base.union(base)
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(hole_offset, y_spacing), (hole_offset, y_spacing)])
    .hole(hole_diameter)
)
rib_count = int((base_width - 2 * rib_spacing) // rib_spacing)
ribs = cq.Workplane("XY")
for x_offset in (-base_width/2 + rib_spacing, base_offset/2 - rib_spacing):
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_depth)
        .extrude(rib_height)
        .translate((x_offset, 0, base_thickness))
    )
    ribs = ribs.union(rib)
result = base.union(ribs)
