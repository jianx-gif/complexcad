import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_height = 6.0
rib_stem_width = 12.0
rib_top_width = 30.0
rib_top_thickness = 6.0
hole_diameter = 8.0
corner_offset = 12.0
edge_chamfer = 1.0

base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# central clearance hole
base = base.faces(">Z").workplane().hole(hole_diameter)

# corner clearance holes (four)
corner_pattern = base.faces(">Z").workplane()
corner_pattern = corner_pattern.rect(plate_length - 2*corner_offset, plate_width - 2*corner_offset, forConstruction=True).vertices().hole(hole_diameter)
base = corner_pattern

# extrude T‑shaped rib on top surface
rib_stem = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_stem_width, plate_width)
    .extrude(rib_height)
)

rib_flange = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_top_width, rib_top_thickness)
    .extrude(rib_height + rib_top_thickness)
    .translate((0, 0, plate_thickness - rib_top_thickness))
)

rib = rib_stem.union(rib_flange)

result = base.union(rib).edges("|Z").chamfer(edge_chamfer)
