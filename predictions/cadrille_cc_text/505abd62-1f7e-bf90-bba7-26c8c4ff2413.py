import cadquery as cq
cavity_width = 80.0
cavity_length = 60.0
cavity_height = 15.0
dome_radius = 30.0
dome_cut_depth = 12.0
vent_slot_width = 20.0
vent_slot_height = 5.0
vent_slot_offset = 10.0
rib_height = 5.0
rib_thickness = 3.0
rib_notch_width = 4.0
rib_notch_height = 2.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 8.0
base = cq.Workplane('XY').box(cavity_width, cavity_length, cavity_height)
base = base.edges().chamfer(chamfer_size)
vent = (
    cq.Workplane('XY')
    .polyline([
        (0, 0),
        (cavity_width, 0),
        (cavity_width, cavity_length - dome_cut_depth),
        (cavity_width - dome_cut_depth, cavity_length - dome_cut_depth),
        (cavity_width - dome_cut_depth, cavity_length),
        (0, cavity_length),
    ])
    .close()
    .extrude(cavity_height)
)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_notch_width)
    .translate((0, 0, cavity_height))
)
rib = rib.union(rib)
result = base.union(rib)
result = result.edges().chamfer(chamfer_size)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.edges().chamfer(chamfer_size)
