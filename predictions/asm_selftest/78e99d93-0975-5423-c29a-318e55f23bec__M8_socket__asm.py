parts = [base]
parts.append(place(fastener("washer", 'M8', 0), axis=(0, 0, 1), point=(0, 0, 0), seat=4.8, flip=False))
parts.append(place(fastener("screw", 'M8-1.25', 20, 0), axis=(0, 0, 1), point=(0, 0, 0), seat=6.6, flip=False))
parts.append(place(fastener("nut", 'M8-1.25', 'M8', 0), axis=(0, 0, 1), point=(0, 0, 0), seat=-5, flip=True))
