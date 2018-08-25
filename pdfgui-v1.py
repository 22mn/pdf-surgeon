import tkinter as tk,subprocess,os
from pdfoperator import PdfSetOperator,PdfGetOperator
from tkinter import *
from tkinter import ttk,messagebox,font
from tkinter.filedialog import askopenfilenames,askopenfilename

class PdfGui():
	def __init__(self,master):

		#variables
		self.outputDir = "";
		self.bindUploadFiles = '';
		self.extractUploadFile='';
		self.extractUploadFileName = StringVar();
		self.pageNumList = StringVar();
		self.numPages = StringVar();
		self.combine = BooleanVar();
		self.combine.set(False);
		self.getOperator=None;
		self.NameDirectoryDict = {};

		self.master = master
		master.configure(background="light grey")
		master.title("PDF-Surgeon® [beta 0.0.1v]")
		master.resizable(width=False, height=False);
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(size=12,family="Candara")
		
		#mainframe
		self.mainframe = ttk.Frame(master,relief=tk.RIDGE,width=500,height=500);
		#labelframe - one
		self.labelframeone = ttk.LabelFrame(self.mainframe,text="Bind Files")
		
		#labelframe for [uploadfiles,up,down,view,remove ]
		self.newframe = ttk.Frame(self.labelframeone);
		#labelframe for [up,down]
		self.updownframe = ttk.Frame(self.newframe);
		#labelframe for [view,remove]
		self.viewremoveframe = ttk.Frame(self.newframe);

		#upload files button
		self.uploadfilesbtn = ttk.Button(self.newframe,text="Upload Files",command=self.bindUpload,style="i12n.TButton")
		# up,down,remove button
		self.upbtn = ttk.Button(self.updownframe,text="↑", command=self.up,style="r9n.TButton")
		self.downbtn =ttk.Button(self.updownframe,text="↓", command=self.down, style="r9n.TButton")
		self.viewbtn = ttk.Button(self.viewremoveframe,text="⬜",command=self.view, style="r9n.TButton")
		self.removebtn = ttk.Button(self.viewremoveframe,text="X",command=self.remove, style="r9nc.TButton")


		#files info list
		self.lbframe = ttk.Frame(self.labelframeone,relief=SUNKEN)
		self.uploadfileslist = tk.Listbox(self.lbframe,exportselection=False,height=6,width=35)		
		self.scrollbar= ttk.Scrollbar(self.lbframe,orient=VERTICAL,command=self.uploadfileslist.yview) 
		self.uploadfileslist["yscrollcommand"]=self.scrollbar.set;
		#bind confirm button
		self.bindokbtn = ttk.Button(self.labelframeone,text="Bind PDFs",command=self.bind,style="i12b.TButton");
		
		#events [double-click open]
		self.uploadfileslist.bind("<Double-Button-1>",self.doubleClickOpen);

		#labelframe - two
		self.labelframetwo = ttk.LabelFrame(self.mainframe,text="Extract Pages")
		#upload file button
		self.uploadframe = ttk.Frame(self.labelframetwo)	
		self.l2uploadbtn = ttk.Button(self.uploadframe,text="Upload File",command=self.extractUpload,style="i12n.TButton")
		self.l2uploadlabel = ttk.Label(self.uploadframe,textvariable=self.extractUploadFileName)
		self.l2uploadpages = ttk.Label(self.uploadframe,textvariable=self.numPages);
		#numbers of page
		self.numlbframe = ttk.Frame(self.labelframetwo)
		self.pagenumlb = ttk.Label(self.numlbframe,text="Page Number:")
		self.pagenumbers = ttk.Entry(self.numlbframe,width=15,textvariable=self.pageNumList,style="i10n.TEntry")
		self.pagenumbers.insert(0,"eg: 1,3-5,9,11-17");
		self.pagenumbers.bind("<FocusIn>",self.hideText)
		self.combinepage = ttk.Checkbutton(self.labelframetwo,text="Combine",variable=self.combine,
			onvalue=True,offvalue=False)		
		#extract confirm button
		self.l2extractok = ttk.Button(self.labelframetwo,text="Extract PDFs",command=self.extract,style="i12b.TButton");

		#tooltips
		tooltip(self.uploadfilesbtn,"Upload PDFs to merge");
		tooltip(self.upbtn,"Up");
		tooltip(self.downbtn,"Down");
		tooltip(self.viewbtn,"Open");
		tooltip(self.removebtn,"Remove");
		tooltip(self.bindokbtn,"Files merge to single PDF")
		tooltip(self.l2uploadbtn,"Upload PDF to extract");
		tooltip(self.l2extractok,"Extract files from uploaded PDF")


		#grids
		self.mainframe.grid(row=0,column=0)

		#labelframeone -grids
		self.labelframeone.grid(row=0,column=0,padx=10,pady=10,sticky=(N))
		self.newframe.grid(row=0,column=0,pady=5)
		self.updownframe.grid(row=0,column=0,sticky=(W,N,S),pady=5)
		self.viewremoveframe.grid(row=0,column=2,sticky=(E,N,S),pady=5)
		self.uploadfilesbtn.grid(row=0,column=1,ipadx=8,padx=40)
		self.upbtn.grid(row=0,column=0,sticky=(N,E))
		self.downbtn.grid(row=0,column=1,sticky=(N,W,E))
		self.viewbtn.grid(row=0,column=2,sticky=(N,W,E))	
		self.removebtn.grid(row=0,column=3,sticky=(N,E))
		self.lbframe.grid(row=1,column=0,padx=10)
		self.uploadfileslist.grid(row=0,column=0,sticky=(N,W,E,S))
		self.scrollbar.grid(row=0,column=1,sticky=(N,S))
		self.bindokbtn.grid(row=3,column=0,pady=6,ipadx=10);

		#labelframetwo -grids
		self.labelframetwo.grid(row=0,column=2,padx=10,pady=10,sticky=(N))
		self.uploadframe.grid(row=0,column=0,padx=35,pady=7)
		self.l2uploadbtn.grid(row=0,column=0,ipadx=10)
		self.l2uploadlabel.grid(row=1,column=0,sticky=(N))
		self.l2uploadpages.grid(row=2,column=0,sticky=(N))
		self.numlbframe.grid(row=2,column=0,sticky=(N))
		self.pagenumlb.grid(row=0,column=0)
		self.pagenumbers.grid(row=1,column=0)
		self.combinepage.grid(row=4,column=0,pady=3)
		self.l2extractok.grid(row=5,column=0,ipadx=10,pady=10);

		# styles
		self.style = ttk.Style();
		self.style.configure("r9n.TButton",font=("Candara",9,"normal","bold"),height=4,width=3)
		self.style.configure("r9nc.TButton",font=("Candara",9,"normal","bold"),height=4,width=3,foreground="red")
		self.style.configure("i12b.TButton",font = ("Candara",12,"italic","bold"))
		self.style.configure("i12n.TButton",font = ("Candara",12,"italic","normal"),relief=RAISED)
		self.style.configure("i10n.TEntry",font = ("Candara",10,"italic","normal"))
		self.style.configure("i12.TFrame",font=("Candara",12))

		# display window
		master.mainloop()


	def bindUpload(self):
		self.bindUploadFiles = askopenfilenames(initialdir = "./",title="Select PDF Files",
			filetypes=(("PDF File/Files","*.pdf"),))
		if not self.bindUploadFiles:
			return '';
		self.outputDir = "/".join(self.bindUploadFiles[0].split("/")[:-1]);
		for i in self.bindUploadFiles:
			self.uploadfileslist.insert("end",i.split("/")[-1]);
			self.NameDirectoryDict[i.split("/")[-1]] = i;

	def bind(self):
		if not self.uploadfileslist or len(self.uploadfileslist.get(0,END))<2:
			return ;
		newList = self.uploadfileslist.get(0,len(self.bindUploadFiles))
		reorderList = [];
		[reorderList.append(self.NameDirectoryDict[i]) for i in newList];
		pdf = PdfSetOperator();
		pdf.bind(*tuple(reorderList),outputDir=self.outputDir);
		messagebox.showinfo("PDF Operation Completed","Your output-binder file is ready!")

	def extractUpload(self):
		self.extractUploadFile = askopenfilename(initialdir = "./",
			title="Select PDF File", filetypes=(("PDF File","*.pdf"),))
		if not self.extractUploadFile:
			return '';
		self.outputDir= "/".join(self.extractUploadFile.split("/")[:-1]);
		self.getOperator = PdfGetOperator(self.extractUploadFile);
		numpages= self.getOperator.numberOfPage()
		isPlural = "pages" if numpages > 1 else "page";
		self.numPages.set(" (%s%s)" %(numpages,isPlural)); 
		self.extractUploadFileName.set(self.extractUploadFile.split("/")[-1]);

	def extract(self):
		if not self.extractUploadFile or self.pageNumList.get()=="eg: 1,3-5,9,11-17":
			return '';
		if not self.pageNumList.get():
			messagebox.showerror("Page Number Error!","Please type in your page number 'eg: 1,3-5,9,11-17'.")
			return;
		self.getOperator = PdfGetOperator(self.extractUploadFile);
		self.getOperator.extract(self.check(self.pageNumList.get()),self.outputDir,self.combine.get());
		isMultiple = "file is" if len(self.pageNumList.get().split(","))<2 else "files are"
		message = "combined file is" if self.combine.get() else isMultiple;
		messagebox.showinfo("PDF Operation Completed","Your %s ready!" %message);
	
	def check(self,strList):
		strList = strList.split(",")
		numberList = []
		for i in strList:
			if "-" in i:
				fnum = i.split("-")[0];
				snum = i.split("-")[1];
				numberList.extend(range(int(fnum),int(snum)+1))
			else:
				numberList.append(int(i));
		return numberList;

	def hideText(self,event):
		self.pagenumbers.delete(0,END)
	def showText(self,event):
		self.pagenumbers.insert(0,"eg: 1,3-5,9,11-17");

	def doubleClickOpen(self,event):
		self.index = self.uploadfileslist.curselection();
		if self.index:
			path = os.path.join(self.outputDir, self.uploadfileslist.get(self.index));
			subprocess.Popen(r"%s" %path,shell=True);

	def view(self):
		self.doubleClickOpen(None);

	def remove(self):
		index = self.uploadfileslist.curselection();
		if not index:
			return ;
		self.uploadfileslist.delete(index)

	def move(self,sign):
		index = self.uploadfileslist.curselection();
		if not index:
			return;
		item = self.uploadfileslist.get(index);
		self.uploadfileslist.delete(index);
		self.uploadfileslist.insert(index[0]+ sign,item);
		self.uploadfileslist.select_set(index[0]+ sign);
		self.uploadfileslist.event_generate("<<ListboxSelect>>");

	def up(self):
		self.move(-1);

	def down(self):
		self.move(+1);
class ToolTip():
	def __init__(self, widget):
		self.widget    = widget
		self.tipwindow = None
		self.id        = None
		self.x         = self.y = 0

	def showtip(self, text):
		'Display text in tooltip window'
		self.text = text
		if self.tipwindow or not self.text:
			return
		x, y, _cx, cy = self.widget.bbox('insert')
		x = x + self.widget.winfo_rootx()
		y = y + cy + self.widget.winfo_rooty()+28
		self.tipwindow = tw = tk.Toplevel(self.widget)
		tw.wm_overrideredirect(1)
		tw.wm_geometry("+%d+%d" %(x,y))
		
		label = ttk.Label(tw, text = self.text, justify= tk.LEFT, 
				relief = tk.GROOVE, borderwidth = 1, font = ('Candara', '11', 'normal'))
		label.pack(ipadx=1)

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()

def tooltip(widget, text):
	toolTip  = ToolTip(widget)
	def enter(event):
		toolTip.showtip(text)
	def leave(event):
		toolTip.hidetip()
	widget.bind('<Enter>', enter)
	widget.bind('<Leave>', leave)


if __name__ == "__main__":
	root = tk.Tk();
	PdfGui(root);