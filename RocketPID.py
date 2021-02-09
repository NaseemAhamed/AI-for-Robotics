######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################
import random

from RocketPID_tester import *
# Optimize your PID parameters here:
pressure_tau_p = 0.6
pressure_tau_d = 1

rocket_tau_p = 9
rocket_tau_i = 0.3
rocket_tau_d = 0.8

rocket_tau_p_ff = 15
rocket_tau_i_ff = 0
rocket_tau_d_ff = 2

bipropellant_rocket_fuel_tau_p = 6
bipropellant_rocket_fuel_tau_i = 0.05
bipropellant_rocket_fuel_tau_d = 0.1

bipropellant_rocket_oxidizer_tau_p = 25
bipropellant_rocket_oxidizer_tau_i = 0.1
bipropellant_rocket_oxidizer_tau_d = 0.2

bipropellant_rocket_fuel_tau_p_ff = 11
bipropellant_rocket_fuel_tau_i_ff = 0
bipropellant_rocket_fuel_tau_d_ff = 0

bipropellant_rocket_oxidizer_tau_p_ff = 22
bipropellant_rocket_oxidizer_tau_i_ff = 0
bipropellant_rocket_oxidizer_tau_d_ff = 0

def pressure_pd_solution(delta_t, current_pressure, target_pressure, data):
    """Student solution to maintain LOX pressure to the turbopump at a level of 100.

    Args:
        delta_t (float): Time step length.
        current_pressure (float): Current pressure level of the turbopump.
        target_pressure (float): Target pressure level of the turbopump.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0
    """

    # TODO: remove naive solution
    # adjust_pressure = current_pressure

    # TODO: implement PD solution here

    cte = current_pressure - target_pressure
    diff_cte = cte
    if data.get('cte') is None:
        diff_cte -= cte
    else:
        diff_cte -= data['cte']
    adjust_pressure = - pressure_tau_p * cte - pressure_tau_d * diff_cte
    data.update({'cte': cte})
    return adjust_pressure, data


def rocket_pid_solution(delta_t, current_velocity, optimal_velocity, data):
    """Student solution for maintaining rocket throttle through out the launch based on an optimal flight path

    Args:
        delta_t (float): Time step length.
        current_velocity (float): Current velocity of rocket.
        optimal_velocity (float): Optimal velocity of rocket.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorI': Integral error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0

    Returns:
        Throttle to set, data dictionary to be passed through run.
    """

    # TODO: remove naive solution
    # throttle = optimal_velocity - current_velocity

    # TODO: implement PID Solution here

    cte = current_velocity - optimal_velocity
    diff_cte = -cte
    int_cte = 0.0
    if data.get('counter') is None:
        counter = 0.0
    else:
        counter = data['counter']
    if data.get('cte') is None:
        diff_cte += cte
        int_cte += cte
    else:
        diff_cte += data['cte']
        int_cte = cte + data['int_cte']
    if counter < 150:
        throttle = - rocket_tau_p * cte - rocket_tau_d * diff_cte - rocket_tau_i * int_cte
    else:
        throttle = - rocket_tau_p_ff * cte - rocket_tau_d_ff * diff_cte - rocket_tau_i_ff * int_cte
    counter += delta_t
    data.update({'cte': cte})
    data.update({'int_cte': int_cte})
    data.update({'counter': counter})

    return throttle, data
    

def bipropellant_rocket_pid_solution(delta_t, current_velocity, optimal_velocity, data):
    """Student solution for maintaining fuel and oxidizer throttles through out the launch based on an optimal flight path

    Args:
        delta_t (float): Time step length.
        current_velocity (float): Current velocity of rocket.
        optimal_velocity (float): Optimal velocity of rocket.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorI': Integral error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0

    Returns:
        Fuel Throttle, Oxidizer Throttle to set, data dictionary to be passed through run.
    """

    # TODO: remove naive solution
    # fuel_throttle = optimal_velocity - current_velocity
    # oxidizer_throttle = optimal_velocity - current_velocity

    # TODO: implement PID Solution here

    cte = current_velocity - optimal_velocity
    diff_cte = -cte
    int_cte = 0.0
    if data.get('counter') is None:
        counter = 0.0
    else:
        counter = data['counter']
    if data.get('cte') is None:
        diff_cte += cte
        int_cte += cte
    else:
        diff_cte += data['cte']
        int_cte = cte + data['int_cte']
    if counter < 150:
        fuel_throttle = - bipropellant_rocket_fuel_tau_p * cte - bipropellant_rocket_fuel_tau_d * diff_cte - bipropellant_rocket_fuel_tau_i * int_cte
        oxidizer_throttle = - bipropellant_rocket_oxidizer_tau_p * cte - bipropellant_rocket_oxidizer_tau_d * diff_cte - bipropellant_rocket_oxidizer_tau_i * int_cte
    else:
        fuel_throttle = - bipropellant_rocket_fuel_tau_p_ff * cte - bipropellant_rocket_fuel_tau_d_ff * diff_cte - bipropellant_rocket_fuel_tau_i_ff * int_cte
        oxidizer_throttle = - bipropellant_rocket_oxidizer_tau_p_ff * cte - bipropellant_rocket_oxidizer_tau_d_ff * diff_cte - bipropellant_rocket_oxidizer_tau_i_ff * int_cte

    counter += delta_t
    data.update({'cte': cte})
    data.update({'int_cte': int_cte})
    data.update({'counter': counter})

    return fuel_throttle, oxidizer_throttle, data


