import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,1)]).rect(104,164).push([(-83,-29)]).circle(11,mode='s').push([(81,31)]).circle(11,mode='s').finalize().extrude(11).union(w1.sketch().segment((-100,-19),(-99,-19)).arc((-10,-94),(80,-19)).segment((81,-19)).segment((81,19)).segment((80,19)).arc((-10,94),(-99,19)).segment((-100,19)).close().assemble().circle(94,mode='s').finalize().extrude(-200))