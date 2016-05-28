#!/usr/bin/env python3

from enum import Enum, IntEnum
import serial
import time

class Bad_Command_Parameter_or_Timing(Exception):
    '''Raised if the command, parameter, or timing is wrong.
    
    This exception raises when the controller responds 'NG'.
    '''
    pass
class Not_Supported(Exception):
    ''' Raised if the command is not supported by the controller.
    '''
    pass

class Undefined_Controller(Exception):
    pass

class Undefined_Stage(Exception):
    pass

class Controllers(Enum):
    SHOT_302GS = 1
    SHOT_304GS = 2
    SHOT_702 = 3
    Undefined = 99
    
    
class Controller_Modes(Enum):
    ''' Instruction set of controller's operation.
    '''
    SHOT = 0
    SHOT_enhanced = 1
    HIT = 2
    
class Comm_ack(Enum):
    MAIN = 0
    SUB = 1
    
class Excitation(IntEnum):
    Free = 0
    Hold = 1

class Stages(IntEnum):
    #
    # Linear translation stages
    #
    Linear_stage = 0
    
    # SGSP series
    SGSP15_10 = 151
    SGSP20_20 = 202
    SGSP20_35 = 203
    SGSP20_85 = 208
    SGSP26_50 = 265
    SGSP26_100 = 2610
    SGSP26_150 = 2615
    SGSP26_200 = 2620
    SGSP33_50 = 335
    SGSP33_100 = 3310
    SGSP33_200 = 3320
    SGSP46_300 = 4630
    SGSP46_400 = 4640
    SGSP46_500 = 4650
    SGSP46_800 = 4680
    SGSP65_1200 = 6512
    SGSP65_1500 = 6515
    
    # OSMS series are compatible to SGSP series.
    OSMS15_10 = 151
    OSMS20_20 = 202
    OSMS20_35 = 203
    OSMS20_85 = 208
    OSMS26_50 = 265
    OSMS26_100 = 2610
    OSMS26_150 = 2615
    OSMS26_200 = 2620
    OSMS33_50 = 335
    OSMS33_100 = 3310
    OSMS33_200 = 3320
    OSMS46_300 = 4630
    OSMS46_400 = 4640
    OSMS46_500 = 4650
    OSMS46_800 = 4680
    OSMS65_1200 = 6512
    OSMS65_1500 = 6515
    
    # HST series
    HST_50 = 5
    HST_100 = 10
    HST_200 = 20
    
    # HPS series
    HPS60_20 = 602
    HPS80_50 = 805
    HPS120_60 = 1206
    
    # TAMM series
    TAMM40_10 = 401
    TAMM60_15 = 601
    TAMM100_50 = 1005
    TAMM100_100 = 1001
    
    Linear_stage_end = 9999
    #
    # Rotation stages
    #
    Rotation_stage = 10000
    
    # SGSP series
    SGSP_40YAW = 10040
    SGSP_60YAW = 10060
    SGSP_80YAW = 10080
    SGSP_120YAW = 10120
    SGSP_160YAW = 10160
    
    # HST series
    HST_120YAW = 11120
    HST_160YAW = 11160
    
    # TODO: HDS series
    
    Rotation_stage_end = 19999
    #
    # Gonio stage
    #
    Gonio_stage = 20000
    
    # SGSP series
    SGSP_60A75 = 26075
    SGSP_60A100 = 26010
    SGSP_60A130 = 26030
    
    Gonio_stage_end = 29999
    
