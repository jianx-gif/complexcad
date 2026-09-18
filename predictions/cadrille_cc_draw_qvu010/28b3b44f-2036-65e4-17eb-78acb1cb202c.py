import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 15.0
rib_width = 12.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = thickness / 2.0
hole_spacing = 20.0
rib_count = int(36)
rib_positions = [(-inner_diameter/2 + rib_spacing/2, 0) for i in range(rib_count)]
result = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
