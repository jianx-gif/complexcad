import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-100,-17),(-26,-100)).segment((100,17)).segment((26,100)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-79,-48),(-44,-87),(-1,-60)).arc((44,-31),(54,21)).arc((66,76),(13,60)).arc((-71,38),(-79,-48)).assemble().finalize().extrude(-159))