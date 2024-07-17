import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from src.utils import spacing

# Function to calculate similarity score
def calculate_similarity(input_string, label):
    return fuzz.token_set_ratio(input_string.lower(), label.lower())

# Function to search and rank DataFrame rows
def search_dataframe(df, search_string):
    df['similarity'] = df['labels'].apply(lambda x: calculate_similarity(search_string, x))
    return df.sort_values('similarity', ascending=False).reset_index(drop=True)

st.set_page_config(page_title="docSHARE", page_icon="📚")

st.title("📚 docSHARE")
st.markdown("Find the themes that have been covered in [SHARE](https://share-eric.eu/) (Survey of Health, Ageing and Retirement in Europe)")
st.markdown("This app uses string similarity to find which column of the numerous dataset can be related to your query. It's open source: [browse the code](https://github.com/JosephBARBIERDARNAL/docSHARE)")
spacing(2)

# Load the DataFrame
df = pd.read_csv('metadata-share.csv')

# User input
search_query = st.text_input("Enter your search query:", placeholder="e.g., sport, cigarettes, earnings...")


if search_query:
   
   spacing(2)
   # Search and rank the DataFrame
   results = search_dataframe(df, search_query)

   # Display results
   st.subheader("Search Results")
   for i, row in results.iterrows():
      similarity = row['similarity']
      if similarity > 30:  # Only show results with similarity > 30%
         with st.expander(f"{row['labels']} (Similarity: {similarity:.2f}%)"):
            st.markdown(f"**Column name:** {row['columns']}")
            st.markdown(f"**File Name:** {row['file_name']}")
            st.markdown(f"**Labels:** {row['labels']}")
            st.progress(similarity / 100)
      
      if i == 9:  # Show only top 10 results
         break

else:
   st.info("Enter a search query to find relevant documents.")

spacing(2)
st.subheader("All Documents")
st.dataframe(df[['file_name', 'labels']], use_container_width=True)