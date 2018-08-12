from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

class PdfGetOperator():

	def __init__(self,file):
		self.file = PdfFileReader(file);

	def fileInfo(self):
		return self.file.getDocumentInfo();

	def fileMetaData(self):
		return self.file.getXmpMetadata();

	def isEncrypt(self):
		return self.file.isEncrypted;

	def numberOfPage(self):
		return self.file.numPages;

	def extract(self,pageNumberList,outputDir,combine=False):

		if not hasattr(type(pageNumberList),"__iter__"):
			pageNumberList = [pageNumberList];

		#combine output pages into single pdf file
		if combine:
			fileWriter = PdfFileWriter();
			for num,page in enumerate(pageNumberList):		
				fileWriter.addPage(self.file.getPage(page));
				fileWriter.addBookmark("page-%s"%num,num);
			sinOrmulti = "pages" if len(pageNumberList)>1 else "page";
			self.newPdf = open("%s/%s%s-combined.pdf" %(outputDir,len(pageNumberList),sinOrmulti),"wb");
			fileWriter.write(self.newPdf);
			self.newPdf.close();
		
		# one-page, one-pdf output file
		else:
			for page in pageNumberList:
				fileWriter = PdfFileWriter();
				fileWriter.addPage(self.file.getPage(page));
				self.newPdf = open("%s/page-%s.pdf" %(outputDir,page),"wb");
				fileWriter.write(self.newPdf);
				self.newPdf.close();

class PdfSetOperator():
	def __init__(self):
		pass
	def bind(self, *files,outputDir="./"):
		merger = PdfFileMerger();
		for num,file in enumerate(files):
			# bind files
			merger.append(file,import_bookmarks=False);
			merger.addBookmark("page-%s"%num,num,parent=None);
		output = open("%s/output-binder.pdf" %outputDir,"wb");
		merger.write(output);
		merger.close();
		output.close();

if __name__ == "__main__":
	pdf = PdfSetOperator()
	file1 = r"page-1.pdf";
	file2 = r"page-3.pdf";
	file3 = r"page-4.pdf";
	file4 = r"page-5.pdf";
	pdf.bind(file1,file2,file3,file4)