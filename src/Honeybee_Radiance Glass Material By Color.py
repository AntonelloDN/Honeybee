#
# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# 
# This file is part of Honeybee.
# 
# Copyright (c) 2013-2015, Mostapha Sadeghipour Roudsari <Sadeghipour@gmail.com> 
# Honeybee is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# Honeybee is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Radiance Glass Material By Color
Read more here to understand Radiance materials: http://www.artifice.com/radiance/rad_materials.html
-
Provided by Honeybee 0.0.58

    Args:
        _materialName: Unique name for this material
        _color: color of the glass
        refractiveIndex_: RefractiveIndex is 1.52 for glass and 1.4 for ETFE
    Returns:
        avrgTrans: Average transmittance of this glass
        RADMaterial: Radiance Material string

"""

ghenv.Component.Name = "Honeybee_Radiance Glass Material By Color"
ghenv.Component.NickName = 'radGlassMaterialByColor'
ghenv.Component.Message = 'VER 0.0.58\nNOV_13_2015'
ghenv.Component.Category = "Honeybee"
ghenv.Component.SubCategory = "01 | Daylight | Material"
#compatibleHBVersion = VER 0.0.58\nNOV_13_2015
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "0"
except: pass


import math
import scriptcontext as sc
import Grasshopper.Kernel as gh

# read here to understand RAD materials
# http://www.artifice.com/radiance/rad_materials.html

# refractiveIndex is 1.52 for glass and 1.4 for ETFE

def getTransmissivity(transmittance):
    return (math.sqrt(0.8402528435 + 0.0072522239 * (transmittance ** 2)) - 0.9166530661 ) / 0.0036261119 / transmittance
    
def createRadMaterial(modifier, name, *args):
    # I should check the inputs here
    
    radMaterial = "void " + modifier + " " + name + "\n" + \
                  "0\n" + \
                  "0\n" + \
                  `int(len(args))`
                  
    for arg in args: radMaterial = radMaterial + (" " + "%.3f"%arg)
    
    return radMaterial + "\n"


modifier = "glass"

if sc.sticky.has_key('honeybee_release'):
    
    sc.sticky['honeybee_release'].isInputMissing(ghenv.Component)
    
    if _materialName!=None and _color != None:
        RTransmittance = _color.R/255
        GTransmittance = _color.G/255
        BTransmittance = _color.B/255
        
        if 0 <= RTransmittance <= 1 and 0 <= GTransmittance <= 1 and 0 <= BTransmittance <= 1:
            avrgTrans = (0.265 * RTransmittance + 0.670 * GTransmittance + 0.065 * BTransmittance)
            
            materialName = _materialName.Replace(" ", "_")
            RADMaterial = createRadMaterial(modifier, materialName, RTransmittance, GTransmittance, BTransmittance, refractiveIndex_)
        else:
            msg =  "Transmittance values should be between 0 and 1"
            e = gh.GH_RuntimeMessageLevel.Error
            ghenv.Component.AddRuntimeMessage(e, msg)
else:
    print "You should first let Honeybee to fly..."
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "You should first let Honeybee to fly...")

