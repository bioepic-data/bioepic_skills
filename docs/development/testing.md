# Testing

BioEPIC Skills uses pytest for testing.

## Running Tests

### Run All Tests

```bash
uv run pytest
```

### Run with Coverage

```bash
uv run pytest --cov=bioepic_skills --cov-report=html
```

View the coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Tests

Run a specific test file:
```bash
uv run pytest bioepic_skills/test/test_api_search.py
```

Run a specific test class:
```bash
uv run pytest bioepic_skills/test/test_api_search.py::TestAPISearch
```

Run a specific test method:
```bash
uv run pytest bioepic_skills/test/test_api_search.py::TestAPISearch::test_get_records
```

### Verbose Output

```bash
uv run pytest -v
```

### Stop on First Failure

```bash
uv run pytest -x
```

## Writing Tests

### Test Structure

Tests are located in `bioepic_skills/test/`:

```
bioepic_skills/test/
├── __init__.py
├── test_api_search.py
└── test_data_processing.py
```

### Example Test

```python
import pytest
from bioepic_skills.api_search import APISearch

class TestAPISearch:
    def setup_method(self):
        """Set up test fixtures"""
        self.api = APISearch(collection_name="test")
    
    def test_initialization(self):
        """Test API client initialization"""
        assert self.api.collection_name == "test"
        assert self.api.base_url is not None
    
    def test_get_records(self):
        """Test getting records"""
        records = self.api.get_records(max_page_size=10)
        assert isinstance(records, list)
        assert len(records) <= 10
```

### Using Fixtures

```python
import pytest
from bioepic_skills.api_search import APISearch

@pytest.fixture
def api_client():
    """Create an API client for testing"""
    return APISearch(collection_name="test")

def test_with_fixture(api_client):
    """Test using a fixture"""
    records = api_client.get_records(max_page_size=5)
    assert isinstance(records, list)
```

### Mocking API Calls

```python
from unittest.mock import Mock, patch

def test_api_with_mock():
    """Test with mocked API response"""
    with patch('requests.get') as mock_get:
        # Set up mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [{"id": "1", "name": "Test"}]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test your code
        api = APISearch(collection_name="test")
        records = api.get_records()
        
        # Assertions
        assert len(records) == 1
        assert records[0]["id"] == "1"
```

### Testing Exceptions

```python
import pytest

def test_error_handling():
    """Test that proper errors are raised"""
    api = APISearch(collection_name="test")
    
    with pytest.raises(RuntimeError):
        api.get_record_by_id(None)
```

## Test Coverage

### View Coverage

After running tests with coverage:
```bash
pytest --cov=bioepic_skills --cov-report=term
```

### Coverage Goals

- Aim for >80% code coverage
- Focus on critical functionality
- Don't obsess over 100% - quality over quantity

### Exclude from Coverage

To exclude code from coverage, use `# pragma: no cover`:

```python
def debug_function():  # pragma: no cover
    """This function is only for debugging"""
    print("Debug info")
```

## Continuous Integration

Tests run automatically on:
- Every push to GitHub
- Every pull request
- Python versions: 3.10, 3.11, 3.12

See `.github/workflows/ci.yml` for CI configuration.

## Best Practices

### 1. Test Naming

Use descriptive test names:

```python
# Good
def test_get_records_returns_list():
    pass

def test_get_records_respects_max_page_size():
    pass

# Avoid
def test_1():
    pass

def test_records():
    pass
```

### 2. Arrange-Act-Assert

Structure tests with AAA pattern:

```python
def test_merge_dataframes():
    # Arrange
    df1 = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
    df2 = pd.DataFrame({"id": [1, 2], "value": [10, 20]})
    dp = DataProcessing()
    
    # Act
    result = dp.merge_dataframes("id", df1, df2)
    
    # Assert
    assert len(result) == 2
    assert "name" in result.columns
    assert "value" in result.columns
```

### 3. Test One Thing

Each test should verify one behavior:

```python
# Good
def test_convert_to_df_returns_dataframe():
    dp = DataProcessing()
    records = [{"id": "1"}]
    df = dp.convert_to_df(records)
    assert isinstance(df, pd.DataFrame)

def test_convert_to_df_has_correct_columns():
    dp = DataProcessing()
    records = [{"id": "1", "name": "Test"}]
    df = dp.convert_to_df(records)
    assert list(df.columns) == ["id", "name"]

# Avoid testing multiple things in one test
```

### 4. Use Descriptive Assertions

```python
# Good
assert len(records) == 5, "Expected 5 records"
assert record["type"] == "sample", "Record type should be 'sample'"

# Also good
assert len(records) == 5
assert record["type"] == "sample"
```

### 5. Clean Up Resources

```python
class TestWithResources:
    def setup_method(self):
        """Set up before each test"""
        self.temp_file = "test.txt"
        with open(self.temp_file, "w") as f:
            f.write("test data")
    
    def teardown_method(self):
        """Clean up after each test"""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_something(self):
        # Test uses self.temp_file
        pass
```

## Debugging Tests

### Run with Print Statements

```bash
uv run pytest -s  # Shows print output
```

### Use pdb Debugger

```python
def test_debug():
    import pdb; pdb.set_trace()
    # Test code...
```

### Show Locals on Failure

```bash
uv run pytest -l  # Show local variables on failure
```

## Common Testing Patterns

### Testing Data Processing

```python
def test_data_transformation():
    dp = DataProcessing()
    input_data = [{"id": "1", "value": "10"}]
    
    df = dp.convert_to_df(input_data)
    
    assert df["id"][0] == "1"
    assert df["value"][0] == "10"
```

### Testing API Calls

```python
@pytest.mark.integration
def test_real_api_call():
    """Integration test with real API"""
    api = APISearch(collection_name="samples")
    records = api.get_records(max_page_size=1)
    
    assert len(records) > 0
    assert "id" in records[0]
```

### Testing Authentication

```python
def test_authentication():
    auth = BioEPICAuth(
        client_id="test_id",
        client_secret="test_secret"
    )
    
    assert auth.has_credentials()
```

## Next Steps

- Review existing tests in `bioepic_skills/test/`
- Add tests when contributing new features
- Run tests before submitting pull requests
