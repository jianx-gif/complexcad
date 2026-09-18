import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-18,0))
w1=cq.Workplane('ZX',origin=(0,-21,0))
r=w0.sketch().segment((-49,-11),(-29,41)).segment((49,11)).segment((49,19)).segment((46,19)).segment((46,24)).segment((49,24)).segment((49,41)).arc((-49,72),(-49,-11)).assemble().finalize().extrude(75).union(w1.workplane(offset=-29/2).moveTo(12,12).cylinder(29,88))