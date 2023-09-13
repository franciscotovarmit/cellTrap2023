
import sys

sys.path.append("C:/Work/Software/")  # Need to change the path to the folder containing icrofluidics_ipkiss3 and microfluidics_pdk
sys.path.append("../../../")

# Import basic microfluidics PDK
import microfluidics_pdk.all as pdk

# Import IPKISS3 Packages.
from ipkiss3 import all as i3

# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics


from components.cell_trap.pcell import CellTrap

cell_trap = CellTrap()
cell_trap_lo = cell_trap.Layout()

cell_trap_lo.visualize(annotate=True)
