# Problem description

The objective is to forecast energy consumption from little data:

 - Historical building consumption data
 - Historical weather data and weather forecast for one or a few places geographically close to the building
 - Calendar information, identifying working and off days
 - Meta-data about the building, e.g., whether it is an office space, a restaurant, etc.

In the context of this challenge, we do not want to look at all of the details of the building--the objective of the challenge is to provide an algorithm that can (i) either make a good forecast for all or some of the buildings or (ii) bring the conclusion that other data would be necessary to make relevant forecasts.

<div class="container">
	<div class="row">
		<div class="col-xs-3">
			<ul style="list-style: none">
				<li><strong>The Data</strong></li>
				<li><a href="#features_list">Overview</a></li>
				<li><a href="#datasets">Datasets</a></li>
				<li><a href="#external">External data</a></li>
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

 - To forecast the consumption for each quarter of an hour over the next 24 hours (96 quarters).
 - To forecast the consumption for each hour over the next four days (96 hours).
 - To forecast the consumption for each day over the coming month (30 days).

Historical data are given at the granularity that is required for the consumption forecast. So, when historical data are given by steps of 15 minutes, forecasts are required by steps of 15 minutes. When historical data are given by steps of 1 hour, forecasts are required by steps of 1 hour. When historical data are given by steps of 1 day, forecasts are required by steps of 1 day.

These data may contain a small portion of wrong / missing values.

Weather forecasts are given for several stations around each building site. The distance between the site and the station is given. The time granularity of the weather data varies from a station to the other.

For each data set, several test periods over which a forecast is required will be specified. Data over these periods will be relatively clean. Participants can use the actual consumption over these test periods to determine whether their algorithm is working well. For each building and test period, it is allowed for the algorithm to use any form of model learned from previous data. On the other hand, participants are not supposed to attempt to get additional external information about the building sites.


<a id="datasets"></a>

## Datasets

### Historical Consumption

A selected time series of consumption data for over 200 buildings.

 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `Timestamp` - The time of the measurement
 * `Value` - A measure of consumption for that building

### Building Metadata

Additional information about the included buildings.

 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `Surface` - The surface area of the building
 * `BaseTemperature` - The base temperature for the building
 * `[DAY_OF_WEEK]IsDayOff` - `True` if `DAY_OF_WEEK` is not a work day

### Historical Weather Data

This dataset contains temperature data from several stations near each site. For each site several temperature measurements were retrieved from stations in a radius of 30 km.

 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `Timestamp` - The time of the measurement
 * `Temperature` - The temperature as measured at the weather station
 * `Distance` - The distance in km from the weather station to the building in km

### Public Holidays

Public holidays at the sites included in the dataset, which may be helpful for identifying days where consumption may be lower than expected.

 * `SiteId` - An arbitrary ID number for the building, matches across datasets
 * `Date` - The date of the holiday
 * `Holiday` - The name of the holiday

<a id="external"></a>

## External data

For this competition, use of external data is prohibited, with the sole exception of pre-trained Neural Networks that are included on the External Data thread in the forum.


<a id="metric"></a>

## Performance metric

-----

For each building and test period, the quality of the forecast will be evaluated using the Weighted Root Mean Squared Error (WRMSE) measure. Each consecutive time step for a building is weighted by a weight equal to |$\frac{(3T_n - 2t +1)}{2 T_n^2}$| to down-weight predictions farther in the future.

To obtain a global performance index, the WRMSE is normalized by dividing it by the average consumption of the building over the test period, which is denoted as |$\mu_n$|. The average NWRMSE over all buildings and test periods is retained as a global performance index for the algorithm.

$$
NWRMSE = \frac{1}{N_{sites}} \sum_{n=1}^{N_{sites}} \frac{1}{\mu_n} \sqrt{ \frac{1}{T_n}\sum_{t=1}^{T_n} \frac{(3T_n - 2t +1)}{2 T_n^2} (y_t - \hat{y}_t)^2 }
$$

 * |$N_{sites}$| - is the total number of sites
 * |$\mu_n$| - is the average consumption for site (building)  over the time period |$T_n$|, which is calculated as |$ \frac{1}{T_n} \sum_{t=1}^{T_n} y_t $| This is used to normalize the error across sites.
 * |$T_n$| - the number of timestamps that we are calculating the metric over for site |$n$|
 * |$y_t$| - the actual value at timestamp |$t$|
 * |$\hat{y}_t$| - the predicted value at timestamp |$t$|

Schneider Electric expects that some algorithms will perform better on some buildings or on some time horizons than on others. Average NWRMSE for some categories of buildings will be computed to appreciate performance on some categories. Participants who identified worthwhile categories to look at are invited to make suggestions to Schneider Electric.

## Submission format

-----

The format for the submission file is the same as the historical consumption data. The timestamps to make predictions are included in the submission format file which is provided.

<a id="sub_values"></a>

<div class="well">

For example, if you predicted...

<table class="table">
 OUTPUT OF df.head()
 OUTPUT OF df.tail()
</table>

</div>

Your `.csv` file that you submit would look like:

OUTPUT_OF_HEAD
...
OUTPUT_OF_TAIL


## Good luck!

--------

Good luck and enjoy this problem! If you have any questions you can always visit the [user forum](http://community.drivendata.org/)!