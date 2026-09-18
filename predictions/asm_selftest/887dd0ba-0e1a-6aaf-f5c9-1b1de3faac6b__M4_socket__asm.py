parts = [base]
parts.append(place(fastener("washer", 'M8', 0), axis=(0, 0, 1), point=(0, 0, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("screw", 'M8-1.25', 14, 0), axis=(0, 0, 1), point=(0, 0, 2.5), seat=4.3, flip=False))
parts.append(place(fastener("nut", 'M8-1.25', 'M8', 0), axis=(0, 0, 1), point=(0, 0, 2.5), seat=-2.5, flip=True))
parts.append(place(fastener("washer", 'M4', 1), axis=(0, 0, 1), point=(37.5, 10, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 1), axis=(0, 0, 1), point=(37.5, 10, 2.5), seat=3.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 1), axis=(0, 0, 1), point=(37.5, 10, 2.5), seat=-2.5, flip=True))
