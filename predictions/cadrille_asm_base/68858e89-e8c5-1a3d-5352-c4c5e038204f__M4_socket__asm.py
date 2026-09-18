import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
r=w0.sketch().segment((-33,-66),(12,-100)).segment((33,-72)).segment((-12,-38)).close().assemble().push([(14.5,0)]).rect(37,200).finalize().extrude(6).union(w0.workplane(offset=76/2).moveTo(-12.5,0).box(15,200,76))