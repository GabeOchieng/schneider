import numpy as np
import pandas as pd

# ==============================================================================
#    THIS CLASS WILL BE IMPLEMENTED BY COMPETITORS
# ==============================================================================
class BatteryContoller(object):
    """ The BatteryContoller class handles providing a new "target charge"
        at each time step.

        This class is instantiated by the simulation script, and it can
        be used to store any state that is needed for the call to
        propose_charge that happens in the simulation.
    """

    def propose_charge(self,
                       current_charge,
                       previous_price_buy,
                       previous_price_sell,
                       load_15,
                       load_30,
                       load_1440,
                       pv_15,
                       pv_40,
                       pv_1440):

        # return 100 every time....
        return 100.0


class Simulation(object):
    """ Handles running a simulation.
    """
    def __init__(self,
                 data,
                 previous_price_buy=1.0,
                 previous_price_sell=1.0,
                 initial_battery_charge=0.0,
                 maximum_battery_charge=1000.,
                 battery_charging_power_limit=1.0,
                 battery_discharging_power_limit=-1.0,
                 battery_charging_efficiency=0.5,
                 battery_discharging_efficiency=0.5):
        """ Creates initial simulation state based on data passed in.
        """
        self.data = data

        # initialize money at 0.0
        self.money_spent = 0.0
        self.previous_price_buy = previous_price_buy
        self.previous_price_sell = previous_price_sell

        # battery initialization
        self.battery_charge = initial_battery_charge
        self.maximum_battery_charge = maximum_battery_charge

        # maximal battery charging power
        self.battery_charging_power_limit = battery_charging_power_limit
        self.battery_discharging_power_limit = battery_discharging_power_limit

        self.battery_charging_efficiency = battery_charging_efficiency
        self.battery_discharging_efficiency = battery_discharging_efficiency

    def run(self):
        """ Executes the simulation by iterating through each of the data points
        """
        battery_controller = BatteryContoller()

        for i, timestep in self.data.iterrows():
            self.simulate_timestep(battery_controller, timestep)

        return self.money_spent

    def simulate_timestep(self, battery_controller, timestep):
        """ Executes a single timestep using `battery_controller` to get
            a proposed charge.
        """

        # get proposed charge from the battery controller
        proposed_charge = battery_controller.propose_charge(
            self.battery_charge,
            self.previous_price_buy,
            self.previous_price_sell,
            timestep.load_15,
            timestep.load_30,
            timestep.load_1440,
            timestep.pv_15,
            timestep.pv_40,
            timestep.pv_1440
        )

        # get energy required to achieve charge
        grid_energy = self.simulate_battery_charge(proposed_charge,
                                                   timestep.actual_consumption,
                                                   timestep.actual_pv)

        # buy or sell energy depending on needs
        price = timestep.price_buy if grid_energy >= 0 else timestep.price_sell
        self.money_spent += grid_energy * price

        # track previous prices to pass to battery controller
        self.previous_price_buy = timestep.price_buy
        self.previous_price_sell = timestep.price_sell

    def simulate_battery_charge(self, proposed_charge, actual_consumption, actual_pv):
        """ Charges or discharges the battery based on what is desired and
            available energy from grid and pv
        """
        # charge is bounded by what is feasible
        proposed_charge = np.clip(proposed_charge, 0., self.maximum_battery_charge)

        # calculate proposed energy change in the battery
        target_energy_change = (proposed_charge - self.battery_charge)

        # efficiency is different whether we intend to charge or discharge
        if target_energy_change >= 0:
            efficiency = self.battery_charging_efficiency
        else:
            efficiency = self.battery_discharging_efficiency

        # calculate the power needed to achieve proposed difference with P = E / eff
        target_charging_power = target_energy_change / ((15. / 60.) * efficiency)

        # actual power is bounded by the properties of the battery
        actual_charging_power = np.clip(target_charging_power,
                                        self.battery_discharging_power_limit,
                                        self.battery_charging_power_limit)

        # actual energy change is based on the actual power possible and the efficiency
        actual_energy_change = actual_charging_power * (15. / 60.) * efficiency

        # what we need from the grid = (the change in the battery + the consumption) - what is available from pv
        grid_energy = (actual_energy_change + actual_consumption) - actual_pv

        # if positive, we are buying from the grid; if negative, we are selling
        return grid_energy


if __name__ == '__main__':
    # Generate random data for simulation
    N_SAMPLES = 10
    rng = np.random.RandomState(1337)
    data = dict(
        # What the building actually consumed during the timestep (not provided to battery controller)
        actual_consumption=rng.randint(100, 1000, N_SAMPLES),

        # actual pv available at this time step (not provided to battery controller)
        actual_pv=rng.randint(0, 200, N_SAMPLES),

        # the price to buy at this time step (not provided to battery controller)
        price_buy=rng.randint(0, 100, N_SAMPLES),

        # the price for selling energy at this timestep (not provided to battery controller)
        price_sell=rng.randint(0, 10, N_SAMPLES),

        # forecasts for energy needed
        load_15=rng.randint(100, 1000, N_SAMPLES),
        load_30=rng.randint(100, 1000, N_SAMPLES),
        load_1440=rng.randint(100, 1000, N_SAMPLES),

        # forecasts for available pv
        pv_15=rng.randint(0, 200, N_SAMPLES),
        pv_40=rng.randint(0, 200, N_SAMPLES),
        pv_1440=rng.randint(0, 200, N_SAMPLES),
    )

    data = pd.DataFrame(data)

    # pass initial state and steps to simulation. See Simulation object for more options
    simulation = Simulation(data, previous_price_buy=10.0, previous_price_sell=1.0)

    # execute the simulation
    money_spent = simulation.run()

    print("Your algorithm spent {:,.2f} over {} timesteps.".format(money_spent, data.shape[0]))

