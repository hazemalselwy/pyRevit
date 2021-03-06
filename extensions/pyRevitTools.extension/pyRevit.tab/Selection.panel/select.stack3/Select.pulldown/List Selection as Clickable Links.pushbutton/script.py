from pyrevit import script, revit


__context__ = 'selection'
__doc__ = 'Lists the selected element ids as clickable links. '\
          'This is a quick way to go through a series of elements.'


output = script.get_output()
selection = revit.get_selection()


if len(selection.element_ids) > 0:
    output.set_width(200)

    if len(selection.element_ids) < 50:
        print('{}'.format(output.linkify(selection.element_ids,
                                         title='All Elements')))

    for idx, elid in enumerate(selection.element_ids):
        print('{}: {}'.format(idx+1, output.linkify(elid)))
