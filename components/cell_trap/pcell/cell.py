
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from ...trap.pcell import TrapOnly
from ...trap_cup.pcell import TrapCupRectangle
from ...trap_drain.pcell import TrapDrain


class CellTrap (i3.Circuit):
    """
    A full cell trap PCell
    """

    trace_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT, doc="what is this template used for?")

    trap_only = i3.ChildCellProperty()
    trap_cup = i3.ChildCellProperty()
    trap_drain = i3.ChildCellProperty()

    def _default_trap_only(self):
        trap_only = TrapOnly(channel_template = self.trace_template)
        return  trap_only

    def _default_trap_cup(self):
        trap_cup = TrapCupRectangle(channel_template = self.trace_template, out_channel_template=self.trace_template)
        return  trap_cup

    def _default_trap_drain(self):
        trap_drain = TrapDrain(channel_template = self.trace_template, out_channel_template=self.trace_template)
        return  trap_drain

    def _default_insts(self):
        return {'trap': self.trap_only,
                'cup': self.trap_cup,
                'drain': self.trap_drain
                }
    
    def _default_specs(self):
        specs = [
                    i3.Place('trap', (0, 0)),
                    i3.Join('trap:out2', 'cup:in'),
                    i3.Join('cup:out', 'drain:in1')
                ]

        return specs
    
    def _default_exposed_ports(self):
        return {
                'trap:in': 'in1',
                'trap:out1': 'out1',
                'drain:in2': 'in2',
                'drain:out': 'out2'
                }

    class Layout(i3.Circuit.Layout):
        pass