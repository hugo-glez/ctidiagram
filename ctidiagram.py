#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 - Hugo Gonzalez (@hugo_glez)
# This file is part of CTIdiagram

"""

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

"""

"""

CTIdiagram is basically a way to convert a YAML file with the description of the 
attack flow to a web page with a graphical representation.
It includes icons related to the steps performed on the attack, descriptions 
and it is possible to include IoC in the same diagram.

Then you just need to screenshoot the part of the diagram and include in your
documentation or in your twitter account

"""

import yaml  
import sys
from datetime import datetime
import argparse 



header = """
<!DOCTYPE html>
<html>
<head>


<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Stardos+Stencil">
<style>
    
td {   
    text-align: center; 
}

table {
  border-collapse: collapse;
  border: 1px solid;
}

tr.thick {
  font-weight: bold;
  font-size:14;
}

tr.icons {
  font-family: "Stardos+Stencil","Times New Roman", Times, serif;
  font-weight: bold;
  font-size:32px;
}

tr.iocs {
  font-family: "Times New Roman", Times, serif;
  font-weight: italic;
  font-size:14px;
}

</style>
</head>
<body>
<center>
"""


footer = """
</center>
</body>
</html>
"""


def logo():
    print("""
 _____ _____ _____   _ _                                 
/  __ \_   _|_   _| | (_)                                
| /  \/ | |   | | __| |_  __ _  __ _ _ __ __ _ _ __ ___  
| |     | |   | |/ _` | |/ _` |/ _` | '__/ _` | '_ ` _ \ 
| \__/\_| |_  | | (_| | | (_| | (_| | | | (_| | | | | | |
 \____/\___/  \_/\__,_|_|\__,_|\__, |_|  \__,_|_| |_| |_|
                                __/ |                    
                               |___/            @hugo_glez         
    
    """
    )


def main():

    parser = argparse.ArgumentParser(description ="Convert YAML file to attack flow diagram")
    parser.add_argument("yamlfile", help="YAML file to convert")
    parser.add_argument("-o","--output", help="File to save the output",  type=argparse.FileType('w'))
    parser.add_argument("-r","--resources", help="Directory to get images, default is imgs/", default = "imgs/")
    parser.add_argument("--iocs", help="Write also IoCs", action='store_true')
    parser.add_argument("--ttps", help="Write also TTPs", action='store_true')
    args = parser.parse_args()
    
    
    resource_folder = args.resources
    
    if args.output:
        logo()
        orig_stdout = sys.stdout
        f = args.output
        sys.stdout = f


    
    try:
        fichero = open(args.yamlfile)
            
    except:
        print("Error opening the file")
        fichero.close()
        sys.exit(-1)
        
    doc=yaml.load(fichero, Loader=yaml.BaseLoader)
    fichero.close        
    


    diagrama = doc['diagram']


    mdate = doc.get("date", " ")
    mtitle = doc.get("title", "Here is your title!")



    print (header)
    print ("""
    <h1>"""+ mtitle + """</h1>
    <h3> Original date:"""+mdate+"""</h3>
    <br><br>
    <table width="90%">
    """)


    #print numbers
    num = 1
    print ('<tr class="icons">')
    for a in diagrama[:-1]:
        print ("<td>")
        print (num)
        num += 1
        print ("</td><td></td>")
    print ("<td>")
    print (num)
    print ('</td>')
    print ('</tr>')

    #print icons
    print ('<tr class="thick">')
    for a in diagrama[:-1]:
        print ("<td>")
        ticon = a.get("icon", "default")
        if type(ticon) == list:
            for ico in ticon:
                print ("<img src='"+resource_folder+ico+".png'>")
        else:
            print ("<img src='"+resource_folder+ticon+".png'>")
        print ("</td><td><img src='"+resource_folder+"flecha.png'> </td>")
    print ("<td>")
    ticon = diagrama[-1].get("icon", "default")
    if type(ticon) == list:
        for ico in ticon:
            print ("<img src='"+resource_folder+ico+".png'>")
    else:
        print ("<img src='"+resource_folder+ticon+".png'>")
    print ('</td>')
    print ('</tr>')


    # print titles
    print ('<tr class="thick">')
    for a in diagrama[:-1]:
        print ("<td>")
        print (a.get('text', " "))
        print ("</td><td></td>")
    print ("<td>")
    print (diagrama[-1].get('text', " "))
    print ('</td>')
    print ('</tr>')

    # print description
    print ('<tr>')
    for a in diagrama[:-1]:
        print ("<td>")
        print (a.get('description'," "))
        print ("</td><td></td>")
    print ("<td>")
    print (diagrama[-1].get('description', " "))
    print ('</td>')
    print ('</tr>')


    if args.iocs:
        #print iocs
        print ('<tr class="iocs">')
        for a in diagrama[:-1]:
            print ("<td>")
            tiocs = a.get('iocs', None)
            if not tiocs is None:
                print ("<br>".join(tiocs))
            print ("</td><td></td>")
        print ("<td>")
        tiocs = diagrama[-1].get('iocs', None)
        if not tiocs is None:
            print ("<br>".join(tiocs))
        print ('</td>')
        print ('</tr>')

    if args.ttps:
        #print ttps
        print ('<tr class="iocs">')
        for a in diagrama[:-1]:
            tttps = a.get('ttps', None)
            print ("<td>")
            if not tttps is None:
                print ("<br>".join(tttps))
            print ("</td><td></td>")
        print ("<td>")
        tttps = diagrama[-1].get('ttps', None)
        if not tttps is None:
            print ("<br>".join(tttps))
        print ('</td>')
        print ('</tr>')


    #print logo
    print ('<tr>')
    for a in diagrama[:-1]:
        print ("<td></td><td></td>")
    print ('<td style="text-align:right"><img src="'+resource_folder+'logo.png"></td>')
    print ('</tr>')
    print ('</table>')

    print('<br><br>Generated on '+datetime.now().strftime("%Y-%m-%d, %H:%M") + ' by CTIdiagrams')

    print (footer)

    if args.output:
        sys.stdout = orig_stdout
        f.close()



if __name__ == "__main__":
    main()
    








