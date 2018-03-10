# Problem description

The objective is to forecast energy consumption from little data:

 - Historical building consumption data
 - Historical weather data and weather forecast for one or a few places geographically close to the building
 - Calendar information, identifying working and off days
 - Meta-data about the building, e.g., whether it is an office space, a restaurant, etc.

In the context of this challenge, we do not want to look at all of the details of the building--the objective of the challenge is to provide an algorithm that can (i) either make a good forecast for all or some of the buildings or (ii) bring the conclusion that other data would be necessary to make relevant forecasts.

** CONSIDER ONLY PAST DATA WHEN MAKING YOUR PREDICTIONS **

The goal of this competition is to _forecast_ consumption accurately. Only algorithms that can be fully replicated and shown to only use past data to create the forecasts will be considered eligible for the prize money.

<div class="container">
	<div class="row">
		<div class="col-xs-3">
			<ul style="list-style: none">
				<li><strong>The Data</strong></li>
				<li><a href="#features_list">Overview</a></li>
				<li><a href="#datasets">Datasets</a></li>
				<li><a href="#external">External data</a></li>
        <li><a href="#what-when">Eligibility Rules</a></li>

			</ul>
		</div>
		<div class="col-xs-3">
			<ul style="list-style: none">
				<li><strong>Evaluation</strong></li>
				<li><a href="#metric">Metric</a></li>
				<li><a href="#format">Format</a></li>
			</ul>
		</div>
	</div>
</div>

<a id="features_list"></a>

## Overview

-----

More than 200 building sites are considered. Three time horizons and time steps are distinguished. The goal is either:

 - To forecast the consumption for each quarter for the length of time specified by the submission format.
 - To forecast the consumption for each hour for the length of time specified by the submission format.
 - To forecast the consumption for each day for the length of time specified by the submission format.

Historical data are given at the granularity that is required for the consumption forecast. So, when historical data are given by steps of 15 minutes, forecasts are required by steps of 15 minutes. When historical data are given by steps of 1 hour, forecasts are required by steps of 1 hour. When historical data are given by steps of 1 day, forecasts are required by steps of 1 day.

These data may contain a small portion of wrong / missing values.

Weather forecasts are given for several stations around each building site. The distance between the site and the station is given. The time granularity of the weather data varies from a station to the other.

For each data set, several test periods over which a forecast is required will be specified. For each building and test period, it is allowed for the algorithm to use any form of model learned from previous data. On the other hand, participants are not supposed to attempt to get additional external information about the building sites. Also, when forecasting values for a given time period, participants are also not allowed to use given data from the following period (no interpolation is allowed).


<a id="datasets"></a>

## Datasets

### Historical Consumption

A selected time series of consumption data for over 200 buildings.

 * `obs_id` - An arbitrary ID for the observationaa
 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `ForecastId` - An ID for a timeseries that is part of a forecast (can be matched with the submission file)
 * `Timestamp` - The time of the measurement
 * `Value` - A measure of consumption for that building

### Building Metadata

Additional information about the included buildings.

 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `Surface` - The surface area of the building
 * `Sampling` - The number of minutes between each observation for this site. The timestep size for each `ForecastId` can be found in the separate "Submission Forecast Period" file on the data download page.
 * `BaseTemperature` - The base temperature for the building
 * `[DAY_OF_WEEK]IsDayOff` - `True` if `DAY_OF_WEEK` is not a work day

### Historical Weather Data

This dataset contains temperature data from several stations near each site. For each site several temperature measurements were retrieved from stations in a radius of 30 km if available.

** Note: Not all sites will have available weather data.  **

** Note: Weather data is available for test periods under the assumption that reasonably accurate forecasts will be available to algorithms that the time that we are attempting to make predictions about the future. **

 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `Timestamp` - The time of the measurement
 * `Temperature` - The temperature as measured at the weather station
 * `Distance` - The distance in km from the weather station to the building in km

### Public Holidays

Public holidays at the sites included in the dataset, which may be helpful for identifying days where consumption may be lower than expected.

** Note: Not all sites will have available public holiday data. **

 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `Date` - The date of the holiday
 * `Holiday` - The name of the holiday

<a id="external"></a>

## External data

For this competition, use of external data is prohibited, with the sole exception of pre-trained Neural Networks that are included on the External Data thread in the forum.


<a id="what-when"></a>

## Eligibility Rules (what data you can use when)

As already mentioned, **your solution cannot be a function that interpolates between past and future data**. Submissions that are determined by the judges to violate this constraint will not be eligible for a prize. In general, intellectual honesty should be your guiding principle. Your goal is to build a model that generalizes well enough to forecasting the future, so you must believe you have not overfit the training data.


