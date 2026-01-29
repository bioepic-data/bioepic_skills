from bioepic_skills.try_parser import parse_try_datasets_html_with_header


def test_parse_try_datasets_html_with_header():
    html = """
    <table>
      <tr><th>DatasetID</th><th>Dataset</th><th>Description</th></tr>
      <tr><td>1</td><td>Example</td><td>Example dataset</td></tr>
      <tr><td>2</td><td>Second</td><td>Another dataset</td></tr>
    </table>
    """

    header, records = parse_try_datasets_html_with_header(html)

    assert header == ["DatasetID", "Dataset", "Description"]
    assert len(records) == 2
    assert records[0]["DatasetID"] == "1"
    assert records[0]["Dataset"] == "Example"
