
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

#from ..trap_block import CellTrap
#from ..inlet_outlet import InletWithLeadin, OutletWithLeadin

from ..trapOnly import TrapOnly
from ..trapCup import TrapCupRectangle
from ..trapDrain import TrapDrain


class CellTrap (microfluidics.PlaceAndAutoRoute):

    trace_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT, channel_width=20)



    trap_only = i3.ChildCellProperty()
    trap_cup = i3.ChildCellProperty()
    trap_drain = i3.ChildCellProperty()

    def _default_trap_only(self):
        trap_only = TrapOnly(channel_template = self.trace_template)
        return  trap_only

    def _default_trap_cup(self):
        trap_cup = TrapCupRectangle(channel_template = self.trace_template)
        return  trap_cup

    def _default_trap_drain(self):
        trap_drain = TrapDrain(channel_template = self.trace_template)
        return  trap_drain


    def _default_child_cells(self):   #for PlaceAndAutoRoute
        return {"trap_only": self.trap_only,
                "trap_cup": self.trap_cup,
                "trap_drain": self.trap_drain,
                }

    def _default_links(self):  #parallel
        return [("trap_only:out2", "trap_cup:in"),
                ("trap_cup:out", "trap_drain:in1")
                ]

    class Layout(microfluidics.PlaceAndAutoRoute.Layout):

        def _default_cell_trap(self):
            lo = self.cell.cell_trap.get_default_view(i3.LayoutView)
            return lo

        def _default_trap_only(self):
            lo = self.cell.trap_only.get_default_view(i3.LayoutView)
            return lo

        def _default_trap_cup(self):
            lo = self.cell.trap_cup.get_default_view(i3.LayoutView)
            return lo

        def _default_trap_drain(self):
            lo = self.cell.trap_drain.get_default_view(i3.LayoutView)
            return lo


        def _default_child_transformations(self):
            trap_only_pos =(0.0, 20.0)
            trap_cup_pos =(0.0, 0.0)
            trap_drain_pos =(0.0, -20.0)
            return {"trap_only": i3.Translation(trap_only_pos),
                    "trap_cup": i3.Translation(trap_cup_pos) + i3.Rotation(rotation=0),
                    "trap_drain":  i3.Translation(trap_drain_pos) + i3.Rotation(rotation=0)
            }

        def _generate_elements(self, elems):
            return elems