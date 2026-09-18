import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,-14))
r=w0.sketch().arc((-57,11),(57,-10),(-56,14)).arc((-56,12),(-57,11)).assemble().push([(0,1)]).circle(6,mode='s').finalize().extrude(-177).union(w0.sketch().arc((-85,18),(-79,-36),(-40,-75)).segment((-40,-80)).segment((-26,-80)).arc((-10,-82),(6,-80)).segment((20,-80)).segment((20,-75)).arc((69,-36),(75,26)).segment((75,18)).close().assemble().finalize().extrude(-14)).union(w1.sketch().circle(86).circle(51,mode='s').finalize().extrude(-86))