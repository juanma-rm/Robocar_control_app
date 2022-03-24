#==============================================================================
# Project: Robocar
# Application: Remote_Control
# File: CommunMessages.py
# Description: structure of messages exchanged between car and control app
#==============================================================================

#==============================================================================
# Import
#==============================================================================


#==============================================================================
# Protocol information
#==============================================================================

"""
/* For signed fields:
 * 	- INT16_MIN (-32768) will be considered as error
 * 	- Negative values refer to backward or left. Ex: -30 in linear speed refers 
      to 30 backward
 * 	- Positive values refer to forward or right
 * For unsigned fields:
 *  - UINT16_MAX (+65535) will be considered as error
 */
"""
"""
/* Control app outgoing message structure:
 * 		Field 0: working mode. Unsigned. 0: manual, 1: automatic
 * 		Field 1: manual control / Y-axis. Signed: [-100%, +100%]
 * 		Field 2: manual control / X-axis. Signed: [-100%, +100%]
 * 		Field 3: automatic control / setpoint speed (mm/s) / Y-axis.
        Signed: [-32767, +32767] mm/s
 * 		Field 4: automatic control / setpoint speed (??) / X-axis. Signed: [??]
 */
"""
outgoing_pos_dic = {
    0:"MESSAGE_IN_POS_WORKMODE",
    1:"MESSAGE_IN_POS_MANCTRLY_PERC",
    2:"MESSAGE_IN_POS_MANCTRLX_PERC",
    3:"MESSAGE_IN_POS_AUTCTRL_SPEEDY_MMS",
    4:"MESSAGE_IN_POS_AUTCTRL_SPEEDX_MMS",
}
"""
/* Control app incoming message structure:
 * 		Field 0: working mode. Unsigned. 0: manual, 1: automatic
 * 		Field 1: manual control / Y-axis. Signed: [-100%, +100%]
 * 		Field 2: manual control / X-axis. Signed: [-100%, +100%]
 * 		Field 3: automatic control / setpoint speed (mm/s) / Y-axis. 
        Signed: [-32767, +32767] mm/s
 * 		Field 4: automatic control / setpoint speed (??) / X-axis. Signed: [??]
 * 		Field 5: linear speed (mm/s). Unsigned: [-32767, +32767] mm/s
 * 		Field 6: left wheel speed (rpm). Signed: [-32767, +32767] rpm
 * 		Field 7: right wheel speed (rpm). Signed: [-32767, +32767] rpm
 *		Field 8: left distance (mm). Unsigned. [0,65535] mm
 *		Field 9: right distance (mm). Unsigned. [0,65535] mm
 *
 *		Errors, other...
 */
"""
incoming_pos_dic = {
    "MESSAGE_OUT_POS_WORKMODE"              :0,
    "MESSAGE_OUT_POS_MANCTRLY_PERC"         :1,
    "MESSAGE_OUT_POS_MANCTRLX_PERC"         :2,
    "MESSAGE_OUT_POS_AUTCTRL_SPEEDY_MMS"    :3,
    "MESSAGE_OUT_POS_AUTCTRL_SPEEDX_MMS"    :4,
    "MESSAGE_OUT_POS_LINSPEED_MMS"          :5,
    "MESSAGE_OUT_POS_LSPEED_RPM"            :6,
    "MESSAGE_OUT_POS_RSPEED_RPM"            :7,
    "MESSAGE_OUT_POS_LDIST_MM"              :8,
    "MESSAGE_OUT_POS_RDIST_MM"              :9,
}
def get_workmode_id(mode_str:str) -> int:
    ret_val = -1
    if mode_str == "Manual mode":
        ret_val = 0
    elif mode_str == "Automatic mode":
        ret_val = 1
    return ret_val
def get_workmode_name(mode_int:int) -> str:
    ret_val = "invalid mode name"
    if mode_int == 0:
        ret_val = "Manual mode"
    elif mode_int == 1:
        ret_val = "Automatic mode"
    return ret_val

#==============================================================================
# Global data
#==============================================================================

NB_CHAR_PER_MESS = 5

INT16_MIN = -32768
UINT16_MAX = 65535



#==============================================================================
# Classes
#==============================================================================

