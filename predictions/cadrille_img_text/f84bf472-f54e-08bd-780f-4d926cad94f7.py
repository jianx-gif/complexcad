import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
w1=cq.Workplane('ZX',origin=(0,29,0))
r=w0.sketch().segment((-67,70),(-47,31)).arc((-42,23),(-37,15)).segment((-17,-24)).segment((67,18)).segment((47,57)).arc((42,65),(37,73)).segment((17,100)).close().assemble().finalize().extrude(-76).union(w0.sketch().circle(87).circle(38,mode='s').finalize().extrude(-43)).union(w1.sketch().arc((-70,29),(33,73),(70,-33)).arc((39,88),(-70,29)).assemble().finalize().extrude(-57))