### Data use at training time

When you are training your model, you can use any of the training data available to you. However, you must not use that data to create an interpolation across the omitted test periods.

If you're having trouble knowing if your model is eligible, here is an example that might help. Say you are asked to make predictions for March 2016. At prediction time, your model can use the following features: any data before March 2016, any weather data we provide, and the fact that we want to make predictions in March. However, the model shouldn’t need to know that we are predicting in the year 2016. For the same historical time series and weather data, the model should make the same predictions in March regardless of year. If your model requires the year to make a prediction, then you’ve probably created an interpolation. This is just an example, not a rule so consider your training approach carefully.

### Data use at prediction time


When making a forecast, you can use the following data for constructing features that are inputs to your model. Say that we're making predictions for building |$B_i$| at timestep |$t_5$| for the larger forecast period |$T_p$|.

**Data you can use in this case is:**

 - Any weather data, including data during |$T_p$|
 - Any consumption data from |$B_i$| that is before |$T_p$|
 - Any predictions that we have made for |$T_p$| (the goal is to predict for the entire period, not necessarily for each step sequentially, which means that any other predictions during |$T_p$| can be used)
 - Data from buildings other than |$B_i$| before |$T_p$|, but not during or after

**Data you cannot use in this case is:**

 - Actual consumption data for |$B_i$| during |$T_p$| (this is not provided)
 - Consumption for |$B_i$| after |$T_p$|
 - Consumption for building other than |$B_i$| during |$T_p$|
 - Consumption for building other than |$B_i$| after |$T_p$|


<a id="metric"></a>

## Performance metric

-----

For each building and test period, the quality of the forecast will be evaluated using the Weighted Root Mean Squared Error (WRMSE) measure. Each consecutive time step for a building is weighted by a weight equal to |$\frac{(3T_n - 2t +1)}{2 T_n^2}$| to down-weight predictions farther in the future.

To obtain a global performance index, the WRMSE is normalized by dividing it by the average consumption of the building over the test period, which is denoted as |$\mu_n$|. The average NWRMSE over all buildings and test periods is retained as a global performance index for the algorithm.

$$
NWRMSE = \frac{1}{N_{f}} \sum_{n=1}^{N_{f}} \frac{1}{\mu_n} \sqrt{ \sum_{t=1}^{T_n} \frac{(3T_n - 2t +1)}{2 T_n^2} (y_t - \hat{y}_t)^2 }
$$

 * |$N_{f}$| - is the total number of forecast periods (there are multiple test periods per site)
 * |$\mu_n$| - is the average consumption for site (building)  over the time period |$T_n$|, which is calculated as |$ \frac{1}{T_n} \sum_{t=1}^{T_n} y_t $| This is used to normalize the error across multiple forecasts at different sites.
 * |$T_n$| - the number of timestamps that we are calculating the metric over for this forecast |$n$|
 * |$y_t$| - the actual value at timestamp |$t$|
 * |$\hat{y}_t$| - the predicted value at timestamp |$t$|

Schneider Electric expects that some algorithms will perform better on some buildings or on some time horizons than on others. Average NWRMSE for some categories of buildings will be computed to appreciate performance on some categories. Participants who identified worthwhile categories to look at are invited to make suggestions to Schneider Electric.

## Submission format

-----

The format for the submission file is the same as the historical consumption data with the addition of an extra column `ForecastId`. This variables makes it easy to calculate the metric over the groups represented by |$N_{f}$| in the evaluation metric. The timestamps to make predictions are included in the submission format file which is provided.

<a id="sub_values"></a>

<div class="well">

For example, if you predicted...

<table class="table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SiteId</th>
      <th>Timestamp</th>
      <th>ForecastId</th>
      <th>Value</th>
    </tr>
    <tr>
      <th>obs_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1677832</th>
      <td>1</td>
      <td>2015-08-29</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5379616</th>
      <td>1</td>
      <td>2015-08-30</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>496261</th>
      <td>1</td>
      <td>2015-08-31</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4567147</th>
      <td>1</td>
      <td>2015-09-01</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3684873</th>
      <td>1</td>
      <td>2015-09-02</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>

</div>

Your `.csv` file that you submit would look like:

    obs_id,SiteId,Timestamp,ForecastId,Value
    1677832,1,2015-08-29 00:00:00,1,0.0
    5379616,1,2015-08-30 00:00:00,1,0.0
    496261,1,2015-08-31 00:00:00,1,0.0
    4567147,1,2015-09-01 00:00:00,1,0.0
    3684873,1,2015-09-02 00:00:00,1,0.0


## Good luck!

--------

Good luck and enjoy this problem! If you have any questions you can always visit the [user forum](http://community.drivendata.org/)!
