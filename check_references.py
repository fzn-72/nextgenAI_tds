"""Verification independante des 20 references : recalcul en Python pur sur les CSV (sans SQL),
puis comparaison avec la requete SQL et la valeur de reference-td1.csv."""
import csv, sqlite3, sys
from datetime import datetime
kit, ref_path = sys.argv[1], sys.argv[2]
price = {r["product_id"]: int(r["price"]) for r in csv.DictReader(open(f"{kit}/data/product.csv", encoding="utf-8"))}
birth = {r["customer_id"]: r["birth_date"] for r in csv.DictReader(open(f"{kit}/data/customers.csv", encoding="utf-8"))}
orders = list(csv.DictReader(open(f"{kit}/data/orders.csv", encoding="utf-8")))

def age(b, on):  # age revolu : annees, moins 1 si l'anniversaire (mois, jour) n'est pas encore passe
    by, bm, bd = map(int, b[:10].split("-")); y, m, d = map(int, on[:10].split("-"))
    return y - by - ((m, d) < (bm, bd))

def rev(start=None, end=None, prods=None, ref_date=None, age_at_order=False):
    t = 0
    for o in orders:
        if start and not (datetime.fromisoformat(start) <= datetime.fromisoformat(o["date"]) < datetime.fromisoformat(end)): continue
        if prods and o["product_id"] not in prods: continue
        if ref_date and age(birth[o["customer_id"]], ref_date) != 25: continue
        if age_at_order and age(birth[o["customer_id"]], o["date"]) != 25: continue
        t += int(o["quantity_product"]) * price[o["product_id"]]
    return t

P = lambda a, b: dict(start=f"{a} 00:00:00", end=f"{b} 00:00:00")
spec = {
 "C01": rev(**P("2026-03-01","2026-06-01")),
 "C02": rev(ref_date="2026-09-25"),
 "C03": rev(prods="abc", **P("2026-01-01","2026-07-01")),
 "C04": rev(**P("2026-01-01","2026-10-01")),
 "C05": rev(**P("2026-06-01","2026-06-02")),
 "C06": rev(**P("2025-01-01","2026-01-01")),
 "C07": rev(**P("2026-05-31","2026-06-01")),
 "C08": rev(ref_date="2026-09-24"),
 "C09": rev(ref_date="2026-09-26"),
 "C10": rev(age_at_order=True),
 "C11": rev(ref_date="2026-12-01"),
 "C12": rev(prods="abc"),
 "C13": rev(prods="ac", **P("2026-04-01","2026-05-01")),
 "C14": rev(prods="abc", **P("2026-10-01","2026-12-01")),
 "C15": rev(ref_date="2026-09-25", **P("2026-03-01","2026-06-01")),
 "C16": rev(prods="abc", ref_date="2026-09-25"),
 "C17": rev(prods="abc", ref_date="2026-09-25", **P("2026-01-01","2026-07-01")),
 "C18": rev(age_at_order=True, **P("2026-05-01","2026-06-01")),
 "C19": rev(prods="d", ref_date="2026-09-25", **P("2026-09-01","2026-10-01")),
 "C20": rev(**P("2026-06-01","2026-09-01")),
}
con = sqlite3.connect(f"file:{kit}/data/boutique.sqlite?mode=ro", uri=True); con.execute("PRAGMA query_only=1")
ok = 0
print("case | valeur CSV | SQL executee | python independant | verdict")
for r in csv.DictReader(open(ref_path, encoding="utf-8")):
    v_sql = con.execute(r["sql"]).fetchone()[0]
    good = int(r["revenue_cents"]) == v_sql == spec[r["case_id"]]
    ok += good
    print(r["case_id"], r["revenue_cents"], v_sql, spec[r["case_id"]], "OK" if good else "ECART", sep=" | ")
print(f"{ok}/20 references concordantes")
