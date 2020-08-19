import pandas

def toExcel(answerArray):
    processedfile = []
    processedfile.append(["Word", "Answer", "Strand"])
    for x in answerArray:
        processedfile.append([x.word, x.answer, x.strand])
    dataframe = pandas.DataFrame(processedfile)
    dataframe.to_excel("static/scivocab/answers.xlsx")
