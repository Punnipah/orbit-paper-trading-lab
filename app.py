import streamlit as st
import random
import csv
import io
st.set_page_config(page_title="Orbit Paper Lab",layout="centered")
st.title("Orbit Paper Lab")
st.caption("Fictional data only • educational simulation • no real market connection")
s=st.session_state
if "day" not in s:
    s.day=0
    s.cash=1000.0
    s.units=0
    s.log=[]
    s.history=[1000.0]
rng=random.Random(42)
prices=[100.0]
for i in range(199):
    prices.append(round(max(10,prices[-1]+rng.gauss(0,3)),2))
p=prices[s.day]
st.metric("Fictional price",f"{p:.2f}")
st.line_chart(prices[:s.day+1])
a,b=st.columns(2)
a.metric("Virtual cash",f"{s.cash:.2f}")
b.metric("Virtual units",s.units)
st.metric("Simulated total",f"{s.cash+s.units*p:.2f}")
fee=0.002
if st.button("Simulate purchase of one unit",disabled=s.cash<p*(1+fee)):
    s.cash-=p*(1+fee)
    s.units+=1
    s.log.append([s.day,"Purchase",p,p*fee])
    st.rerun()
if st.button("Simulate sale of one unit",disabled=s.units==0):
    s.cash+=p*(1-fee)
    s.units-=1
    s.log.append([s.day,"Sale",p,p*fee])
    st.rerun()
if st.button("Next simulated day",disabled=s.day>=199):
    s.day+=1
    s.history.append(s.cash+s.units*prices[s.day])
    st.rerun()
st.line_chart(s.history)
st.caption("Fictional results cannot predict future returns.")
if s.log:
    st.dataframe([dict(day=r[0],action=r[1],price=r[2],fee=r[3]) for r in s.log])
    out=io.StringIO()
    w=csv.writer(out)
    w.writerow(["day","action","price","fee"])
    w.writerows(s.log)
    st.download_button("Export CSV",out.getvalue(),"experiment.csv","text/csv")
if st.button("Reset"):
    for k in ["day","cash","units","log","history"]:
        del s[k]
    st.rerun()
