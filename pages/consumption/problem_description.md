# Problem description

The objective is to forecast energy consumption from little data:
 - Historical building consumption data;
 - Weather historical data and weather forecast for one or a few places geographically close to the building;
 - Calendar information, identifying working and off days;
 - Possibly a few meta-data about the building, e.g., whether it is an office space, a restaurant, etc.
In the context of this challenge, we do not want to look at details of the building.
The objective of the challenge is to provide an algorithm that can (i) either make a good forecast for all or some of the buildings or (ii) bring the conclusion that other data would be necessary to make relevant forecasts.


<div class="container">
	<div class="row">
		<div class="col-xs-3">
			<ul style="list-style: none">
				<li><strong>Features</strong></li>
				<li><a href="#features_list">List of features</a></li>
				<li><a href="#features_eg">Example of features</a></li>
			</ul>
		</div>
		<div class="col-xs-3">
			<ul style="list-style: none">
				<li><strong>Performance metric</strong></li>
				<li><a href="#metric">Example</a></li>
			</ul>
		</div>
		<div class="col-xs-3">
			<ul style="list-style: none">
				<li><strong>Submission Format</strong></li>
				<li><a href="#sub_values">Format example</a></li>
			</ul>
		</div>
	</div>
</div>

<a id="features_list"></a>

## The features in this dataset

-----

More than 200 building sites are considered. Three time horizons and time steps are distinguished. The goal is either:
 - To forecast the consumption for each quarter of an hour over the next 24 hours (96 quarters).
 - To forecast the consumption for each hour over the next four days (96 hours).
 - To forecast the consumption for each day over the coming month (30 days).

Historical data are given at the granularity that is required for the consumption forecast. So, when historical data are given by steps of 15 minutes, forecasts are required by steps of 15 minutes. When historical data are given by steps of 1 hour, forecasts are required by steps of 1 hour. When historical data are given by steps of 1 day, forecasts are required by steps of 1 day.

These data may contain a small portion of wrong / missing values.

Weather forecasts are given for several stations around each building site. The distance between the site and the station is given. The time granularity of the weather data varies from a station to the other.
For each data set, several test periods over which a forecast is required will be specified. Data over these periods will be relatively clean. Participants can use the actual consumption over these test periods to determine whether their algorithm is working well. For each building and test period, it is allowed for the algorithm to use any form of model learned from previous data. On the other hand, participants are not supposed to attempt to get additional external information about the building sites.


### Dataset
 * `feature` - description

<a id="features_eg"></a>

<div class="well">

<h3> Feature data example</h3>

<hr/>

For example, a single row in the dataset, has these values:

<br/>
<br/>

<table style="width:70%; margin-left:15%; margin-right:15%;" class="table">
  TABLE_BODY_FROM_PANDAS_TO_HTML
</table>

</div>

<a id="metric"></a>

## Performance metric

-----

For each building and test period, the quality of the forecast will be evaluated using the Weighted Root Mean Squared Error (WRMSE) measure. Let n be the number of time steps, pi be the predicted value for each time step i, and ai be the actual (measured) value for time step i. Each time step is given a weight equal to wi = (3n – 2i + 1) / (2n2). With these weights, the WRMSE is computed as the square root of 1  i  n wi (pi – ai)2
To obtain a global performance index, the WRMSE is normalized by dividing it by the average consumption of the building over the test period, i.e., NWRMSE = WRMSE / (1/n 1  i  n ai), and the average NWRMSE over all buildings and test periods is retained as a global performance index for the algorithm.
Schneider Electric expects that some algorithms will perform better on some buildings or on some time horizons than on others. Average NWRMSE for some categories of buildings will be computed to appreciate performance on some categories. Participants who identified worthwhile categories to look at are invited to make suggestions to Schneider Electric.


## Submission format

-----

The format for the submission file is...

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
