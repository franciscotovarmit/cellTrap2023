import sys
sys.path.append("C:/Users/e54491/OneDrive - RMIT University-/Software")
sys.path.append("../")

from microfluidics_pdk.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3
import microfluidics_pdk.all as pdk

from components.trapOnly import TrapOnly
from components.trapCup import TrapCupRectangle
from components.trapDrain import TrapDrain
from components.cellTrap import CellTrap

# Input and output channel of a trap
channel_template = pdk.FluidChannelTemplate()
channel_template.Layout(channel_width=10)

out_channel_template = pdk.FluidChannelTemplate()
out_channel_template.Layout(channel_width=10)

trapOnly = TrapOnly(channel_template=channel_template, out_channel_template=out_channel_template)
trapOnly_lo = trapOnly.Layout(in_length=10, out_length=10)
#trapOnly_lo.visualize(annotate=True)

trapCup = TrapCupRectangle(channel_template=channel_template, out_channel_template=out_channel_template)
trapCup_lo = trapCup.Layout(in_length=10, out_length=10)
#trapCup_lo.visualize(annotate=True)

trapDrain = TrapDrain(channel_template=channel_template, out_channel_template=out_channel_template)
trapDrain_lo = trapDrain.Layout(in_length=10, out_length=10)
#trapDrain_lo.visualize(annotate=True)

cellTrap = CellTrap(trace_template=channel_template)
cellTrap_lo = cellTrap.Layout()
cellTrap_lo.visualize(annotate=True)

cellTrap_lo.write_gdsii('cell_trap.gds')