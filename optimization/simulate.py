import numpy as np
import pandas as pd

# ==============================================================================
#    THIS CLASS WILL BE IMPLEMENTED BY COMPETITORS
# ==============================================================================
class BatteryContoller(object):
    """ The BatteryContoller class handles providing a new "target state of charge"
        at each time step.

        This class is instantiated by the simulation script, and it can
        be used to store any state that is needed for the call to
        propose_state_of_charge that happens in the simulation.

        The propose_state_of_charge method returns the state of
        charge between 0.0 and 1.0 to be attained at the end of the coming
        quarter, i.e., at time t+15 minutes.
        The arguments to propose_state_of_charge are as follows:
        - The current state of charge of the battery at time t, between 0.0
          and 1.0.
        - The capacity of the battery in Wh
        - The actual load of the previous quarter.
        - The actual PV production of the previous quarter.
        - The price at which electricity can be bought from the grid for the
          next 96 quarters (i.e., an array of 96 values).
        - The price at which electricity can be sold to the grid for the
          next 96 quarters (i.e., an array of 96 values). This is often 0.
        - The forecast of the load established at time t for the next 96
          quarters (i.e., an array of 96 values).
        - The forecast of the PV production established at time t for the next
          96 quarters (i.e., an array of 96 values).
    """
    def propose_state_of_charge(self,
                                current_state_of_charge,
                                battery_capacity,
                                actual_previous_load,
                                actual_previous_pv_production,
                                price_buy,
                                price_sell,
                                load_forecast,
                                pv_forecast):

        # return the proposed state of charge ...
        return 0.0


class Simulation(object):
    """ Handles running a simulation.

        Each simulation concerns a given period (typically 10 days).

        The arguments to the constructor are as follows:
        - data contains all the time series needed over the considered period
        - initial_battery_state_of_charge is the initial state of charge of the
          battery (0.0 in our examples)
        - battery_capacity is the battery capacity in Wh
        - battery_charging_power_limit in W
        - battery_discharging_power_limit in W (counted negatively)
        - battery_charging_efficiency
        - battery_discharging_efficiency
        - actual_previous_load of the timestep right before the simulation starts
        - actual_previous_pv of the timestep right before the simulation starts
    """
    def __init__(self,
                 data,
                 initial_battery_state_of_charge=0.0,
                 battery_capacity=10000.0,
                 battery_charging_power_limit=1.0,
                 battery_discharging_power_limit=-1.0,
                 battery_charging_efficiency=0.8,
                 battery_discharging_efficiency=0.8,
                 actual_previous_load=0.0,
                 actual_previous_pv=0.0):
        """ Creates initial simulation state based on data passed in.
        """
        self.data = data

        # initialize money at 0.0
        self.money_spent = 0.0
        self.money_spent_without_battery = 0.0

        # battery initialization
        self.battery_state_of_charge = initial_battery_state_of_charge
        self.battery_capacity = battery_capacity
        self.battery_charging_power_limit = battery_charging_power_limit
        self.battery_discharging_power_limit = battery_discharging_power_limit
        self.battery_charging_efficiency = battery_charging_efficiency
        self.battery_discharging_efficiency = battery_discharging_efficiency

        # building initialization
        self.actual_previous_load = actual_previous_load
        self.actual_previous_pv = actual_previous_pv

    def run(self):
        """ Executes the simulation by iterating through each of the data points
            It returns both the electricity cost spent using the battery and the
            cost that would have been incurred with no battery.
        """
        battery_controller = BatteryContoller()

        for i, timestep in self.data.iterrows():
            self.simulate_timestep(battery_controller, timestep)

        return self.money_spent, self.money_spent_without_battery

    def simulate_timestep(self, battery_controller, timestep):
        """ Executes a single timestep using `battery_controller` to get
            a proposed state of charge.
        """

        # construct the arrays from the data and get previous load and pv production
        load_columns = timestep.index.str.startswith('load_')
        pv_columns = timestep.index.str.startswith('pv_')
        price_sell_columns = timestep.index.str.startswith('price_sell_')
        price_buy_columns = timestep.index.str.startswith('price_buy_')

        # get proposed state of charge from the battery controller
        proposed_state_of_charge = battery_controller.propose_state_of_charge(
            self.battery_state_of_charge,
            self.battery_capacity,
            self.actual_previous_load,
            self.actual_previous_pv,
            timestep[price_buy_columns].values,
            timestep[price_sell_columns].values,
            timestep[load_columns].values,
            timestep[pv_columns].values
        )

        # get energy required to achieve the proposed state of charge
        grid_energy, battery_energy_change = self.simulate_battery_charge(self.battery_state_of_charge,
                                                                          proposed_state_of_charge,
                                                                          timestep.actual_consumption,
                                                                          timestep.actual_pv)

        grid_energy_without_battery, _ = self.simulate_battery_charge(0.0,
                                                                      0.0,
                                                                      timestep.actual_consumption,
                                                                      timestep.actual_pv)

        # buy or sell energy depending on needs
        price = timestep.price_buy_0 if grid_energy >= 0 else timestep.price_sell_0
        price_without_battery = timestep.price_buy_0 if grid_energy_without_battery >= 0 else timestep.price_sell_0
        self.money_spent += grid_energy * price
        self.money_spent_without_battery += grid_energy_without_battery * price_without_battery

        # update current state of charge
        self.battery_state_of_charge += battery_energy_change / self.battery_capacity
        self.actual_previous_load = timestep.actual_consumption
        self.actual_previous_pv = timestep.actual_pv

    def simulate_battery_charge(self, initial_state_of_charge, proposed_state_of_charge, actual_consumption, actual_pv):
        """ Charges or discharges the battery based on what is desired and
            available energy from grid and pv
        """
        # charge is bounded by what is feasible
        proposed_state_of_charge = np.clip(proposed_state_of_charge, 0.0, 1.0)

        # calculate proposed energy change in the battery
        target_energy_change = (proposed_state_of_charge - initial_state_of_charge) * self.battery_capacity

        # efficiency is different whether we intend to charge or discharge
        if target_energy_change >= 0:
            efficiency = self.battery_charging_efficiency
            target_charging_power = target_energy_change / ((15. / 60.) * efficiency)
        else:
            efficiency = self.battery_discharging_efficiency
            target_charging_power = target_energy_change * efficiency / (15. / 60.)

        # actual power is bounded by the properties of the battery
        actual_charging_power = np.clip(target_charging_power,
                                        self.battery_discharging_power_limit,
                                        self.battery_charging_power_limit)

        # actual energy change is based on the actual power possible and the efficiency
        if actual_charging_power >= 0:
            actual_energy_change = actual_charging_power * (15. / 60.) * efficiency
        else:
            actual_energy_change = actual_charging_power * (15. / 60.) / efficiency

        # what we need from the grid = (the change in the battery + the consumption) - what is available from pv
        grid_energy = (actual_energy_change + actual_consumption) - actual_pv

        # if positive, we are buying from the grid; if negative, we are selling
        return grid_energy, actual_energy_change