def __get_baserate(stype):
    ''' Resolution (full) of each stage. 
    '''
    # translation stages. 1 means 1 micro-meter.
    if stype is Stages.SGSP15_10:
        return 2
    if stype is Stages.SGSP20_20:
        return 2
    if stype is Stages.SGSP20_35:
        return 2
    if stype is Stages.SGSP20_85:
        return 2
    if stype is Stages.SGSP26_50:
        return 4
    if stype is Stages.SGSP26_100:
        return 4
    if stype is Stages.SGSP26_150:
        return 4
    if stype is Stages.SGSP26_200:
        return 4
    if stype is Stages.SGSP33_50:
        return 12
    if stype is Stages.SGSP33_100:
        return 12
    if stype is Stages.SGSP33_200:
        return 12
    if stype is Stages.SGSP46_300:
        return 20
    if stype is Stages.SGSP46_400:
        return 20
    if stype is Stages.SGSP46_500:
        return 20
    if stype is Stages.SGSP46_800:
        return 20
    if stype is Stages.SGSP65_1200:
        return 50
    if stype is Stages.SGSP65_1500:
        return 50
        
    if stype is Stages.HST_50:
        return 4
    if stype is Stages.HST_100:
        return 4
    if stype is Stages.HST_200:
        return 4
        
    if stype is Stages.HPS60_20:
        return 2 # TODO: and other HPS series

    if stype is Stages.TAMM40_10:
        return 2 # TODO: and other TAMM series        
        
    # Rotation stages. 1 means 0.001 degree.
    if stype is Stages.SGSP_40YAW:
        return 5 
    if stype is Stages.SGSP_60YAW:
        return 5
    if stype is Stages.SGSP_80YAW:
        return 5
    if stype is Stages.SGSP_120YAW:
        return 5
    if stype is Stages.SGSP_160YAW:
        return 5
        
    if stype is Stages.HST_120YAW:
        return 5 # TODO: and oterh HSP series
        
    # Gonio stages. 1 means 0.001 degree.
    if stype is Stages.SGSP_60A75:
        return 2
    if stype is Stages.SGSP_60A100:
        return 1
    if stype is Stages.SGSP_60A130:
        return 1
        
    raise Undefined_Stage(stype.name + ' is not defined as a valid stage, or just not implemented.')
    
    
def is_linear_stage(stype):
    return int(stype) > int(Stages.Linear_stage) and int(stype) < int(Stages.Linear_stage_end)
    
def is_rotation_stage(stype):
    return int(stype) > int(Stages.Rotation_stage) and int(stype) < int(Stages.Rotation_stage_end)
    
def is_gonio_stage(stype):
    return int(stype) > int(Stages.Gonio_stage) and int(stype) < int(Stages.Gonio_stage_end)
    
def get_value_per_pulse(stype):
    return __get_baserate(stype)

def get_micro_meter_per_pulse(stype):
    if not is_linear_stage(stype):
        raise Undefined_Stage(stype.name + ' is not a linear stage.')
    return __get_baserate(stype)
    
