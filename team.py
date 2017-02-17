"""
.. moduleauthor:: Ravi Shivaraman <ravi.shivaraman@gmail.com>
"""

from TEAM import team_conn

class TEAM:
    
    def __init__(self):
        """Constructor for the :class:`TEAM` class. This creates an instance of the :class:`TEAMConnection`. """
        self.connection = team_conn.TEAMConnection()
                
    def Connect(self, address, port):
        """ This method calls the :func:`Connect` method from :class:`TEAMConnection` to open a socket connection with the TEAM server. 
        
            :param str address: TEAM server IP address
            :param str port:    The port number accessed by the socket. 
        """        
        self.connection.Connect(address,port)
        
    def Disconnect(self):
        """ This method calls the :func:`Disconnect` method from :class:`TEAMConnection` to close a socket connection with the TEAM server. 
        """
        self.connection.Disconnect()
    
    def Initialize(self):
        """ This method calls three methods :func:`EDAXUnlock`, :func:`IsTEAMStarted` and :func:`RemoteAccessType` from :class:`TEAMConnection` that initialize and verify connection with TEAM server. 
        
            :returns:  ``get_system_isteamstarted_ebsd RESPONSE "True"`` or ``get_system_isteamstarted_ebsd RESPONSE "False"``
        """
        self.connection.EDAXUnlock()
        return self.connection.IsTEAMStarted()
        self.connection.RemoteAccessType()
        
    def CameraPosition(self):
        """ This method calls the :func:`GetEBSDCameraStatus` method from :class:`TEAMConnection`. 
        
            :returns: ``get_camera_status RESPONSE *Camera_Status*``
        """
        return self.connection.GetEBSDCameraStatus()
        
    def RetractCamera(self):
        """ This method calls the :func:`RetractEBSDCamera` method from :class:`TEAMConnection`. 
        """
        self.connection.RetractEBSDCamera(self.CameraPosition())

    def InsertCamera(self):
        """ This method calls the :func:`InsertEBSDCamera` method from :class:`TEAMConnection`. 
        """
        self.connection.InsertEBSDCamera(self.CameraPosition())
        
    def MappingSetup(self, AreaName, fPath, NumSlices, SliceThickness, GridType, 
                     XStart, YStart, XSize, YSize, ResVal, Step):
        """ This method calls the :func:`SetFolderParams`, :func:`SetFolderPath`, :func:`SetEBSDGrid`, :func:`SetEBSDXStart`, 
            :func:`SetEBSDYStart`, :func:`SetEBSDXSize`, :func:`SetEBSDYSize`, :func:`SetEBSDResolution`, 
            and :func:`SetEBSDStepSize` methods from :class:`TEAMConnection` that setup Mapping parameters. 
            
            :param str AreaName: Each scan is stored under a folder called ``AreaName`` that resides under the project folder
            :param str fPath: path of the project folder. 
            :param int NumSlices: Number of slices that are collected during a given volumetric scan.
            :param float SliceThickness: The thickness of each slice in *microns*
            :param int GridType: set GridType to "0" - Square or "1" - Hexagonal
            :param float XStart: Sets the X coordinate for the EBSD mapping area in microns.
            :param float YStart: Sets the Y coordinate for the EBSD mapping area in microns.
            :param float XSize: Extent of the map in X-direction in microns. 
            :param float YSize: Extent of the map in Y-direction in microns.
            :param int ResVal: EBSD Mapping resolution type. If ``ResVal`` is set to *3* then :func:`SetEBSDStepSize` needs to be set.
            :param float Step:   Sets the step size of the EBSD map in microns.
            
        """
        self.connection.SetFolderParams(NumSlices, SliceThickness, AreaName)
        self.connection.SetFolderPath(fPath)
        self.connection.SetEBSDGrid(GridType)
        self.connection.SetEBSDXStart(XStart) 
        self.connection.SetEBSDYStart(YStart)
        self.connection.SetEBSDXSize(XSize)
        self.connection.SetEBSDYSize(YSize)
        self.connection.SetEBSDResolution(ResVal)
        self.connection.SetEBSDStepSize(Step)
        
    def MapStatus(self):
        """ This method calls the :func:`GetEBSDMapStatus` method from :class:`TEAMConnection`. 
        
            :returns: ``get_map_status RESPONSE *Map_Status*``
        """
        return self.connection.GetEBSDMapStatus()
        
    def CollectEBSDMap(self, MapID):
        """ This method calls the :func:`EBSDMapCollection` method from :class:`TEAMConnection`.
        
            :param int mapID: unique map identifier.
        """
        self.connection.EBSDMapCollection(self.MapStatus(), MapID)
    
    def EDSMappingSetup(self, AreaName, fPath, NumSlices, SliceThickness, nFrames, 
                     nPoints, nLines):
        """ This method calls the :func:`SetEDSFolderParams`, :func:`SetEDSFolderPath`, 
            :func:`SetEDSFrames`, :func:`SetEDSXResolution`, :func:`SetEDSYResolution`, 
            methods from :class:`TEAMConnection` that setup Mapping parameters. 
            
            :param str AreaName: Each scan is stored under a folder called ``AreaName`` that resides under the project folder
            :param str fPath: path of the project folder. 
            :param int NumSlices: Number of slices that are collected during a given volumetric scan.
            :param float SliceThickness: The thickness of each slice in *microns*
            :param int nFrames: Sets the number of frames for the EDS map.
            :param float nPoints: Sets the number of points for one line of the EDS map.
            :param float nLines: Sets the number of lines for one frame of the EDS map.
                
        """
        self.connection.SetEDSFolderParams(NumSlices, SliceThickness, AreaName)
        self.connection.SetEDSFolderPath(fPath)        
        self.connection.SetEDSFrames(nFrames) 
        self.connection.SetEDSXResolution(nPoints)
        self.connection.SetEDSYResolution(nLines)        
    
    def EDSMapStatus(self):
        """ This method calls the :func:`GetEBSDMapStatus` method from :class:`TEAMConnection`. 
        
            :returns: ``get_map_status RESPONSE *Map_Status*``
        """
        return self.connection.GetEDSMapStatus()
        
    def CollectEDSMap(self, MapID):
        """ This method calls the :func:`EBSDMapCollection` method from :class:`TEAMConnection`.
        
            :param int mapID: unique map identifier.
        """
        self.connection.EDSMapCollection(self.EDSMapStatus(), MapID)
        
        