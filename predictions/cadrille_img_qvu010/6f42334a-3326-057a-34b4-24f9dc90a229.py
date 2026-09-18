import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,-89,0))
r=w0.sketch().arc((-100,-37),(-61,-49),(-23,-60)).segment((-23,-62)).segment((23,-62)).segment((23,-60)).arc((61,-49),(100,-37)).segment((99,-37)).arc((61,-48),(23,-59)).segment((23,99)).segment((-23,99)).segment((-23,-59)).arc((-61,-48),(-99,-37)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-30,-83),(36,-1),(-30,83)).segment((-30,38)).arc((-17,1),(-30,-38)).close().assemble().push([(1,-68)]).circle(11,mode='s').finalize().extrude(179))