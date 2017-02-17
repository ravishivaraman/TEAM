"""
.. moduleauthor:: Ravi Shivaraman <ravi.shivaraman@gmail.com>
"""

import socket
import time
import select

class TEAMConnection:
    """ This class creates objects that initialize connections to the EBSD camera. The Map collection is enabled by an IP / API (Application Programming Interface) interface to the TEAM software. 
            
    """
    
    def __init__(self):
        """ This is the constructor for the :class:`TEAMConnection` class. 
        
        :param str sock_team: A variable used to represent the socket object.
        """
        self.sock_team = 0                      
    
    def Connect(self, host, port):
        """ This method enables TEAM software connect to the server. 
        
        The :mod:`socket` module is employed here (see `documentation <https://docs.python.org/3/library/socket.html#socket.socket>`_).  
        
        :param str host: The IP address of the server to be connected to. 
        :param str port: The Port number of the connection. 
        
        """
        try:
            self.sock_team = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_team.connect((host, port))
            return 0
        
        except:
            self.Disconnect()
            return -1
    #end def
            
    def Disconnect(self):
        """ This method closes the socket connection. (see `documentation <https://docs.python.org/3/library/socket.html#socket.socket.close>`_).
        """
        try:
            if self.sock_team != 0:
                socket.close(self.sock_team)
                self.sock_team = 0
        except:
            pass
    #end def            
    
    def EDAXUnlock(self):    
        """ This method issues the command ``edax_unlock`` required when opening a new connection with the IPAPI.
        
            :returns: ``Client Connection Accepted``
        """        
        self.sock_team.send('edax_unlock'.encode())
        msg = self.sock_team.recv(4096).decode()
        if msg.lower() != 'client connection accepted':
            socket.close(self.sock_team)
            exit()
        return msg
        
    def IsTEAMStarted(self):
        """ This method issues the command ``get_system_isteamstarted_ebsd`` and verifies if the TEAM software is running. 
        
            :returns: ``get_system_isteamstarted_ebsd RESPONSE "True"`` or ``get_system_isteamstarted_ebsd RESPONSE "False"``
        """
        self.sock_team.send('get_system_isteamstarted_ebsd'.encode())
        msg = self.sock_team.recv(4096).decode()
        if msg.lower() != 'get_system_isteamstarted_ebsd response "true"':
            socket.close(self.sock_team)
            exit()
        return msg
    
    def RemoteAccessType(self):
        """ This method sets the Remote Access Type for map setup. If **1** (*NoWait*) is specified then the command 
            ``SET_MAP_PARAMS_FOLDERPATH`` or ``SET_EBSD_PARAMS_FOLDERPATH`` be sent before mapping begins otherwise the path won't be set.
            
            :returns: ``set_system_remoteaccesstype RESPONSE "Execution Successful"``
        """
        self.sock_team.send('set_system_remoteaccesstype "1"'.encode())
        msg = self.sock_team.recv(4096).decode()
        if msg.lower() != 'set_system_remoteaccesstype response "execution successful"':
            socket.close(self.sock_team)
            exit()
        return msg

