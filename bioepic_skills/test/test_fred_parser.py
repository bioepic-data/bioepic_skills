from bioepic_skills.fred_parser import (
    parse_fred_traits_html,
    parse_fred_species_html,
    parse_fred_data_sources_html,
)


def test_parse_fred_traits_html():
    html = """
    <table>
      <tr>
        <th>Trait Category</th><th>Trait Type</th><th>Traits</th><th>Column ID</th>
        <th>Description</th><th>Single-species Observations</th>
        <th>Multi-species Observations</th><th>Total observations</th>
      </tr>
      <tr>
        <td>Chemistry</td><td>Root</td><td>Calcium content</td><td>Ca_root</td>
        <td>Root calcium content</td><td>30</td><td>30</td><td>60</td>
      </tr>
    </table>
    """
    records = parse_fred_traits_html(html)
    assert len(records) == 1
    record = records[0]
    assert record.trait_category == "Chemistry"
    assert record.trait_type == "Root"
    assert record.column_id == "Ca_root"
    assert record.single_species_observations == 30
    assert record.total_observations == 60


def test_parse_fred_species_html():
    html = """
    <table>
      <tr><th>Scientific name</th><th>Observations</th></tr>
      <tr><td>Abies alba</td><td>12</td></tr>
      <tr><td>Picea abies</td><td>4</td></tr>
    </table>
    """
    records = parse_fred_species_html(html)
    assert len(records) == 2
    assert records[0].name == "Abies alba"
    assert records[0].observations == 12


def test_parse_fred_data_sources_html():
    html = """
    <table>
      <tr><th>Year</th><th>Citation</th><th>DOI</th></tr>
      <tr><td>2020</td><td>Smith J. Example study. https://doi.org/10.1000/example.</td><td></td></tr>
    </table>
    """
    records = parse_fred_data_sources_html(html)
    assert len(records) == 1
    assert records[0].year == 2020
    assert records[0].citation == "Smith J. Example study"
    assert records[0].doi == "https://doi.org/10.1000/example"
