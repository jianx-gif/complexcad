import cadquery as cq

overall_length = 80
outer_diameter = 50
inner_bore_diameter = 20
wall_thickness = (outer_diameter - inner_bore_diameter) / 2
chamfer_length = 2
fastener_hole_diameter = 6
fastener_hole_offset = 15
rib_height = 8
rib_thickness = 3
rib_count = 8
rib_extrude = wall_thickness

groove_outer_diameter = 30
groove_inner_diameter = 24
groove_depth = 4

def base_housing():
    outer = cq.Workplane('XY').cylinder(overall_length, outer_diameter / 2)
    bore = cq.Workplane('XY').cylinder(overall_length + 2, inner_bore_diameter / 2)
    housing = outer.cut(bore)
    housing = housing.faces('>Z').edges().chamfer(chamfer_length)
    return housing

def add_fastener_holes(part):
    hole1 = (
        cq.Workplane('YZ')
        .center(0, fastener_hole_offset)
        .cylinder(outer_diameter + 2, fastener_hole_diameter / 2)
    )
    hole2 = (
        cq.Workplane('YZ')
        .center(0, -fastener_hole_offset)
        .cylinder(outer_diameter + 2, fastener_hole_diameter / 2)
    )
    part = part.cut(hole1).cut(hole2)
    return part

def add_o_ring_groove(part):
    part = part.faces('>Z').workplane(centerOption='CenterOfMass')
    part = part.circle(groove_outer_diameter / 2).circle(groove_inner_diameter / 2).cutBlind(groove_depth)
    return part

def add_ribs(part):
    angle_step = 360 / rib_count
    for i in range(rib_count):
        rib = (
            cq.Workplane('XZ')
            .rect(rib_thickness, rib_height)
            .extrude(rib_extrude)
            .translate((outer_diameter / 2, 0, 0))
            .rotate((0, 0, 0), (0, 0, 1), i * angle_step)
        )
        part = part.union(rib)
    return part

result = base_housing()
result = add_fastener_holes(result)
result = add_o_ring_groove(result)
result = add_ribs(result)
