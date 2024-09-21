# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under proprietary license. See license file in the directory of this plugin for details.
#
# This file is part of Prism-Plugin-PrismInternals.
#
# Prism-Plugin-PrismInternals is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


import os


class Prism_PrismInternals_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.10"
        self.pluginName = "PrismInternals"
        self.pluginType = "Custom"
        self.platforms = ["Windows", "Linux"]
        self.pluginDirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
