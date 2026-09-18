import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-75,0))
r=w0.sketch().segment((-20,-100),(8,-100)).arc((11,-76),(20,-54)).segment((20,-69)).segment((8,-69)).segment((8,-49)).segment((10,-49)).segment((10,69)).segment((8,69)).segment((8,78)).segment((16,78)).arc((12,84),(8,89)).segment((8,100)).segment((-20,100)).close().assemble().push([(1,0)]).rect(14,90,mode='s').finalize().extrude(150)