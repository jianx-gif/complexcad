import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,95,0))
w1=cq.Workplane('ZX',origin=(0,29,0))
r=w0.sketch().segment((-59,-73),(59,-73)).segment((59,-2)).close().assemble().finalize().extrude(-190).union(w0.sketch().arc((-26,-16),(0,-28),(26,-16)).close().assemble().finalize().extrude(-189)).union(w1.sketch().push([(0,0.5)]).rect(200,199).push([(0,1)]).circle(90,mode='s').finalize().extrude(-53))