def get_milli_degree_per_pulse(stype):
    if not (is_rotation_stage(stype) or is_gonio_stage(stype)):
        raise Undefined_Stage(stype.name + ' is not a rotation stage.')
    return __get_baserate(stype)
    

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
        

   
class Session:
    '''Session of controlling OptoSigma's stage.
    
    Attributes
    ----------
    controller : Controller
        Parameters of the controller.
    stages : array of Stages
        Parameters of connected stages.
    
    Methods
    -------
    append_stage(stage)
        Add stage parameter.
    connect(portname = '/dev/ttyUSB0')
        Port name to connect to the controller.
    reset()
        Reset or initialize the position of stages.
    initialize()
        Initialize the position of stages to the mechanical origin.
    move()
        Change the position of the stages.
    jog()
        Continue moving stages
    is_busy()
        Check if the controller is under operation
    
    Parameters
    ----------
    ctype : Controllers
        Controller type.
    verbose_level : int, optional
        More messages are output as higher value is set.
    wait_time : int, optional
        Polling time while waiting busy status.
    '''
    def __init__(self, ctype, verbose_level=0, wait_time=2.):
        self.controller = Controller(ctype)
        self.__d = -1 * len(self.controller.delimiter)
        self.stages = []
        self.divisions = []
        self.verbose_level = verbose_level
        self.wait_time = wait_time
        self.connected = False
        self.divisions_loaded = False
                       
    def append_stage(self, stype):
        ''' Set new stage parameter.
        
        Setting stage parameters is not mandatory when all operation is done by in_pulse mode.
        
        Parameters
        ----------
        stype : Stages
            The stage type of a new axis stage.
        '''
        if not isinstance(stype, Stages):
            raise ValueError('Must be one of Stages Enum.')
        self.stages.append(stype)
              
    def connect(self, portname = '/dev/ttyUSB0'):
        ''' Connect to the controller via RS232C.
        
        Parameters
        ----------
        portname : str, optional
            Port name of the machine where the controller is connected.
        '''
        self.port = serial.Serial(port    = portname,
                             baudrate     = self.controller.baudrate,
                             bytesize     = self.controller.databit,
                             parity       = self.controller.parity,
                             stopbits     = self.controller.stopbit,
                             timeout      = self.controller.read_timeout,
                             writeTimeout = self.controller.write_timeout,
                             rtscts       = self.controller.rtscts)
        self.connected = True
        
        
    def __print(self, msg, level=1):
        if level <= self.verbose_level:
            print(msg)
        
    def __send(self, command, no_response=True):
       if not self.connected:
           raise Bad_Command_Parameter_or_Timing('Not connected to the controller yet.')
       self.port.write(command.encode('ascii') + self.controller.delimiter)
       if self.controller.comm_ack is Comm_ack.MAIN or not no_response:
          response = (self.port.readline()[:self.__d]).decode('utf-8')
          self.__print(command + ' >> ' + response, level=2)
          if response == 'NG':
              raise Bad_Command_Parameter_or_Timing(command + ' failed.')
          return response
       self.__print('[SUB] ' + command, level=2)
       
    def is_busy(self):
        ''' Whether the controller is under operation or not.
        
        If the controller is busy, only stop and status retrieve commands are accepted and other commands will fail.
        
        Returns
        -------
        busy : bool
            The controller is busy or not.
            
        See also
        --------
        is_ready()
        '''
        if not self.controller.is_support_Ex():
            if not self.controller.is_support_Q():
                raise Not_Supported()
            return self.get_status()[3].startswith('B')
        return self.__send('!:', no_response=False).startswith('B')
        
    def is_ready(self):
        ''' Whether the controller is ready for operation or not.
        
        If the controller is ready, all commands are acceptable, otherwise limited.
        
        Returns
        -------
        busy : bool
            The controller is ready or not.
            
        See also
        --------
        is_busy()
        '''
        if not self.controller.is_support_Ex():
            if not self.controller.is_support_Q():
                raise Not_Supported()
            return self.get_status()[3].startswith('R')
        return self.__send('!:', no_response=False).startswith('R')
       
    def __wait_for_ready(self):
       self.__print('Waiting.')
       while self.is_busy():
          self.__print('     sleep ' + str(self.wait_time), level=2)
          time.sleep(self.wait_time)
       
    def __load_divisions(self):
        self.__print('Load division settings.')
        if not self.controller.is_support_Qu():
            raise Not_Supported()
        if not self.controller.is_support_QuS():
            raise Not_Supported()
        response = self.__send('?:SW', no_response=False)
        self.divisions = [int(v) for v in response.split(',')]
        self.divisions_loaded = True
        
    def __direction(self, pulse):
        return '-' if pulse < 0 else '+'
        
    def reset(self, stage=1, all_stages=False, mechanical=False, wait_for_finish=False):
        ''' Reset or initialize the position of stages.
        
        Parameters
        ----------
        stage : int, optional
            Target stage number. If all_stage is set to True, this value is ignored.
        all_stages : bool, optional
            If True, all stages are reset simultaneously. In case mechanical is False, all stage parameters must be set.
        mechanical : bool, optional
            If True, stages will reset to the mechanical origin, otherwise, to the electrical zero point.
        wait_for_finish : bool, optional
            If True, check status and wait for operation finish.
        '''
        if self.controller.is_SHOT():
            self.__reset_shot(stage, all_stages, mechanical, wait_for_finish)
        elif self.controller.is_HIT():
            raise NotImplemented()
            
    def __reset_shot(self, stage, all_stages, mechanical, wait_for_finish):
        if mechanical:
            if not self.controller.is_support_H():
                raise Not_Supported()
            if all_stages:
                self.__print('Mechanical reset, all stages.')
                self.__send('H:W')
            else:
                self.__print('Mechanical reset, #' + str(stage))
                self.__send('H:' + str(stage))
        else:
            if not (self.controller.is_support_A() and self.controller.is_support_G()):
                raise Not_Supported()
            if all_stages:
                self.__print('Electrical reset, ' + str(len(self.stages)) + ' stages')
                com = ['A:W']
                for i in self.stages:
                    com.append(['+P0'])
                self.__send(''.join(com))
                self.__send('G:')
            else:
                self.__print('Electrical reset, #' + str(stage))
                self.__send('A:'+str(stage)+'+P0')
                self.__send('G:')
                
        if wait_for_finish:
            self.__wait_for_ready()
        
            
    def initialize(self):
        ''' Initialize all stages at the mechanical origin.
        
        Equivalent to reset(all_stages=True, mechanical=True, wait_for_finish=True)
        
        See also
        --------
        reset()
        '''
        self.reset(all_stages=True, mechanical=True, wait_for_finish=True)
                
    def move(self, stage=1, amount=0, in_pulse=False, absolute=False, wait_for_finish=True):
        '''Move stages.
        
        Parameters
        ----------
        stage : int
            Target operation stage number. When amount is tuple or list, this value is ignored.
        amount : int or (tuple or list) of int
            Amount of the transition. When a iterable values are specified, corresponding stages are moved simultaneously.
        in_pulse : bool, optional
            If False, the unit of amount is micro-meters/milli-degrees, otherwise, the unit is pulses.
        absolute : bool, optional
            Represents specified values are absolute position or relative travel.
        wait_for_finish : bool, optional
            If True, check status and wait for operation finish.
        '''
        if not self.controller.is_support_G():
            raise Not_Supported()
        msg = ['Move']
        if absolute:
            if not self.controller.is_support_A():
                raise Not_Supported()
            com = ['A:']
            msg.append('absolutely,')
        else:
            if not self.controller.is_support_M():
                raise Not_Supported()
            com = ['M:']
            msg.append('relatively,')
        if isinstance(amount, (list, tuple)):
            com.append('W')
            msg.append(str(len(amount))+' stages,')
            msg.extend([str(m) for m in amount])
            if not in_pulse:
                msg.append('micro-meters/degrees.')
                if not self.divisions_loaded:
                    self.__load_divisions()
                amount = [v * d / get_value_per_pulse(p) for p, v, d in zip(self.stages, amount, self.divisions)]
            com.extend([self.__direction(v)+'P'+str(abs(v)) for v in [int(m) for m in amount]])
            self.__print(' '.join(msg))
            self.__send(''.join(com))
            self.__send('G:')
        else:
            com.append(str(stage))
            com.append(self.__direction(amount))
            com.append('P')
            msg.append('#'+str(stage)+', '+str(amount))
            if not in_pulse:
                msg.append('micro-meters/degrees.')
                if not self.divisions_loaded:
                    self.__load_divisions()
            self.__print('Amount: '+str(amount)+' Base rate: '+str(get_value_per_pulse(self.stages[stage-1])) + ' Devision:' + str(self.divisions[stage-1]), level=3)
            amount *= self.divisions[stage-1] / get_value_per_pulse(self.stages[stage-1]) if not in_pulse else 1
            com.append(str(abs(int(amount))))
            self.__print(' '.join(msg))
            self.__send(''.join(com))
            self.__send('G:')
            
        if wait_for_finish:
            self.__wait_for_ready()
            
            
    def jog(self, stage=1, directions=1):
        '''Jog drive. Continue moving before arriving the limit point or system limit.
        
        The drive speed is the slowest speed (S-speed).
        To stop the drive, use stop() method.
        
        Jog operation stops automatically when \pm 268,435,455 pulses are sent.
        When the position of a stage becomes \pm 999,999,999, operation is aborted and become a overflow alert mode.
        In this case, call stop() and set_origin() methods to get back to a normal mode.
        
        Parameters
        ----------
        stage : int
            The target stage number. If directions are given by tuple or list, this value is ignored.
        directions : int, tuple, or list
            Jog drive directions. Only a sign of a number is used.
        '''
        if not self.controller.is_support_J():
            raise Not_Supported()
        if not self.controller.is_support_G():
            raise Not_Supported()
        if isinstance(directions, (tuple, list)):
            arg = [self.__direction(d) for d in directions]
            com = 'J:W' + ''.join(arg)
            self.__print('Jog drive, multi-stages.')
            self.__send(com)
            self.__send('G:')
        else:
            com = 'J:'+str(stage)+self.__direction(directions)
            self.__print('Jog drive, single stage.')
            self.__send(com)
            self.__send('G:')
            
    def stop(self, stage=1, all_stages=False, emergency=False):
        ''' Stop stages.
        
        Parameters
        ----------
        stage : int
            Target stage number. If emergency or all_stages are used, this value is ignored.
        all_stages : bool, optional
            Stop all stages.
        emergency : bool, optional
            Force stop all stages immediately. All operations are aborted. 
            This may cause a big reaction when a stage is moving fast. 
            Also, this mode does not check the capability of the controller to this operation.
        '''
        if emergency:
            self.__send('L:E')
            self.__print('Emergency stop.')
            return
        if not self.controller.is_support_L():
            raise Not_Supported()
        if all_stages:
            self.__print('Stop All stages.')
            self.__send('L:W')
        else:
            self.__print('Stop stage #'+str(stage))
            self.__send('L:'+str(stage))
        self.__wait_for_ready()
        
    def abort(self):
        ''' Equivalent to stop(emergency = True)
        
        See also
        --------
        stop()
        '''
        self.stop(emergency=True)
            
    def set_origin(self, stage=1, all_stages=False):
        ''' Set the electrical zero point of a stage at current position.
        
        Paramters
        ---------
        stage : int
            Target stage number.
        all_stages : bool, optional
            If True, all stages' origin point are set.
        '''
        if not self.controller.is_support_R():
            raise Not_Supported()
        if all_stages:
            self.__print('Set origin for all stages.')
            self.__send('R:W')
        else:
            self.__print('Set origin for stage #'+str(stage))
            self.__send('R:'+str(stage))

    def __check_SFR(self, s, f, r):
        s_lim, f_lim, r_lim = self.controller.get_support_speed_ranges()    
        f = max(f_lim[0], min(f_lim[1], f))
        s = max(s_lim[0], min(s_lim[1], s, f))
        r = max(r_lim[0], min(r_lim[1], r))
        if f >= 8000 and s < 64:
            s = 64
        return s, f, r
            
    def set_speed(self, stage=1, S=1000, F=10000, R=100):
        ''' Set drive speed.
        
        Parameters
        ----------
        stage : int
            Target stage number. If S, F, R are specified by tuple or list, this value is ignored.
        S, F, R : int, tuple, or list
            Speed parameters of each stage.
            S: the slowest speed, F: the fastest speed, R: acceleration and deceleration time.
        '''
        if not self.controller.is_support_D():
            raise Not_Supported()
        if isinstance(S, (tuple, list)):
            self.__print('Set speed of multi-stages.')
            SFRs = [self.__check_SFR(s, f, r) for s, f, r in zip(S, F, R)]
            arg = ['S'+str(s)+'F'+str(f)+'R'+str(r) for s, f, r in SFRs]
            com = 'D:W' + ''.join(arg)
            self.__send(com)
        else:
            self.__print('Set speed of stage #'+str(stage))
            s, f, r = self.__check_SFR(S, F, R)
            com = 'D:'+str(stage)+'S'+str(s)+'F'+str(f)+'R'+str(r)
            self.__send(com)
            
    def set_speed_reset_drive(self, stage=1, S=1000, F=10000, R=100):
        ''' Set drive speed of going back to the origin.
        
        Parameters
        ----------
        stage : int
            Target stage number. If S, F, R are specified by tuple or list, this value is ignored.
        S, F, R : int, tuple, or list
            Speed parameters of each stage.
            S: the slowest speed, F: the fastest speed, R: acceleration and deceleration time.
        '''
        if not self.controller.is_support_V():
            raise Not_Supported()
        if isinstance(S, (tuple, list)):
            self.__print('Set speed of multi-stages.')
            SFRs = [self.__check_SFR(s, f, r) for s, f, r in zip(S, F, R)]
            arg = ['S'+str(s)+'F'+str(f)+'R'+str(r) for s, f, r in SFRs]
            com = 'V:W' + ''.join(arg)
            self.__send(com)
        else:
            self.__print('Set speed of stage #'+str(stage))
            s, f, r = self.__check_SFR(S, F, R)
            com = 'V:'+str(stage)+'S'+str(s)+'F'+str(f)+'R'+str(r)
            self.__send(com)
            
    def set_excitation_mode(self, stage=1, mode=Excitation.Hold, all_stages=False):
        '''Set excitation of the moters.
        
        When releasing excitation, stages can be moved manually.
        
        Parameters
        ----------
        mode : Excitation
            Excitation mode.
        '''
        if not self.controller.is_support_C():
            raise Not_Supported()
        if all_stages:
            self.__print('Set all stages to '+mode.name)
            self.__send('C:W'+str(int(mode)))
        else:
            self.__print('Set stage #'+str(stage)+' to '+mode.name)
            self.__send('C:'+str(stage)+str(int(mode)))
        
    def set_division(self, stage=1, division=2):
        ''' Set division of step angle of a stepping moter.
        
        Parameters
        ----------
        stage : int
            Target stage number.
        division : int
            Divisions of a stepping moter.
            When a stage is operated by closed-loop method, Higher value is recommended.
        '''
        if not self.controller.is_support_S():
            raise Not_Supported()
        if not division in self.controller.get_support_devisions():
            raise ValueError('Unsupported division value.')
        self.__print('Set division of #'+str(stage)+' to '+str(division))
        self.__send('S:' + str(stage) + str(division))
        self.__load_divisions()
    
    def get_status(self):
        ''' Get status of stages and the controller.
        
        Returns
        -------
        positions : list
            List of positions of stages.
        ack1 : str
            'X' or 'K', which represent that the command is denined or accepted, respectively.
        ack2 : str
            'K' represents all stages are stable, and other strings represent one or more stages are stopped at limit sensor.
        ack3 : str
            'B' or 'R', which represent the controller is busy or ready, respectively.
        '''
        if not self.controller.is_support_Q():
            raise Not_Supported()
        response = self.__send('Q:', no_response=False)
        data = response.split(',')
        ack1, ack2, ack3 = data[-3:]
        positions = [int(d) for d in data[:len(data) - 3]]
        return positions, ack1, ack2, ack3
        
    def get_position(self, in_pulse=False):
        ''' Get positions of stages.
        
        Parameters
        ----------
        in_pulse : bool, optional
            If True, returns a position as is (pulses), otherwise, returns in micro-meters or milli-degrees.
            
        Returns
        -------
        positions : list
            List of positions of stages.
        '''
        positions =  self.get_status()[0]
        if in_pulse:
            return positions
        else:
            if not self.divisions_loaded:
                self.__load_divisions()
            return [p * get_value_per_pulse(s) / d in p, s, d in zip(positions, self.stages, self.divisions)]
        
