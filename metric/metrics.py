import numpy as np


def _per_site_wrmse(actual, predicted):
    # generate per-building weights according to
    # wi = (3n –2i + 1) / (2n^2)
    n_obs = actual.shape[0]
    weights = np.arange(1, n_obs + 1, dtype=np.float64)
    weights = (3 * n_obs - (2 * weights) + 1) / (2 * (n_obs ** 2))

    # calculated weighted rmse
    total_error = np.sqrt((weights * ((predicted - actual) ** 2)).sum())

    # normalized by actual consumption
    return total_error / np.mean(actual)


def weighted_rmse(actual, predicted):
    """ col 0: timestamps
        col 1: site id
        col 2: consumption value

        Computes the weighted, normalized RMSE per site and then
        averages across sites for a final score.
    """
    unique_sites = np.unique(actual[:, 1])
    per_site_errors = np.zeros_like(unique_sites, dtype=np.float64)

    for i, site in enumerate(unique_sites):
        mask = actual[:, 1] == site
        per_site_errors[i] = _per_site_wrmse(actual[mask, 2].ravel(),
                                             predicted[mask, 2].ravel())

    return np.mean(per_site_errors)


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


def adjusted_precision_recall(actual, predicted):
    tp = (predicted & actual).sum()
    fp = (predicted & ~actual).sum()
    fn = (~predicted & actual).sum()

    apr = 0.8 * (tp / (tp + fp)) + 0.2 * (tp / (tp + fn))
    return apr


def test_adjusted_precision_recall():
    actual = np.array([0, 1, 1, 0])
    predicted = np.array([1, 1, 0, 0])

    assert 0.5 == adjusted_precision_recall(actual, predicted)
    assert 0.0 == adjusted_precision_recall(actual, ~actual)
    assert 1.0 == adjusted_precision_recall(actual, actual)


def test():
    test_weighted_rmse()
    test_adjusted_precision_recall()


if __name__ == "__main__":
    test()
