
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

import math

class _TrapCup(i3.PCell):
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
            ports += microfluidics.FluidicPort(name='in', position = (0.0, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=90,
                                               trace_template=self.channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out', position = (0.0, -self.out_length),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=270,
                                               trace_template=self.out_channel_template
                                               )

            return ports


    class Netlist(i3.NetlistFromLayout):
        pass

class TrapCupRectangle(_TrapCup):
    """
    Trap Cup with rectangle shapes
    """

    class Layout(_TrapCup.Layout):
        def _generate_elements(self, elems):
            in_width = self.channel_template.channel_width
            out_width = self.out_channel_template.channel_width
            point_list = [(in_width * 0.5, 0),
                          (in_width * 0.25, -self.in_length),
                          (-in_width * 0.25, -self.in_length),
                          (-in_width * 0.5, 0)
                          ]

            shape = i3.Shape(point_list, closed=True)
            boundary = i3.Boundary(self.channel_template.layer, shape)
            elems += boundary

            return elems



class TrapCupRound(_TrapCup):

    class Layout(_TrapCup.Layout):
        def _generate_elements(self, elems):
            in_width = self.channel_template.channel_width
            out_width = self.out_channel_template.channel_width
            point_list = [(in_width * 0.5, 0),
                          (in_width * 0.5, -self.in_length),
                          (out_width * 0.5, -self.in_length),
                          (out_width * 0.5, -self.in_length - self.out_length),
                          (-out_width * 0.5, -self.in_length - self.out_length),
                          (-out_width * 0.5, -self.in_length),
                          (-in_width * 0.5, -self.in_length),
                          (-in_width * 0.5, 0)
                          ]

            shape = i3.Shape(point_list, closed=True)

            boundary1 = i3.Boundary(self.channel_template.layer,
                                    i3.Shape([(out_width * 0.5, 0),
                                              (out_width * 0.5, -self.in_length - self.out_length),
                                              (-out_width * 0.5, -self.in_length - self.out_length),
                                              (-out_width * 0.5, 0)
                                              ]))

            arc = i3.ShapeArc(center=(0, -self.in_length + in_width * 0.5),
                              radius=in_width * 0.5,
                              start_angle=180,
                              end_angle=0)

            p = min(arc.points[0][1], arc.points[-1][1])


            boundary2 = i3.Boundary(self.channel_template.layer,
                                    i3.Shape([(in_width * 0.5, 0),
                                              (in_width * 0.5, p),
                                              (-in_width * 0.5, p),
                                              (-in_width * 0.5, 0)
                                              ]))
            boundary3 = i3.Boundary(self.channel_template.layer,
                                    i3.ShapeArc(center=(0, -self.in_length + in_width * 0.5),
                                                radius=in_width * 0.5,
                                                start_angle=180,
                                                end_angle=0)
                                    )

            elems +=  ((boundary1 | boundary2)[0] | boundary3)

            return elems
