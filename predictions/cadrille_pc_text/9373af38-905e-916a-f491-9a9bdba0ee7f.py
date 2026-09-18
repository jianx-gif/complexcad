import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-34))
w1=cq.Workplane('YZ',origin=(30,0,0))
r=w0.sketch().push([(-73,0)]).circle(27).circle(16,mode='s').finalize().extrude(-26).union(w0.sketch().arc((30,3),(99,-8),(41,29)).arc((56,9),(30,3)).assemble().push([(74,0)]).circle(19,mode='s').finalize().extrude(119)).union(w1.sketch().push([(0,-54)]).circle(39).circle(31,mode='s').finalize().extrude(-99))