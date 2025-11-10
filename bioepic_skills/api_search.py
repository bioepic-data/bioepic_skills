# -*- coding: utf-8 -*-
import requests
from bioepic_skills.api_base import APIBase
import urllib.parse
import logging

logger = logging.getLogger(__name__)


class APISearch(APIBase):
    """
    Class to interact with the BioEPIC API to get collections of data.
    """

    def __init__(self, collection_name=None, env="prod"):
        super().__init__(env=env)
        self.collection_name = collection_name

    def get_records(
        self,
        filter: str = "",
        max_page_size: int = 100,
        fields: str = "",
        all_pages: bool = False,
    ) -> list[dict]:
        """
        Get a collection of data from the API.

        Parameters
        ----------
        filter: str
            The filter to apply to the query. Default is an empty string.
        max_page_size: int
            The maximum number of items to return per page. Default is 100.
        fields: str
            The fields to return. Default is all fields.
        all_pages: bool
            True to return all pages. False to return the first page. Default is False.

        Returns
        -------
        list[dict]
            A list of records.

        Raises
        ------
        RuntimeError
            If the API request fails.

        """
        logging.debug(f"get_records Filter: {filter}")
        filter = urllib.parse.quote(filter)
        logging.debug(f"get_records encoded Filter: {filter}")
        
        url = f"{self.base_url}/api/{self.collection_name}?filter={filter}&max_page_size={max_page_size}&projection={fields}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("API request failed", exc_info=True)
            raise RuntimeError("Failed to get collection from BioEPIC API") from e
        else:
            logging.debug(
                f"API request response: {response.json()}\n API Status Code: {response.status_code}"
            )

        if all_pages:
            return self._get_all_pages(response, filter, max_page_size, fields)
        else:
            return response.json().get("results", [])

    def _get_all_pages(
        self,
        response: requests.models.Response,
        filter: str = "",
        max_page_size: int = 100,
        fields: str = "",
    ):
        """
        Get all pages of results from the API.

        Parameters
        ----------
        response: requests.models.Response
            The initial response from the API.
        filter: str
            The filter to apply to the query.
        max_page_size: int
            The maximum number of items to return per page.
        fields: str
            The fields to return.

        Returns
        -------
        list[dict]
            A list of all records from all pages.
        """
        results = response.json()

        while True:
            if response.json().get("next_page_token"):
                next_page_token = response.json()["next_page_token"]
            else:
                break
            
            url = f"{self.base_url}/api/{self.collection_name}?filter={filter}&max_page_size={max_page_size}&projection={fields}&page_token={next_page_token}"
            
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error("API request failed", exc_info=True)
                raise RuntimeError("Failed to get collection from BioEPIC API") from e
            else:
                logging.debug(
                    f"API request response: {response.json()}\n API Status Code: {response.status_code}"
                )
                results["results"].extend(response.json()["results"])

        return results.get("results", [])

    def get_record_by_id(self, record_id: str) -> dict:
        """
        Get a record by its ID.

        Parameters
        ----------
        record_id: str
            The ID of the record to retrieve.

        Returns
        -------
        dict
            The record data.

        Raises
        ------
        RuntimeError
            If the API request fails.
        """
        url = f"{self.base_url}/api/{self.collection_name}/{record_id}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("API request failed", exc_info=True)
            raise RuntimeError(f"Failed to get record {record_id} from BioEPIC API") from e
        
        return response.json()

    def get_record_by_filter(
        self, filter: str, max_page_size=25, fields: str = "", all_pages=False
    ) -> list[dict]:
        """
        Get records by a filter.

        Parameters
        ----------
        filter: str
            The filter to apply to the query.
        max_page_size: int
            The maximum number of items to return per page. Default is 25.
        fields: str
            The fields to return. Default is all fields.
        all_pages: bool
            True to return all pages. False to return the first page. Default is False.

        Returns
        -------
        list[dict]
            A list of records matching the filter.
        """
        return self.get_records(filter, max_page_size, fields, all_pages)

    def get_record_by_attribute(
        self,
        attribute_name: str,
        attribute_value: str,
        max_page_size: int = 25,
        fields: str = "",
        all_pages: bool = False,
        exact_match: bool = False,
    ) -> list[dict]:
        """
        Get records by a specific attribute value.

        Parameters
        ----------
        attribute_name: str
            The name of the attribute to filter by.
        attribute_value: str
            The value of the attribute to filter by.
        max_page_size: int
            The maximum number of items to return per page. Default is 25.
        fields: str
            The fields to return. Default is all fields.
        all_pages: bool
            True to return all pages. False to return the first page. Default is False.
        exact_match: bool
            If True, performs an exact match. If False, performs a regex match. Default is False.

        Returns
        -------
        list[dict]
            A list of records matching the attribute criteria.
        """
        from bioepic_skills.data_processing import DataProcessing
        
        dp = DataProcessing()
        filter_dict = dp.build_filter({attribute_name: attribute_value}, exact_match=exact_match)
        
        return self.get_records(filter_dict, max_page_size, fields, all_pages)
