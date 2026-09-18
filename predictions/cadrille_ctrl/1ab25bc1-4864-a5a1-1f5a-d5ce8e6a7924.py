import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-39,11),(-37,11)).arc((0,-40),(37,11)).segment((39,11)).segment((39,12)).segment((37,12)).arc((0,40),(-37,12)).segment((-39,12)).close().assemble().reset().face(w0.sketch().arc((-23,11),(0,-24),(23,11)).segment((17,11)).arc((0,-10),(-17,11)).close().assemble(),mode='s').reset().face(w0.sketch().segment((-23,12),(-17,12)).arc((0,33),(17,12)).segment((23,12)).arc((0,38),(-23,12)).assemble(),mode='s').finalize().extrude(2).union(w0.sketch().arc((-39,10),(38,-13),(-38,13)).arc((-37,11),(-39,10)).assemble().push([(1,0)]).circle(21,mode='s').finalize().extrude(60)).union(w1.workplane(offset=-62/2).moveTo(0,-37).cylinder(62,2))
