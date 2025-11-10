# bioepic_skills

A Python library designed to simplify various research tasks for users looking to extract and prepare structured data from scientific literature for use with the EcoSIM model.

# Usage

Example use of the API client:
```python
from bioepic_skills.api_search import APISearch

# Create an instance of the module
api_client = APISearch()
# Use the variable to call the available functions
api_client.get_record_by_id(record_id="example-id")
```

## Logging - Debug Mode
To see debugging information, include these two lines where ever you are running the functions:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# when this is run, you will see debug information in the console.
api_client.get_record_by_id(record_id="example-id")
```

# Installation

To install, run:

```bash
python3 -m pip install bioepic_skills
```

Periodically run
```bash
python3 -m pip install --upgrade bioepic_skills
```
to ensure you have the latest updates from this package.

# Documentation

Documentation about available functions and helpful usage notes can be found in the `docs/` directory.