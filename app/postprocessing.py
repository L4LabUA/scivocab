import pandas

# This method turns a list of answers into an excel file.
def toExcel(answerArray):
    processedfile = []
    processedfile.append(["Word", "Answer", "Strand"])
    # This creates an empty 2D array with three columns, word, answer, and strand.
    for x in answerArray:
        processedfile.append([x.word, x.answer, x.strand])
        # Then for each answer in answerArray, add those three things in the next row.
    #  This then gets translated into a dataframe, which is processed into an excelsheet using the to_excel method,
    dataframe = pandas.DataFrame(processedfile)
    dataframe.to_excel("static/scivocab/answers.xlsx")  # Saved at this file position
    # This overwrite old files with that name without asking, fair warning.
