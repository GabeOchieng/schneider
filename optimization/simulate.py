



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
