import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

@st.cache_data
def read_data():
    df = pd.read_csv(URL, dtype={'Quarter': str, 
                                'Canada': np.int32,
                                'Newfoundland and Labrador': np.int32,
                                'Prince Edward Island': np.int32,
                                'Nova Scotia': np.int32,
                                'New Brunswick': np.int32,
                                'Quebec': np.int32,
                                'Ontario': np.int32,
                                'Manitoba': np.int32,
                                'Saskatchewan': np.int32,
                                'Alberta': np.int32,
                                'British Columbia': np.int32,
                                'Yukon': np.int32,
                                'Northwest Territories': np.int32,
                                'Nunavut': np.int32})
    return df


def validate(start_quarter, start_year, end_quarter, end_year):
    error_msg = ''
    # validate start deate is within the data limits >= Q3 1991
    if start_year == 1991 and (start_quarter == 'Q1' or start_quarter == 'Q2'):
        error_msg = 'Error: Start date is outside data period !!!'
    if end_year < start_year or (end_year == start_year and (int(end_quarter[1]) <= int(start_quarter[1]))):
        error_msg = 'Error: End date is before or equal to start date !!!'
    return error_msg

@st.cache_data
def format_year_quarter(date):
    if date[1] == 2:
        return float(date[2:]) + 0.2
    elif date[1] == 3:
        return float(date[2:]) + 0.3
    elif date[1] == 4:
        return float(date[2:]) + 0.4
    else:
        return float(date[2:])
    
@st.cache_data
def end_before_start(start_date, end_date):
    num_start = format_year_quarter(start_date)
    num_end = format_year_quarter(end_date)

    if num_start > num_end:
        return True
    else:
        return False

def display_dash(start_date, end_date, location):
    popul_change, compare = st.tabs(['Population change', 'Compare'])
    with popul_change:
        st.subheader(f'Population change from {start_quarter}{start_year} to {end_quarter}{end_year}')
        tab_metrics, tab_plot = st.columns(2)
        with tab_metrics:
            start_value = df.loc[df["Quarter"] == start_date, location].item()
            end_value = df.loc[df["Quarter"] == end_date, location].item()
            diff = round((end_value - start_value) / start_value * 100, 2)
            delta = f'{diff}%'
            st.metric(start_date, value=start_value)
            st.metric(end_date, value=end_value, delta=delta)
        with tab_plot:
            start_row_num = df.loc[df['Quarter'] == start_date].index.item()
            end_row_num = df.loc[df['Quarter'] == end_date].index.item()
            df_plot = df.iloc[start_row_num:end_row_num+1]
            fig, ax = plt.subplots()
            ax.plot(df_plot['Quarter'], df_plot[location], color='blue')
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([df_plot['Quarter'].iloc[0], df_plot['Quarter'].iloc[-1]])
            ax.ticklabel_format(axis='y' , style='plain')  # this prevents the y=axis to display value in scientific notation
            fig.autofmt_xdate()
            st.pyplot(fig) # instead of plt.show()
    with compare:
        st.subheader('Compare with other locations')
        all_locations = st.multiselect('Select other locations', df.columns[1:], default=location)
        fig, ax = plt.subplots()
        for each in all_locations:
            ax.plot(df_plot['Quarter'], df_plot[each])
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_xticks([df_plot['Quarter'].iloc[0], df_plot['Quarter'].iloc[-1]])
        ax.ticklabel_format(axis='y' , style='plain')  # this prevents the y=axis to display value in scientific notation
        st.pyplot(fig)




if __name__ == '__main__':
    df = read_data()

    st.title('Population of Canada')
    st.markdown('Source table can be found [here](https://www.bbc.co.uk)')
    
    with st.expander('Click to see full data table'):
        st.table(df)

    with st.form('input_form'):
        col1, col2, col3 = st.columns(3)
        col1.write('Choose a starting date')
        start_quarter = col1.selectbox('Quarter', options=['Q1', 'Q2', 'Q3', 'Q4'], index=2, key='q_start')
        start_year = col1.slider('Year', min_value=1991, max_value=2023, step=1, key='y_start')
        col2.write('Choose an end date')
        end_quarter = col2.selectbox('Quarter', options=['Q1', 'Q2', 'Q3', 'Q4'], index=0, key='q_end')
        end_year = col2.slider('Year', min_value=1992, max_value=2023, step=1, key='y_end')
        col3.write('Choose a location')
        location = col3.selectbox('Select location', options=list(df.columns[1:]), index=0, key='loc')
        submitted = st.form_submit_button('Analyze', type = 'primary')

    start_date = f'{start_quarter} {start_year}'
    end_date = f'{end_quarter} {end_year}'

    if start_date not in df['Quarter'].tolist() or end_date not in df['Quarter'].tolist():
        st.error('Error: Date not in the data set !!!')
    elif end_before_start(start_date, end_date):
        st.error('Error: End date is before the start date !!!')
    else:
        display_dash(start_date, end_date, location)

