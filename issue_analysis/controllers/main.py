from odoo import http
from odoo.http import request
import plotly as py
import plotly.graph_objs as go

class issue(http.Controller):

    @http.route("/issues/analysis", auth='public' ,website=True)
    def send_view(self,**kwargs):
        Issue = request.env['issue_new.model']
        Product = request.env['product.product']
        new_stat = len(Issue.search([('stage_id', '=', 'New')]))
        pending_stat = len(Issue.search([('stage_id', '=', 'Pending')]))
        solved_stat = len(Issue.search([('stage_id', '=', 'Solved')]))

        data = [go.Bar(x=["New", "Pending", "Solved"], y=[new_stat, pending_stat, solved_stat])]
        result1 = py.offline.plot(data, include_plotlyjs=False, output_type='div')

        lis = [person.salesperson.name for person in Issue.search([])]
        listy = {pers: lis.count(pers) for pers in lis}

        prod_list = [person.product.name for person in Issue.search([])]
        prody = {pers: prod_list.count(pers) for pers in prod_list}

        fig = {
            "data": [
                {
                    "values": [prod for prod in prody.values()],
                    "labels": [prod for prod in prody.keys()],
                    "name": "",
                    "hoverinfo": "label+percent",
                    "hole": .4,
                    "type": "pie"
                }],
            "layout":{
                "title":"Product-Issue Chart",
                "legend" :{'x':-.1,'y':1.2},
                "grid": {"rows": 1, "columns":1},
                "annotations": [
                    {
                        "font": {
                            "size": 10
                        },
                        "showarrow": False,
                        "text": "",
                        "x": 0.50,
                        "y": 0.5
                    }
                ],
            },
        }
        result3 = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        res = [go.Bar(x=[person for person in listy.keys()], y=[value for value in listy.values()])]
        result2 = py.offline.plot(res, include_plotlyjs=False, output_type='div')

        return request.render('issue_analysis.hello',{'result1':result1,'result2':result2,'new':new_stat,
                                                      'pending':pending_stat,'solved':solved_stat,'result3':result3})

    def back_to_issues(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'issue.model',
            'view_type':'kanban',
            'view_mode':'kanban',
            'target':'current',
        }
