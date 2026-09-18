import cadquery as cq

outer_diameter = 80.0
outer_diameter = 60.0
outer_diameter = 10.0
outer_diameter = 10.0
inner_diameter = 2.0
inner_diameter = 1.0
inner_diameter = 1.0
inner_diameter = 1.0
inner_diameter = 1.0
inner_diameter = 0.5
hole_diameter = 0.5
hole_count = 0.8

hole_count = 0.8
hole_count = 0.8
hole_count = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_spacing = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
rib = (
    cq.Workplane('XY')
    .box(rib_length, rib_width, rib_height)
    .faces('>Z')
    .faces('>Z')
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
    .faces(">Z')
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
    .faces(">Z')
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
)
