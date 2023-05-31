# Makeathon 2023
This is our project for TUM.ai Makeathon 2023. We chose the Bridge the Gap challenge presented by Knowron.

### Our Team
[@deadlyseagull](https://github.com/deadlyseagull)
[@ibrahimey](https://github.com/ibrahimey)
[@nataliablasco00](https://github.com/nataliablasco00)
[@razreshili](https://github.com/razreshili)

### The Challenge

Make the integration into the job market easier for immigrant workers by allowing them to document their work without speaking the native language of the country. Imagine a Ukrainian service technician being able to come to Germany and make a voice memo in Ukranian of his or her work routine of the day. Provide an efficient and effective process for report creation that incorporates notes and voice memos to enable talents worldwide to collaborate. Do so by creating a tool that automatically generates a report with sections and clear descriptions in German or English.

The deliverable should be an MVP showcasing a report-generation tool powered by NLP models. Your tool should have a faithfulness metric implemented in the system to validate the accuracy of the generated reports and to ensure high-quality outputs. The solution should be able to take text, voice memos, and pictures from a mobile device. The final report's language should be English or German, but you are free to choose the input language.

In your product, you should try to incorporate the following points: 

- Generate documentation from different input sources: text, voice memo, and pictures in a foreign language
- Faithfulness review in form of links to original source, comparison with other texts, or a metric showcasing fidelity to the original text
- The correct output of documents in PDF format
- Easy to understand UX/UI, focused on function rather than aesthetics

The extra mile:

- Create reports that combine voice memo transcriptions with created videos and images.

### How to Build

We used Microsoft Azure Services in this project, so to be able to run it you need the following credentials from Azure in a .env file.

```python
TRANSLATOR_ENDPOINT, TRANSLATOR_KEY, SOURCE_SAS_URL, TARGET_SAS_URL, SPEECH_KEY, SPEECH_REGION, STORAGE_KEY, STORAGE_NAME, STORAGE_CONN, IMAGE_KEY, IMAGE_ENDPOINT
```
After you have the Azure services set up and required packages installed. You can just run

```
streamlit run main.py
```
