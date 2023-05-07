import streamlit as st
import pandas as pd
import sys
sys.path.append('../Scripts')
from JobPrediction import JobPrediction
import plotly
import plotly.express as px



MLFLOW_TRACKING_URI='../models/mlruns'
MLFLOW_EXPERIMENT_NAME="skills_jobs_stackoverflow"
MLFLOW_RUN_ID="cb06262089ad4c5c82d2da3046219870"
CLUSTERS_YAML_PATH="../Notebook/features_skills_clusters_description.yaml"

data=pd.read_pickle('../Notebook/skills_freq.pkl')
skills=pd.read_pickle('../Notebook/skills.pkl')
norm_skills=pd.read_pickle('../Notebook/normalized_skills.pkl')
df=pd.read_pickle('../Notebook/binary_data.pkl')

roles=['Marketing or sales professional',
 'Scientist',
 'Senior Executive (C-Suite, VP, etc.)',
 'Developer, game or graphics',
 'Educator',
 'Engineer, site reliability',
 'Academic researcher',
 'Product manager',
 'Other (please specify):',
 'Developer, QA or test',
 'Data or business analyst',
 'Engineering manager',
 'Engineer, data',
 'Student',
 'Data scientist or machine learning specialist',
 'Developer, embedded applications or devices',
 'Designer',
 'Database administrator',
 'System administrator',
 'DevOps specialist',
 'Developer, mobile',
 'Developer, desktop or enterprise applications',
 'Developer, front-end',
 'Developer, back-end',
 'Developer, full-stack']


# options = ["Job Recommandation", "Job Market Analysis"]
# page = st.sidebar.radio("Select a page", options)



st.title('Enter the world of tech')



group_skills=data.groupby(data.columns[0]).apply(lambda x:x[x.columns[1]].tolist()).to_dict()


group_skills={
        "Database you have worked with":group_skills["DatabaseHaveWorkedWith"],
        "Language you have worked with":group_skills["LanguageHaveWorkedWith"],
        "other Technology that you have worked with":group_skills["MiscTechHaveWorkedWith"],
        "Collaboration tools that you have worked with":group_skills["NEWCollabToolsHaveWorkedWith"],
        "Plateform that you have worked with":group_skills["PlatformHaveWorkedWith"],
        "Tools that you have worked with":group_skills["ToolsTechHaveWorkedWith"],
        "Web framework that you have worked with":group_skills["WebframeHaveWorkedWith"]
    }
selected_skills={}

container_style = """
        .stContainer {
            background-color: blue;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 1px 1px 10px grey;
        }
    """

for group,skills in group_skills.items():

        # st.write(f'**{group}')

        with st.markdown(f'<div style="{container_style}">', unsafe_allow_html=True):



            st.header(group)
            
            selected_skills[group]=st.multiselect(f'select skill from {group}',skills)


container=st.container()

button_col1,button_col2=container.columns(2)

with button_col1:
        st.write('')

with button_col2:

        button=st.button("What is my match?",key='find my match button',help="click to find your match")

current_skills = [skill for group, skills in selected_skills.items() if len(skills) != 0 for skill in skills]


st.markdown(
        """<style>
            .stButton button {
                background-color: #1E90FF;
                color: white;
                padding: 0.7rem 1.5rem;
                border-radius: 0.5rem;
                font-size: 1.2rem;
                display: block;
                margin: 0 auto;
            }
        </style>""",
        unsafe_allow_html=True,
    )

if button :    

        if len(current_skills)>0:
            model = JobPrediction(MLFLOW_TRACKING_URI, MLFLOW_RUN_ID, CLUSTERS_YAML_PATH)

            base_predictions=model.predict_jobs_probabilities(current_skills)
            base_predictions = base_predictions.sort_values(ascending=True)

            fig = px.bar(x=base_predictions.values, y=base_predictions.index, orientation='h')
            fig.update_layout(title='Top Job Recommendations Based on Your Skills', xaxis_title='Probability of Job Match', yaxis_title='Job Titles',height=500, width=800)

            st.plotly_chart(fig)

            

        else:

            st.write('You have to select a skills !')


# with st.container():


#         if selected_role:

#             single_role_skills=pd.concat([skills.loc[selected_role],norm_skills.loc[selected_role]],axis=1)
#             single_role_skills.columns=['percentage','specifity']
#             single_role_skills=single_role_skills.sort_values('percentage')

#             thersh=25

#             single_role_skills=single_role_skills[single_role_skills['percentage']>thersh]

#             fig=px.bar(df,
#                     y=single_role_skills.index,
#                     x=single_role_skills["percentage"],
#                     color=single_role_skills['specifity'],
#                     color_continuous_scale='orrd',
#                     range_color=[norm_skills.values.min(),norm_skills.values.max()],
#                     orientation='h')

#             fig.update_layout(width=400, height=400,title=selected_role)
#             fig.show()

#         else:

#             st.write('please select a role!')




spacer = st.empty()
spacer.markdown("<br><br>", unsafe_allow_html=True)

# create the second button
button1 = st.button("You have a dreamed Job?", key='Click here')


if button1:
    
      st.selectbox('Choose your dream job',roles)

      

# adjust the layout of the buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.write("")
with col2:
    st.markdown("<center><h2 style='color:blue'></h2></center>", unsafe_allow_html=True)
with col3:
    st.write("")






    





# if __name__=='__main__':
