import crud

ls = crud.list_files('1')
for l in ls:
	print l['filename']
