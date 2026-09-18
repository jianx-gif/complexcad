import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('YZ',origin=(94,0,0))
r=w0.sketch().segment((45,-12),(47,-14)).segment((51,-12)).segment((49,-10)).arc((47,-11),(45,-12)).assemble().finalize().extrude(-200).union(w1.sketch().segment((-51,-3),(-48,-3)).segment((-48,-5)).segment((19,-5)).segment((19,-3)).segment((20,-3)).segment((20,13)).segment((19,13)).segment((19,14)).segment((-48,14)).segment((-48,13)).segment((-51,13)).close().assemble().push([(-16,2)]).circle(2,mode='s').push([(-15,11)]).circle(2,mode='s').finalize().extrude(-188))