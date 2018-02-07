# Problem description

The objective is to create an optimization algorithm that effectively uses available solar power, building energy consumption, and a battery system to buy, sell, and consume energy in the way that saves the most money and puts the least demand on the energy grid.

For this challenge, you will be provided the input data where each row represents a time at which you have to make a decision whether to consume power from the battery or to charge the battery.


<div class="container">
	<div class="row">
		<div class="col-xs-3">
			<ul style="list-style: none">
				<li><a href="#data">Available Data</a></li>
				<li><a href="#sim">The Simulation</a></li>
				<li><a href="#subs">Code Submission Format</a></li>
				<li><a href="#eval">Evaluation Environment and Assessment</a></li>
				<li><a href="#scores">Leaderboard Scores</a></li>
			</ul>
		</div>
	</div>
</div>


<a id="data"></a>

## Available data

Your algorithm must be engineered to accept data as defined by the `BatteryController.propose_state` function and use that data to propose a new state for the charge of the battery. The data passed to that function are as follows:

 - `timestamp` - The current date and time.
 - `battery` - A battery object with properties like `current_charge` which is a float from 0 (empty) to 1 (full).
 - `actual_previous_load` - The actual load (consumption) of the site during the last time step.
 - `actual_previous_pv_production` - The actual pv available to the site during the last time step.
 - `price_buy` (`array`) - The actual prices to buy energy for the next 96 time steps.
 - `price_sell` (`array`) - The actual prices to sell energy for the next 96 time steps.
 - `load_forecast` (`array`) - A forecast for the load (consumption) at the site for the next 96 time steps. Actual consumption may or may not match the forecast.
 - `pv_forecast` (`array`) - A forecast for the photovoltaic energy that will be available at the site for the next 96 time steps. Actual pv production may or may not match the forecast.

The load and PV forecasts are not perfect. This means that the actual load and PV production are not known when the `propose_state` method is called. After a proposal is made, the actual values (not the forecast) will be used to determine at what cost the proposed state of charge can effectively be attained.

We provide two folders of data, and each one contains a single `csv` file named with the site id (e.g., `2.csv`). The two folders are:

 - `submit`: contains site simulations for ~10 days. This should be used by the simulation script to generate a leaderboard submission.
 - `train`: a much longer period of data for discovering patterns and training algorithms that may be used in generating submissions.

<a id="sim"></a>

## The Simulation

[The simulation engine](https://github.com/drivendataorg/power-laws-optimization) provides data to the battery controller at every time step and asks for a desired charge of the battery for the next time step. The aim of this challenge is to provide, every 15 minutes, the state of the charge of the battery to target 15 minutes later. If that charge can be achieved in that time it will be. If not, the battery will get as close as possible. At each time step the energy needed from the grid will be calculated and the price for that energy will be calculated. If the energy needed is negative, that much energy will be sold. The simulation engine will track the total amount of money spent by the algorithm over the course of the simulation and compare that to the cost of the energy if the building had no battery at all.

The simulation proceeds as follows for each timestep (for implementation, see `simulate.py`):
 - Get the proposed state of charge by calling `propose_state` as provided by the competitors.
 - Simulate charging or discharing the battery by doing the following:
 	- Restrict the proposed charge to valid values `[0, 1]`
 	- Calculate how much energy is required to make the proposed change.
 	- Calculate the power that would need to be applied to make that change.
 	- Restrict the actual power applied according to the limits of the battery.
 	- Charge or discharge at the actual power for 15 minutes to calculate the actual energy change.
 	- Add the energy change to the building consumption for the timestep to get total energy required.
 	- Subtract any energy that is provided by pv to get the total energy needed from the grid (or, if negative, sold back to the grid).
 - Using the total needed from the grid, calculate the price paid and add that to the running total.
 - Perform the same computation as if there is no battery to get a baseline.
 - Update the battery state to the new state.

 This will be executed as it is coded in `simulate.py` which is available in the [competition repository](https://github.com/drivendataorg/power-laws-optimization).


<a id="subs"></a>

## Code submission format

[We provide a sample repository](https://github.com/drivendataorg/power-laws-optimization) that shows how the simulations will be executed. We will only accept a single `battery_controller.py` file as your submission. That file must implement the `propose_state` method on the `BatteryController` object, which will be called by the simulation. You cannot change the method signature of `propose_state`, but you can add any supplementary methods you may need, including ones that store state on the BatteryController object. This object is instantiated once at the begininning of each simulation, and persists throughout the entire simulation.

Before the end of February, we will add a `Code Submission` link to the right hand column when you have joined the competition. Through this link you can submit your code implementation. Submit only the following file:

 - battery_controller.py

You may continue to submit your latest code up until the deadline. We will only keep your most recent submission.


<a id="eval"></a>

## Evaluation environment and assessment

The code will be executed inside a Docker container. [The competition repository](https://github.com/drivendataorg/power-laws-optimization) provides the Dockerfile and the instructions for running the container.

The container will provide Python 3.6 and versions of the Python libraries specified in the `requirements.txt` file, which include `pandas`, `numpy`, `scikit-learn`, and other common data libraries. Libraries outside of those identified can be requested to be included on the forum for the competition up until February 26, at which point we will stop making changes to the requirements. Only libraries that are installable with `pip` will be accepted. The algorithm must only use the libraries listed in the requirements file.

Additionally, the container will be given a limited runtime, CPU (`1 CPU`, 2.5 GHz Intel Xeon® Platinum 8175 processors or equivalent), and RAM (`4GB`, no swap). The container will not have access to a GPU. These limits will be included in the competition repository. The runtime will be no more than 30 minutes to make predictions over the course of a 10 day simulation.

At the end of the competition, submitted `battery.py` files will be used in a simulation under the above constraints. We will test each submission against multiple 10 day periods (same for all competitors) with different properties and record the results as a ratio of the money spent using the battery over the money spent without the battery. These results will be averaged over all of the simulations for a final score where a lower score is better. Winning competitors will be notified by email.

Code that does not execute within the constraints will not be disqualified.

<a id="scores"></a>

## Leaderboard scores

The leadeboard allows competitors to self-report their results from running simulation against the `submit` dataset.

The leaderboard will not be used in the evaluation of this competition. However, you can use the leaderboard to share with the community how well you are doing. By submitting the output of the simulation after executing it as it is in the competition repository, your current score will be included on the leaderboard.

Again, **the leaderboard is only to share your progress**, leaderboard scores will not be part of the awarding of prizes for the competition.


## Good luck!

--------

Good luck and enjoy this problem! If you have any questions you can always visit the [user forum](http://community.drivendata.org/)!
