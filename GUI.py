#==============================================================================
# Project: Robocar
# Application: Remote_Control
# File: GUI.py
# Description: graphical user interface, which allows sending commands to the
# car and shows information about the current state.
#==============================================================================

#==============================================================================
# Import
#==============================================================================

import PySimpleGUI as sg
from GUI_constants import *
import CommunMessages
import time
from multiprocessing import Queue
from typing import Tuple

#==============================================================================
# Global data
#==============================================================================

DEBUG = False
TIMEOUT_GUI_MS = 100
TIMEOUT_SERVER_MS = 2*TIMEOUT_GUI_MS    # Time above server lag is considered

#==============================================================================
# Function definitions
#==============================================================================

def _time_now_ms() -> int:
    return int(0.000001*time.time_ns())

def _gui_init_layout_windows() -> Tuple[list, sg.Window]:
    """
    Builds the layout row by row, builds the window and returns both

    :return: layout (list of widgets) and window
    :rtype: (list, Window)
    """

    layout = [
        # Connection
        [ sg.Text(CONNECTION_TEXT, size=SIZE3, pad=PAD_HDR1, justification='c', background_color=HDR_COL, font=FONT2) ],
        [ sg.Text(CONNECTION_ST_TEXT, pad=PAD4, size=SIZE5, justification='c', key=CONNECTION_ST_KEY) ],
        
        # Control
        [ sg.Text(CTRL_TEXT, size=SIZE3,pad=PAD_HDR2, justification='c', background_color=HDR_COL, font=FONT2) ],
        [ sg.Text(CTRL_WORKM_TEXT, size=SIZE1,pad=PAD2, justification='r'), 
          sg.Radio(CTRL_WORKM_STOP_IN_TEXT,CTRL_WORKM_IN_GROUP, font=FONT, key=CTRL_WORKM_STOP_IN_KEY, pad=PAD2, default=True),
          sg.Radio(CTRL_WORKM_MAN_IN_TEXT,CTRL_WORKM_IN_GROUP, font=FONT, key=CTRL_WORKM_MAN_IN_KEY, pad=PAD2),
          sg.Radio(CTRL_WORKM_AUT_IN_TEXT,CTRL_WORKM_IN_GROUP, font=FONT, key=CTRL_WORKM_AUT_IN_KEY, pad=PAD2)
        ],
        [ sg.Text(CTRL_MAN_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(CTRL_MAN_OX_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Input(size=SIZE2, pad=PAD5, justification='l', key=CTRL_MAN_OX_IN_KEY, font=FONT, disabled_readonly_background_color='grey'),
          sg.Text(CTRL_MAN_OY_TEXT, pad=PAD5, justification='l', font=FONT),    
          sg.Input(size=SIZE2, pad=PAD2, justification='l', key=CTRL_MAN_OY_IN_KEY, font=FONT, disabled_readonly_background_color='grey')
        ],
        [ sg.Text(CTRL_AUT_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(CTRL_AUT_OX_TEXT, pad=PAD5, justification='l',  font=FONT),                    
          sg.Input(size=SIZE2, pad=PAD5, justification='l', key=CTRL_AUT_OX_IN_KEY, font=FONT, disabled_readonly_background_color='grey'),
          sg.Text(CTRL_AUT_OY_TEXT, pad=PAD5, justification='l', font=FONT),   
          sg.Input(size=SIZE2, pad=PAD2, justification='l', key=CTRL_AUT_OY_IN_KEY, font=FONT, disabled_readonly_background_color='grey')
        ],
        [ sg.Button(button_text=CTRL_SEND_BUT_TEXT, size=SIZE4, pad=PAD3, key=CTRL_SEND_BUT_KEY, font=FONT) ],
        
        # Telemetry
        [ sg.Text(TLMT_TEXT, size=SIZE3,pad=PAD_HDR2, justification='c', background_color=HDR_COL, font=FONT2) ],
        [ sg.Text(TLMT_WORKM_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(TLMT_WORKM_OUT_TEXT, size=SIZE1, pad=PAD2, justification='l', key=TLMT_WORKM_OUT_KEY)
        ],
        [ sg.Text(TLMT_MAN_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(TLMT_MAN_OX_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD5, justification='l', key=TLMT_MAN_OX_OUT_KEY, font=FONT),
          sg.Text(TLMT_MAN_OY_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD2, justification='l', key=TLMT_MAN_OY_OUT_KEY, font=FONT)
        ],
        [ sg.Text(TLMT_AUT_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(TLMT_AUT_OX_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD5, justification='l', key=TLMT_AUT_OX_OUT_KEY, font=FONT),
          sg.Text(TLMT_AUT_OY_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD2, justification='l', key=TLMT_AUT_OY_OUT_KEY, font=FONT)
        ],
        [ sg.Text(TLMT_LINSP_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(TLMT_LINSP_OUT_TEXT, size=SIZE1, pad=PAD2, justification='l', key=TLMT_LINSP_OUT_KEY)
        ],
        [ sg.Text(TLMT_WHESP_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(TLMT_WHESP_L_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD5, justification='l', key=TLMT_WHESP_L_OUT_KEY, font=FONT),
          sg.Text(TLMT_WHESP_R_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD2, justification='l', key=TLMT_WHESP_R_OUT_KEY, font=FONT)
        ],
        [ sg.Text(TLMT_DIST_TEXT, size=SIZE1,pad=PAD2, justification='r'),
          sg.Text(TLMT_DIST_L_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD5, justification='l', key=TLMT_DIST_L_OUT_KEY, font=FONT),
          sg.Text(TLMT_DIST_R_TEXT, pad=PAD5, justification='l', font=FONT),
          sg.Text(size=SIZE2, pad=PAD2, justification='l', key=TLMT_DIST_R_OUT_KEY, font=FONT)
        ],
        [   
        ],
    ]
    # sg.theme("DarkBlue")
    sg.set_options(font=('Courier New', 12))
    window = sg.Window(WINDOW_TEXT, layout, margins=WINDOW_MARGIN)
    window.finalize = True
    return layout, window

def _control_update(window: sg.Window, manual_enabled:bool, auto_enabled:bool):
    """
    Enables or disables the control inputs according to the current working
    mode selected (stop / manual / auto)
    """

    if manual_enabled:
        window[CTRL_MAN_OX_IN_KEY].update(disabled=False)
        window[CTRL_MAN_OY_IN_KEY].update(disabled=False)
    else:
        window[CTRL_MAN_OX_IN_KEY].update(disabled=True, value='')
        window[CTRL_MAN_OY_IN_KEY].update(disabled=True, value='')
    if auto_enabled:
        window[CTRL_AUT_OX_IN_KEY].update(disabled=False)
        window[CTRL_AUT_OY_IN_KEY].update(disabled=False)
    else:
        window[CTRL_AUT_OX_IN_KEY].update(disabled=True, value='')
        window[CTRL_AUT_OY_IN_KEY].update(disabled=True, value='')

def _send_message(window:sg.Window, queue_2_car:Queue(1)):
    # Create message with current parameters to send
    workmode_str = ""
    manctrly_perc = 0
    manctrlx_perc = 0
    autctrl_speedy_mms = 0
    autctrl_speedx_mms = 0

    if window[CTRL_WORKM_STOP_IN_KEY].get():
        workmode_str = "Manual mode"
        manctrly_perc = 0
        manctrlx_perc = 0
    elif window[CTRL_WORKM_MAN_IN_KEY].get():
        workmode_str = "Manual mode"
        manctrly_perc = int(window[CTRL_MAN_OY_IN_KEY].get())
        manctrlx_perc = int(window[CTRL_MAN_OX_IN_KEY].get())
    elif window[CTRL_WORKM_AUT_IN_KEY].get():
        workmode_str = "Automatic mode"
        autctrl_speedy_mms = int(window[CTRL_AUT_OY_IN_KEY].get())
        autctrl_speedx_mms = int(window[CTRL_AUT_OX_IN_KEY].get())
    workmode_id = CommunMessages.get_workmode_id(workmode_str)
    out_raw = CommunMessages.Message_struct_out(workmode_id,
        manctrly_perc, manctrlx_perc,
        autctrl_speedy_mms, autctrl_speedx_mms)
    # Get message formatted
    out_formatted = out_raw.get_output_format()
    # Empty queue if full and push new message
    if (queue_2_car.full() == True):
        queue_2_car.empty()  # Only most recent data is valid
    queue_2_car.put(out_formatted)
    if (DEBUG): print("GUI: message sent")

def _str_is_number(str:str) -> bool:
    """ Returns True if str represents number or False otherwise """
    try:
        number = int(str)
        return True
    except ValueError:
        return False

def _check_input(window:sg.Window) -> bool:
    """ Checks if the control inputs typed by the user are valid """
    status_is_ok = False
    if (window[CTRL_WORKM_STOP_IN_KEY].get()):
        status_is_ok = True
    elif (window[CTRL_WORKM_MAN_IN_KEY].get()):
        ox_str = window[CTRL_MAN_OX_IN_KEY].get()
        oy_str = window[CTRL_MAN_OY_IN_KEY].get()
        if (_str_is_number(ox_str) and _str_is_number(oy_str)):
            ox_nb = int(ox_str)
            oy_nb = int(oy_str)
            if (ox_nb >= -100 and ox_nb <= 100 and 
                    oy_nb >= -100 and oy_nb <= 100):
                status_is_ok = True
    elif (window[CTRL_WORKM_AUT_IN_KEY].get()):
        ox_str = window[CTRL_AUT_OX_IN_KEY].get()
        oy_str = window[CTRL_AUT_OY_IN_KEY].get()
        if (_str_is_number(ox_str) and _str_is_number(oy_str)):
            ox_nb = int(ox_str)
            oy_nb = int(oy_str)
            if (ox_nb >= -32767 and ox_nb <= 32767 and 
                    oy_nb >= -32767 and oy_nb <= 32767):
                status_is_ok = True        
    return status_is_ok

#----------------------------------------------------------------------
# Main flow
#----------------------------------------------------------------------

def gui_main( queue_2_car:Queue(1), queue_from_car:Queue(1), 
              queue_exit:Queue(1) ):
    """ Handles all the GUI behaviour, updates data from the car and sends
    to the car control data introduced by the user """
    layout, window = _gui_init_layout_windows()
    time_ms_from_last_update = 0
    time_ms_last_update = _time_now_ms()
    while True:
        # Update user events
        event, values = window.read(timeout=TIMEOUT_SERVER_MS)
        # If user closes the window, send message to all processes
        if event == sg.WINDOW_CLOSED:
            if (queue_exit.full() == False):  
                queue_exit.put("UNUSED_DATA")
        # If message in exit queue, close process
        if queue_exit.full() == True:
            if DEBUG: print("Exiting from GUI...")
            break
        
        # Process info to send to car (Control section)
        # Check radio button choice
        if values[CTRL_WORKM_STOP_IN_KEY]:
            _control_update(window, False, False)
        elif values[CTRL_WORKM_MAN_IN_KEY]:
            _control_update(window, True, False)
        elif values[CTRL_WORKM_AUT_IN_KEY]:
            _control_update(window, False, True)
        # Update button status and check input
        input_is_valid = _check_input(window)
        server_is_ok = True if time_ms_from_last_update < TIMEOUT_SERVER_MS else False
        if input_is_valid and server_is_ok:
            window[CTRL_SEND_BUT_KEY].update(disabled=False)
        else:
            window[CTRL_SEND_BUT_KEY].update(disabled=True)
        # Send if button pressed
        if event == CTRL_SEND_BUT_KEY:
            _send_message(window, queue_2_car)
        
        # Update info coming from car (Telemetry section) and Last connection
        if (queue_from_car.empty() == False):
            message = CommunMessages.decode_in_message(queue_from_car.get())
            if message != None:
                window[TLMT_WORKM_OUT_KEY].Update(message.get_workmode_str() if message.workmode_err==False else "Error")
                window[TLMT_MAN_OY_OUT_KEY].Update(message.manctrly_perc if message.manctrly_err==False else "Error")
                window[TLMT_MAN_OX_OUT_KEY].Update(message.manctrlx_perc if message.manctrlx_err==False else "Error")
                window[TLMT_AUT_OY_OUT_KEY].Update(message.autctrl_speedy_mms if message.autctrl_speedy_err==False else "Error")
                window[TLMT_AUT_OX_OUT_KEY].Update(message.autctrl_speedx_mms if message.autctrl_speedx_err==False else "Error")
                window[TLMT_LINSP_OUT_KEY].Update(message.linspeed_mms if message.linspeed_err==False else "Error")
                window[TLMT_WHESP_L_OUT_KEY].Update(message.lspeed_rpm if message.lspeed_err==False else "Error")
                window[TLMT_WHESP_R_OUT_KEY].Update(message.rspeed_rpm if message.rspeed_err==False else "Error")
                window[TLMT_DIST_L_OUT_KEY].Update(message.ldist_mm if message.ldist_err==False else "Error")
                window[TLMT_DIST_R_OUT_KEY].Update(message.rdist_mm if message.rdist_err==False else "Error")
            window[CONNECTION_ST_KEY].Update(
                value = "Connected < " + str(TIMEOUT_GUI_MS) + "ms",
                text_color = "white")
            time_ms_from_last_update = 0
            time_ms_last_update = _time_now_ms()
        else:
            time_ms_from_last_update = _time_now_ms() - time_ms_last_update
            my_str = "Disconnected. " + str(time_ms_from_last_update) + " ms ago"
            window[CONNECTION_ST_KEY].Update(
                value = my_str,
                text_color = "red")

    # If infinite loop is broken, close window and finalise
    window.close()