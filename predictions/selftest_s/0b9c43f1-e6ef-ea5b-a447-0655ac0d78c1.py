import cadquery as cq

height = 80.0
radius_bottom = 20.0
radius_top = 35.0
wall_thickness = 2.0
spot_radius = 5.0
spot_depth = 1.5
chamfer_size = 0.8
spot_offset = radius_bottom / 2.0

profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(radius_bottom, 0)
    .lineTo(radius_top, height)
    .lineTo(0, height)
    .close()
)

solid = profile.revolve(360)

result = (
    solid
    .shell(-wall_thickness)
    .edges().chamfer(chamfer_size)
    .workplane(offset=height)
    .center(spot_offset, 0)
    .circle(spot_radius)
    .cutBlind(-spot_depth)
)
