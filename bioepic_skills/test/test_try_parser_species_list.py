from bioepic_skills.try_parser import parse_try_species_list_text


def test_parse_try_species_list_text():
    sample = "\nAa achalensis\n\nAa argyrolepis\n"
    species = parse_try_species_list_text(sample)

    assert species == ["Aa achalensis", "Aa argyrolepis"]
