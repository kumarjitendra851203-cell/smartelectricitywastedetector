"""Smart Energy Analyzer - Streamlit dashboard.  Run:  streamlit run app.py"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from src import data_manager as dm, analysis as an
from src.tariff_calculator import Tariff, estimate_bill, DISCLAIMER

st.set_page_config(page_title="Smart Energy Analyzer", page_icon="⚡", layout="wide")
TEAL, RED, GREY = "#0f766e", "#dc2626", "#94a3b8"


def chart(w=11, h=3.6):
    f, ax = plt.subplots(figsize=(w, h))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25)
    return f, ax


def show(f):
    f.tight_layout(); st.pyplot(f); plt.close(f)


@st.cache_data(show_spinner=False)
def load_upload(raw: bytes):
    return dm.validate_dataframe(pd.read_csv(io.BytesIO(raw), comment="#"))


@st.cache_data(show_spinner=False)
def load_sample():
    df, events = dm.generate_sample()
    return df, events


# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("⚡ Energy Analyzer")
    source = st.radio("Data source", ["Demo data (hostel)", "Upload my CSV"])
    events, invalid = [], []
    df = None
    try:
        if source.startswith("Demo"):
            df, events = load_sample()
            st.caption("Synthetic demo data - real meter data nahi hai.")
        else:
            up = st.file_uploader("CSV file", type="csv")
            st.caption("Columns: timestamp, property_id, property_type, consumption_kwh (kWh, kW nahi)")
            if up:
                df, invalid = load_upload(up.getvalue())
    except dm.DataError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"CSV read nahi ho paayi: {e}")

    st.divider()
    st.subheader("💰 Tariff")
    cur = st.text_input("Currency", "₹")
    model = st.radio("Model", ["Flat rate", "Tiered slabs"], horizontal=True)
    fixed = st.number_input("Fixed monthly charge", 0.0, value=0.0, step=50.0)
    extra = st.number_input("Taxes / surcharge (%)", 0.0, value=0.0, step=1.0)
    if model == "Flat rate":
        tariff = Tariff(currency=cur, price_per_kwh=st.number_input("Price per kWh", 0.0, value=6.0, step=0.5),
                        fixed_monthly_charge=fixed, additional_percent=extra)
    else:
        a, b = st.columns(2)
        u1 = a.number_input("Slab 1 up to (kWh)", 1.0, value=1000.0); r1 = b.number_input("Rate 1", 0.0, value=4.0)
        u2 = a.number_input("Slab 2 up to (kWh)", 1.0, value=3000.0); r2 = b.number_input("Rate 2", 0.0, value=5.5)
        r3 = st.number_input("Rate above slab 2", 0.0, value=7.0)
        tariff = Tariff(currency=cur, tiers=[{"upto": u1, "rate": r1}, {"upto": u2, "rate": r2},
                                             {"upto": None, "rate": r3}],
                        fixed_monthly_charge=fixed, additional_percent=extra)
    st.caption(f"Engine: **{an.ENGINE}**")

# ---------------- Main ----------------
st.title("Smart Energy Analyzer")
st.caption("Consumption analysis · anomaly detection · forecast · bill prediction")

if df is None:
    st.info("👈 Sidebar se demo data chuno ya apni CSV upload karo.")
    st.stop()

props = sorted(df["property_id"].unique())
c1, c2 = st.columns([1, 2])
prop = c1.selectbox("Property", props)
d = df[df["property_id"] == prop]
lo, hi = d["timestamp"].min().date(), d["timestamp"].max().date()
rng = c2.date_input("Date range", (lo, hi), min_value=lo, max_value=hi)
if len(rng) == 2:
    d = d[(d["timestamp"].dt.date >= rng[0]) & (d["timestamp"].dt.date <= rng[1])]
if d.empty:
    st.warning("Is range me data nahi hai."); st.stop()

daily = dm.daily_totals(d)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🚨 Anomalies", "🔮 Forecast & Bill", "🧹 Data quality"])

# ---- Overview
with tab1:
    last30 = daily[daily["date"] > daily["date"].max() - pd.Timedelta(days=30)]["kwh"].sum()
    hourly = d.groupby(d["timestamp"].dt.hour)["consumption_kwh"].mean()
    m = st.columns(4)
    m[0].metric("Total consumption", f"{d.consumption_kwh.sum():,.0f} kWh")
    m[1].metric("Avg per day", f"{daily.kwh.mean():,.1f} kWh")
    m[2].metric("Peak hour (avg)", f"{hourly.idxmax():02d}:00")
    try:
        m[3].metric("Bill, last 30 days", f"{cur}{estimate_bill(last30, tariff)['total']:,.0f}")
    except ValueError as e:
        m[3].error(str(e))
    f, ax = chart(); ax.bar(daily["date"], daily["kwh"], color=TEAL, width=0.8)
    ax.set_title("Daily consumption (kWh)"); ax.set_ylabel("kWh"); show(f)
    a, b = st.columns(2)
    with a:
        f, ax = chart(5.4, 3.4); ax.plot(hourly.index, hourly.values, marker="o", color=TEAL)
        ax.set_title("Average hourly profile"); ax.set_xlabel("Hour of day"); ax.set_ylabel("kWh"); show(f)
    with b:
        piv = d.assign(h=d.timestamp.dt.hour, w=d.timestamp.dt.dayofweek).pivot_table(
            index="w", columns="h", values="consumption_kwh")
        f, ax = plt.subplots(figsize=(5.4, 3.4)); im = ax.imshow(piv.values, aspect="auto", cmap="YlGnBu")
        ax.set_yticks(range(len(piv.index))); ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][:len(piv.index)] if len(piv.index) == 7 else piv.index)
        ax.set_xlabel("Hour of day"); ax.set_title("Weekday × hour heatmap"); f.colorbar(im, ax=ax); show(f)

# ---- Anomalies
with tab2:
    a, b = st.columns(2)
    method = a.radio("Method", ["Rolling z-score (C++ engine)", "Isolation Forest (ML)"], horizontal=True)
    if method.startswith("Rolling"):
        thr = b.slider("Sensitivity: z-threshold (kam = zyada alerts)", 2.0, 8.0, 4.0, 0.5)
        res = an.detect_anomalies(d, "zscore", threshold=thr)
    else:
        cont = b.slider("Expected anomaly share (%)", 0.1, 5.0, 0.5, 0.1)
        res = an.detect_anomalies(d, "iforest", contamination=cont / 100)
    ev = an.group_events(res)
    rate = tariff.tiers[-1]["rate"] if tariff.tiers else tariff.price_per_kwh
    hi_ev = ev[ev["type"] == "High usage"]
    m = st.columns(3)
    m[0].metric("Events found", len(ev))
    m[1].metric("Extra energy (high events)", f"{hi_ev.extra_kwh.sum():,.1f} kWh")
    m[2].metric("Approx. extra cost", f"{cur}{hi_ev.extra_kwh.sum() * rate:,.0f}")
    f, ax = chart(11, 3.8)
    ax.plot(res["timestamp"], res["consumption_kwh"], color=GREY, lw=0.8, label="Hourly kWh")
    pts = res[res["is_anomaly"]]
    ax.scatter(pts["timestamp"], pts["consumption_kwh"], color=RED, s=18, zorder=3, label="Anomaly")
    ax.set_ylabel("kWh"); ax.legend(loc="upper right"); show(f)
    if ev.empty:
        st.success("Koi anomaly nahi mili.")
    else:
        st.dataframe(ev, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Download events CSV", ev.to_csv(index=False), "anomaly_events.csv", "text/csv")
    if events and source.startswith("Demo"):
        with st.expander("Demo data ke known (synthetic) events - match karke dekho"):
            st.dataframe(pd.DataFrame(events), hide_index=True, use_container_width=True)

# ---- Forecast & Bill
with tab3:
    horizon = st.slider("Forecast days", 7, 60, 30)
    try:
        hist, fc = an.forecast_daily(daily, horizon)
        f, ax = chart(); ax.plot(hist["date"], hist["kwh"], color=TEAL, label="Actual")
        ax.plot(fc["date"], fc["kwh"], color="#f59e0b", label="Forecast")
        ax.fill_between(fc["date"], fc["low"], fc["high"], color="#f59e0b", alpha=0.2, label="95% range")
        ax.set_ylabel("kWh / day"); ax.legend(); show(f)
        month = fc.head(30)
        pred_kwh, prev_kwh = month["kwh"].sum(), last30
        try:
            pb, ob = estimate_bill(pred_kwh, tariff), estimate_bill(prev_kwh, tariff)
            m = st.columns(3)
            m[0].metric("Predicted next 30 days", f"{pred_kwh:,.0f} kWh", f"{pred_kwh - prev_kwh:+,.0f} vs last 30d", delta_color="inverse")
            m[1].metric("Predicted bill", f"{cur}{pb['total']:,.0f}", f"{pb['total'] - ob['total']:+,.0f} vs last 30d", delta_color="inverse")
            m[2].metric("Likely range", f"{cur}{estimate_bill(month['low'].sum(), tariff)['total']:,.0f} - "
                                         f"{cur}{estimate_bill(month['high'].sum(), tariff)['total']:,.0f}")
            st.table(pd.DataFrame({"Item": ["Energy charge", "Fixed charge", "Taxes / surcharge", "Total"],
                                   f"Amount ({cur})": [round(pb[k], 2) for k in ("energy_charge", "fixed_charge", "additional_charge", "total")]}))
        except ValueError as e:
            st.error(f"Tariff problem: {e}")
        st.download_button("⬇️ Download forecast CSV", fc.round(2).to_csv(index=False), "forecast.csv", "text/csv")
    except ValueError as e:
        st.warning(str(e))
    st.caption(DISCLAIMER)

# ---- Data quality
with tab4:
    m = st.columns(3)
    m[0].metric("Valid rows", f"{len(df):,}"); m[1].metric("Rejected rows", len(invalid))
    m[2].metric("Incomplete days", int((daily["readings"] < daily["readings"].max()).sum()))
    if invalid:
        st.dataframe(pd.DataFrame(invalid), hide_index=True, use_container_width=True)
    else:
        st.success("Koi invalid row nahi.")
    st.caption("Missing days ko zero nahi maana jaata; rows silently fix nahi hoti.")
    if source.startswith("Demo"):
        st.download_button("⬇️ Sample CSV (apne data ka format dekhne ke liye)", df.to_csv(index=False),
                           "sample_electricity.csv", "text/csv")
