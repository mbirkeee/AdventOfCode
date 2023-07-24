# PROGRAM_1 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 1',
#     'add x 14',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 1',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_2 = [
#     'inp w',       # Get
#     'mul x 0',     # Get previous result into X
#     'add x z',
#     'mod x 26',    # Divide by 26 and keep remainder
#     'div z 1',     # no-op??
#     'add x 15',    # Add 15
#     'eql x w',     # 1 if equal to input, zero otherwise ... how can this ever not be zero????
#     'eql x 0',     # Flip X... so 0 if equal to input, 1 otherwise - I think
#     'mul y 0',     # Clear y, - get 25 into it
#     'add y 25',
#     'mul y x',     # Multiply by X (so it will be either 0 or 25
#     'add y 1',     # 1 or 26
#     'mul z y',     # Mult prev result (will be unchanged OR a multiple of 26)
#     'mul y 0',     # Get input into y
#     'add y w',
#     'add y 7',     # Add 7 to input
#     'mul y x',     # Mult by X (which is 0 or 1)
#     'add z y',     # Add to previous result
# ]
#
# PROGRAM_3 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 1',
#     'add x 15',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 13',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_4 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 26',
#     'add x -6',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 10',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_5 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 1',
#     'add x 14',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 0',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_6 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 26',
#     'add x -4',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 13',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_11 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 26',
#     'add x 0',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 11',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_12 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 26',
#     'add x -3',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 14',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_13 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 26',
#     'add x -9',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 4',
#     'mul y x',
#     'add z y',
# ]
#
# PROGRAM_14 = [
#     'inp w',
#     'mul x 0',
#     'add x z',
#     'mod x 26',
#     'div z 26',
#     'add x -9',
#     'eql x w',
#     'eql x 0',
#     'mul y 0',
#     'add y 25',
#     'mul y x',
#     'add y 1',
#     'mul z y',
#     'mul y 0',
#     'add y w',
#     'add y 10',
#     'mul y x',
#     'add z y',
# ]
