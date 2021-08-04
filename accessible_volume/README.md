# Accessible volume using LAMMPS

The scripts in this folder can be used to estimate the acessible volume inside a nanotube using LAMMPS.

The idea is to insert a probe (Ne atom) hundreds or millions of times to perform a Monte Carlo integration, similar to what is performed in the common exercise of [estimating the value of pi](https://www.geeksforgeeks.org/estimating-value-pi-using-monte-carlo/).
The accessible volume is determined by the Lennard-Jones interaction energy: if the energy is lesser than zero, the probe is in, if the energy is positive the probe is out of the accessible volume.
This idea was previously explored in [this](http://dx.doi.org/10.1016/j.jcis.2010.05.001) reference.

First, you need to generate a sequence of random rumbers to be used as seed for each insertion in LAMMPS.
To generate the seeds, run the python script as below, replacing `NSTEPS` with the number of steps you wish to use in your MC integration:
```bash
python gen_rand_ints.py NSTEPS > rngs.txt
```

Note that the seed should be >= 1, so beware if you generate the seeds using another method.

With the seeds in hand, open your LAMMPS topology file containing the nanotube and edit a few things:
1. Make sure your NT does not wrap around PBCs. You'll have to edit the `volume.in` with the origin (axis) of the NT, but if it is 0.0 0.0 0.0 and your box start at 0.0, you'll get a wrong volume.
2. Add an extra atom type (replacing `X` with the correct number), and attribute the following parameters to it (Ne atom):
```
Masses
  X  20.180  # Ne
Pair Coeffs
  X 0.0694  2.78  # Ne
```

Then, you should edit the `volume.in` (or `volume_box.in` for non-cylindrical NTs) file with the proper parameters.
The lines you need to change are the ones that are with an "ATTENTION" comment:
1. You'll need an estimative of the NT radius (use an upper bound), in which the probe atoms will be inserted.
2. Set the number of MC steps (should be the same `NSTEPS` used in the python script above or lower)
3. Adjust the axial direction accordingly (in the example it's `z`).
4. Use the proper topology filename in `read_data`
5. Basically, look for `ATTENTION` in the file and fix it.

An example is provided in the [example](./example/) folder.
The resuls are shown at the end of the output file as:
```
------ Accessible volume info ------

Number points inside = 4248
Number points outside = 5752
Cylinder radius = 5
Cylinder length = 152.2749939

Cylinder volume (A^3) = 11959.6500540418

Acessible volume (A^3) = 8832.50928886814

------------------------------------
```