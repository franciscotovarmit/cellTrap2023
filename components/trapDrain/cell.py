
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

import math

class _TrapDrain(i3.PCell):
    """"
    Base class for different types of cell traps
    """
    channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                doc="Inport channel template")
    out_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                doc="Outport channel template")

    class Layout(i3.LayoutView):
        in_length = i3.PositiveNumberProperty(default=20, doc="Input part of the trap")
        out_length = i3.PositiveNumberProperty(default=20, doc="Output part of the trap")

        def _generate_ports(self, ports):
            # input port
            ports += microfluidics.FluidicPort(name='out', position = (-self.in_length*0.5, -self.in_length*0.5),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.channel_template
                                               )

            ports += microfluidics.FluidicPort(name='in2', position = (self.in_length*0.5, -self.out_length*0.5),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=0,
                                               trace_template=self.out_channel_template
                                               )

            ports += microfluidics.FluidicPort(name='in1', position = (0.0, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=90,
                                               trace_template=self.out_channel_template
                                               )

            return ports


    class Netlist(i3.NetlistFromLayout):
        pass

class TrapDrain(_TrapDrain):
    """
    Trap drain with rectangle shapes
    """

    class Layout(_TrapDrain.Layout):
        def _generate_elements(self, elems):
            in_width = self.in_length #self.in_channel_template.channel_width
            out_width = self.out_length #self.out_channel_template.channel_width
            point_list = [(in_width * 0.5, 0),
                          (in_width * 0.5, -self.in_length),
                          (-in_width * 0.5, -self.in_length),
                          (-in_width * 0.5, 0)
                          ]

            shape = i3.Shape(point_list, closed=True)
            boundary = i3.Boundary(self.channel_template.layer, shape)
            elems += boundary

            return elems