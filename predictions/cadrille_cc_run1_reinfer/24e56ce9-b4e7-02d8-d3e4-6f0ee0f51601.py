import cadquery as cq
outer_diameter = 60.0
inner_diameter = 40.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 12.0
rib_thickness = 5.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
result = rib
for i in range(1, hole_offset):
    angle = i * 360.0 / hole_spacing
    rib_i = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rib_i)
result = result.edges('|Z').chamfer(chamfer_size)
