class Result:

	def __init__(self, result_number:int, doc_id:int, parent_folder:int, doc_name:str, score:float, key_words):
		self.result_number = result_number
		self.doc_id = doc_id
		self.parent_folder = parent_folder
		self.doc_name = doc_name
		self.score = score
		self.key_words = key_words

	def __str__(self):
		template = " #{}\t--document: {}\n\t--folder: {} --score: {:.2f} --keywords: {}\n"
		return template.format(self.result_number, self.doc_name, self.parent_folder, self.score, self.key_words)