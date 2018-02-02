# Problem description

The overall objective is to provide methods for automatically detecting abnormal energy consumption data in buildings, as well as potential savings opportunities with all relevant details. Beyond detecting overconsumption, it is important to provide correct interpretation of overconsumption and, when possible, provide actionable recommendations.

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
				<li><a href="#metric">Assessment</a></li>
				<li><a href="#format">Format</a></li>
			</ul>
		</div>
	</div>
</div>

<a id="features_list"></a>

## Overview

-----

A few data sets, corresponding to different types of building sites from different geographies, will be provided. Some building sites will correspond to a unique main activity (office) while some will be mixed (office, research, cafeteria). The goal is to cover various situations and test solutions in differing conditions.

Data sets will include global energy consumption (cumulative or not) in Watt-hours (Wh), at intervals of 10, 15, or 30 minutes (depending on local utility standards). Some will also optionally include sub-metering information along with some usage data (daily building occupancy, schedule, weather). Data sets may include missing and incorrect values.


<a id="datasets"></a>

## Datasets

### Consumption Values

A selected time series of consumption data for over 200 buildings.

 * `meter_id` - An arbitrary ID number for a meter in a building (site). A building can have multiple meters. This id matches across datasets
 * `Timestamp` - The time of the measurement
 * `Values` - A measure of consumption for that meter

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

## Assessment

-----

There are two "tracks" for this competition. The first is an algorithm for anomaly detection that matches hand-labeled anomalies from Schneider Electric. This will be evaluated against the submissions that competitors make. The second is a submitted report. These reports will suggest anomaly detection methodology and outline classes of anomalies identified by the algorithms. The reports will be reviewed by an expert judging panel. The algorithm submissions will be scored using a weighted combination of precision and recall:

$$
WPR = \frac{1}{5} \bigg(\frac{T_p}{T_p + F_n} \bigg) + \frac{4}{5} \bigg(\frac{T_p}{T_p + F_p} \bigg)
$$

 * |$T_p$| - is the number of true positives. That is, the number of anomalies in the labeled set that also appear in the predictions.
 * |$F_n$| - is the number of false negatives. That is, the number of anomalies in the labeled set that do not appear in the predictions.
 * |$F_p$| - is the number of false positives. That is, the number of anomalies that are predicted, but are not anomalies in the labeled set.

WPR will be calculated for each building site and the final score will be the average of the per-building `WPR` score.


## Submission format

-----

The format for the submission file is the same as the historical consumption data that has the `site_id`, the `timestamp` of the reading, and a `1` in the `anomaly` column if the reading is an anomaly. For non-anomalous readings, a value of `0` will be in the `anomaly` column.

A portion of the submission will be used to compute a leaderboard score against a set of hand-labeled anomalies.

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