def __test_304GS_SGSP46():
    ''' Test code #1 '''
    stages = Session(Controllers.SHOT_304GS, verbose_level=3)
    stages.append_stage(Stages.SGSP46_800)
    stages.connect()
    stages.initialize()
    stages.set_speed(1, 1000, 10000, 500)
    stages.move(amount=100000, wait_for_finish=True)
    stages.move(amount=200000, wait_for_finish=True, absolute=True)
    stages.set_origin()
    stages.jog()
    time.sleep(10)
    stages.stop()
    stages.get_position()
    stages.reset(wait_for_finish=True)
    stages.move(amount=-200000, wait_for_finish=True, absolute=True)
    
def __test_702_SGSP120Y():
    ''' Test code #2 '''
    stages = Session(Controllers.SHOT_702, verbose_level=3)
    stages.append_stage(Stages.SGSP_120YAW)
    stages.connect()
    stages.initialize()
    stages.set_speed(1, 1000, 10000, 500)
    stages.move(amount=45000, wait_for_finish=True)
    stages.move(amount=90000, wait_for_finish=True, absolute=True)
    stages.set_origin()
    stages.jog()
    time.sleep(10)
    stages.stop()
    stages.get_position()
    stages.reset(wait_for_finish=True)
    stages.move(amount=-90000, wait_for_finish=True, absolute=True)
    
if __name__ == '__main__':
    __test_304GS_SGSP46()
#    __test_702_SGSP120Y()