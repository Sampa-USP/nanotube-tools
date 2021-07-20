#!/usr/bin/env python3
"""
Concatenate if inside or outside in the lammpstrj

Author: Henrique Musseli Cezar
Date: JUL/2021
"""

import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Concatenate if inside or outside in the lammpstrj.")
  parser.add_argument("traj", help=".lammpstrj trajectory")
  parser.add_argument("inten", help="file containing the interaction energies")
  parser.add_argument("laststep", type=int, help="number of last step")

  args = parser.parse_args()

  with open(args.traj, "r") as ftraj:
    while True:
      line = ftraj.readline()  
      if "ITEM: TIMESTEP" in line:
        line2 = int(ftraj.readline())
        if line2 == args.laststep:
          break

    print(line.rstrip())
    print(line2)

    for line in ftraj:
      if "ITEM: ATOMS" in line:
        print(line.rstrip()+" inside")
        break
      else:
        print(line.rstrip())

    with open(args.inten, "r") as fen:
      for line in ftraj:
        if "Ne" in line:
          en = float(fen.readline())
          if en <= 0.0:
            inside = 1
          else:
            inside = 0
          print(line.rstrip()+" {}".format(inside))
        else:
          print(line.rstrip()+" 2")