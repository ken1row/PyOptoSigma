#!/usr/bin/env python3


from enum import Enum #, IntEnum

class Controllers(Enum):
    SHOT_302GS = 1
    SHOT_304GS = 2
    SHOT_702 = 3
    Undefined = 99
    
    
class Controller_Modes(Enum):
    SHOT = 0
    SHOT_enhanced = 1
    HIT = 2
    
class Comm_ack(Enum):
    MAIN = 0
    SUB = 1
    
class Undefined_Controller(Exception):
    pass


class Controller:
    '''Class for a controller's parameters.
    
    Attributes
    ----------
    ctype : Controllers
        Type of a controller.
    baudrate : int
        Baudrate of RS232C communication.
    delimiter : str
        Delimiter of RS232C communication.
    comm_ack : Comm_ack
        COMM/ACK mode.
        
    Methods
    -------
    get_support_baudrates()
        Get the tuple of supported baudrates of this controller.
    get_support_axes()
        Get the number of controllable stages.
    get_support_speed_ranges()
        Get the range of speed values.
    is_support_[COM]() : bool
        Returns whether the controller supports [COM] operation.
        
    Parameters
    ----------
    ctype : Controllers
        Type of the controller.
        
    Raises
    ------
    Undefined_Controller
    '''
    def __init__(self, ctype):
        self.ctype = ctype
        self.parity = 'N'
        self.databit = 8
        self.stopbit = 1
        self.rtscts = True
        self.read_timeout = 1
        self.write_timeout = 1
        self.delimiter = b'\r\n'
        self.comm_ack = Comm_ack.MAIN
        # Load default values.
        if self.ctype is Controllers.SHOT_302GS or self.ctype is Controllers.SHOT_304GS:
            self.baudrate = 9600
            self.cmode = Controller_Modes.SHOT
        elif ctype is Controllers.SHOT_702:
            self.baudrate = 38400
            self.cmode = Controller_Modes.SHOT
        else:
            raise Undefined_Controller('Controller is undefined.')
    
    def __is_30X(self):
        return self.ctype is Controllers.SHOT_302GS or self.ctype is Controllers.SHOT_304GS
    def __is_70X(self):
        return self.ctype is Controllers.SHOT_702
    
    def is_SHOT(self):
        if self.cmode is Controller_Modes.SHOT:
            return True
        if self.cmode is Controller_Modes.SHOT_enhanced:
            return True
        return False
        
    def is_HIT(self):
        return self.cmode is Controller_Modes.HIT
    
    def get_support_baudrates(self):
        if self.__is_30X():
            return (4800, 9600, 19200, 38400)
        if self.__is_70X():
            return (38400, )
        return ()
        
    def get_support_devisions(self):
        return (1,2,4,5,8,10,20,25,40,50,80,100,125,200,250)
    
    def get_support_axes(self):
        ''' Get the number of controllable stages.
        
        This method does not check the value of AXIS memory switch nor how many stages are connected.
        '''
        if self.ctype == Controllers.SHOT_304GS:
            return 4
        return 2
        
    def get_support_speed_ranges(self):
        '''Get the range of speed.
        
        Returns
        -------
        ((S_min, S_max), (F_min, F_max), (R_min, R_max))
        '''
        return ((1, 500000), (1, 500000), (0, 1000))        
        
    # Whether the controller supports specific command.
    # Moving operations
    def is_support_H(self):
        return True
    def is_support_M(self):
        return True
    def is_support_A(self):
        return True
    def is_support_E(self):
        if self.__is_30X():
            return True
        return False
    def is_support_K(self):
        if self.__is_30X():
            return True
        return False
    def is_support_J(self):
        return True
    def is_support_G(self):
        return True
    def is_support_R(self):
        return True
    def is_support_L(self):
        return True
    def is_support_D(self):
        return True
    def is_support_V(self):
        if self.__is_30X():
            return False
        return True
    def is_support_U(self):        
        if self.__is_30X():
            return True
        return False
    def is_support_W(self):
        if self.__is_30X():
            return True
        return False
    def is_support_T(self):
        if self.__is_30X():
            return True
        return False
    def is_support_C(self):
        return True
    def is_support_S(self):
        return True
    # Status operations
    def is_support_Q(self):
        return True
    def is_support_Ex(self):
        return True
    def is_support_Qu(self):
        return True
    def is_support_QuV(self):
        return True
    def is_support_QuP(self):
        return True
    def is_support_QuS(self):
        return True
    def is_support_QuD(self):
        return True
    def is_support_QuB(self):
        if self.__is_30X():
            return False
        return True
    def is_support_QuM(self):
        if self.__is_30X():
            return True
        return False
    def is_support_QuA(self):
        if self.__is_30X():
            return True
        return False
    def is_support_QuO(self):
        if self.__is_30X():
            return True
        return False
    def is_support_QuW(self):
        if self.__is_30X():
            return True
        return False
    def is_support_QuK(self):
        if self.__is_30X():
            return True
        return False
    def is_support_QuE(self):
        if self.__is_30X():
            return True
        return False
    # I/O and others
    def is_support_O(self):
        return True
    def is_support_I(self):
        return True
    def is_support_P(self):
        if self.__is_30X():
            return True
        return False
        