import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from loader import load_all_data
from map_utils import add_pixel_coordinates
from config import MAP_CONFIG, HEATMAP_CONFIG

st.set_page_config(page_title="LILA BLACK - Player Journey Viewer", layout="wide")
# st.title("LILA BLACK - Player Journey Viewer")

# st.write("Version", st.__version__)
# st.write("Has rerun", hasattr(st, "rerun"))
# st.write("Has experimental_rerun", hasattr(st, "experimental_rerun"))


@st.cache_data
def load_dataset():
    df = load_all_data("player_data")
    df = add_pixel_coordinates(df)
    return df


@st.cache_data
def load_map_image(map_id):
    img = Image.open(MAP_CONFIG[map_id]["image"])
    img_width, img_height = img.size
    img_array = np.array(img)

    return img_array, img_width, img_height


@st.cache_resource
def create_base_figure(map_id):
    img_array, _, _ = load_map_image(map_id)

    fig = px.imshow(img_array)

    fig.update_xaxes(visible=False)

    fig.update_yaxes(visible=False, scaleanchor="x")

    fig.update_layout(
        width=800,
        height=800,
        # autosize=False,
        margin=dict(l=0, r=0, t=0, b=0),
        dragmode="pan",
        coloraxis_showscale=False,
    )

    return fig


df = load_dataset()

# storm_events = df[df["event"].str.contains("storm", case=False, na=False)]
# st.write("Storm events:", len(storm_events))
# if len(storm_events):
#     st.write(storm_events["event"].value_counts())


if "mode" not in st.session_state:
    st.session_state["mode"] = "Journey"

if "selected_player" not in st.session_state:
    st.session_state["selected_player"] = "All"

if "heatmap_type" not in st.session_state:
    st.session_state["heatmap_type"] = "High Traffic"

if "playback_pct" not in st.session_state:
    st.session_state["playback_pct"] = 100

if "mode" not in st.session_state:
    st.session_state["mode"] = "Journey"

left_panel, center_panel, right_panel = st.columns([1.2, 4, 1.2])

with left_panel:
    # st.subheader("Select Match")

    maps = ["All"] + sorted(df["map_id"].unique())

    selected_map = st.selectbox("Map", maps)

    heatmap_btn = st.button(
        "Heatmap",
        type="primary",
        use_container_width=True,
        disabled=(selected_map == "All"),
    )

    if heatmap_btn:
        st.session_state["mode"] = "Heatmap"
        st.session_state["journey_loaded"] = True

    dates = ["All"] + sorted(df["date"].unique())

    selected_date = st.selectbox("Date", dates)

    if selected_date == "All":
        date_df = df
    else:
        date_df = df[df["date"] == selected_date]

    if selected_map == "All":
        map_df = date_df
    else:
        map_df = date_df[date_df["map_id"] == selected_map]

    match_summary = (
        map_df.groupby("match_id")
        .agg(players=("user_id", "nunique"), map_id=("map_id", "first"))
        .reset_index()
    )

    match_summary["short_id"] = match_summary["match_id"].str[:8]

    match_summary["label"] = (
        match_summary["map_id"]
        + " | Players: "
        + match_summary["players"].astype(str)
        + " | "
        + match_summary["short_id"]
    )

    selected_label = st.selectbox("Match", match_summary["label"])
    selected_match = match_summary.loc[
        match_summary["label"] == selected_label, "match_id"
    ].iloc[0]

    match_df = map_df[map_df["match_id"] == selected_match].copy()

    # st.write(match_df["event"].value_counts())

    selection_key = (selected_date, selected_map, selected_match)

    if selection_key != st.session_state.get("selection_key"):
        st.session_state["journey_loaded"] = False
        st.session_state["selection_key"] = selection_key

    journey_btn = st.button("Journey", type="primary", use_container_width=True)

    if journey_btn:
        st.session_state["mode"] = "Journey"
        st.session_state["journey_loaded"] = True

    st.markdown("---")
    st.subheader("Journey Legend")

    st.markdown("🟩 Human")
    st.markdown("🟧 Bot")
    # st.markdown("🟢 Start Position")
    # st.markdown("🟥 End Position")
    st.markdown("🟨 Loot")
    st.markdown("❌ Kill Location")
    st.markdown("🔴 Death Location")
    st.markdown("⭐ Storm Death")


