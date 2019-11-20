# -*- coding: UTF-8 -*-
import datetime
from random import shuffle
from nose.tools import eq_, raises, assert_raises

from pivottable import (
PivotTable, GroupBy, Sum
)
from pivottable.pivottable import PivotTableError

class TestError(Exception):
    pass

class DummyData(object):

    def __init__(self, team, city, period, won, drawn, lost):
        self.team = team
        self.city = city
        self.period = period
        self.won = won
        self.drawn = drawn
        self.lost = lost

    @property
    def played(self):
        return self.won+self.drawn+self.lost

    @property
    def points(self):
        return self.won*3+self.drawn*1

    @property
    def effectivity(self):
        try:
            return float(self.won)/float(self.played)
        except ZeroDivisionError:
            return float(0)

    def __repr__(self):
        return "<DummyData: %s, %s, %s>" % (self.team.encode('utf-8'), 
                                            self.city.encode('utf-8'), 
                                            self.period)

class GenericObject(object):

    def __init__(self, **kw):
        for k, v in list(kw.items()):
            setattr(self, k, v)

    def __repr__(self):
        return "Values: <%s>" % (", ".join([str(getattr(self, a)) for a in \
                                            dir(self) if not a.startswith('_')]))

def percent(value):
    return '%.2f%%' % (value*100)

def year_month(value):
    return value.strftime("%b-%y")

class TestPivot_A(object):

    pt = PivotTable()
    pt.rows = [
        GenericObject(**{'name':'Asia', 'population':3879000000,
                         'area':44579000}),
        GenericObject(**{'name':'North America', 'population':528720588,
                         'area':24709000}),
        GenericObject(**{'name':'Africa', 'population':1000010000,
                         'area':30221532}),
        GenericObject(**{'name':'Antarctica', 'population':1000,
                         'area':1400000}),
        GenericObject(**{'name':'Europe', 'population':731000000,
                         'area':10180000}),
        GenericObject(**{'name':'South America', 'population':385742554,
                         'area':17840000})
    ]
    pt.xaxis = "name"
    pt.xaxis_sort = True
    pt.yaxis = [
        {'attr':'population', 'label':'Population', 'aggr':Sum},
        {'attr':'area', 'label':'Area', 'aggr':Sum}]

    def test_AA_data(self):
        eq_(self.pt.headers, ["metric", "Africa", "Antarctica", "Asia",
                              "Europe", "North America", "South America"])

    def test_AB_results(self):
        eq_([a for a in self.pt.result], [
            ["metric", "Africa", "Antarctica", "Asia", "Europe", 
             "North America", "South America"],
            ["Population", '1000010000', '1000', '3879000000', '731000000',
             '528720588', '385742554'],
            ["Area", '30221532', '1400000', '44579000', '10180000', 
             '24709000', '17840000']
        ])

