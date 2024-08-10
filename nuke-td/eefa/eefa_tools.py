"""
    __author__ = "Bardia Hassanzadeh"
    __copyright__ = "Copyright (C) 2024 EEFA VFX"
    __license__ = "Public Domain"
    __version__ = "1.0"
"""
import hiero.core
import hiero.ui
import nuke
import nukescripts


class EEFAPanel(nukescripts.PythonPanel):
    '''
    MultiChannelSplitPanel
    '''
    def __init__( self ):
            '''
            init values
            '''
            nukescripts.PythonPanel.__init__(self, "EEFAT", "EEFAT")
    
    def change_clip_knobs(self):
        # Get the current project
        project = hiero.core.projects()[-1]
        print('Project:', project)

        # Iterate through all sequences in the project
        for sequence in project.sequences():
            print('Sequence:', sequence)

            # Iterate through all video tracks in the sequence
            for track in sequence.videoTracks():
                print('Track:', track)

                # Iterate through all track items in the video track
                for track_item in track.items():
                    print('Track Item:', track_item)
                    methods = [method for method in dir(track_item) if callable(getattr(track_item, method))]
                    for method in methods:
                        print("method: ", method)
                    #print("Available OCIO: ", track_item.getAvailableOcioColourTransforms()) 
                    try:
                        track_item.setSourceMediaColourTransform('raw')
                        track_item.setCameraColourTransform('raw')
                    except Exception as e:
                        print("Exception Occured:", e) 
                
                    print('-----------------------------------------------------------')
    
    def show(self):
        print("Adding menu item...")
   
        # Create the "Tools" menu
        menubar = nuke.menu("Nuke")
        tools_menu = menubar.addMenu("EEFA Tools")
        tool_input_transform = tools_menu.addMenu("Input Transform")
   
        # Add "Tool1" to the "Tools" menu
        tool_input_transform.addCommand("RAW", self.change_clip_knobs)

        print("Menu item added: Tools > Tool1")
               

def initiate():
    print("Hello")
    EEFAPanelInstance = EEFAPanel()
    EEFAPanelInstance.show()