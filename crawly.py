import os
import re
import json
import docx
import click
import fileinput

@click.command()
@click.argument('string')
@click.option('--regex', '-r', is_flag=True, help="Search with regex")
@click.option('--case', '-c', is_flag=True, help="Search case sensitive")
@click.option('--replace', '-R', help="String to replace the found strings")
@click.option('--verbose', '-v', is_flag=True, help="Print more output")
@click.option('--directory', '-d', default='.', help='The root directory to check')

# Yes this should all be split into classes etc. I am *Aware*
def main(string, directory, verbose, regex, replace, case):
        def log(message):
            if verbose:
                print(message)

        # WIP: Doesn't yet work for case sensitive replacements 
        def deface(line, thing, replace, full_name):
            try:
                if replace:                    
                    for line in fileinput.FileInput(full_name, inplace=True, backup='.bak'):
                        if case:
                            search = re.compile(thing, re.IGNORECASE)
                            replaced  = search.sub(replace, line)
                            print(line.replace(replaced, replaced), end='')
                        else:
                            print(line.replace(thing, replace), end='')
                            
                    print(f'[+] Replacement in file {full_name}:\n\tBefore: {thing}\n\tAfter: {replace}')
                    
            except Exception as e:
                print(e)
        
        def check_case(string, line):
            if not regex:
                global search
                global liner
                if case:
                    search = string
                    liner = line
                else:
                    search = string.lower()
                    liner = line.lower()
        
        def extract_from_word(full_name):
            doc = docx.Document(full_name)
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            return text
        
        #Pure shite. I'll fix this 'later'. Don't read this is you're considering employing me.
        def check(read_obj):
            for line in read_obj:
                if regex:
                    reg = re.findall(string, line)
                    if len(reg) > 0:
                        for find in reg:
                            if find in line:
                                list_build(full_name, find, line)
                                deface(line, find, replace, full_name)
                
                check_case(string, line)
                if string in line:
                    list_build(full_name, search, line)
                    deface(line, search, replace, full_name)
        try:
            files = []
            root_dir = directory
            log('[+] Discovered Directory Structure:\n')

            for dir_name, subdir_list, file_list in os.walk(root_dir): 
                log(f'└── {dir_name}')
                for fname in file_list:
                    log(f'  ├── {fname}')
                    full_name = dir_name+'/'+fname
                    
                    if full_name.lower().endswith(('.docx', '.html', '.txt', '.md')):
                        if fname.startswith('~$'):
                            print(f"Possible open file, cannot scan file in this state: {full_name}")
                        if full_name.lower().endswith('.docx'):
                            check(extract_from_word(full_name))
                        else:
                            with open(full_name) as read_obj:
                                check(read_obj)
                            
                        def list_build(file, content, line):
                            files.append({ 'File' : file, 'Content' : content, "Line": line })

            if not replace and len(files) != 0:
                print('\n[+] Discovered Files:\n\n%s' % json.dumps(files, indent=4))
            
            else:
                print('[-] No Results')

        except Exception as e: 
            print(f'[-] Search Failed. Please see error below:\n\t{e}')

if __name__ == "__main__":
    main()
