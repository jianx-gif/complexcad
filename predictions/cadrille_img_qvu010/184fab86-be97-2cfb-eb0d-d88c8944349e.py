import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-45,0))
w1=cq.Workplane('YZ',origin=(-16,0,0))
r=w0.sketch().arc((-99,-16),(15,38),(100,-71)).segment((100,-16)).segment((99,-16)).arc((0,48),(-99,-16)).assemble().finalize().extrude(131).union(w1.sketch().arc((-99,-100),(-19,-10),(71,61)).arc((-49,61),(-99,-100)).assemble().finalize().extrude(-54))