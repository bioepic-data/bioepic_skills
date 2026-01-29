from bioepic_skills.try_parser import parse_try_traits_html


def test_parse_try_traits_html():
    html = """
    <table>
      <tr>
        <th>TraitID</th><th>Trait</th><th>ObsNum</th><th>ObsGRNum</th><th>PubNum</th><th>AccSpecNum</th>
      </tr>
      <tr>
        <td>2957</td><td>Bark calcium (Ca) content per bark dry mass</td>
        <td>30</td><td>30</td><td>30</td><td>5</td>
      </tr>
      <tr>
        <td>617</td><td>Bark carbon (C) content per bark dry mass</td>
        <td>772</td><td>534</td><td>772</td><td>274</td>
      </tr>
    </table>
    """

    records = parse_try_traits_html(html)

    assert len(records) == 2
    assert records[0].trait_id == 2957
    assert records[0].trait.startswith("Bark calcium")
    assert records[0].obs_num == 30
    assert records[0].obs_gr_num == 30
    assert records[0].pub_num == 30
    assert records[0].acc_spec_num == 5
