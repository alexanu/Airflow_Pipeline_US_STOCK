from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class
class CustomPlugin(AirflowPlugin):
    name = "usstock_custom_plugin"
    operators = [
        operators.StageJsonToS3,
        operators.S3CreateBucket,
        operators.TiingoPricePerIndustryHistorical,
        operators.TargetS3StockSymbols,
        operators.TargetS3EodLoad,
    ]
    helpers = [
        helpers.StockSymbols,
    ]
