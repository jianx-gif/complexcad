import cadquery as cq

pipe_outer_radius = 10
pipe_thickness = 2
pipe_centerline_radius = 30
chamfer_distance = 1
thread_cavity_diameter = 6
thread_cavity_depth = 8
boss_width = 12
boss_height = 6
boss_length = 8
countersink_diameter = thread_cavity_diameter * 1.5
countersink_angle = 82

profile = cq.Workplane('XY').circle(pipe_outer_radius)
path = (cq.Workplane('XZ')
        .moveTo(pipe_centerline_radius, 0)
        .threePointArc((pipe_centerline_radius, pipe_centerline_radius), (0, pipe_centerline_radius))
        )
outer_elbow = profile.sweep(path)
result = outer_elbow.shell(-pipe_thickness)
result = result.edges().chamfer(chamfer_distance)
result = (result
          .faces('>X')
          .workplane()
          .cskHole(thread_cavity_diameter, countersink_diameter, countersink_angle, depth=thread_cavity_depth)
          )
result = (result
          .faces('>Z')
          .workplane()
          .rect(boss_width, boss_height)
          .extrude(boss_length)
          )
result = (result
          .faces('>X')
          .workplane()
          .rect(4, 4)
          .cutBlind(6)
          )