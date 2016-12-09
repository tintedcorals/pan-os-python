#!/usr/bin/env python

# Copyright (c) 2014, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Brian Torres-Gil <btorres-gil@paloaltonetworks.com>

"""Objects module contains objects that exist in the 'Objects' tab in the firewall GUI"""

# import modules
import re
import logging
import xml.etree.ElementTree as ET
import pandevice
from base import PanObject, Root, MEMBER, ENTRY
from base import VarPath as Var
from pandevice.base import VersionedPanObject
from pandevice.base import VersionedParamPath

# import other parts of this pandevice package
import errors as err

# set logging to nullhandler to prevent exceptions if logging not enabled
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class AddressObject(VersionedPanObject):
    """Address Object

    Args:
        name (str): Name of the object
        value (str): IP address or other value of the object
        type (str): Type of address:
                * ip-netmask (default)
                * ip-range
                * fqdn
        description (str): Description of this object
        tag (list): Administrative tags
    """
    ROOT = Root.VSYS
    SUFFIX = ENTRY

    def _setup(self):
        # xpaths
        self._xpaths.add_profile(value='/address')

        # params
        params = []

        params.append(VersionedParamPath(
            'value', path='{type}'))
        params.append(VersionedParamPath(
            'type', default='ip-netmask',
            values=['ip-netmask', 'ip-range', 'fqdn'], path='{type}'))
        params.append(VersionedParamPath(
            'description', path='description'))
        params.append(VersionedParamPath(
            'tag', path='tag', vartype='member'))

        self._params = tuple(params)


class AddressGroup(VersionedPanObject):
    ROOT = Root.VSYS
    SUFFIX = ENTRY

    def _setup(self):
        # xpaths
        self._xpaths.add_profile(value='/address-group')

        # params
        params = []

        params.append(VersionedParamPath(
            'static_value', path='static', vartype='member'))
        params.append(VersionedParamPath(
            'dynamic_value', path='dynamic/filter'))
        params.append(VersionedParamPath(
            'description', path='description'))
        params.append(VersionedParamPath(
            'tag', path='tag', vartype='member'))

        self._params = tuple(params)


class Tag(PanObject):
    """Administrative tag

    Args:
        name (str): Name of the tag
        color (str): Color ID or name (eg. 'color1', 'color4', 'purple')
        comments (str): Comments

    """
    ROOT = Root.VSYS
    XPATH = "/tag"
    SUFFIX = ENTRY

    COLOR = {
        "red":         1,
        "green":       2,
        "blue":        3,
        "yello":       4,
        "copper":      5,
        "orange":      6,
        "purple":      7,
        "gray":        8,
        "light green": 9,
        "cyan":        10,
        "light gray":  11,
        "blue gray":   12,
        "lime":        13,
        "black":       14,
        "gold":        15,
        "brown":       16,
    }

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        if not hasattr(self, "_color"):
            self._color = None

    @classmethod
    def variables(cls):
        return (
            Var("color"),
            Var("comments"),
        )

    @property
    def color(self):
        if self._color in self.COLOR:
            return "color"+str(self.COLOR[self._color])
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
