import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('XY',origin=(0,0,81))
r=w0.sketch().push([(0,18)]).rect(130,136).circle(58,mode='s').circle(17).finalize().extrude(11).union(w0.sketch().arc((-29,34),(1,45),(31,48)).arc((-4,52),(-29,34)).assemble().finalize().extrude(124)).union(w1.sketch().arc((-89,-49),(-81,-51),(-73,-53)).arc((-68,-51),(-63,-50)).arc((0,-65),(63,-40)).arc((61,-26),(75,-23)).arc((78,18),(68,58)).arc((1,1),(-89,-49)).assemble().finalize().extrude(-131))