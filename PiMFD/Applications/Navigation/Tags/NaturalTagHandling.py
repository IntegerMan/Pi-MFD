# coding=utf-8

"""
Handles the "natural" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class NaturalTagHandler(TagHandler):
    def get_color(self, entity, value, cs):

        """
        :type entity: MapEntity
        :type value: string
        :type cs: ColorScheme
        :rtype : tuple
        """
        if value in ('wood', 'tree_row', 'tree', 'scrub'):
            return cs.map_vegetation
        elif value in ('heath', 'moor', 'mud', 'sinkhole'):
            return cs.map_vegetation  # TODO: Maybe something more beige?
        elif value in ('grassland', 'fell'):
            return cs.map_vegetation  # TODO: Maybe something more grass like?
        elif value in ('bare_rock', 'scree', 'peak', 'ridge', 'arete', 'cliff', 'saddle', 'rock', 'stone'):
            return cs.gray
        elif value == 'volcano':
            return cs.map_emergency
        elif value in ('sand', 'beach', 'coastline'):
            return cs.map_vegetation  # TODO: Maybe something more sand-like?
        elif value in ('water', 'bay', 'glacier', 'spring'):
            return cs.map_water
        elif value == 'cave_entrance':
            return cs.map_recreation

        return super(NaturalTagHandler, self).get_color(entity, value, cs)

    def get_description_text(self, entity, value):
        """
        :type entity: MapEntity
        :type value: string
        :rtype: string
        """

        if value == 'wood':
            return 'Woods'
        elif value == 'tree_row':
            return 'Tree Row'
        elif value == 'tree':
            return 'Tree'
        elif value == 'scrub':
            return 'Bushlands'
        elif value == 'heath':
            return 'Wasteland'
        elif value == 'moor':
            return 'Moor'
        elif value == 'grassland':
            return 'Grassland'
        elif value == 'fell':
            return 'Highlands'
        elif value == 'bare_rock':
            return 'Bedrock'
        elif value == 'scree':
            return 'Gravel'
        elif value == 'sand':
            return 'Sand'
        elif value == 'mud':
            return 'Mud'
        elif value == 'water':
            return 'Water'
        elif value == 'wetland':
            return 'Wetland'
        elif value == 'glacier':
            return 'Glacier'
        elif value == 'bay':
            return 'Bay'
        elif value == 'beach':
            return 'Beach'
        elif value == 'coastline':
            return 'Coastline'
        elif value == 'spring':
            return 'Spring'
        elif value == 'peak':
            return 'Peak'
        elif value == 'volcano':
            return 'Volcano'
        elif value == 'ridge':
            return 'Ridge'
        elif value == 'arete':
            return 'Arete (Knife Ridge)'
        elif value == 'cliff':
            return 'Cliff'
        elif value == 'saddle':
            return 'Mountain / Hill Saddle'
        elif value == 'rock':
            return 'Rock'
        elif value == 'stone':
            return 'Stone'
        elif value == 'sinkhole':
            return 'Sinkhole'
        elif value == 'cave_entrance':
            return 'Cave Entrance'

        return super(NaturalTagHandler, self).get_description_text(entity, value)