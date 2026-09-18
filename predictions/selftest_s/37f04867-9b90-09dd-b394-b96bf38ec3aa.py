import cadquery as cq

outer_radius = 30
wall_thickness = 5
height = 70
guide_length = 40
inner_radius_bottom = outer_radius - wall_thickness
inner_radius_top = inner_radius_bottom - 5
entry_chamfer = 2
clearance_hole_diameter = 5
hole_circle_radius = 15
notch_width = 8
notch_height = 12
notch_depth = 2
mid_height = height / 2

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height - guide_length)
    .lineTo(inner_radius_bottom, height - guide_length)
    .lineTo(inner_radius_top, height)
    .lineTo(0, height)
    .lineTo(0, 0)
    .close()
)

solid = profile.revolve()

solid = solid.faces(">Z").edges().chamfer(entry_chamfer)

notch_box = (
    cq.Workplane('XY')
    .center(outer_radius - notch_depth / 2, 0)
    .box(notch_depth, notch_width, notch_height)
    .translate((0, 0, mid_height))
)
solid = solid.cut(notch_box)

solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(count=5, radius=hole_circle_radius, startAngle=0, angle=360)
    .hole(clearance_hole_diameter)
)

result = solid