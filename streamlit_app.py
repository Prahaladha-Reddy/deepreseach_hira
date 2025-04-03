import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/generate_report/"

st.title("📑 AI Report Generator")
st.subheader("Enter a topic and generate a detailed AI-generated markdown report.")

topic = st.text_area("Enter the topic:", height=100)

if st.button("Generate Report"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic before generating a report.")
    else:
        st.info("⏳ Generating report... This may take some time.")
        
        # Send request to FastAPI backend
        response = requests.post(API_URL, json={"topic": topic})

        if response.status_code == 200:
            report = response.json().get("report", "")
            
            if not report:
                st.error("❌ No report generated. Try again with a different topic.")
            else:
                st.success("✅ Report Generated Successfully!")
                st.markdown(report, unsafe_allow_html=True)  # Display the content

                # Generate filename based on user's topic
                markdown_filename = f"{topic.replace(' ', '_')}.md"
                markdown_data = report.encode('utf-8')

                st.download_button(
                    label="📥 Save as Markdown",
                    data=markdown_data,
                    file_name=markdown_filename,
                    mime="text/markdown"
                )
        else:
            st.error(f"❌ Failed to generate report. Error Code: {response.status_code}")