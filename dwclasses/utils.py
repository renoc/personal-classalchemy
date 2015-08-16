from combinedchoices.models import Choice, ChoiceSection, Section


SECTIONS = [
    ['drive', 'Drive', {
        'cross_combine': True, 'field_type': Section.SINGLE,
        'instructions': 'Fulfill your drive to gain exp.'}],
    ['aspect', 'Aspect', {
        'cross_combine': True, 'field_type': Section.SINGLE,
        'instructions': 'Choose one aspect/race'}],
    ['bond', 'Bonds', {
        'cross_combine': True, 'field_type': Section.MULTIPLE,
        'max_selects': 10, 'instructions': 'Form at least one bond'}],
    ['gear', 'Gear', {
        'cross_combine': False, 'field_type': Section.MULTIPLE,
        'instructions': 'Pay attention to number of selections'}],
    ['start', 'Starting Moves', {
        'cross_combine': True, 'field_type': Section.DESCRIPTION}],
    ['2-5', 'Advanced Moves 2-5', {
        'cross_combine': True, 'field_type': Section.DESCRIPTION,
        'instructions': 'Choose one move each time you gain a level 2-5'}],
    ['6-10', 'Advanced Moves 6-10', {
        'cross_combine': True, 'field_type': Section.DESCRIPTION,
        'instructions': 'Choose one move each time you gain a level 6-10'}],
]


def get_section(section_def, user=None):
    regee, verbose, kwargs = section_def
    section_query = Section.objects.filter(
        field_name__icontains=regee, user=user)
    if section_query.exists():
        section = section_query[0]
    else:
        section = Section.objects.create(
            field_name=verbose, user=user, **kwargs)
    return section


def populate_sections(compendium, sections=SECTIONS):
    move = 'Gain one move from a playbook no one else is currently using.'
    user = compendium.user
    for section_def in sections:
        section = get_section(section_def, user=user)
        choice_section, _ = ChoiceSection.objects.get_or_create(
            section=section, basecco=compendium)
        if 'Advanced' in section.field_name:
            move_name = 'Worldy\n'
            if '6-10' in section.field_name:
                move_name = 'Otherworldy\n'
            Choice.objects.create(
                choice_section=choice_section, text='%s%s' % (move_name, move))
