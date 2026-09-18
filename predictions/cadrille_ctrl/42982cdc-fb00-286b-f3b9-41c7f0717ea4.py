import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,80))
r=w0.sketch().push([(0,-1)]).circle(9).circle(3,mode='s').finalize().extrude(-80).union(w0.sketch().segment((-20,-3),(19,-8)).segment((20,3)).segment((-19,8)).close().assemble().finalize().extrude(-80)).union(w0.sketch().segment((-20,-3),(19,-3)).segment((20,3)).segment((-19,3)).close().assemble().finalize().extrude(-9))
