import cadquery as cq
outer_diameter = 80.0
wall_thickness = 4.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 6
hole_offset = 20.0
rib_width = 10.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .moveTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .line