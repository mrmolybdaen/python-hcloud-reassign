# Unit testing

This directory provides unit tests.

We resemble the library's directory tree to structure the tests. So every subdir of the lib will have a corresponding directory.
Every module has corresponding test module. The test module name is prefixed with `test_`, for example the module `metrics.py` has
a corresponding file `test_metrics.py`.

For grouping of test cases one has to define a class prefixed with `Test`, for example `TestMetrics`.
The test case has to be prefixed with `test_` the same way as the module.

To avoid the need of API tokens for testing, we need a mockup api. This can be achieved with pytest's `monkeypatch.setattr`.
See [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
