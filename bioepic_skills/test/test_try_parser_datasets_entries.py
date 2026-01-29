from bioepic_skills.try_parser import parse_try_dataset_entries_html


def test_parse_try_dataset_entries_html():
    html = """
    <table>
      <tr><td><b>Title: </b></td><td>TRY - Categorical Traits Dataset</td></tr>
      <tr><td><b>TRY File Archive ID: </b></td><td>3</td></tr>
      <tr><td><b>Rights of use: </b></td><td>Public, CC.BY.3.0</td></tr>
      <tr><td><b>Publication Date: </b></td><td>2012-03-19</td></tr>
      <tr><td><b>Version: </b></td><td>1.0</td></tr>
      <tr><td><b>Author: </b></td><td>Jens Kattge</td></tr>
      <tr><td><b>Contributors: </b></td><td>TRY Consortium</td></tr>
      <tr><td><b>Reference to publication: </b></td><td>TRY - a global database</td></tr>
      <tr><td><b>Reference to data package: </b></td><td>TRY File Archive</td></tr>
      <tr><td><b>DOI: </b></td><td>10.17871/TRY.3</td></tr>
      <tr><td><b>Format: </b></td><td>Zipped archive</td></tr>
      <tr><td><b>File name: </b></td><td>TRY_Categorical_Traits.zip</td></tr>
      <tr><td><b>Description: </b></td><td>Categorical traits</td></tr>
      <tr><td><b>Geolocation: </b></td><td>Global</td></tr>
      <tr><td><b>Temporal coverage: </b></td><td>Holocene</td></tr>
      <tr><td><b>Taxonomic coverage: </b></td><td>terrestrial vascular plants</td></tr>
      <tr><td><b>Field list: </b></td><td>AccSpeciesID, AccSpeciesName, Genus</td></tr>
    </table>
    """

    entries = parse_try_dataset_entries_html(html)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.title == "TRY - Categorical Traits Dataset"
    assert entry.try_file_archive_id == "3"
    assert entry.doi == "10.17871/TRY.3"
    assert entry.field_list == ["AccSpeciesID", "AccSpeciesName", "Genus"]
