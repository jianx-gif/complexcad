import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-1,0))
w1=cq.Workplane('XY',origin=(0,0,-13))
r=w0.sketch().segment((-42,-100),(0,-100)).segment((0,-96)).segment((-41,-96)).segment((-41,64)).segment((0,64)).segment((0,68)).segment((-42,68)).close().assemble().finalize().extrude(-85).union(w0.sketch().push([(10.5,16)]).rect(63,168).push([(10.5,16.5)]).rect(51,155,mode='s').finalize().extrude(84)).union(w1.sketch().segment((-24,53),(-7,53)).segment((-7,92)).segment((-24,92)).segment((-24,89)).arc((-22,88),(-24,87)).close().assemble().finalize().extrude(-6))