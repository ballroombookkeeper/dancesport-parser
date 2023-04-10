from datetime import date
from typing import Callable, List

from dancesport_parser.o2cm.model import Competition
from dancesport_parser.o2cm.parser import parseMain
from dancesport_parser.util import parseHtml

MAIN_RESULTS_PAGE1 = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<HTML  xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<HEAD>
   <title>O2CM Results List</title>
   <link rel='stylesheet' href='compdb.css'>
    <style type="text/css">
    </style>
	</HEAD>
<BODY bgcolor="#FFFFFF"  text="#000000" link="#0000CC" vlink="#CC0000" alink="#0000CC" class="t1n"  onresize="ReSize();">
	    <table name="main_tbl" id="main_tbl" style="max-width:520px">
        <tr><td width=50></td><td></td></tr>
            <tr><td colspan="2">
            <form name=FilterList action="default.asp" method=post>
                <h2>O<sup>2</sup>CM Results Search</h2>
                Enter the Year and Month of the Event for which you wish to find results<br />
                Year:&nbsp;<input type="number" id="inyear" name="inyear" maxlength="4" value="2023" min="2005" max="2023" style="WIDTH: 60px;" /> 
                Month:&nbsp;<input type="number" id="inmonth" name="inmonth" length="2" value="4" min="1" max="12" style="WIDTH: 30px;" /> 
                &nbsp;then click -> <input type=submit value="Go" name="Go" /><br /><br />
            </form>
            <form name="IndivSearch" action="individual.asp" method="post">
                OR Enter competitor First and Last name and click Search to find individual results<br /></br>
                First:&nbsp;<input id="szFirst" name="szFirst" style="WIDTH: 100px;" /> 
                Last:&nbsp;<input id="szLast" name="szLast" style="WIDTH: 100px;" /> 
                &nbsp;<input type="submit" value="Search" name="Search"  /><br /><br />
            </form>
            </td></tr>
			<tr> <td colspan=2 class=h3 align=center>2023</td> </tr>
			    <tr class=t1n><td>Apr 08</td><td><a href='event3.asp?event=ndc23&bclr=#FFFFFF&tclr=#000000' target=_blank>Northwestern DanceSport Classic</td></tr>
			    <tr class=t1n><td>Apr 08</td><td><a href='event3.asp?event=bcb23&bclr=#FFFFFF&tclr=#000000' target=_blank>Berkeley Classic Ballroom Competition</td></tr>
			    <tr class=t1n><td>Apr 08</td><td><a href='event3.asp?event=fdf23a&bclr=#FFFFFF&tclr=#000000' target=_blank>April Dance Fest</td></tr>
			    <tr class=t1n><td>Jan 14</td><td><a href='event3.asp?event=mac23&bclr=#FFFFFF&tclr=#000000' target=_blank>The MAC (NQE)</td></tr>
			<tr> <td colspan=2 class=h3 align=center>2022</td> </tr>
			    <tr class=t1n><td>Dec 10</td><td><a href='event3.asp?event=big22&bclr=#FFFFFF&tclr=#000000' target=_blank>Big Apple Dancesport Challenge</td></tr>
			    <tr class=t1n><td>Dec 03</td><td><a href='event3.asp?event=pbd22&bclr=#FFFFFF&tclr=#000000' target=_blank>Princeton Ballroom Competition 2022</td></tr>
        </table>
<div colspan=4 style="font-size:8pt">hosted at AWS</div>
</BODY>
</HTML>
"""

def test_o2cm_parser_dom() -> None:
    # Setup
    dom = parseHtml(MAIN_RESULTS_PAGE1)

    # Execute
    results = parseMain(dom)

    # Verify
    o2cm_parser_assertion_helper(results)


def test_o2cm_parser_raw() -> None:
    # Execute
    results = parseMain(rawHtml=MAIN_RESULTS_PAGE1)

    # Verify
    o2cm_parser_assertion_helper(results)


def o2cm_parser_assertion_helper(results: List[Competition]) -> None:
    competitionSorter: Callable[[Competition, ], str] = lambda comp: comp.id
    results.sort(key=competitionSorter)
    assert len(results) == 6
    assert results[0].id == "bcb23"
    assert results[0].date == date(2023, 4, 8)
    assert results[0].name == "Berkeley Classic Ballroom Competition"
    assert results[1].id == "big22"
    assert results[1].date == date(2022, 12, 10)
    assert results[1].name == "Big Apple Dancesport Challenge"
