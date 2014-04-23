#!usr/bin/env python3
import sys
from fslib import *


if len(sys.argv) == 3:
    if sys.argv[1] == "line":
        print("line")
        test.line(int(sys.argv[2]))
    elif sys.argv[1] == "direct_square":  
        print("direct_square")
        test.direct_square(int(sys.argv[2]))
    elif sys.argv[1] == "square":  
        print("square")
        test.square(int(sys.argv[2]))
    elif sys.argv[1] == "cube":
        print("cube")
        test.cube(int(sys.argv[2]))
    elif sys.argv[1] == "base":
        print("base")
        test.base(int(sys.argv[2]))
    elif sys.argv[1] == "sec_influence_test":
        print("sec_influence_test")
        test.sec_influence_test(int(sys.argv[2]))
    elif sys.argv[1] == "fight":
        print("fight")
        test.fight(int(sys.argv[2]))
    test.plt.show()
