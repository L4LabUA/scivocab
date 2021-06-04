DATABASE=${CURDIR}/../app/app.db

# Create an Excel workbook for scoring the definition task.
definition_responses.xlsx: make_definition_scoring_workbook $(DATABASE)
	./$^ $@
