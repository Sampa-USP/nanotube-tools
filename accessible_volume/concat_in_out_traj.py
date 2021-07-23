#!/usr/bin/env python3
"""
Concatenate if inside or outside in the lammpstrj

Author: Henrique Musseli Cezar
Date: JUL/2021
"""

import argparse
import numpy as np

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Concatenate if inside or outside in the lammpstrj.")
  parser.add_argument("traj", help=".lammpstrj trajectory")
  parser.add_argument("inten", help="file containing the interaction energies")
  parser.add_argument("--only-in", action="store_true", help="exclude all the out atoms")

  args = parser.parse_args()

  nout = 0
  if args.only_in:
    energies = np.loadtxt(args.inten)
    nout = np.count_nonzero(energies > 0.)

  with open(args.traj, "r") as ftraj:
    fndnum = False
    for line in ftraj:
      if "ITEM: ATOMS" in line:
        print(line.rstrip()+" inside")
        break
      elif "ITEM: NUMBER OF ATOMS" in line:
        print(line.rstrip())
        fndnum = True
      elif fndnum:
        print(int(line.strip())-nout)
        fndnum = False
      else:
        print(line.rstrip())

    with open(args.inten, "r") as fen:
      for line in ftraj:
        if "Ne" in line:
          en = float(fen.readline())
          if en <= 0.0:
            print(line.rstrip()+" 1")
          elif not args.only_in:
            print(line.rstrip()+" 0")
        else:
          print(line.rstrip()+" 2")