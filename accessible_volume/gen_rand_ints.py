#!/usr/bin/env python3
"""
Generate sequence of random integers

Author: Henrique Musseli Cezar
Date: JUL/2021
"""

import argparse
import random

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Generate sequence of random integers and print to STDOUT.")
  parser.add_argument("nnums", type=int, help="number of generated random numbers")
  parser.add_argument("--seed", type=int, help="manual seed for the PRNG")
  parser.add_argument("--min", type=int, default=1, help="minimum integer generated (default = 1)")
  parser.add_argument("--max", type=int, default=1000000, help="minimum integer generated (default = 1000000)")

  args = parser.parse_args()

  if args.seed:
    random.seed(args.seed)

  for i in range(args.nnums):
    print(random.randint(args.min, args.max))
