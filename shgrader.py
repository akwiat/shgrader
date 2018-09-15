import cmd
import csv
import re
import os

completions = [
    'Mage Slayer (Alara Reborn)',
    'Magefire Wings (Alara Reborn)',
    'Sages of the Anima (Alara Reborn)',
    'Sanctum Plowbeast (Alara Reborn)',
    'Sangrite Backlash (Alara Reborn)',
    'Sanity Gnawers (Alara Reborn)',
    'Sen Triplets (Alara Reborn)'
]

def process_file(fname):
    students = []
    with open(fname) as csvfile:
        headers = None
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i is 0: 
                headers = row
            name = row[0]
            if name == "Points Possible": continue
            if name == "Student, Test": continue
            students.append(row[0])
    print(students)
    return students, headers

class mycmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.grade_finder = re.compile(r"([^0-9]+, [^0-9]+) ([0-9]*)")

    def do_quit(self, s):
        return True

    def do_add(self, s):
        pass
    
    def do_file(self, s):
        self.filebase = s
        self.inputfile = os.path.join("input", self.filebase)
        self.outputfile = os.path.join("output", self.filebase)

        self.names, self.headers = process_file(self.inputfile)
        self.data = {}

    def complete_file(self, text, line, b, e):
        return [f for f in os.listdir("input") if f.startswith(text)]

    def do_column(self, s):
        self.column = s
        print("column: ", self.column)

    def complete_column(self, text, line, b, e):
        # return [h for h in self.headers if h.startswith(text)]
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in self.headers if s.startswith(mline)]

    def do_g(self, s):
        print("doing g: ", s)
        r = self.grade_finder.match(s.strip())
        self.data[r.group(1)] = r.group(2)
        # print(r.group(1))
        # print(r.group(2))

    def do_write(self, s):
        col_index = self.headers.index(self.column)
        print("index: ", col_index)
        with open(self.outputfile, "w") as outfile:
            writer = csv.writer(outfile)
            with open(self.inputfile) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    student = row[0]
                    if student in self.data:
                        row[col_index] = self.data[student]
                    writer.writerow(row)

    def complete_g(self, text, line, b, e):
        return [n for n in self.names if n.startswith(text)]

    def completedefault(self, text, line, begidx, endidx):
        print("text", text)
        print(line)
        print(begidx)
        print(endidx)
        print("end")
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in completions if s.startswith(mline)]

    # def complete_add(self, text, line, begidx, endidx):


if __name__ == '__main__':
    mycmd().cmdloop()