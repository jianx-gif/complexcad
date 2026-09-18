import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,58))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-84,16),(-29,-78)).segment((-17,-71)).arc((40,-68),(73,-23)).segment((84,-16)).segment((29,78)).segment((17,71)).arc((-40,68),(-73,23)).close().assemble(),mode='s').finalize().extrude(-116)