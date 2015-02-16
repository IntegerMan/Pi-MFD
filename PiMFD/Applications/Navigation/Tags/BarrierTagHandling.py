# coding=utf-8

"""
Handles the "barrier" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class BarrierTagHandler(TagHandler):
    def get_color(self, entity, value, cs):

        if value in ('city_wall', 'guard_rail', 'cable_barrier', 'block', 'border_control', 'debris',
                     'height_restrictor', 'jersey_barrier', 'sally_port'):
            return cs.map_structural

        elif value in ('ditch', 'retaining_wall', 'hedge', 'horse_stile', 'log'):
            return cs.map_vegetation

        elif value in ('wall', 'fence', 'entrance', 'gate', 'hampshire_gate', 'lift_gate', 'spikes'):
            return cs.map_private

        elif value in ('bollard', 'kerb', 'cycle_barrier', 'chain', 'full-height_turnstile', 'kissing_gate',
                       'kent_carriage_gap', 'rope', 'motorcycle_barrier'):
            return cs.map_pedestrian

        return super(BarrierTagHandler, self).get_color(entity, value, cs)

    def get_description_text(self, entity, value):

        if value == 'bollard':
            return 'Bollard'
        elif value == 'gate':
            return 'Gate'
        elif value == 'city_wall':
            return 'City Wall'
        elif value == 'guard_wall':
            return 'Guard Wall'
        elif value == 'cable_barrier':
            return 'Cable Barrier'
        elif value == 'block':
            return 'Block'
        elif value == 'border_control':
            return 'Border Control'
        elif value == 'debris':
            return 'Debris'
        elif value == 'height_restrictor':
            return 'Height Restrictor'
        elif value == 'jersey_barrier':
            return 'Jersey Barrier'
        elif value == 'sally_port':
            return 'Sally Port'
        elif value == 'ditch':
            return 'Ditch'
        elif value == 'retaining_wall':
            return 'Retaining Wall'
        elif value == 'hedge':
            return 'Hedge Wall'
        elif value == 'horse_stile':
            return 'Horse Stile'
        elif value == 'log':
            return 'Log'
        elif value == 'wall':
            return 'Wall'
        elif value == 'fence':
            return 'Fence'
        elif value == 'entrance':
            return 'Entrance'
        elif value == 'hampshire_gate':
            return 'Hampshire Gate'
        elif value == 'lift_gate':
            return 'Lift Gate'
        elif value == 'spikes':
            return 'Spike Strip'
        elif value == 'kerb':
            return 'Kerb'
        elif value == 'cycle_barrier':
            return 'Cycle Barrier'
        elif value == 'chain':
            return 'Chain'
        elif value == 'full-height_turnstile':
            return 'Full-Height Turnstile'
        elif value == 'kissing_gate':
            return 'Kissing Gate'
        elif value == 'kent_carriage_gap':
            return 'Kent Carriage Gap'
        elif value == 'rope':
            return 'Rope'
        elif value == 'motorcycle_barrier':
            return 'Motorcycle Barrier'

        return super(BarrierTagHandler, self).get_description_text(entity, value)