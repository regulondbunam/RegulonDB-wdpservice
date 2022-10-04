class SequenceFormat:
    
    baseColor = {
        'A':'<span class="rdb_sequence_A">A</span>',
        'C':'<span class="rdb_sequence_C">C</span>',
        'G':'<span class="rdb_sequence_G">G</span>',
        'T':'<span class="rdb_sequence_T">T</span>',
        'a':'<span class="rdb_sequence_a">a</span>',
        'c':'<span class="rdb_sequence_c">c</span>',
        'g':'<span class="rdb_sequence_g">g</span>',
        't':'<span class="rdb_sequence_t">t</span>'
    }
    
    def __init__(self, sequence:str, title:str):
        self.sequence = sequence
        self.title = title
        self.size = len(sequence)
        self.info_sequence = self.pros_info_sequence()
        
    
    def put_color(self,x):
        return self.baseColor[x]
    
    def pros_info_sequence(self):
        infoSequence ={
            "elements": {},
            "size": self.size,
            "sequence": self.sequence,
            "title": self.title
        }
        element_read = []
        for element in self.sequence:
            if not element in element_read:
                element_read.append(element)
                element_count = self.sequence.count(element)
                infoSequence['elements'][element] = element_count
        return infoSequence
    
    def get_str_info_sequence(self):
        str_info_sequence = "size: "+str(self.info_sequence["size"])
        for element in self.info_sequence["elements"]:
            str_info_sequence += " "+element+": "+str(self.info_sequence["elements"][element])
        return str_info_sequence
    
    def get_fasta_format(self,color=False):
        count = 1
        sequence_format = ""
        for bp in self.sequence:
            x = bp
            if color:
                x = self.put_color(x)
            if count == 60:
                count = 0;
                sequence_format += x+"<br>"
            else:
                sequence_format += x
            count += 1
        return "#"+self.title+"<br>#"+self.get_str_info_sequence()+"<br>"+sequence_format
    
    def get_genebank_format(self,color=False):
        space_number = len(str(self.size))
        count = 0
        line = ""
        sequence_format = ""
        index = 0
        for bp in self.sequence:
            x = bp
            if color:
                x = self.put_color(x)
            count += 1

            line = ''
            if count == 1:
                for n in range(space_number-len(str(index))):
                    line += "&nbsp;"
                sequence_format += "\t"+line+str(index)+" "+x
            if count == 60:
                count = 0;
                sequence_format += x+"<br>"
            elif count%10 == 0:
                sequence_format += ""+x+" "
            else:
                sequence_format += x
            index += 1
        return "#"+self.title+"<br>#"+self.get_str_info_sequence()+"<br>"+sequence_format            

    def get_info_sequence(self):
        return self.info_sequence

def pros_sequence(sequence,title):
    infoSequence ={
        "elements": {},
        "size": len(sequence),
        "sequence": sequence,
        "title": title
    }
    element_read = []
    for element in sequence:
        if not element in element_read:
            element_read.append(element)
            element_count = sequence.count(element)
            infoSequence['elements'][element] = element_count
    return infoSequence


def info_str_sequence(info_sequence):
    str_info_sequence = "size: "+str(info_sequence["size"])
    for element in info_sequence["elements"]:
        str_info_sequence += " "+element+": "+str(info_sequence["elements"][element])
    return str_info_sequence
    
def fasta_format(sequence, title):
    info_sequence = pros_sequence(sequence,title)
    count = 1
    sequence_format = ""
    for bp in sequence:
        x = bp
        if count == 60:
            count = 0;
            sequence_format += x+"<br>"
        else:
            sequence_format += x
        count += 1
    head = "#"+title+"<br>#"+info_str_sequence(info_sequence)+"<br>"
    if(title == ""):head = ""
    return head+sequence_format