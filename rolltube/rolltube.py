"""
Receives a xyz file containing a sheet to roll into a nanotube.

Procedure to use:
  - Open unit cell in zeobuilder
  - Use nanotube builder with the flat option
  - Wrap atoms to unit cell (ctrl + w)
  - Save to .xyz
  - Use the script passing this .xyz

Author: Henrique Musseli Cezar
Date: MAR/2020
"""

import os
import argparse
import sys
import numpy as np

# from https://stackoverflow.com/a/11541495
def extant_file(x):
  """
  'Type' for argparse - checks that file exists but does not open.
  """
  if not os.path.exists(x):
      # Argparse uses the ArgumentTypeError to give a rejection message like:
      # error: argument input: x does not exist
      raise argparse.ArgumentTypeError("{0} does not exist".format(x))
  return x

def readxyz(file):
  species = []
  atoms = []
  with open(file,"r") as f:
    try:
      natoms = int(f.readline())
    except:
      print("The first line of the xyz file should be the number of atoms")
      sys.exit(0)

    # skip comment and read atomic positions and species
    f.readline()
    for line in f:
      species.append(line.split()[0])
      atoms.append(np.array([float(x) for x in line.split()[1:]]))

  return species, np.array(atoms)

def writexyz(species, atoms, file):
  with open(file,"w") as f:
    f.write("%d\n\n" % (len(species)))
    for sp, acoord in zip(species, atoms):
      f.write("%s\t%.6f\t%.6f\t%.6f\n" % (sp, acoord[0], acoord[1], acoord[2]))

def rollsheet(atoms, length, xbuffer):
  # center the atoms at the centroid
  catoms = centersheet(atoms)

  if not xbuffer: xbuffer = 0.

  if length:
    perimeter = length
  else:
    perimeter = np.amax(catoms, axis=0)[0] - np.amin(catoms, axis=0)[0] + xbuffer # perimeter from structure + buffer
  radius = perimeter/(2.*np.pi)

  ratoms = []
  for atom in catoms:
    ang = 2.*np.pi*atom[0]/perimeter
    xr = (radius-atom[2])*np.cos(ang)
    yr = atom[1]
    zr = (radius-atom[2])*np.sin(ang)
    ratoms.append(np.array([xr,yr,zr]))

  return np.array(ratoms)

def centersheet(atoms):
  centroid = atoms.mean(axis=0)
  return atoms - centroid

def alignsheetx(atoms, vec):
  # make sure vec is a unit vector
  uvec = vec / np.linalg.norm(vec)
  
  xvec = np.array([1., 0., 0.])

  R = rotationmatrix(uvec,xvec)

  return centersheet(np.dot(atoms,R))

# rotate v1 to v2 - expression from https://math.stackexchange.com/a/476311
def rotationmatrix(v1, v2):
  # make sure vectors are unit vectors
  uv1 = v1 / np.linalg.norm(v1)
  uv2 = v2 / np.linalg.norm(v2)

  # create rotation matrix
  v = np.cross(uv1,uv2)
  c = np.dot(uv1, uv2) # cosine of angle between vecs

  # if parallel or anti parallel just returns
  if (c == 1.) or (c == -1.):
    return np.identity(3) 

  # skew-symmetric cross product matrix
  vmx = np.array([[0.,-v[2],v[1]],[v[2],0.,-v[0]],[-v[1],v[0],0.]])

  # rotation matrix
  return np.identity(3) + vmx + (1./(1.+c))*np.dot(vmx,vmx)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Receives a xyz file containing a sheet to roll into a nanotube")
  parser.add_argument("xyzfile", type=extant_file, help="xyz containing the sheet")
  parser.add_argument("--atoms-to-align", nargs="+", type=int, help="atom indexes to align to the x axis (roll axis)")
  parser.add_argument("--x-length", type=float, help="length of the x axis, which will be rolled")
  parser.add_argument("--buffer", type=float, help="add a buffer to the automatically determined length of the x axis, which will be rolled")
  parser.add_argument("--align-to-z", action="store_true", help="align the final nanotube center axis to z")

  args = parser.parse_args()

  if args.atoms_to_align:
    if len(args.atoms_to_align) != 2:
      print("You should pass just two atoms, which will be aligned to the x axis, the rolled axis.")
      sys.exit(0)

  if args.x_length and args.buffer:
    print("You cannot used the --x-length and --buffer at the same time. Add the buffer distance to your x length.")
    sys.exit(0)

  species, atoms = readxyz(args.xyzfile)

  if args.atoms_to_align:
    atoms = alignsheetx(atoms,atoms[args.atoms_to_align[1]-1]-atoms[args.atoms_to_align[0]-1])
    writexyz(species, atoms, "rotated.xyz")

  rolledatoms = rollsheet(atoms, args.x_length, args.buffer)

  if args.align_to_z:
    R = rotationmatrix([0.,1.,0.],[0.,0.,1.])
    rolledatoms = np.dot(rolledatoms,R)

  writexyz(species, rolledatoms, "nanotube.xyz")
