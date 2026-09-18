import cadquery as cq
outer_radius = 80.0
outer_radius = 20.0
wall_thickness = 40.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 4.0
wall_thickness = 1.0
wall_thickness = 1.0
wall_thickness = 2.0
wall_thickness = 1.0
wall_thickness = 1.0
hole_positions = 2.0

hole_cols = 1.0
hole_cols = 1.0
hole_cols = 1.0
hole_cols = 1.0
hole_cols = 0.5
hole_cols = 0.5
hole_cols = 0.5
hole_cols = cq.Workplane('XY').box(200,outer_length, 200).union(w0.sketch().segment((-95,-48),(-65,-48)).segment((-66,-40)).segment((-76,-40)).segment((-76,-12)).segment((-68,-12)).segment((-69,1)).segment((-66,1)).segment((-66,2)).segment((-65,2)).segment((-65,10)).segment((-95,10)).close().assemble().reset().face(w0.sketch().segment((-60,2),(-59,2)).segment((-59,-12)).segment((-58,-12)).segment((-58,-40)).segment((100,-40)).segment((100,2)).segment((70,2)).segment((70,9)).segment((20,9)).segment((20,28)).segment((-20,28)).segment((-20,9)).segment((-60,9)).close().assemble()).push([(1,-15)]).circle(10,mode='s').finalize().extrude(-40)).union(w0.workplane(offset=50/2).box(200,116,50))