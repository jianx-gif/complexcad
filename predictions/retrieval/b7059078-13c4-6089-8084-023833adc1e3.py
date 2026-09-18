import cadquery as cq
import math

outer_radius = 40.0
inner_radius = 30.0
height = 50.0
base_chamfer = 2.0
thread_pitch = 5.0
thread_depth = 2.0
relief_groove_width = 5.0
relief_groove_position = height / 2.0
counterbore_diameter = 10.0
counterbore_depth = 8.0

profile = cq.Workplane('XY').polyline([(outer_radius,0),(inner_radius,height),(inner_radius,0)]).close()
body = profile.revolve()
body = body.faces('<Z').edges().chamfer(base_chamfer)
thread_path = cq.Wire.makeHelix(pitch=thread_pitch, height=height, radius=inner_radius - thread_depth/2.0)
thread_profile = cq.Workplane('XZ').polyline([(-thread_depth,0),(thread_depth,0),(0,thread_pitch/2.0),(-thread_depth,0)]).close().wire()
thread_cut = thread_profile.sweep(thread_path)
body = body.cut(thread_cut)
# groove
body = body.cut(
    cq.Workplane('XY').cylinder(relief_groove_width, inner_radius - thread_depth - 0.5).translate((0,0,relief_groove_position))
)
body = body.faces('>Z').hole(counterbore_diameter, depth=counterbore_depth)
result = body