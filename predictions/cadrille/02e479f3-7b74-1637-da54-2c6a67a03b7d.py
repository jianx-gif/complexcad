import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-27))
w1=cq.Workplane('XY',origin=(0,0,-37))
r=w0.sketch().segment((-91,-41),(-34,-93)).segment((-19,-77)).arc((73,-63),(87,29)).segment((91,34)).segment((34,86)).segment((29,80)).arc((-73,63),(-87,-39)).close().assemble().finalize().extrude(-10).union(w0.workplane(offset=39/2).moveTo(0,-4).cylinder(39,69)).union(w0.sketch().push([(0,-4)]).circle(74).circle(67,mode='s').finalize().extrude(65)).union(w1.sketch().push([(0,-4)]).circle(86).circle(56,mode='s').finalize().extrude(15))