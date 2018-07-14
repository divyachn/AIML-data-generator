from aiml import DefaultSubs 
from aiml.WordSub import WordSub
import re

class Aiml_Generator(object):

    def print_categories(self):
        # For testing purpose.
        for cat in self.categories:
            print('pattern_head: ',cat['pattern_head'])
            print('srai: ',cat['srai'])
            print('think_dict: ',cat['think_dict'])
            print('condition_flag: ',cat['condition_flag'])
            print('response: ',cat['response'])
            print('topic_flag_begin: ',cat['topic_flag_begin'])
            print('topic_flag_end: ',cat['topic_flag_end'])
            print()

    def __init__(self):
        self._classifier = {
            "#":    self._process_hash,
            "-":    self._process_hyphen,
            "$":    self._process_dollar,
        }
        
        self._hash_type = {
            "intent":    self._process_patent,
            "pattern":   self._process_patent,
            "topic":     self._process_topic,
        }
        
        self.categories = []
        self.topic = {
            'topic_name':'',
            'flag':0,
            'topic_begins':'<topic name="topic_name">\n',
            'topic_ends':'</topic>\n'
        }
        
        self.subs = WordSub(DefaultSubs.defaultNormal)
                
    def classify_line(self, line, line_number):
    
        """ This method takes two inputs line and it's number. The line has been stripped of extra leading and trailing spaces.
            It then checks for the first element and accordingly calls the handler function.
        """
        if line[0] in self._classifier:
            handler_function = self._classifier[line[0]]
            handler_function(line, line_number)
        elif self.categories[-1]['condition_flag'] == 1 and line[0] in ['c','d','?']:
            # It is a valid <condition> format
            self._process_condition(line)
        else:
            print("ERROR: go to line: ",line_number)
            print(line)
            exit()
        
    def _process_hash(self, line, line_number):
        # line_type should be in ['intent','pattern','topic']
        line_type = line.split(':')[0].split(' ')[1]
        try:
            handler_function = self._hash_type[line_type]
        except:
            print('You can only use "intent", "pattern", or "topic". Error in line number:',line_number)
            exit()
        handler_function(line,line_type)
    
    def _process_hyphen(self, line, line_number):
        text = line.split('-')[1].strip()
        text, key, value = self.extract_entity(text)
        temp = {}
        if key:
            temp[key] = value
        array = [text,temp]
        self.categories[-1]['srai'].append(array)
    
    def _process_dollar(self, line, line_number):
        text = line.split('$')[1].strip()
        if text[0] == '?':
            # <condition> tag begins, make condition_flag = 1, and remove the '?' and ':'
            condition_name = text[1:-1]
            self.categories[-1]['response'].append('<condition>')
            self.categories[-1]['response'].append([])
            self.categories[-1]['response'][-1].append(condition_name)
            self.categories[-1]['response'][-1].append([])
            self.categories[-1]['condition_flag'] = 1
        elif self.categories[-1]['condition_flag'] == 1:
            self._process_condition(line)
        else:
            try: text = self.set_entity(text)
            except: pass
            try: text = self.get_entity(text)
            except: pass
            self.categories[-1]['response'].append(text)
            
    def _process_condition(self, line):
        if line == '?':
            # condition evaluation done
            self.condition_flag = 0
        elif line[0] == '$':
            # Extract the possible responses
            text = line.split('$')[1].strip()
            self.categories[-1]['response'][-1][-1][-1].append(text)
        elif 'case' in line:
            # Extract the possible condition value
            value = line.split()[1]
            # Remove the quotes and ':'
            value = value[1:-2]
            self.categories[-1]['response'][-1][-1].append(value)
            self.categories[-1]['response'][-1][-1].append([])
        elif 'default' in line:
            value = 'default'
            self.categories[-1]['response'][-1][-1].append(value)
            self.categories[-1]['response'][-1][-1].append([])
            
    def set_entity(self, text):
        key = text.split('(')[1].split(')')[0]
        value = text.split('[')[1].split(']')[0]
        # Remove the [text]
        temp = re.sub(r'\([^)]*\)', '', text)
        # Replace the (text) with <set name="key">value</set>
        repl = '<set name="'+key+'">'+value+'</set>'
        temp = re.sub(r'\[[^]]*\]',repl,temp)
        return temp
    
    def get_entity(self, text):
        key = text.split('{')[1].split('}')[0]
        # Replace the {text} with '<get name="text"/>'
        repl = '<get name="'+key+'"/>'
        temp = re.sub(r'\{[^}]*\}',repl,text)
        return temp
    
    def extract_entity(self, text):
        # Extract entity if present in text within () and remove '[', ']'.
        if '(' in text:
            key = text.split('(')[1].split(')')[0]
            value = text.split('[')[1].split(']')[0]
            result = re.sub(r'\([^)]*\)', '', text)
            brackets = re.compile("|".join([r'\[', r'\]']))
            result = brackets.sub('', result)
            return result, key, value
        return text, '', ''
            
    def create_dictionary(self, text):
        # This method creates think_dict = {}, setting variable name as it's key and variable value as it's value
        think_dict = {}
        extract_dictionary = text.split(',')
        for elem in extract_dictionary:
            elem = elem.split(':')
            key, value = elem[0].strip(), elem[1].strip()
            think_dict[key.strip()[1:-1]] = value.strip()[1:-1]
        return think_dict
        
    def create_category(self, pattern_head,srai,think_dict,condition_flag,response,topic_flag_begin,topic_flag_end):
        temp = {}
        temp['pattern_head'] = pattern_head
        temp['srai'] = srai
        temp['think_dict'] = think_dict
        temp['response'] = response
        temp['condition_flag'] = 0
        temp['topic_flag_begin'] = topic_flag_begin
        temp['topic_flag_end'] = topic_flag_end
        return temp
    
    def _process_patent(self, line, line_type):
        text = line
        think_dict = {}
        if '{' in text:
            extract_dictionary = text[text.index('{')+1:text.index('}')].strip()
            think_dict = self.create_dictionary(extract_dictionary)
            text = re.sub(r'\{[^}]*\}', '', text)
        text = text.split(':')[1]
        text, key, value = self.extract_entity(text)
        if key:
            think_dict[key] = value
        pattern_head = text                
        elem = self.create_category(pattern_head,[],think_dict,0,[],self.topic['flag'],0)
        self.topic['flag'] = 0
        self.categories.append(elem)
    
    def _process_topic(self,line,line_number):
        temp = line.split(':')[1]
        if temp == 'end_topic':
            self.categories[-1]['topic_flag_end'] = 1
        else:
            self.topic['topic_name'] = temp.upper()
            self.topic['flag'] = 1
        
    def combine(self):
        # Remove last entry and prepare it's respective tags
        elem = self.categories.pop()
        start = ''
        end = ''
        if elem['topic_flag_begin'] == 1:
            start = re.sub(r'topic_name',self.topic['topic_name'],self.topic['topic_begins'])
        # Template for <srai> tags
        # Remove the punctuations
        regex = re.compile('|'.join([r'\.',r'\?',r'!']))
        pattern_head = self.subs.sub(elem['pattern_head'].lower(), 'normal').upper()
        pattern_head = regex.sub('', pattern_head)
        string = '<category>\n<pattern>srai_data</pattern>\n<template><srai>'+pattern_head+'</srai><think><set name="variable_name">variable_value</set></think></template>\n</category>\n\n'
        srai_category = start
        for srai in elem['srai']:
            srai_text = srai[0].lower()
            srai_think = srai[1]
            srai_text = self.subs.sub(srai_text, 'normal')
            srai_text = srai_text.upper()
            srai_text = regex.sub('',srai_text)
            temp = re.sub(r'srai_data',srai_text,string)
            if bool(srai_think):
                key = list(srai_think.keys())[0]
                value = srai_think[key]
                temp = re.sub(r'variable_name',key,temp)
                temp = re.sub(r'variable_value',value,temp)
            else:
                temp = re.sub(r'<think>.*</think>','',temp)
            srai_category += temp
            
        # Prepare the main unit
        str_category = '<category>\n<pattern>'+self.subs.sub(elem['pattern_head'].lower(),'normal').upper()+'</pattern>\n'
        head_category = ''
        that_clause = []
        if len(self.categories):
            # Fetch the previous response of bot for <that>
            that_clause = self._process_that(self.categories[-1]['response'])
            str_category += '<that>that_clause</that>\n'
            
        # Create <template> tag only if <think> tag or some response is present
        if bool(elem['think_dict']) or len(elem['response']):
            str_category += '<template>'
            if bool(elem['think_dict']):
                # If there are variables to be set using <think> and <set>
                think_dict = elem['think_dict']
                str_category += '\n<think>\n'
                for key in think_dict:
                    value = think_dict[key]
                    str_category += '<set name="'+key+'">'+value+'</set>'
                str_category += '</think>\n'
            if len(elem['response']):
                response = elem['response']
                template = self._form_template(response)
                str_category += template
            str_category += '</template>\n'
            str_category += '</category>\n\n'
            if len(that_clause):
                for t in that_clause:
                    repl = self.subs.sub(t.lower(), 'normal').upper()
                    repl = regex.sub('',repl)
                    head_category += re.sub(r'that_clause', repl, str_category)
            else:
                head_category = str_category
        else:
            # Erase the str_category
            str_category = ''
        if elem['topic_flag_end'] == 1:
            end = self.topic['topic_ends']
            head_category += end
        return srai_category + head_category
        
    def _process_that(self, response):
        """This method receives the self.categories[-1]['response'] list.
           It then classifies the type of it's last entry and accordingly returns that_clause. 
        """
        that_clause = []
        last_entry = response[-1]
        if len(response)>1 and self.classify_reply(response[-2]) == 3:
            that_clause.append(last_entry[1][-1][-1])
        elif self.classify_reply(last_entry) == 2:
            text = re.sub(r'\]\s*\[', ']|[', last_entry)
            text = text.split('|')[-1]
            # Remove the '[',']'
            text = text[1:-1]
            if ',' in text:
                text = text.split(',')
                for t in text:
                    t = t.strip()[1:-1]
                    that_clause.append(t)
            else:
                # Remove the leading and trailing quotes
                that_clause.append(text[1:-1]) 
        else:
            that_clause.append(last_entry)
        return that_clause
        
    def classify_reply(self, reply):
        # Classify the type of entry of response
        reply_type = 1
        if reply == '<condition>':
            reply_type = 3
        elif re.search(r'\[', reply):
            reply_type = 2
        return reply_type
        
    def _form_template(self, response):    
        """ Reponse is a list. It's each entry needs to be processed and accordingly added to li.
            li[] is a list storing the converted aiml format of each entry of response[].
            It's length determines the usage of <random>.
        """
        index = 0
        li = []
        while index < len(response):
            reply = response[index]
            reply_type = self.classify_reply(reply)
            if reply_type == 3:
                # Move to next element
                index += 1
            text = self._process_response(response[index], reply_type)
            li.append(text)
            index += 1
        # Compile all those responses :)
        if len(li) == 1:
            text = li[0];
        else:
            text = '<random>\n'
            for l in li:
                text += '<li>'+l+'</li>\n'
            text += '</random>'
        return text
        
    def _process_response(self, reply, reply_type):
    
        """response[] has three types of entries:
               i. One line response ['Hello. What's up?', 'Hi']
               ii. Multi line response ["['Howdy.','Yo']['How are you?', 'What's up?']", "['good'] ['XYZ','xyz']"]
               iii. Conditional response ['<condition>', "['condition_name', ['hot', ['yes', 'very hot'], 'cold', ['cold'], 'dry' ['very much'], 'default', ['default case'] ] ]" ]
           This method identifies the type of reply and convert it to aiml format accordingly.
        """
        answer = ''
        if reply_type == 3:
            condition_name = reply[0]
            answer = '<condition name="'+condition_name+'">\n'
            count = 0
            text = reply[1]
            while count < len(text):
                item = text[count]
                if count%2==0:
                    # On even indices, possible condition_value is present
                    value = item
                    answer += '<li value="'+value+'">value_text</li>\n'
                    if value == 'default':
                        answer = re.sub(r'\s*value="default"','',answer)
                else:
                    # On odd indices, responses for previously extracted condition_value are present, item is a list in this case
                    i = 0
                    while i<len(item):
                        reply_type = self.classify_reply(item[i])
                        if reply_type == 3:
                            i += 1
                        value = self._process_response(item[i],reply_type)
                        i += 1
                        answer = re.sub(r'value_text', value, answer)
                count += 1
            answer += '</condition>\n'
        elif reply_type == 2:
            # Replace the '] [' with ']|['
            text = re.sub(r'\]\s*\[', ']|[', reply)
            text = text.split('|')
            for t in text:
                # Remove '[' and ']'
                t = t[1:-1]
                temp = t.split(',')
                if len(temp) == 1:
                    ans = temp[0][1:-1]+'\n'
                else:
                    ans = '\n<random>\n'
                    for v in temp:
                        ans += '<li>'+v.strip()[1:-1]+'</li>\n'
                    ans += '</random>\n'
                answer += ans
        else:
            answer = reply
        return answer
