from __future__ import print_function
import sys
import re


def slack_chat_to_github_md(slack_msgs, nicks):
    output = ''
    
    time_regex_str = '[[][0-9]{1,2}:[0-9]{2}( [PA]M)?[]][ ]*'
    nicks_regexes = [re.compile('^({}) {}$'.format(nick, time_regex_str)) for nick in nicks]
    nick_replace_with = r'**\1**'
    
    hour_regex = re.compile('^' + time_regex_str + '$')
    
    for line in slack_msgs:
        line_processed = False
        
        for nick_regex in nicks_regexes:
            replaced = nick_regex.sub(nick_replace_with, line)
            if replaced != line:
                output += replaced
                line_processed = True
                break
        
        if not line_processed:
            if hour_regex.match(line):
                continue
            elif line != '':
                output += '> ' + line
            else:
                output += ''

    return output


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s <input_file> <output_file> <nick1> <nick2>..." % sys.argv[0])
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    nicks = sys.argv[3:]
    
    with open(input_filename) as f:
        slack_msgs = f.readlines()
    
    with open(output_filename, 'w') as f:
        f.write(slack_chat_to_github_md(slack_msgs, nicks))