class TestPivot_B(object):

    pt = PivotTable()
    pt.rows = [
        GenericObject(**{'country':'Uruguay', 'year':1930, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Argentina', 'year':1930,
                         'champion':None, 'runnerup':'x'}),
        GenericObject(**{'country':'Italy', 'year':1934, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Czechoslovakia', 'year':1934, 
                         'champion':None, 'runnerup':'x'}),
        GenericObject(**{'country':'Italy', 'year':1938, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Hungary', 'year':1938, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Uruguay', 'year':1950, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Brazil', 'year':1950, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Germany', 'year':1954, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Hungary', 'year':1954, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Brazil', 'year':1958, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Sweden', 'year':1958, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Brazil', 'year':1962, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Czechoslovakia', 'year':1962, 
                         'champion':None, 'runnerup':'x'}),
        GenericObject(**{'country':'England', 'year':1966, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Germany', 'year':1966, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Brazil', 'year':1970, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Italy', 'year':1970, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Germany', 'year':1974, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Netherlands', 'year':1974, 
                         'champion':None, 'runnerup':'x'}),
        GenericObject(**{'country':'Argentina', 'year':1978,
                         'champion':'x', 'runnerup':None}),
        GenericObject(**{'country':'Netherlands', 'year':1978, 
                         'champion':None, 'runnerup':'x'}),
        GenericObject(**{'country':'Italy', 'year':1982, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Germany', 'year':1982, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Argentina', 'year':1986,
                         'champion':'x', 'runnerup':None}),
        GenericObject(**{'country':'Germany', 'year':1986, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Germany', 'year':1990, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Argentina', 'year':1990,
                         'champion':None, 'runnerup':'x'}),
        GenericObject(**{'country':'Brazil', 'year':1994, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Italy', 'year':1994, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'France', 'year':1998, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Brazil', 'year':1998, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Brazil', 'year':2002, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Germany', 'year':2002, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Italy', 'year':2006, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'France', 'year':2006, 'champion':None,
                         'runnerup':'x'}),
        GenericObject(**{'country':'Spain', 'year':2010, 'champion':'x',
                         'runnerup':None}),
        GenericObject(**{'country':'Netherlands', 'year':2010, 
                         'champion':None, 'runnerup':'x'})
        ]
    pt.xaxis = "year"
    pt.xaxis_sort = True
    pt.yaxis = [
        {'attr':'country', 'label':'Country', 'aggr':GroupBy},
        {'attr':'champion', 'label':'Champion', 'aggr':Sum},
        {'attr':'runnerup', 'label':'Runner Up', 'aggr':Sum}
    ]
    pt.yaxis_order = ["country"]

    def test_BA_result(self):
        shuffle(self.pt.rows)
        all1 = self.pt.result
        all2 = [
            ["country", "metric", "1930", "1934", "1938", "1950", "1954",
             "1958", "1962", "1966", "1970", "1974", "1978", "1982",
             "1986", "1990", "1994", "1998", "2002", "2006", "2010"],
            ["Argentina", "Champion", None, None, None, None, None, 
             None, None, None, None, None, 'x', None, 
             'x', None, None, None, None, None, None], 
            ["Argentina", "Runner Up", 'x', None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, 'x', None, None, None, None, None], 
            ["Brazil", "Champion", None, None, None, None, None, 
             'x', 'x', None, 'x', None, None, None, 
             None, None, 'x', None, 'x', None, None], 
            ["Brazil", "Runner Up", None, None, None, 'x', None, 
             None, None, None, None, None, None, None, 
             None, None, None, 'x', None, None, None], 
            ["Czechoslovakia", "Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Czechoslovakia", "Runner Up", None, 'x', None, None, None, 
             None, 'x', None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["England", "Champion", None, None, None, None, None, 
             None, None, 'x', None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["England", "Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["France", "Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, 'x', None, None, None], 
            ["France", "Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, 'x', None], 
            ["Germany", "Champion", None, None, None, None, 'x', 
             None, None, None, None, 'x', None, None, 
             None, 'x', None, None, None, None, None], 
            ["Germany", "Runner Up", None, None, None, None, None, 
             None, None, 'x', None, None, None, 'x', 
             'x', None, None, None, 'x', None, None], 
            ["Hungary", "Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Hungary", "Runner Up", None, None, 'x', None, 'x', 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Italy", "Champion", None, 'x', 'x', None, None, 
             None, None, None, None, None, None, 'x', 
             None, None, None, None, None, 'x', None], 
            ["Italy", "Runner Up", None, None, None, None, None, 
             None, None, None, 'x', None, None, None, 
             None, None, 'x', None, None, None, None], 
            ["Netherlands", "Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Netherlands", "Runner Up", None, None, None, None, None, 
             None, None, None, None, 'x', 'x', None, 
             None, None, None, None, None, None, 'x'], 
            ["Spain", "Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, 'x'], 
            ["Spain", "Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Sweden", "Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Sweden", "Runner Up", None, None, None, None, None, 
             'x', None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Uruguay", "Champion", 'x', None, None, 'x', None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            ["Uruguay", "Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None]] 
        for i in enumerate(all1): 
            eq_(i[1], all2[i[0]])

class TestPivot_C(object):

    pt = PivotTable()
    pt.rows = [
    DummyData('Estudiantes', 'La Plata', datetime.date(2011,2,1), 14, 3,
              2),
    DummyData('Vélez Sársfield', 'Buenos Aires', datetime.date(2011,2,1),
              13, 4, 2),
    DummyData('Arsenal', 'Sarandí', datetime.date(2011,2,1), 9, 5, 5),
    DummyData('River Plate', 'Buenos Aires', datetime.date(2011,2,1), 8, 
              7, 4),
    DummyData('Godoy Cruz', 'Mendoza', datetime.date(2011,2,1), 7, 8, 4),
    DummyData('Banfield', 'Banfield', datetime.date(2009,12,13), 12, 5, 
              2),
    DummyData("Newell's Old Boys", 'Rosario', datetime.date(2009,12,13), 
              12, 3, 4),
    DummyData('Colón', 'Santa Fé', datetime.date(2009,12,13), 10, 4, 5),
    DummyData('Independiente', 'Avellaneda', datetime.date(2009,12,13), 
              10, 4, 5),
    DummyData('Vélez Sársfield', 'Buenos Aires', datetime.date(2009,12,13),
              10, 4, 5),
    DummyData('Argentinos Juniors', 'Buenos Aires',
              datetime.date(2010,5,23), 12, 5, 2),
    DummyData('Estudiantes', 'La Plata', datetime.date(2010,5,23), 12, 4,
              3),
    DummyData('Godoy Cruz', 'Mendoza', datetime.date(2010,5,23), 11, 4,
              3),
    DummyData('Independiente', 'Avellaneda', datetime.date(2010,5,23),
              10, 4, 5),
    DummyData('Banfield', 'Banfield', datetime.date(2010,5,23), 9, 5, 5),
    DummyData('San Lorenzo', 'Buenos Aires', datetime.date(2008, 12, 14),
              12, 3, 4),
    DummyData('Boca Juniors', 'Buenos Aires', datetime.date(2008,12,14), 
              12,3,4),
    DummyData('Tigre', 'Tigre', datetime.date(2008,12,14),12,3,4),
    DummyData('Lanús', 'Lanús', datetime.date(2008,12,14),11,4,4),
    DummyData("Newell's Old Boys", 'Rosario', datetime.date(2008,12,14),
              8,7,4),
    DummyData('Vélez Sársfield', 'Buenos Aires', 
              datetime.date(2009, 7,5), 11, 7, 1),
    DummyData('Huracán', 'Buenos Aires', datetime.date(2009,7,5),
              12,2,5),
    DummyData('Lanús', 'Lanús', datetime.date(2009,7,5), 12,2,5),
    DummyData('Colón', 'Santa Fé', datetime.date(2009,7,5), 10,4,5),
    DummyData('Racing', 'Avellaneda', datetime.date(2009,7,5), 8,6,5)
    ]

    def test_CA_xaxis_property(self):
        self.pt.xaxis = "period"
        self.pt.xaxis_sort = True
        try:
            self.pt.xaxis_format = "hello world"
        except PivotTableError:
            pass
        else:
            raises(TestError("Assigning a non callable to xaxis_format should "
                             "raise an error"))
        self.pt.xaxis_format = year_month
        eq_(self.pt.xaxis_format(datetime.date(2010,1,1)), "Jan-10")

    def test_CC_wrong_attr_xaxis(self):
        assert_raises(PivotTableError, setattr, self.pt, 'xaxis', "johnny")
        eq_(self.pt.xaxis, "period")

    @raises(PivotTableError)
    def test_CD_yaxis_property(self):
        self.pt.yaxis = [
                {'hello':'world', 'label':'Team', 'aggr':GroupBy}]

    def test_CE_yaxis_property(self):
        self.pt.yaxis = [
                    {'attr':'team', 'label':'Team', 'aggr':GroupBy},
                    {'attr':'city', 'label':'City', 'aggr':GroupBy},
                    {'attr':'won', 'label':'Won', 'aggr':Sum},
                    {'attr':'lost', 'label':'Lost', 'aggr':Sum},
                    {'attr':'drawn', 'label':'Drawn', 'aggr':Sum},
                    {'attr':'effectivity', 'label':'Efectivity', 
                     'aggr':Sum, 'format':percent}]

    def test_CF_yaxis_order(self):
        self.pt.yaxis_order = ['city', 'team']
        # let's check the headers: they must obey yaxis_order and, if declared, 
        # the sort order for xaxis 
        eq_(self.pt.headers, 
            ['city', 'team', 'metric', datetime.date(2008, 12, 14),
             datetime.date(2009, 7, 5), datetime.date(2009, 12, 13),
             datetime.date(2010, 5, 23), datetime.date(2011, 2, 1)])

    @raises(PivotTableError)
    def test_CG_wrong_xaxis_attr(self):
        self.pt.xaxis = "hello_world"

    def test_CH_wrong_xaxis_attr(self):
        eq_(self.pt.xaxis, "period")

    @raises(AttributeError)
    def test_CI_headers_ro(self):
        self.pt.headers = ["These", "are", "my", "headers"]

    @raises(AttributeError)
    def test_CJ_result_ro(self):
        self.pt.result = ["This", "is", "my", "result"]

    def test_CK_result(self):
        all1 = self.pt.result
        all2 = [
         ['city', 'team', 'metric', "Dec-08", "Jul-09", "Dec-09",
          "May-10", "Feb-11"], 
         ['Avellaneda', 'Independiente', 'Won', None, None, '10', '10',
          None],
         ['Avellaneda', 'Independiente', 'Lost', None, None, '5', '5',
          None],
         ['Avellaneda', 'Independiente', 'Drawn', None, None, '4', '4',
          None],
         ['Avellaneda', 'Independiente', 'Efectivity', None, None,
          '52.63%', '52.63%', None],
         ['Avellaneda', 'Racing', 'Won', None, '8', None, None, None],
         ['Avellaneda', 'Racing', 'Lost', None, '5', None, None, None],
         ['Avellaneda', 'Racing', 'Drawn', None, '6', None, None, None],
         ['Avellaneda', 'Racing', 'Efectivity', None, '42.11%', None, None,
          None],
         ['Banfield', 'Banfield', 'Won', None, None, '12', '9', None],
         ['Banfield', 'Banfield', 'Lost', None, None, '2', '5', None],
         ['Banfield', 'Banfield', 'Drawn', None, None, '5', '5', None],
         ['Banfield', 'Banfield', 'Efectivity', None, None, '63.16%',
          '47.37%', None],
         ['Buenos Aires', 'Argentinos Juniors', 'Won', None, None, None,
          '12', None],
         ['Buenos Aires', 'Argentinos Juniors', 'Lost', None, None, None,
          '2', None],
         ['Buenos Aires', 'Argentinos Juniors', 'Drawn', None, None, None,
          '5', None],
         ['Buenos Aires', 'Argentinos Juniors', 'Efectivity', None, None,
          None, '63.16%', None],
         ['Buenos Aires', 'Boca Juniors', 'Won', '12', None, None, None,
          None],
         ['Buenos Aires', 'Boca Juniors', 'Lost', '4', None, None, None,
          None],
         ['Buenos Aires', 'Boca Juniors', 'Drawn', '3', None, None, None,
          None],
         ['Buenos Aires', 'Boca Juniors', 'Efectivity', '63.16%', None,
          None, None, None],
         ['Buenos Aires', 'Huracán', 'Won', None, '12', None, None, None],
         ['Buenos Aires', 'Huracán', 'Lost', None, '5', None, None, None],
         ['Buenos Aires', 'Huracán', 'Drawn', None, '2', None, None, None],
         ['Buenos Aires', 'Huracán', 'Efectivity', None, '63.16%', None,
          None, None],
         ['Buenos Aires', 'River Plate', 'Won', None, None, None, None,
          '8'],
         ['Buenos Aires', 'River Plate', 'Lost', None, None, None, None,
          '4'],
         ['Buenos Aires', 'River Plate', 'Drawn', None, None, None, None,
          '7'],
         ['Buenos Aires', 'River Plate', 'Efectivity', None, None, None,
          None, '42.11%'],
         ['Buenos Aires', 'San Lorenzo', 'Won', '12', None, None, None,
          None],
         ['Buenos Aires', 'San Lorenzo', 'Lost', '4', None, None, None,
          None],
        ['Buenos Aires', 'San Lorenzo', 'Drawn', '3', None, None, None,
         None],
        ['Buenos Aires', 'San Lorenzo', 'Efectivity', '63.16%', None, None,
         None, None],
        ['Buenos Aires', 'Vélez Sársfield', 'Won', None, '11', '10', None,
         '13'],
        ['Buenos Aires', 'Vélez Sársfield', 'Lost', None, '1', '5', None,
         '2'],
        ['Buenos Aires', 'Vélez Sársfield', 'Drawn', None, '7', '4', None,
         '4'],
        ['Buenos Aires', 'Vélez Sársfield', 'Efectivity', None, '57.89%',
         '52.63%', None, '68.42%'],
        ['La Plata', 'Estudiantes', 'Won', None, None, None, '12', '14'],
        ['La Plata', 'Estudiantes', 'Lost', None, None, None, '3', '2'],
        ['La Plata', 'Estudiantes', 'Drawn', None, None, None, '4', '3'],
        ['La Plata', 'Estudiantes', 'Efectivity', None, None, None,
         '63.16%', '73.68%'],
        ['Lanús', 'Lanús', 'Won', '11', '12', None, None, None],
        ['Lanús', 'Lanús', 'Lost', '4', '5', None, None, None],
        ['Lanús', 'Lanús', 'Drawn', '4', '2', None, None, None],
        ['Lanús', 'Lanús', 'Efectivity', '57.89%', '63.16%', None, None,
         None],
        ['Mendoza', 'Godoy Cruz', 'Won', None, None, None, '11', '7'],
        ['Mendoza', 'Godoy Cruz', 'Lost', None, None, None, '3', '4'],
        ['Mendoza', 'Godoy Cruz', 'Drawn', None, None, None, '4', '8'],
        ['Mendoza', 'Godoy Cruz', 'Efectivity', None, None, None, '61.11%',
         '36.84%'],
        ['Rosario', "Newell's Old Boys", 'Won', '8', None, '12', None,
         None],
        ['Rosario', "Newell's Old Boys", 'Lost', '4', None, '4', None,
         None],
        ['Rosario', "Newell's Old Boys", 'Drawn', '7', None, '3', None,
         None],
        ['Rosario', "Newell's Old Boys", 'Efectivity', '42.11%', None,
         '63.16%', None, None],
        ['Santa Fé', 'Colón', 'Won', None, '10', '10', None, None],
        ['Santa Fé', 'Colón', 'Lost', None, '5', '5', None, None],
        ['Santa Fé', 'Colón', 'Drawn', None, '4', '4', None, None],
         ['Santa Fé', 'Colón', 'Efectivity', None, '52.63%', '52.63%',
          None, None],
         ['Sarandí', 'Arsenal', 'Won', None, None, None, None, '9'],
         ['Sarandí', 'Arsenal', 'Lost', None, None, None, None, '5'],
         ['Sarandí', 'Arsenal', 'Drawn', None, None, None, None, '5'],
         ['Sarandí', 'Arsenal', 'Efectivity', None, None, None, None,
          '47.37%'],
         ['Tigre', 'Tigre', 'Won', '12', None, None, None, None],
         ['Tigre', 'Tigre', 'Lost', '4', None, None, None, None],
         ['Tigre', 'Tigre', 'Drawn', '3', None, None, None, None],
         ['Tigre', 'Tigre', 'Efectivity', '63.16%', None, None, None,
          None]]
        for i in enumerate(all1): 
            eq_(i[1], all2[i[0]])

class TestPivot_D(object):

    pt = PivotTable()
    pt.rows = [
        GenericObject(**{'distro':'Ubuntu', 'page_hits':2075, 'releases':13}),
        GenericObject(**{'distro':'Mint', 'page_hits':1547, 'releases':12}),
        GenericObject(**{'distro':'Fedora', 'page_hits':1460, 'releases':14}),
        GenericObject(**{'distro':'Debian', 'page_hits':1143, 'releases':10}),
        GenericObject(**{'distro':'OpenSuse', 'page_hits':1135, 'releases':26})
    ]

    def test_DA_data(self):
        assert_raises(PivotTableError, getattr, self.pt, 'headers')
        self.pt.xaxis = "distro"
        assert_raises(PivotTableError, getattr, self.pt, 'headers')
        self.pt.yaxis = [
            {'attr':'page_hits', 'label':'Page Hits', 'aggr':Sum},
            {'attr':'releases', 'label':'Releases', 'aggr':Sum}]
        self.pt.xaxis_sort = False
        self.pt.yaxis_order = None
        assert_raises(TypeError, getattr, self.pt, 'result')
        del self.pt.yaxis_order
        self.pt.yaxis.append(
            {'attr':'distro', 'label':'Distro', 'aggr':GroupBy})
        self.pt.headers
        all_ = [a for a in self.pt.result]
