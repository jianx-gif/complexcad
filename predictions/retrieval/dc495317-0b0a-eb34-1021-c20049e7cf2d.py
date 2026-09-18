import cadquery as cq

lever_total_length = 80
lever_base_diameter = 30
lever_tip_diameter = 10
taper_length = 30
counterbore_diameter = 20
counterbore_depth = 12
chamfer_distance = 3

base_radius = lever_base_diameter / 2.0
tip_radius = lever_tip_diameter / 2.0
body_length = lever_total_length - taper_length

profile = (
    cq.Workplane("ZY")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, body_length)
    .lineTo(tip_radius, lever_total_length)
    .lineTo(0, lever_total_length)
    .close()
    .wire()
)

solid = profile.revolve()

# try chamfer on all edges
result = solid.edges().chamfer(chamfer_distance)
