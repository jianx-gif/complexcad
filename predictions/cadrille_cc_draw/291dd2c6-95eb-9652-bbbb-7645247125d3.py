import cadquery as cq
outer_diameter = 70
inner_diameter = 30
thickness = 8
rib_width = 6
rib_height = 4
rib_spacing = 12
chamfer_size = 1
hole_diameter = 8
hole_offset = 10
hole_count = 6
hole_radius = outer_diameter / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_count = int(360 / rib_spacing)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius + rib_width, rib_height)
    .lineTo(inner_radius + rib_width, rib_height + rib_height)
    .lineTo(inner_radius + rib_width, rib_height + rib_height)
    .lineTo(inner_radius, rib_height + rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .circle(rib_width)
    .extrude(rib_height)
    .translate((0, 0, rib_height / 2.0))
)
solid = solid.union(rib)
hole_positions = [(-hole_offset, 0), (hole_offset, 0), (0, hole_offset), (hole_offset, 0)])
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    hole_positions.append((hole_offset, 0))
solid = solid.cut(hole_positions)
result = solid
