import numpy as np


def _per_forecast_wrmse(actual, predicted, weights=None):
    # limit weights to just the ones we need
    weights = weights[:actual.shape[0]]

    # NaNs in the actual should be weighted zero
    nan_mask = np.isnan(actual)
    weights[nan_mask] = 0
    actual[nan_mask] = 0

    # calculated weighted rmse
    total_error = np.sqrt((weights * ((predicted - actual) ** 2)).sum())

    # normalized by actual consumption (avoid division by zero for NaNs)
    denom = np.mean(actual)
    denom = denom if denom != 0.0 else 1e-10
    return total_error / denom


def weighted_rmse(actual, predicted):
    """ col 0: site id
        col 1: timestamp
        col 2: forecast id
        col 3: consumption value

        Computes the weighted, normalized RMSE per site and then
        averages across sites for a final score.
    """
    # flatten and cast forecast ids
    forecast_ids = actual[:, 2].ravel().astype(int)

    # flatten and cast actual + predictions
    actual_float = actual[:, 3].ravel().astype(np.float64)
    predicted_float = predicted[:, 3].ravel().astype(np.float64)

    # get the unique forecasts
    unique_forecasts = np.unique(forecast_ids)
    per_forecast_errors = np.zeros_like(unique_forecasts, dtype=np.float64)

    # pre-calc all of the possible weights so we don't need to do so for each site
    # wi = (3n –2i + 1) / (2n^2)
    n_obs = 200  # longest forecast is ~192 obs
    weights = np.arange(1, n_obs + 1, dtype=np.float64)
    weights = (3 * n_obs - (2 * weights) + 1) / (2 * (n_obs ** 2))

    for i, forecast in enumerate(unique_forecasts):
        mask = (forecast_ids == forecast)
        per_forecast_errors[i] = _per_forecast_wrmse(actual_float[mask],
                                                     predicted_float[mask],
                                                     weights=weights)

    return np.mean(per_forecast_errors)


def test_weighted_rmse():
    n_test = 10000
    rng = np.random.RandomState(109157)

    sites = rng.choice([1.0, 2.0, 3.0, 4.0, 5.0], n_test).reshape(-1, 1)
    idx = np.arange(n_test).reshape(-1, 1)
    values = rng.chisquare(100, n_test).reshape(-1, 1)

    actual = np.hstack((idx, sites, values))

    # actual actual is 1
    assert weighted_rmse(actual, actual) == 0

    # actual + 100 ~= 0.998
    np.testing.assert_approx_equal(weighted_rmse(actual, actual + 100), 0.998, significant=3)

    # with nans
    predicted = actual + 100
    actual[5, 2] = np.nan
    np.testing.assert_approx_equal(weighted_rmse(actual, predicted), 0.998, significant=3)


def weighted_precision_recall(actual, predicted):
    tp = (predicted & actual).sum()
    fp = (predicted & ~actual).sum()
    fn = (~predicted & actual).sum()

    apr = 0.8 * (tp / (tp + fp)) + 0.2 * (tp / (tp + fn))
    return apr


def test_weighted_precision_recall():
    actual = np.array([0, 1, 1, 0])
    predicted = np.array([1, 1, 0, 0])

    assert 0.5 == weighted_precision_recall(actual, predicted)
    assert 0.0 == weighted_precision_recall(actual, ~actual)
    assert 1.0 == weighted_precision_recall(actual, actual)


def test():
    test_weighted_rmse()
    test_weighted_precision_recall()


if __name__ == "__main__":
    test()
