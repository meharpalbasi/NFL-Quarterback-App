#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.graph_objects as go
import nfl_data_py as nfl
import streamlit as st


# In[2]:


df_2022 = nfl.import_pbp_data([2022])
df_players = nfl.import_rosters([2022])
df_teams = nfl.import_team_desc()



# In[4]:


df_2022 = df_2022[df_2022['two_point_attempt'] == False]


# In[5]:


df_2022 = df_2022[df_2022['play_type'] == 'pass']


# In[6]:


df_2022 = df_2022.merge(df_players[["player_id", "player_name"]], left_on = "passer_player_id", right_on ="player_id")


# In[7]:


df_2022["player_name"].unique()


# In[8]:


df_2022 = df_2022.merge(df_teams[["team_abbr", "team_color"]], left_on ='posteam', right_on ='team_abbr')


# In[32]:


df_agg = (
    df_2022.groupby(["player_name", "team_abbr", "team_color", "week"], as_index=False)
    .agg({"passing_yards": "sum", "pass_touchdown":"sum", "interception":"sum"})
)


# In[49]:


def plot_cumulative_passing_yards(player_name):
    fig1 = go.Figure()
    
    for name, values in df_agg.groupby('player_name'):
        if name == player_name:
            fig1.add_trace(
                go.Scatter(
                    x=values['week'],
                    y=values['passing_yards'].cumsum(),
                    name=name,
                    mode='markers+lines',
                    line_color=values.iloc[0].team_color,
                    hovertemplate=f"<b>{name}</b><br>%{{y}} yds through week %{{x}}<extra></extra>"
                )
            )
            
    fig1.update_layout(
        title = "Cumulative Passing Yards",
        xaxis_title="week",
        yaxis_title="Passing Yards",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig1


# In[51]:


def plot_cumulative_touchdown_yards(player_name):
    fig2 = go.Figure()
    
    for name, values in df_agg.groupby('player_name'):
        if name == player_name:
            fig2.add_trace(
                go.Scatter(
                    x=values['week'],
                    y=values['pass_touchdown'].cumsum(),
                    name=name,
                    mode='markers+lines',
                    line_color=values.iloc[0].team_color,
                    hovertemplate=f"<b>{name}</b><br>%{{y}} touchdowns through week %{{x}}<extra></extra>"
                )
            )
            
    fig2.update_layout(
        font_family ="Averta, sans=serif", 
        hoverlabel_font_family="Averta, sans=serif",
        title = "Cumulative Touchdowns",
        xaxis_title="Week",
        yaxis_title="Touchdowns",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig2


# In[53]:


def plot_cumulative_interception(player_name):
    fig3 = go.Figure()
    
    for name, values in df_agg.groupby('player_name'):
        if name == player_name:
            fig3.add_trace(
                go.Scatter(
                    x=[0] + values['week'],
                    y=[0] + values['interception'].cumsum(),
                    name=name,
                    mode='markers+lines',
                    line_color=values.iloc[0].team_color,
                    hovertemplate=f"<b>{name}</b><br>%{{y}} interceptions through week %{{x}}<extra></extra>"
                )
            )
            
    fig3.update_layout(
        font_family ="Averta, sans=serif", 
        hoverlabel_font_family="Averta, sans=serif",
        title = "Cumulative Interception",
        xaxis_title="Week",
        yaxis_title="Interception",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig3


# In[58]:


player_names = df_agg["player_name"].unique()


# In[ ]:


st.title('Quarterback Analysis')


# In[59]:


selected_player = st.selectbox("Select a player", player_names)


# In[63]:

fig = plot_cumulative_passing_yards(selected_player)
st.plotly_chart(fig)


# In[ ]:


fig2 = plot_cumulative_touchdown_yards(selected_player)
st.plotly_chart(fig2)


# In[ ]:


fig3 = plot_cumulative_interception(selected_player)
st.plotly_chart(fig3)

