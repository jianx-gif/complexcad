import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,95,0))
w1=cq.Workplane('YZ',origin=(-59,0,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-45,-79),(-38,-89)).segment((-19,-76)).arc((51,-66),(74,3)).segment((93,16)).segment((86,26)).segment((67,13)).arc((-43,4),(-40,-76)).close().assemble(),mode='s').finalize().extrude(-190).union(w1.sketch().segment((-17,-58),(17,-58)).segment((17,-54)).arc((57,1),(17,56)).segment((17,58)).segment((-17,58)).segment((-17,56)).arc((-57,1),(-17,-54)).close().assemble().push([(0,1)]).circle(12,mode='s').finalize().extrude(149))