with right_panel:
    if st.session_state.get("journey_loaded", False):
        view_mode = st.session_state["mode"]

        show_humans = True
        show_bots = True
        show_loot = True
        show_kills = True

        if view_mode == "Journey":
            player_options = ["All"]

            for user_id in sorted(match_df["user_id"].unique()):
                player_options.append(str(user_id))

            selected_player = st.selectbox(
                "Player", player_options, key="selected_player"
            )

            show_humans = st.checkbox("Humans", True, key="show_humans")
            show_bots = st.checkbox("Bots", True, key="show_bots")
            show_loot = st.checkbox("Loot", True, key="show_loot")
            show_kills = st.checkbox("Kills", True, key="show_kills")

            playback_pct = st.session_state.get("playback_pct", 100)

            st.markdown("---")
            st.subheader(f"Playback ({playback_pct}%)")

            playback_pct = st.slider(
                "Playback Progress",
                min_value=0,
                max_value=100,
                value=st.session_state.playback_pct,
                step=1,
                label_visibility="collapsed",
            )

            st.session_state.playback_pct = playback_pct

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                if st.button("⏮", use_container_width=True):
                    st.session_state.playback_pct = 0
                    # st.experimental_rerun()
                    st.rerun()

            with c2:
                if st.button("◀", use_container_width=True):
                    st.session_state.playback_pct = max(
                        0, st.session_state.playback_pct - 1
                    )
                    # st.experimental_rerun()
                    st.rerun()

            with c3:
                if st.button("▶", use_container_width=True):
                    st.session_state.playback_pct = min(
                        100, st.session_state.playback_pct + 1
                    )
                    # st.experimental_rerun()
                    st.rerun()

            with c4:
                if st.button("⏭", use_container_width=True):
                    st.session_state.playback_pct = 100
                    # st.experimental_rerun()
                    st.rerun()

            st.markdown("---")
            st.subheader("Match Stats")

            tracked_players = match_df["user_id"].nunique()
            loot_count = len(match_df[match_df["event"] == "Loot"])
            kill_count = len(match_df[match_df["event"].isin(["Kill", "BotKill"])])
            death_count = len(match_df[match_df["event"].isin(["Killed", "BotKilled"])])
            storm_count = len(match_df[match_df["event"] == "KilledByStorm"])

            c1, c2, c3 = st.columns(3)
            c1.metric("Players", tracked_players)
            c2.metric("Loot", loot_count)
            c3.metric("Kills", kill_count)

            c4, c5, c6 = st.columns(3)
            c4.metric("Deaths", death_count)
            c5.metric("Storm", storm_count)

        elif view_mode == "Heatmap":

            heatmap_type = st.selectbox(
                "Heatmap Type",
                ["High Traffic", "Kill Zones", "Death Zones"],
                key="heatmap_type",
            )


