"""
/***************************************************************************
Name                 : JapanMesh
Description          : Create a mesh layer(Lat 20-46,Lon 122-154)
Date                 : 6/Sep/14
copyright            : (C) 2014 by Digital Energy
email                : gis@energy.co.jp
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def classFactory(iface):
    from .JapanMesh import JapanMesh
    return JapanMesh(iface)

