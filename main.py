import streamlit as st
import pandas as pd
from processing_file import processing_file
import altair as alt
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="SoDiTEC Course Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")


# Donut chart
def make_donut(total, input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']

    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [total - input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [total, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700,
                          fontStyle="italic").encode(text=alt.value(f'{round((input_response / total)*100, 1)}%'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text
#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:
    selected = option_menu("Course", ["Latex"],
                           icons=['book'], menu_icon="cast", default_index=0)
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload File To Visualize")


#######################
# Dashboard Title
st.markdown("""
    <style>
    .dashboard-title {
        background-color: #3b5998;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    .dashboard-title h1 {
        margin: 0;
        font-size: 2.5em;
    }
    .dashboard-title p {
        font-size: 1.2em;
        margin: 5px 0 0 0;
    }
    </style>"""+f"""
    <div class="dashboard-title">
        <h1>{selected} Course Statistics</h1>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file is not None:
    file_name = uploaded_file.name
    # Kiểm tra loại file
    file_type = uploaded_file.type
    if file_type in ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        df = processing_file(uploaded_file, file_type)



    #######################
    # Dashboard Main Panel
    col = st.columns((1.5, 4.5), gap='medium')
    with col[0]:
        st.markdown("#### Total Registered")
        st.metric(label="Total Registered", value=len(df))


        migrations_col = st.columns(3)
        with migrations_col[1]:
            st.markdown("#### Hust Student")
            hustStudentChart = make_donut(len(df), df["IsHust"].value_counts().to_dict()["Yes"], "Hust Student", "orange")
            st.altair_chart(hustStudentChart)

        st.markdown("#### Top Grade")

        class_detail = df['Grade'].value_counts().to_dict().keys()
        values = df['Grade'].value_counts().to_dict().values()
        class_df = pd.DataFrame({
            "Grade": class_detail,
            "Count": values
        })

        st.dataframe(class_df,
                     column_order=("Grade", "Count"),
                     hide_index=True,
                     width=None,
                     column_config={
                         "Grade": st.column_config.TextColumn(
                             "Grade",
                         ),
                         "Count": st.column_config.ProgressColumn(
                             "Count",
                             format="%f",
                             min_value=0,
                             max_value=max(class_df.Count),
                         )}
                     )


    with col[1]:
        with st.container(border=False):
            st.markdown("#### Top Class")

            class_detail = df['Class'].value_counts().to_dict().keys()
            values = df['Class'].value_counts().to_dict().values()
            class_df = pd.DataFrame({
                "Class": class_detail,
                "Count": values
            })

            class_chart = alt.Chart(class_df).mark_bar().encode(
                x='Class:O',
                y="Count:Q",
                # The highlight will be set on the result of a conditional statement
                color=alt.condition(
                    alt.datum.Count == max(values),  # If the year is 1810 this test returns True,
                    alt.value('orange'),     # which sets the bar orange.
                    alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
                )
            )
            st.altair_chart(class_chart, use_container_width=True)
            time_detail_cols = st.columns(2, gap="medium")
            with time_detail_cols[0]:
                with st.container(border=False):
                    st.markdown("#### Day")
                    day_details = df['Day'].value_counts().to_dict()
                    days = list(day_details.keys())
                    values = list(day_details.values())
                    day = pd.DataFrame({
                        "Day": days,
                        "Value": values
                    })
                    day_chart = alt.Chart(day).mark_line().encode(
                        x="Day:T",
                        y='Value:Q'
                    )
                    st.altair_chart(day_chart, use_container_width=True)
        
        
    
            with time_detail_cols[1]:
                with st.container(border=False):
                    st.markdown("#### Time")
                    day_details = df['Time'].value_counts().to_dict()
                    hours = list(day_details.keys())
                    values = list(day_details.values())
                    day = pd.DataFrame({
                        "Hour": hours,
                        "Value": values
                    })
                    day_chart = alt.Chart(day).mark_line().encode(
                        x="Hour:Q",
                        y='Value:Q'
                    )
                    st.altair_chart(day_chart, use_container_width=True)

