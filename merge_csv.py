from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import os
from tkinter import messagebox as msgbox

root = Tk()
root.title("merge csv")

my_notebook = ttk.Notebook(root)
my_notebook.pack(padx=10, pady=10, fill="both",expand=True)

csv_merger_frame= Frame(my_notebook)
csv_merger_frame.pack(fill="both", expand=True)

error_analysis_frame= Frame(my_notebook)
error_analysis_frame.pack(fill="both",expand=True)

my_notebook.add(csv_merger_frame, text="merge csv")
my_notebook.add(error_analysis_frame, text="추가예정")

### 파일 불러오기 , 병합실행, 저장

# 파일 추가
def add_file_csv():
    files_csv = filedialog.askopenfilenames(title="열기",\
        filetypes=(("csv", "*.csv"),("모든 파일", "*.*")),\
        initialdir=r"C:/")

    #선택한 file 을 list 에 띄움
    for file_csv in files_csv:
        list_file_csv.insert(END, file_csv)

def del_file_csv():
    for index in reversed(list_file_csv.curselection()):
        list_file_csv.delete(index)

def del_allfile_csv():
    list_file_csv.delete(0, END)

def dest_path_csv():
    file_save_csv = filedialog.asksaveasfilename(title="저장",filetypes=(("csv", "*.csv"),("모든 파일", "*.*")),initialfile='m.csv')
    if file_save_csv is None:
        return
    txt_dest_path_csv.delete(0, END)
    txt_dest_path_csv.insert(0, file_save_csv)

def merge_csv():
    li = []
    all_files = list_file_csv.get(0, END)
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    frame_csv = pd.concat(li, axis=0)

    save_file = os.path.join(txt_dest_path_csv.get())

    if chkvar.get()==1:
        frame_csv.to_csv(save_file)

    if chkvar.get()==0:
        filtered_CD = frame_csv[frame_csv["ACD_No"]=="CD"]
        filtered_CD.to_csv(save_file)

    msgbox.showinfo("","-끝-")

def start_csv():
    if list_file_csv.size() == 0:
        msgbox.showwarning("경고","파일을 선택하세요")
        return

    if len(txt_dest_path_csv.get()) == 0:
        msgbox.showwarning("경고","저장경로를 지정하세요")
        return
    merge_csv()

## csv merger 프레임

# 실행 프레임
frame_run=Frame(csv_merger_frame)
frame_run.pack(side="bottom",fill="x", padx=5, pady=5)

btn_exit = Button(frame_run, padx=4, pady=5, width=10, text="Exit", command=root.quit)
btn_exit.pack(side="right", padx=5, pady=5) 
btn_start = Button(frame_run, padx=4, pady=5, width=10, text="Start", command=start_csv)
btn_start.pack(side="right", padx=5, pady=5) 

# 저장 경로 프레임
path_frame = LabelFrame(csv_merger_frame, text="Save to")
path_frame.pack(side="bottom",fill="x", padx=5, pady=5)

txt_dest_path_csv = Entry(path_frame)
txt_dest_path_csv.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=5)  #높이 변경

btn_dest_path = Button(path_frame, text="...", width=3, command=dest_path_csv)
btn_dest_path.pack(side="right",expand=False, padx=5, pady=5) 

# 옵션 프레임
option_frame = LabelFrame(csv_merger_frame, text="Option")
option_frame.pack(side="bottom", fill="x", padx=5, pady=5)

chkvar = IntVar()
chkbox = Checkbutton(option_frame, text="ACD 포함", variable=chkvar)
chkbox.select()
chkbox.pack(side="left", padx=5, pady=5)

# 파일 프레임 (파일 추가, 선택 삭제)
File_frame=LabelFrame(csv_merger_frame, text="File List")
File_frame.pack(fill="both", expand=True, padx=5, pady=5)
file_frame=Frame(File_frame)
file_frame.pack(side="left",fill="y", padx=5, pady=5)

btn_add_file=Button(file_frame, padx=4, pady=5, width=10, text="Add", command=add_file_csv)
btn_add_file.pack(side="top", padx=5, pady=5)
btn_del_file = Button(file_frame,padx=4, pady=5, width=10, text="Delete", command=del_file_csv)
btn_del_file.pack(side="top", padx=5, pady=5)
btn_del_file = Button(file_frame,padx=4, pady=5, width=10, text="Clear", command=del_allfile_csv)
btn_del_file.pack(side="top", padx=5, pady=5)

# 파일 프레임에 리스트 프레임 추가
list_frame=Frame(File_frame)
list_frame.pack(side="left", fill="both" ,expand=True, padx=5, pady=10)
scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right",fill="y", padx=5, pady=10)

list_file_csv = Listbox(list_frame, selectmode="extended",  yscrollcommand=scrollbar.set)
list_file_csv.pack(side="left",fill="both", expand=True)
scrollbar.config(command=list_file_csv.yview)

root.mainloop()