import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('XY',origin=(0,0,-51))
r=w0.sketch().arc((-100,-98),(-81,-99),(-62,-100)).arc((-19,100),(100,-62)).arc((97,-63),(95,-65)).arc((-11,88),(-100,-98)).assemble().finalize().extrude(-159).union(w1.sketch().arc((-38,90),(-11,77),(16,90)).close().assemble().finalize().extrude(47))