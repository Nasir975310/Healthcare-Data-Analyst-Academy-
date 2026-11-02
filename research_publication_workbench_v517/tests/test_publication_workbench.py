import importlib.util
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pub",ROOT/"scripts"/"publication_workbench.py")
pub=importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
DATA=ROOT/"data"/"synthetic_publication_dataset.csv"

def test_table1_build_and_tests():
    df=pd.read_csv(DATA)
    t,groups=pub.build_table1(df,"arm",["age","bmi"],["sex","diabetes"])
    t=pub.add_group_tests(df,t,"arm",["age","bmi"],["sex","diabetes"])
    assert groups==["intervention","control"]
    assert set(["variable","intervention","control","p_value"]).issubset(t.columns)
    assert t.loc[t.variable=="age","p_value"].iloc[0]!=""

def test_consort_count_validation():
    svg=pub.consort_svg(80,40,40,38,39,35,36,36,37)
    assert "<svg" in svg and "Allocated to intervention: 40" in svg
    try: pub.consort_svg(10,8,8,8,8,8,8,8,8)
    except ValueError: pass
    else: raise AssertionError("Allocated count cannot exceed enrolled")

def test_prisma_count_validation():
    svg=pub.prisma_svg(500,80,420,350,70,25,45)
    assert "Studies included" in svg
    try: pub.prisma_svg(100,20,90,95,10,1,5)
    except ValueError: pass
    else: raise AssertionError("Inconsistent stage counts must fail")

def test_ris_import_and_bibliography(tmp_path):
    refs=pub.parse_ris(ROOT/"data"/"sample_references.ris")
    rows=pub.write_bibliography(refs,tmp_path)
    assert len(rows)==2
    assert (tmp_path/"references.csv").exists()
    assert (tmp_path/"references.bib").exists()

def test_ris_parser_and_escaping():
    refs=pub.parse_ris(ROOT/"data"/"sample_references.ris")
    assert refs[0]["DO"][0]=="10.0000/example.2024.001"
    assert pub.esc("<unsafe & text>")=="&lt;unsafe &amp; text&gt;"
