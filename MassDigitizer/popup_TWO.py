import PySimpleGUI as sg
import data_access as db

class AutoSuggest_popup():
    startQueryLimit = 3

    candidateNamesList = []
    rowCandidates = []
    done = False

    def __init__(self, table, collectionID):
        self.tableName = table
        self.collectionID = collectionID


    def auto_suggest(self, name, columnName='fullname', customSQL='', taxDefItemId=None, rowLimit=200):
        """ Purpose: for helping digitizer staff rapidly input names using return suggestions based on three or
          more entered characters. Function only concerns itself with database lookup.
         name: This parameter is the supplied name from the user.
         rowLimit: at or below this the auto-suggest fires of its names
         returns: a list of names
         TODO implement 'taxonTreeDefid' at convienient time.
        """
        responseType = ''
        # Local variable to determine the auto-suggest type: 'storage', taxon-name, or 'parent taxon-name'.
        # It is included in the return statement.
        cur = db.getDbCursor()

        sql = f"SELECT * FROM {self.tableName} WHERE {columnName} LIKE lower('%{name}%');"

        if taxDefItemId:
            sql = sql[:-1]
            sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
        elif customSQL:
            sql = customSQL
        print('the SQL going into cursor :;;', sql)
        rows = cur.execute(sql).fetchall()

        return rows

    def buildGUI(self):
        data = [
            'Ronald Reagan', 'Abraham Lincoln', 'George Washington', 'Andrew Jackson',
            'Thomas Jefferson', 'Harry Truman', 'John F. Kennedy', 'George H. W. Bush',
            'George W. Bush', 'John Quincy Adams', 'Garrett Walker', 'Bill Clinton',
            'Jimmy Carter', 'John Adams', 'Theodore Roosevelt', 'Frank Underwood',
            'Woodrow Wilson',
        ]

        layout = [
            [sg.Text('Input a taxon name:', key='lblInput'),
             sg.InputCombo(data, key='cbxCombo')]
        ]

        window = sg.Window('testing combo', layout, finalize=True)


        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                break

            if event == 'cbxCombo':
                print(values[event])

            if event in ('a','s','d'):
                print('triggered keys')

        window.close()

obj = AutoSuggest_popup('taxonname', 29)

obj.buildGUI()