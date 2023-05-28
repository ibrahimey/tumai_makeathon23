import os
import re

from transformers import pipeline

from pylatex import Document, PageStyle, Head, Foot, MiniPage, LongTable, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Section, Command
from pylatex.utils import bold, NoEscape


def key_point_extraction(text):
    """
    Create dictionary with the information we want to obtain from the given text
    :param text:
    :return: dictionary with key points
    """
    # Instatiate the model from checkpoint
    model_checkpoint = "bert-large-uncased-whole-word-masking-finetuned-squad"
    model = pipeline(
        'question-answering',
        model=model_checkpoint,
        tokenizer=model_checkpoint
    )

    questions = [
        "What is his name?",
        "What is her name?",
        "What is their name?",
        "Who sent this?",
        "What is the Date?",
        "What is the location?",
        "Which equipment was used?",
        "Which is the problem?"
    ]

    map_questions = [
        "Name",
        "Name",
        "Name",
        "Sender",
        "Date",
        "Location",
        "Equipment",
        "Problem"
    ]

    answers = model(
        context=text,
        question=questions,
        top_k =1
    )

    # Summing scores for repeated answers
    unique_answers = {}
    correct_questions = []
    for a, q in zip(answers, map_questions):

        if a["answer"] in unique_answers:
            unique_answers[a["answer"]] = max(a["score"], unique_answers[a["answer"]])
        else:
            unique_answers[a["answer"]] = a["score"]
            correct_questions.append(q)

    # Converting dict to arr
    result = [(q, a, s) for (a, s), q in zip(unique_answers.items(), correct_questions) if s > 0.5]


    return result



def pdf_generator(text):
    """
    Generate the pdf file
    :param text: translated plain text
    :return: pdf file
    """
    # text = re.sub(r'\n (?:[a-zA-Z0-9 ])', "", text)

    key_points = key_point_extraction(text)

    geometry_options = {
        "head": "40pt",
        "margin": "1in",
        "bottom": "0.7in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)

    # Generating first page style
    first_page = PageStyle("firstpage")
    doc.append(Command('fontsize', arguments=['12', '10']))
    doc.append(Command('selectfont'))

    # Header image
    with first_page.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                         pos='c')) as logo_wrapper:
            logo_file = os.path.join(os.path.dirname(__file__),
                                     'faniblurb.jpeg')
            logo_wrapper.append(StandAloneGraphic(image_options="width=120px",
                                                  filename=logo_file))

    # Add document title
    with first_page.create(Head("R")) as right_header:
        with right_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                          pos='c', align='r')) as title_wrapper:
            title_wrapper.append(LargeText(bold("Fani Blurb")))
            title_wrapper.append(LineBreak())

    doc.preamble.append(first_page)
    # End first page style

    # Add customer information
    with doc.create(Tabu("X[l] X[r]")) as first_page_table:
        first_page_table.add_empty_row()

    confidence = []
    with doc.create(Section("Report", numbering=False)) as first_page_text:
        with doc.create(LongTable("|l|l|")) as data_table:
            data_table.add_hline()
            for (q, a, s) in key_points:
                confidence.append(s)
                data_table.add_row([q, a])
                data_table.add_hline()
            data_table.end_table_last_footer()
        if len(confidence) > 0:
            with doc.create(LongTable("|l|")) as acc_table:
                acc_table.add_hline()
                acc_table.add_row(["Table confidence:   {:.2f}".format(sum(confidence)/len(confidence))])
                acc_table.add_hline()
                acc_table.end_table_last_footer()

        first_page_text.append(text)

    doc.change_document_style("firstpage")
    doc.add_color(name="lightgray", model="gray", description="0.80")

    doc.generate_pdf('complex_report', clean_tex=False, compiler='pdflatex')


if __name__ == "__main__":
    text = """Date: March 15, 2023
    Name: Jan Meyer
    Location: Wind Farm Sontheim
    Equipment: Wind Turbines #456, #789, and #123

    Task Operation: Safety inspection
    Process:
    • Traveled to site,
     which required a 
     1.5-hour drive.
    • Conducted a safety i
    nspection before beginning
     work, by looking at three 
     turbines from ground. No issues found.
    • Started inspection on turbi
    ne #456 
    • Damage found on blades, found erosion on two blades. 
    • Performed superficial repair on
     blade with resin.
    • Started inspection on turbine #789 
    • Checked gearbox and lubrication for 
    #789, found leak and low lubrication
    • Changed the oil on rotor of turbine 
    #789, and leak was stopped through sealing patch
    • Started inspection on turbine #123
    • Examined generator and electrical components for 
    #123, found malfunctioning sensor
    • Sensor was corrected through calibration procedure 
    • Started general review for all turbines
    • Tested control system for all turbines, recalibrated for optimal performance
    • Started calibration of energy grid connection with turbines
    • Encountered difficulties due to heavy rain and lightning during maintenance. Stopped calibration of energy grid systems for safety. Will be rescheduled for 4.4.2023.
    • Traveled back to the office, which required another 1.5-hour drive.

    """
    pdf_generator(text)