class Message_struct_in():
    """
    ===========================================================================
    Description
    ===========================================================================
    Message_struct_in class defines an object containing all the parameters
    used in the incoming communication between the car and this application

    ===========================================================================
    Attributes
    ===========================================================================
    - workmode: int. 0: manual. 1: automatic. Other: error
    - workmode_err: bool. True if error in workmode value
    - manctrly_perc: int [-100,100]
    - manctrly_err: bool. True if error in manctrly_perc value
    - manctrlx_perc: int [-100,100]
    - manctrlx_err: bool. True if error in manctrlx_perc value
    - autctrl_speedy_mms: int [-32767, +32767]
    - autctrl_speedy_err: bool. True if error in autctrl_speedy_mms value
    - autctrl_speedx_mms: int [??]
    - autctrl_speedx_err: bool. True if error in autctrl_speedx_mms value
    - linspeed_mms: int [-32767, +32767]
    - linspeed_mms_err: bool. True if error in linspeed_mms value
    - lspeed_rpm: int [-32767, +32767]
    - lspeed_rpm_err: bool. True if error in lspeed_rpm value
    - rspeed_rpm: int [-32767, +32767]
    - rspeed_rpm_err: bool. True if error in rspeed_rpm value
    - ldist_mm: int [0,65535]
    - ldist_mm_err: bool. True if error in ldist_mm value
    - rdist_mm: int [0,65535]
    - rdist_mm_err: bool. True if error in rdist_mm value
    """
    def __init__(   self, workmode: int, 
                    manctrly_perc: int, manctrlx_perc: int, 
                    autctrl_speedy_mms: int, autctrl_speedx_mms: int, 
                    linspeed_mms: int, lspeed_rpm: int, rspeed_rpm: int, 
                    ldist_mm: int, rdist_mm: int
                ):
        """
        :params all: see class info to know about valid types and ranges
        :exception ValueError may arise if types / ranges are not considered
        """
        # workmode
        self.workmode = None
        if _str_is_number(workmode):
            self.workmode = int(workmode)
        if (self.workmode==0 or self.workmode==1):
            self.workmode_err = False
        else:
            self.workmode_err = True
        # manctrly_perc
        self.manctrly_perc = None
        if _str_is_number(manctrly_perc):
            self.manctrly_perc = int(manctrly_perc)
        self.manctrly_err = False if (self.manctrly_perc >= -100 or self.manctrly_perc <= 100) \
            else True
        # manctrlx_perc
        self.manctrlx_perc = None
        if _str_is_number(manctrlx_perc):
            self.manctrlx_perc = int(manctrlx_perc)
        self.manctrlx_err = False if (self.manctrlx_perc >= -100 or self.manctrlx_perc <= 100) \
            else True
        # autctrl_speedy_mms
        self.autctrl_speedy_mms = None
        if _str_is_number(autctrl_speedy_mms):
            self.autctrl_speedy_mms = int(autctrl_speedy_mms)
        self.autctrl_speedy_err = True if (self.autctrl_speedy_mms==INT16_MIN or self.autctrl_speedy_mms==None) \
            else False
        # autctrl_speedx_mms
        self.autctrl_speedx_mms = None
        if _str_is_number(autctrl_speedx_mms):
            self.autctrl_speedx_mms = int(autctrl_speedx_mms)
        self.autctrl_speedx_err = True if (self.autctrl_speedx_mms==INT16_MIN or self.autctrl_speedx_mms==None) \
            else False
        # linspeed_mms
        self.linspeed_mms = None
        if _str_is_number(linspeed_mms):
            self.linspeed_mms = int(linspeed_mms)
        self.linspeed_err = True if (self.linspeed_mms==INT16_MIN or self.linspeed_mms==None) \
            else False
        # lspeed_rpm
        self.lspeed_rpm = None
        if _str_is_number(lspeed_rpm):
            self.lspeed_rpm = int(lspeed_rpm)
        self.lspeed_err = True if (self.lspeed_rpm==INT16_MIN or self.lspeed_rpm==None) \
            else False
        # rspeed_rpm
        self.rspeed_rpm = None
        if _str_is_number(rspeed_rpm):
            self.rspeed_rpm = int(rspeed_rpm)
        self.rspeed_err = True if (self.rspeed_rpm==INT16_MIN or self.rspeed_rpm==None) \
            else False
        # ldist_mm
        self.ldist_mm = None
        if _str_is_number(ldist_mm):
            self.ldist_mm = int(ldist_mm)
        self.ldist_err = True if (self.ldist_mm==UINT16_MAX or self.ldist_mm==None) \
            else False
        # rdist_mm
        self.rdist_mm = None
        if _str_is_number(rdist_mm):
            self.rdist_mm = int(rdist_mm)
        self.rdist_err = True if (self.rdist_mm==UINT16_MAX or self.rdist_mm==None) \
            else False

    def get_workmode_str(self):
        """ Returns string naming the current working mode """
        ret = "error"
        if (self.workmode_err == False):
            ret = get_workmode_name(self.workmode)
        return ret
        