#---------------------------------------------------------------------------------------------------------------------#         
#---------------------------------------------------------------------------------------------------------------------#  

    def GetEBSDCameraStatus(self):
        """ This method issues a comand ``get_camera_status`` that returns the EBSD camera status. The detailed list of Camera slide status enumeration follows:
            
            ========================   =========
            SlideOut                    0 
            SlideIn                     1 
            SlideMovingOut              2 
            SlideMovingIn               3 
            SlideHighCount              4 
            SlideNoPower                5 
            SlideMid                    6 
            SlideStopped                7 
            SlideError                  8 
            SlideInit                   9 
            SlideMoveMidIn              10 
            SlideMoveMidOut             11 
            SlideWatchDog               12 
            SlideMoveWDog               13 
            SlideDisabled               14 
            SlideMoveTouch              15 
            SlideTouchSense             16 
            Unknown                     100
            ========================   =========
            
            :returns: ``get_camera_status RESPONSE *Camera_Status*``
 
        """
        self.sock_team.send('get_camera_status'.encode())
        msg = self.sock_team.recv(4096).decode()
        return msg
        
    def InsertEBSDCamera(self, event):
        """ This method inserts the EBSD camera. First the request for a camera status update is sent. If the camera status response is ``get_camera_status response "slidein"``, 
            then the ``do_map_insert_camera`` command is dispatched. Subsequently, if the ``do_map_insert_camera response "execution successful"`` response is not recieved then the
            error message ``Could not insert Camera.`` is displayed. Post complete insertion, an *event* message ``EVENT_CAMERA_INSERTED_EBSD "Camera inserted"`` is returned. If
            this message is not returned, then the error message ``Could not insert camera`` is displayed. 
            
            :param str event: string describing the EBSD camera status.
        """
        Camera_Status = event
        try:
            if Camera_Status.lower() != 'get_camera_status response "slidein"':
                self.sock_team.send('do_map_insert_camera'.encode())                
                msg = self.sock_team.recv(4096).decode()
                print(msg)
                if 'do_map_insert_camera response "execution successful"' not in msg.lower():
                    print(msg)
                    print('Could not insert Camera.')
                    socket.close(self.sock_team)
                    exit()                
                check_msg = self.sock_team.recv(4096).decode()
                if 'event_camera_inserted_ebsd "camera inserted"' not in check_msg.lower():
                    print('Could not insert Camera.')
                    socket.close(self.sock_team)
                    exit()
                else:
                    print(check_msg)
        except:
            pass    
    
    def RetractEBSDCamera(self, event):
        """ This method retracts the EBSD camera. First the request for a camera status update is sent. If the camera status response is ``get_camera_status response "slideout"``, 
            then the ``do_map_retract_camera`` command is dispatched. Subsequently, if the ``do_map_retract_camera response "execution successful"`` response is not recieved then the
            error message ``Could not retract Camera.`` is displayed. Post complete retraction, an *event* message ``EVENT_CAMERA_RETRACTED_EBSD "Camera retracted"`` is returned. If
            this message is not returned, then the error message ``Could not retract camera`` is displayed. 
            
            :param str event: string describing the EBSD camera status.
        """
        Camera_Status = event
        try:
            if Camera_Status.lower() != 'get_camera_status response "slideout"':
                self.sock_team.send('do_map_retract_camera'.encode())                
                msg = self.sock_team.recv(4096).decode()
                print(msg)
                if 'do_map_retract_camera response "execution successful"' not in msg.lower():
                    print('Could not retract Camera.')
                    socket.close(self.sock_team)
                    exit()
                check_msg = self.sock_team.recv(4096).decode()
                if 'event_camera_retracted_ebsd "camera retracted"' not in check_msg.lower():
                    print('Could not retract Camera.')
                    socket.close(self.sock_team)
                    exit()
                else:
                    print(check_msg)
                
        except:
            pass
    
    def SetFolderParams(self, NumSlices, SliceThickness, AreaName):
        """ This method sets the project information. The GUID - ``{19B4F768-9231-4830-8E1F-69AAC6D59380}`` sets the project folder name as the current selection. 
        
            :param str AreaName: Each scan is stored under a folder called ``AreaName`` that resides under the project folder
            :param int NumSlices: Number of slices that are collected during a given volumetric scan.
            :param float SliceThickness: The thickness of each slice in *microns*
        """
        self.sock_team.send(('set_system_projectinfo_ext_ebsd "{19B4F768-9231-4830-8E1F-69AAC6D59380}" "%s" "%d" "%f" '%(AreaName, NumSlices, SliceThickness)).encode())        
        msg = self.sock_team.recv(4096).decode()
        print(msg)
        
    def SetFolderPath(self, fPath):
        """ This method sets the path of the project folder. 
        
            :param str fPath: path of the project folder. 
        """
        self.sock_team.send(('set_ebsd_params_folderpath "%s"'%fPath).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
        
    def SetEBSDHoughPeakSave(self, val):
        """ This method sends the command ``set_ebsd_params_savehoughpeaks **VAL**`` that enables or disables the saving of hough peaks during EBSD mapping.
        
            :param str val: set val to "TRUE" or "FALSE"
        """
        self.sock_team.send(('set_ebsd_params_savehoughpeaks "%s"'%val).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEBSDPatternSave(self, val):
        """ This method sends the command ``set_ebsd_params_savepatterns **VAL**`` that enables or disables the saving of EBSD patterns during mapping.
        
            :param str val: set val to "TRUE" or "FALSE"
        """
        self.sock_team.send(('set_ebsd_params_savepatterns "%s"'%val).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEBSDSpectraSave(self, val):
        """ This method sends the command ``set_ebsd_params_savespectra **VAL**`` that enables or disables the saving of spectra during mapping combined EDS/EBSD mapping.
        
            :param str val: set val to "TRUE" or "FALSE"
        """
        self.sock_team.send(('set_ebsd_params_savespectra "%s"'%val).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEBSDGrid(self, GridType):
        """ This method sends the command ``set_ebsd_params_grid **GridType**`` that sets the grid topology. 
        
            :param int GridType: set GridType to "0" - Square or "1" - Hexagonal
        """
        self.sock_team.send(('set_ebsd_params_grid "%d"'%GridType).encode())
        msg = self.sock_team.recv(4096).decode()        
        print(msg)

    def SetEBSDXStart(self, XStart):
        """ This method sends the command ``set_ebsd_params_xstart **XStart**`` that Sets the X coordinate for the EBSD mapping area in microns, with 0 being the center of the field of view.
        
            :param float XStart: Sets the X coordinate for the EBSD mapping area in microns.
        """
        self.sock_team.send(('set_ebsd_params_xstart "%f"'%XStart).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
        
    def SetEBSDYStart(self, YStart):
        """ This method sends the command ``set_ebsd_params_ystart **YStart**`` that Sets the Y coordinate for the EBSD mapping area in microns, with 0 being the center of the field of view.
        
            :param float YStart: Sets the Y coordinate for the EBSD mapping area in microns.
        """
        self.sock_team.send(('set_ebsd_params_ystart "%f"'%YStart).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)

    def SetEBSDXSize(self, XSize):
        """ This method sends the command ``set_ebsd_params_xsize **XSize**`` that sets the extent of the MAP in X-direction 
        
            :param float XSize: Extent of the map in X-direction in microns. 
        """ 
        self.sock_team.send(('set_ebsd_params_xsize "%f"'%XSize).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEBSDYSize(self, YSize):
        """ This method sends the command ``set_ebsd_params_ysize **YSize**`` that sets the extent of the MAP in Y-direction 
        
            :param float YSize: Extent of the map in Y-direction in microns.
        """
        self.sock_team.send(('set_ebsd_params_ysize "%f"'%YSize).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEBSDResolution(self, ResVal):
        """ This method sends the command ``set_ebsd_params_resolution **ResVal**`` that sets the EBSD Mapping resolution
            
            #. 0 - Fine
            #. 1 - Medium
            #. 2 - Coarse
            #. 3 - Custom
            
            :param int ResVal: EBSD Mapping resolution type. If ``ResVal`` is set to *3* then :func:`SetEBSDStepSize` needs to be set. 
        """
        self.sock_team.send(('set_ebsd_params_resolution "%d"'%ResVal).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
        
    def SetEBSDStepSize(self, Step):
        """ This method sends the command ``set_ebsd_params_customstepsize **Step**`` that sets the step size of the EBSD map in microns.  This is ignored unless the Resolution is set to Custom.
        
            :param float Step:   Sets the step size of the EBSD map in microns.
        
        """
        self.sock_team.send(('set_ebsd_params_customstepsize "%f"'%Step).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def GetEBSDMapStatus(self):
        """ This functions sends out the command ``get_map_status_ebsd``. The value of current map status is returned. 
            The detailed list of EBSD Map status enumeration is given below:
                
            ========================   =========  
                NotReady                0
                Ready                   1
                SetupActive             2
                SetupComplete           3
                SetupPaused             4 
                SetupResumed            5 
                SetupAborted            6 
                SetupStopped            7
                SetupError              8
                MappingActive           9 
                MappingComplete         10
                MappingPaused           11 
                MappingResumed          12 
                MappingAborted          13 
                MappingStopped          14 
                MappingError            15 
                UnknownError            16
            ========================   =========
            
            :returns: ``get_map_status RESPONSE *Map_Status*``
                
        """
        self.sock_team.send('get_map_status_ebsd'.encode())
        msg = self.sock_team.recv(4096).decode()
        return msg
    
    def EBSDMapCollection(self, event, mapID):
        """ This method starts EBSD map collection. First the request for a camera status update is sent. If the map status response is ``get_map_status RESPONSE "Ready"``, 
            then the ``do_map_collection_start_ebsd`` command is dispatched. Subsequently, if the ``do_map_collection_start_ebsd response "execution successful"`` response is not recieved then the
            error message ``Could not Start Map Collection.`` is displayed. Post mapping complete, an *event* message ``EVENT_MAP_COLLECTION_COMPLETE_EBSD "Mapping Complete"`` is returned. If
            this message is not returned, then the error message ``Mapping was not completed.`` is displayed. 
            
            :param str event: string describing the EBSD map status.
            :param int mapID: unique map identifier.
        """
        EBSD_MapStatus = event
        try:
            if EBSD_MapStatus.lower() == 'get_map_status_ebsd response "ready"':
                self.sock_team.send(('do_map_collection_start_ebsd "%d"'%mapID).encode())                
                msg = self.sock_team.recv(4096).decode()
                if msg.lower() != 'do_map_collection_start_ebsd response "execution successful"':
                    print('Could not Start Map Collection.')
                    socket.close(self.sock_team)
                    exit()
                #print("starting map..")                    
                check_msg = self.sock_team.recv(4096).decode()
                if 'event_map_collection_complete_ebsd "mapping complete"' not in check_msg.lower():
                    print('Mapping was not completed.')
                    socket.close(self.sock_team)
                    exit()
                else:
                    print('Mapping is Complete.')
                
            else:
                print('Map Status is not ready.')
                socket.close(self.sock_team)
                exit()
        except:
            pass

#---------------------------------------------------------------------------------------------------------------------#         
#---------------------------------------------------------------------------------------------------------------------# 

    def GetEDSDetectorStatus(self):
        self.sock_team.send('get_system_detector_status'.encode())
        msg = self.sock_team.recv(4096).decode()
        return msg
        
    def GetEDSMapStatus(self):
        self.sock_team.send('get_map_status'.encode())
        msg = self.sock_team.recv(4096).decode()
        return msg
    
    def SetEDSFolderParams(self, NumSlices, SliceThickness, AreaName):
        self.sock_team.send(('set_system_projectinfo_ext "{19B4F768-9231-4830-8E1F-69AAC6D59380}" "%s" "%d" "%f" '%(AreaName, NumSlices, SliceThickness)).encode())
        #msg = self.recv_fully(2).decode()
        msg = self.sock_team.recv(4096).decode()
        print(msg)
        
    def SetEDSFolderPath(self, fPath):
        self.sock_team.send(('set_map_params_folderpath "%s"'%fPath).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEDSChannel(self, edsChan):
        self.sock_team.send(('set_map_params_edschannel "%d"'%edsChan).encode())
        msg = self.sock_team.recv(4096).decode()        
        print(msg)

    def SetEDSFrames(self, nFrames):
        self.sock_team.send(('set_map_params_numframes "%d"'%nFrames).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
        
    def SetEDSXResolution(self, nPoints):
        self.sock_team.send(('set_map_params_numpoints "%d"'%nPoints).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)

    def SetEDSYResolution(self, nLines):
        self.sock_team.send(('set_map_params_numlines "%d"'%nLines).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEDSDwell(self, EDSDwell):
        self.sock_team.send(('set_map_params_presetdwell "%f"'%EDSDwell).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEDSNumChan(self, numChan):
        self.sock_team.send(('set_map_params_edsnumchan "%d"'%numChan).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEDSBytesPerChane(self, bytesPerChan):
        self.sock_team.send(('set_map_params_bytesperchannel "%d"'%bytesPerChan).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEDS_IPD(self, IPDval):
        self.sock_team.send(('set_map_params_ipd "%f"'%IPDval).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
    
    def SetEDSvideoReads(self, numReads):
        self.sock_team.send(('set_map_params_numreads "%d"'%numReads).encode())
        msg = self.sock_team.recv(4096).decode()
        print(msg)
        
    def EDSMapCollection(self, event, mapID):
        EDS_MapStatus = event
        try:
            if EDS_MapStatus.lower() == 'get_map_status response "ready"':
                self.sock_team.send(('do_map_collection_start "%d"'%mapID).encode())                
                msg = self.sock_team.recv(4096).decode()
                if msg.lower() != 'do_map_collection_start response "execution successful"':
                    print('Could not Start Map Collection.')
                    socket.close(self.sock_team)
                    exit()
                #print("starting map..")                    
                check_msg = self.sock_team.recv(4096).decode()
                if 'event_map_collection_complete "mapping complete"' not in check_msg.lower():
                    print('Mapping was not completed within allotted time. Increase wait time.')
                    socket.close(self.sock_team)
                    exit()
                else:
                    print('Mapping is Complete.')
                
            else:
                print('Map Status is not ready.')
                socket.close(self.sock_team)
                exit()
        except:
            pass

#---------------------------------------------------------------------------------------------------------------------#         
#---------------------------------------------------------------------------------------------------------------------# 
    
    def recv_fully(self,timeout=2):
        """ This method sets the ``socket.recv()`` call to non-blocking mode. It then presets a wait time for the socket.
            At the end of the wait time, the recieved data string is returned. 
            
        """        
        self.sock_team.setblocking(0)
        total_data = []
        data = ''
        begin = time.time()
        
        while 1:
            #if you got some data, then break after wait sec
            if total_data and (time.time() - begin) > timeout:
                break
            #if you got no data at all, wait a little longer
            #elif time.time() - begin > timeout*2:
            #    break

            try:
                data = self.sock_team.recv(4096)
                if data:
                    total_data.append(data)
                    begin=time.time()
                else:
                    time.sleep(1)
            except:
                pass
        self.sock_team.setblocking(1)
        return (''.encode()).join(total_data)
        
    def empty_socket(self):
        """ This method removes the data present on the socket.
        """
        input = [self.sock_team]
        while 1:
            inputready, outputready, exceptready = select.select(input,[],[], 0.0)
            if len(inputready)==0: 
                break
            for sock in inputready: 
                sock.recv(1)
        #end while
    #end def