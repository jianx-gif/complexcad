import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,86))
r=w0.sketch().arc((-76,-56),(-16,-20),(31,-71)).arc((4,88),(-76,-56)).assemble().finalize().extrude(-186).union(w0.sketch().segment((-79,88),(-76,88)).segment((-76,85)).segment((-18,85)).segment((-18,88)).segment((-15,88)).arc((-46,93),(-79,88)).assemble().finalize().extrude(14))