with center_panel:
    if st.session_state.get("journey_loaded", False):
        map_id = match_df["map_id"].iloc[0]

        img_array, img_width, img_height = load_map_image(map_id)

        fig = go.Figure(create_base_figure(map_id))

        view_mode = st.session_state["mode"]

        movement_events = ["Position", "BotPosition"]
        movement_df = match_df[match_df["event"].isin(movement_events)]

        # st.write("Movement rows", len(movement_df))
        # st.write("Unique ts", movement_df["ts"].nunique())
        # st.write(movement_df["ts"].sort_values().head(10))
        # st.write(movement_df["ts"].sort_values().tail(10))
        # st.write(movement_df["ts"].astype("int64").head())

        # raw_ts = movement_df["ts"].astype("int64")

        # st.write("Min", raw_ts.min())
        # st.write("Max", raw_ts.max())
        # st.write("Duration ns", raw_ts.max() - raw_ts.min())
        # st.write("Duration sec", (raw_ts.max() - raw_ts.min()) / 1e9)

        # ts_ms = movement_df["ts"].astype("int64") // 1_000_000
        # st.write("Min ms", ts_ms.min())
        # st.write("Max ms", ts_ms.max())
        # st.write("Duration ms", ts_ms.max() - ts_ms.min())

        selected_player = st.session_state["selected_player"]
        if selected_player != "All":
            movement_df = movement_df[
                movement_df["user_id"].astype(str) == selected_player
            ]

        if not show_humans:
            movement_df = movement_df[movement_df["is_bot"]]

        if not show_bots:
            movement_df = movement_df[~movement_df["is_bot"]]

        min_ts = movement_df["ts"].min()
        max_ts = movement_df["ts"].max()

        ts_ms = movement_df["ts"].astype("int64") // 1_000_000

        relative_ms = ts_ms - ts_ms.min()
        duration_ms = relative_ms.max()

        playback_pct = st.session_state["playback_pct"]
        playback_cutoff = duration_ms * playback_pct / 100

        playback_df = movement_df[relative_ms <= playback_cutoff]

        # match_duration = max_ts - min_ts
        # match_duration_seconds = match_duration.total_seconds()
        # st.write(movement_df["ts"].dtype)
        # st.write("Min", min_ts)
        # st.write("Max", max_ts)
        # st.write("Duration", match_duration)
        # st.write("Seconds", match_duration_seconds)
        # st.write(movement_df["ts"].head())

        heatmap_type = st.session_state["heatmap_type"]

        if view_mode == "Heatmap":
            map_heatmap_df = df[df["map_id"] == map_id]

            if heatmap_type == "High Traffic":
                heatmap_df = map_heatmap_df[
                    map_heatmap_df["event"].isin(["Position", "BotPosition"])
                ]

            elif heatmap_type == "Kill Zones":

                heatmap_df = map_heatmap_df[
                    map_heatmap_df["event"].isin(["Kill", "BotKill"])
                ]

            elif heatmap_type == "Death Zones":

                heatmap_df = map_heatmap_df[
                    map_heatmap_df["event"].isin(
                        ["Killed", "BotKilled", "KilledByStorm"]
                    )
                ]

            x = heatmap_df["pixel_x"].values
            y = heatmap_df["pixel_y"].values

            if len(x) < 2:
                st.caption(
                    f"Only {len(x)} event(s) available for {heatmap_type.lower()}."
                )
            else:
                config = HEATMAP_CONFIG.get(map_id, {}).get(heatmap_type, {})

                heatmap_size = config.get("size", 5)
                heatmap_color = config.get("color", "red")
                heatmap_opacity = config.get("opacity", 0.05)
                heatmap_symbol = config.get("symbol", "circle")

                fig.add_trace(
                    go.Scattergl(
                        x=x,
                        y=y,
                        mode="markers",
                        marker=dict(
                            size=heatmap_size,
                            color=heatmap_color,
                            opacity=heatmap_opacity,
                            symbol=heatmap_symbol,
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

        elif view_mode == "Journey":
            st.markdown(
                f"<h3 style='text-align:center;'>Match Id : {selected_match[:-9]}</h3>",
                unsafe_allow_html=True,
            )

            for user_id, player_df in playback_df.groupby("user_id"):
                player_df = player_df.sort_values("ts")

                start = player_df.iloc[0]
                end = player_df.iloc[-1]
                is_bot = player_df["is_bot"].iloc[0]

                # color = "orange" if is_bot else "deepskyblue"
                color = "lightsalmon" if is_bot else "lightgreen"
                width = 1 if is_bot else 2

                # Player/Bot Journey Path
                fig.add_trace(
                    go.Scatter(
                        x=player_df["pixel_x"],
                        y=player_df["pixel_y"],
                        mode="markers+lines",
                        marker=dict(size=4),
                        line=dict(color=color, width=width),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

                if is_bot:
                    start_color = "darkorange"
                    end_color = "darkorange"
                else:
                    start_color = "lime"
                    end_color = "lime"

                # Journey Start
                fig.add_trace(
                    go.Scatter(
                        x=[start["pixel_x"]],
                        y=[start["pixel_y"]],
                        mode="markers",
                        marker=dict(size=12, color=start_color, symbol="circle"),
                        hovertext=f"START<br>{user_id}",
                        hoverinfo="text",
                        showlegend=False,
                    )
                )

                # Journey End
                fig.add_trace(
                    go.Scatter(
                        x=[end["pixel_x"]],
                        y=[end["pixel_y"]],
                        mode="markers",
                        marker=dict(size=12, color=end_color, symbol="square"),
                        hovertext=f"END<br>{user_id}",
                        hoverinfo="text",
                        showlegend=False,
                    )
                )

            # Event Markers
            event_config = {
                "Loot": {"color": "yellow", "symbol": "diamond"},
                "Kill": {"color": "red", "symbol": "x"},
                "BotKill": {"color": "red", "symbol": "x"},
                "Killed": {"color": "darkred", "symbol": "circle"},
                "BotKilled": {"color": "darkred", "symbol": "circle"},
                "KilledByStorm": {"color": "purple", "symbol": "star"},
            }

            visible_events = []

            if show_loot:
                visible_events.append("Loot")

            if show_kills:
                visible_events.extend(
                    ["Kill", "BotKill", "Killed", "BotKilled", "KilledByStorm"]
                )

            events_df = match_df[match_df["event"].isin(visible_events)].copy()
            events_ts_ms = events_df["ts"].astype("int64") // 1_000_000
            events_relative_ms = events_ts_ms - ts_ms.min()
            events_df = events_df[events_relative_ms <= playback_cutoff]

            for event_name, event_df in events_df.groupby("event"):

                cfg = event_config[event_name]

                fig.add_trace(
                    go.Scatter(
                        x=event_df["pixel_x"],
                        y=event_df["pixel_y"],
                        mode="markers",
                        marker=dict(size=9, color=cfg["color"], symbol=cfg["symbol"]),
                        hovertext=event_df.apply(
                            lambda x: f"""
                            Event : {x['event']}
                            User : {x['user_id']}
                            """,
                            axis=1,
                        ),
                        hoverinfo="text",
                        showlegend=False,
                    )
                )

        st.plotly_chart(fig, use_container_width=True)
