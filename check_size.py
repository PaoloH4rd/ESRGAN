import glob
import nrrd

for f in glob.glob('downscale/*.nrrd'):
    header = nrrd.read_header(f)
    print(f"{f}: {header['sizes']}")
