from pyrevit import UI
from postern import Postern, request


app = Postern('testapp')


# @app.route('/select/<int:element_id>')
# def select(uiapp, element_id):
#     pass


@app.route('/testfunc/anotherlevel', methods=['GET', 'POST'])
def testfunc(uiapp):
    if request.method == 'POST':
        data = request.data
        UI.TaskDialog.Show('Postern App', data['message'])
    elif request.method == 'GET':
        return {'somekey': 18,
                'someotherkey': [1, 2, 3, 'reza']}


app.run()

from postern import rulemap
print(rulemap.get_rule('testapp', '/testfunc/anotherlevel', 'GET'))
print(rulemap.get_rule('testapp', '/testfunc/anotherlevel', 'POST'))