if __name__ == '__main__':
    # Generate random data for simulation
    N_SAMPLES = 1000
    rng = np.random.RandomState(1337)

    load_columns = [f"load_{s}" for s in range(96)]
    pv_columns = [f"pv_{s}" for s in range(96)]
    price_sell_columns = [f"price_sell_{s}" for s in range(96)]
    price_buy_columns = [f"price_buy_{s}" for s in range(96)]

    data = dict(
        # What the building actually consumed during the timestep (not provided to battery controller)
        actual_consumption=rng.randint(100, 1000, N_SAMPLES),

        # actual pv available at this time step (not provided to battery controller)
        actual_pv=rng.randint(0, 200, N_SAMPLES),

        # forecasts for consumption
        **{c: rng.randint(100, 1000, N_SAMPLES) for c in load_columns},

        # forecasts for available pv
        **{c: rng.randint(0, 200, N_SAMPLES) for c in pv_columns},

        # forecasts for price to sell
        **{c: rng.randint(5, 10, N_SAMPLES) for c in price_sell_columns},

        # forecasts for price to buy
        **{c: rng.randint(50, 100, N_SAMPLES) for c in price_buy_columns},
    )

    data = pd.DataFrame(data)

    # pass initial state and steps to simulation. See Simulation object for more options
    simulation = Simulation(data, actual_previous_load=0.0, actual_previous_pv=0.0)

    # execute the simulation
    money_spent, money_no_batt = simulation.run()

    f_str = "Your algorithm spent {:,.2f} with a battery, versus {:,.2f} without a battery over {} timesteps."
    print(f_str.format(money_spent, money_no_batt, data.shape[0]))
