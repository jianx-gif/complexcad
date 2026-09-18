import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,-69,0))
r=w0.sketch().push([(-19,15)]).circle(61).circle(54,mode='s').finalize().extrude(166).union(w0.sketch().arc((-28,-29),(-13,-27),(1,-29)).arc((13,-27),(25,-29)).arc((-27,89),(-28,-38)).close().assemble().finalize().extrude(166)).union(w0.sketch().arc((-25,-38),(55,-59),(39,22)).arc((-49,69),(-25,-30)).close().assemble().finalize().extrude(166)).union(w1.sketch().arc((-19,-89),(15,-53),(63,-38)).arc((-28,29),(-19,-89)).assemble().finalize().extrude(164))