import cadquery as cq
w0=cq.Workplane('XY',origin=(-80,0,-100))
w1=cq.Workplane('XY',origin=(-80,0,-53))
r=w0.sketch().segment((32,-58),(36,-58)).segment((36,-55)).close().assemble().finalize().extrude(200).union(w1.sketch().push([(80,0)]).circle(20).push([(80.5,0)]).rect(19,34,mode='s').finalize().extrude(102))