class Message_struct_out():
    """
    ===========================================================================
    Description
    ===========================================================================
    Message_struct_out class defines an object containing all the parameters
    used in the outgoing communication between the car and this application

    ===========================================================================
    Attributes
    ===========================================================================
    - workmode: int. 0: manual. 1: automatic. Other: error
    - workmode_err: bool. True if error in workmode value
    - manctrly_perc: int [-100,100]
    - manctrly_err: bool. True if error in manctrly_perc value
    - manctrlx_perc: int [-100,100]
    - manctrlx_err: bool. True if error in manctrlx_perc value
    - autctrl_speedy_mms: int [-32767, +32767]
    - autctrl_speedy_err: bool. True if error in autctrl_speedy_mms value
    - autctrl_speedx_mms: int [??]
    - autctrl_speedx_err: bool. True if error in autctrl_speedx_mms value
    """
    def __init__(   self, workmode:int, manctrly_perc:int, manctrlx_perc:int,
                    autctrl_speedy_mms:int, autctrl_speedx_mms:int
                ):
        """
        :param: all: see class info to know about valid types and ranges
        :exception ValueError may arise if types / ranges are not considered
        """
        self.workmode = int(workmode)
        self.manctrly_perc = int(manctrly_perc)
        self.manctrlx_perc = int(manctrlx_perc)
        self.autctrl_speedy_mms = int(autctrl_speedy_mms)
        self.autctrl_speedx_mms = int(autctrl_speedx_mms)
    
    def get_output_format(self):
        """ Returns a str object containing the parameters in the proper
        order to be sent """
        out_formatted = ""
        out_formatted += str(self.workmode).zfill(NB_CHAR_PER_MESS)
        out_formatted += str(self.manctrly_perc).zfill(NB_CHAR_PER_MESS)
        out_formatted += str(self.manctrlx_perc).zfill(NB_CHAR_PER_MESS)
        out_formatted += str(self.autctrl_speedy_mms).zfill(NB_CHAR_PER_MESS)
        out_formatted += str(self.autctrl_speedx_mms).zfill(NB_CHAR_PER_MESS)
        return out_formatted

#==============================================================================
# Function definitions
#==============================================================================

def _str_is_number(str:str) -> bool:
    """ Returns True if str represents number or False otherwise """
    try:
        number = int(str)
        return True
    except ValueError:
        return False

def decode_in_message(message_in:str) -> Message_struct_in:
    """
    Takes incoming message and returns a Message_struct_in object initialised 
    with the parameters stored in the message
    :param message_in: Contains the message to decode, sized as 
    NB_CHAR_PER_MESS * len(incoming_pos_dic)
    :type message_in: (str)
    :exception IndexError may arise if message_in is not sized as expected
    :exception ValueError may arise if types / ranges in incoming message are
    different to what was expected
    """
    # Discard the old messages that could be stored as a same message
    message_size = NB_CHAR_PER_MESS*len(incoming_pos_dic)
    if (len(message_in) >= message_size):
        message_in = message_in[0:message_size]
        # Decode parameters
        list_params = []
        for param_index in range(1,len(incoming_pos_dic)+1):
            pos_message = (param_index-1)*NB_CHAR_PER_MESS
            current_param = message_in[pos_message:pos_message+5]
            list_params.append(current_param)
        my_message = Message_struct_in(
            workmode = list_params[incoming_pos_dic["MESSAGE_OUT_POS_WORKMODE"]],
            manctrly_perc = list_params[incoming_pos_dic["MESSAGE_OUT_POS_MANCTRLY_PERC"]],
            manctrlx_perc = list_params[incoming_pos_dic["MESSAGE_OUT_POS_MANCTRLX_PERC"]],
            autctrl_speedx_mms = list_params[incoming_pos_dic["MESSAGE_OUT_POS_AUTCTRL_SPEEDY_MMS"]],
            autctrl_speedy_mms = list_params[incoming_pos_dic["MESSAGE_OUT_POS_AUTCTRL_SPEEDX_MMS"]],
            linspeed_mms = list_params[incoming_pos_dic["MESSAGE_OUT_POS_LINSPEED_MMS"]],
            lspeed_rpm = list_params[incoming_pos_dic["MESSAGE_OUT_POS_LSPEED_RPM"]],
            rspeed_rpm = list_params[incoming_pos_dic["MESSAGE_OUT_POS_RSPEED_RPM"]],
            ldist_mm = list_params[incoming_pos_dic["MESSAGE_OUT_POS_LDIST_MM"]],
            rdist_mm = list_params[incoming_pos_dic["MESSAGE_OUT_POS_RDIST_MM"]],
        )
    else:
        my_message = None
    return my_message
