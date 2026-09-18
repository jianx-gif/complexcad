import cadquery as cq
plate_width = 80.0
plate_height = 60.0
plate_thickness = 10.0
rib_height = 5.0
rib_width = 12.0
rib_spacing = 12.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(rib_height)
)
rib = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (-plate_width/2 + hole_spacing, -plate_height/2 + hole_spacing),
    ( plate_width/2 - hole_spacing, -plate_height/2 + hole_spacing),
    (-plate_width/2 + hole_spacing,  plate_height/2 - hole_spacing),
    ( plate_width/2 - hole_spacing,  plate_height/2 - hole_spacing)
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
