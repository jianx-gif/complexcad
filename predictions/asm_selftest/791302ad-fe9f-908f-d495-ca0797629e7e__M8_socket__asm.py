parts = [base]
parts.append(place(fastener("screw", 'M8-1.25', 44, 0), axis=(0, 0, 1), point=(-25, -25, 35.25), seat=-31.25, flip=True))
parts.append(place(fastener("screw", 'M8-1.25', 44, 1), axis=(0, 0, 1), point=(25, -25, 35.25), seat=-31.25, flip=True))
parts.append(place(fastener("screw", 'M8-1.25', 44, 2), axis=(0, 0, 1), point=(-25, 25, 35.25), seat=-31.25, flip=True))
parts.append(place(fastener("screw", 'M8-1.25', 44, 3), axis=(0, 0, 1), point=(25, 25, 35.25), seat=-31.25, flip=True))
