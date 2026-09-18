import cadquery as cq
base = 80.0 0.80.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 4.0
wall_thickness = 1.0
wall_thickness = 2.0
wall_thickness = 2.0
wall_thickness = 2.0
wall_thickness = 2.0
wall_thickness = 2.0
wall_thickness = 2.0
hole = wall = cq.Workplane('XY').circle(outer_radius).extrude(- wall_thickness)
solid = solid = solid.faces('>Z').shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell(-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness).shell((-wall_thickness/2),(-wall_thickness/2).finalize().extrude(-wall_thickness).shell(-wall_thickness/2).shell(-wall_thickness/2).shell(-wall_thickness/2).shell((-wall_thickness/2).shell((-wall_thickness/2).finalize().extrude(-wall_thickness).shell(0.sketch().face(w0.sketch().segment((-100,-75),(100,-75)).segment((100,-50)).segment((-21,-50)).segment((-21,-48)).segment((-75,-50)).segment((-75,-14)).segment((-88,-18)).segment((-88,-50)).segment((-95,-50)).segment((-95,-67)).segment((-99,-67)).segment((-99,-74)).close().assemble()).reset().face(w0.sketch().segment((-84,14),(-75,38)).segment((-75,75)).arc((-83,45),(-84,14)).assemble()).finalize().extrude(-20).union(w0.sketch().face(w0.sketch().arc((90,-38),(91,-34),(90,-30)).close().assemble()).finalize().extrude(20))