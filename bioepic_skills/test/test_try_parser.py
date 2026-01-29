from bioepic_skills.try_parser import parse_try_species_text


def test_parse_try_species_text():
    sample = (
        "AccSpeciesID\tAccSpeciesName\tObsNum\tObsGRNum\tMeasNum\tMeasGRNum\tTraitNum\n"
        "271060\tAa achalensis\t5\t\t5\t\t3\n"
        "200002\tAa argyrolepis\t7\t\t9\t\t3\n"
    )

    records = parse_try_species_text(sample)

    assert len(records) == 2
    assert records[0].acc_species_id == 271060
    assert records[0].acc_species_name == "Aa achalensis"
    assert records[0].obs_num == 5
    assert records[0].obs_gr_num is None
    assert records[0].meas_num == 5
    assert records[0].meas_gr_num is None
    assert records[0].trait_num == 3
    assert records[0].pub_num is None
    assert records[0].acc_spec_num is None
