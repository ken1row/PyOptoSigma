#!/usr/bin/env python3

from enum import IntEnum

   
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
    
class Undefined_Stage(Exception):
    pass

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