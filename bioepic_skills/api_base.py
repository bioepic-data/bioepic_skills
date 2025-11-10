# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class APIBase:
    """
    Base class for interacting with the BioEPIC API. Sets the base URL for the API based on the environment.
    Environment is defaulted to the production instance of the API. This functionality is in place for testing different environments.

    Parameters
    ----------
    env: str
        The environment to use. Default is prod. Must be one of the following:
            prod
            dev

    """

    def __init__(self, env="prod"):
        if env == "prod":
            self.base_url = "https://api.bioepic.example.com"  # Update with actual URL
        elif env == "dev":
            self.base_url = "https://api-dev.bioepic.example.com"  # Update with actual URL
        else:
            raise ValueError("env must be one of the following: prod, dev")
