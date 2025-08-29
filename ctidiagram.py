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


CTIdiagram is basically a way to convert a YAML file with the description of the 
attack flow to a web page with a graphical representation.
It includes icons related to the steps performed on the attack, descriptions 
and it is possible to include IoC in the same diagram.

Then you just need to screenshot the part of the diagram and include in your
documentation or in your twitter account

v2.0 option to add screenshots for each step
v2.1 option to embed all icons and screen shots or none of them

"""
import sys
from datetime import datetime
import argparse
import base64
import uuid
import yaml


__version__ = "2.1"

encoded_resources = {}


HEADER = """
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


#myImg {
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

#myImg:hover {opacity: 0.7;}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
}

/* Modal Content (image) */
.modal-content {
  margin: auto;
  display: block;
  width: 90%;

}

/* Caption of Modal Image */
#caption {
  margin: auto;
  display: block;
  width: 90%;
  max-width: 900px;
  text-align: center;
  color: #ccc;
  padding: 10px 0;
  height: 150px;
}

/* Add Animation */
.modal-content, #caption {  
  -webkit-animation-name: zoom;
  -webkit-animation-duration: 0.6s;
  animation-name: zoom;
  animation-duration: 0.6s;
}

@-webkit-keyframes zoom {
  from {-webkit-transform:scale(0)} 
  to {-webkit-transform:scale(1)}
}

@keyframes zoom {
  from {transform:scale(0)} 
  to {transform:scale(1)}
}

/* The Close Button */
.close {
  position: absolute;
  top: 15px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  transition: 0.3s;
}

.close:hover,
.close:focus {
  color: #bbb;
  text-decoration: none;
  cursor: pointer;
}




</style>
</head>
<body>

<!-- The Modal -->
<div id="myModal" class="modal">
  <span class="close">&times;</span>
  <img class="modal-content" id="img01">
  <div id="caption"></div>
</div>

<center>
"""


FOOTER = """
</center>

<script>
// Get the modal

function ShowModal(param) {
    var modal = document.getElementById("myModal");

    // Get the image and insert it inside the modal - use its "alt" text as a caption
    var img = document.getElementById("myImg");
    var modalImg = document.getElementById("img01");

    modal.style.display = "block";
    eval("modalImg.src = "+ param );

}

window.addEventListener('keydown', function(event) {
  // Check if the pressed key is the Escape key
  if (event.key === 'Escape') {
    var modal = document.getElementById("myModal");
    modal.style.display = 'none'; 
    
  }
});

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}
</script>

</body>
</html>
"""


def logo():
    """
    Function to print the logo of the program
    """
    logo_str = r"""
  _____ _____ _____   _ _                                 
 /  __ \_   _|_   _| | (_)                                
 | /  \/ | |   | | __| |_  __ _  __ _ _ __ __ _ _ __ ___  
 | |     | |   | |/ _` | |/ _` |/ _` | '__/ _` | '_ ` _ \ 
 | \__/\_| |_  | | (_| | | (_| | (_| | | | (_| | | | | | |
  \____/\___/  \_/\__,_|_|\__,_|\__, |_|  \__,_|_| |_| |_|
                                 __/ |        v2.1            
                                |___/            @hugo_glez         
    """
    print(logo_str)


def print_resources():
    """
    Function to print the resources embeded
    """

    print("<script>")
    for k, v in encoded_resources.items():
        print("const " + k + ' = "', v + '";')
    print("</script>")


def return_image_2_base64(filep):
    """
    Function to code image file to base64
    """
    blank_pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    # print(filep)
    try:
        with open(filep, "rb") as f:
            rawbytes = f.read()
        encoded = base64.b64encode(rawbytes)
        encoded_string = encoded.decode("utf-8")
        result = "data:image/png;base64," + encoded_string
    except FileNotFoundError:
        # If the file does not exist create a blank pixel
        result = "data:image/png;base64," + blank_pixel
    return result


def convert_image_2_base64(filep, token):
    """
    Function to code image file to base64
    """
    blank_pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    # print(filep)
    try:
        with open(filep, "rb") as f:
            rawbytes = f.read()
        encoded = base64.b64encode(rawbytes)
        encoded_string = encoded.decode("utf-8")
        encoded_resources[token] = "data:image/png;base64," + encoded_string
    except FileNotFoundError:
        # If the file does not exist create a blank pixel
        encoded_resources[token] = "data:image/png;base64," + blank_pixel
    # encoded_resources[token]=filep


def print_icons(resource_folder, data, embed=False, embedall=False):
    """
    Function to print the icons and the javascript code to show a modal with the screenshot

    <img src="data:image/jpeg;base64,iVBOR ...
    """
    if type(data) == list:
        for ico in data:
            if type(ico) == dict:
                nico = list(ico.keys())[0]
                if embed or embedall:
                    token = "T" + str(uuid.uuid4())[:6]
                    convert_image_2_base64(ico[nico][0], token)
                else:
                    token = ico[nico][0]

                ricon = resource_folder + nico + ".png"
                if embedall:
                    ricon = return_image_2_base64(ricon)

                print(
                    "<a href=\"javascript:ShowModal('" + token + "')\">"
                    + "<img src='" + ricon + "'></a>"
                )

            else:
                ricon = resource_folder + ico + ".png"
                if embedall:
                    ricon = return_image_2_base64(ricon)
                print("<img src='" + ricon + "'>")
    else:
        if type(data) == dict:
            ndata = list(data.keys())[0]
            ricon = resource_folder + ndata + ".png"
            if embedall:
                ricon = return_image_2_base64(ricon)

            print("<img src='" + ricon + "'>")
        else:
            ricon = resource_folder + data + ".png"
            if embedall:
                ricon = return_image_2_base64(ricon)
            print("<a href='script'><img src='" + ricon + "'></a>")


def main():
    """
    Main function
    """

    parser = argparse.ArgumentParser(description="Convert YAML file to CTI diagram")
    parser.add_argument("yamlfile", help="YAML file to convert")
    parser.add_argument(
        "-o", "--output", help="File to save the output", type=argparse.FileType("w")
    )
    parser.add_argument(
        "-r",
        "--resources",
        help="Directory to get images, default is imgs/",
        default="imgs/",
    )
    parser.add_argument("-e", "--embed", help="Embed only e screenshots to be practical", action="store_true")
    parser.add_argument("--embedall", help="Embed all the resources to create a single page document",
                        action="store_true")
    parser.add_argument("--iocs", help="Write also IoCs", action="store_true")
    parser.add_argument("--ttps", help="Write also TTPs", action="store_true")
    args = parser.parse_args()

    resource_folder = args.resources

    if args.output:
        logo()
        orig_stdout = sys.stdout
        f = args.output
        sys.stdout = f

    try:
        with open(args.yamlfile, "r") as fichero:
            doc = yaml.load(fichero, Loader=yaml.BaseLoader)

    except FileNotFoundError:
        print("Error opening the file")
        sys.exit(-1)

    diagrama = doc["diagrama"]
    # print (type(diagrama))
    # print (diagrama)

    mdate = doc.get("fecha", " ")
    mtitle = doc.get("title", "Your awesome CTI attack diagram")

    print(HEADER)
    print(
        """
    <h1>"""
        + mtitle
        + """</h1>
    <h3> Original date:"""
        + mdate
        + """</h3>
    <br><br>
    <table width="90%">
    """
    )

    # print numbers
    num = 1
    print('<tr class="icons">')
    for _ in diagrama[:-1]:
        print("<td>")
        print(num)
        num += 1
        print("</td><td></td>")
    print("<td>")
    print(num)
    print("</td>")
    print("</tr>")

    # print icons

    resource_flecha = resource_folder + "flecha.png"
    if args.embedall:
        resource_flecha = return_image_2_base64(resource_flecha)

    print('<tr class="thick">')
    for a in diagrama[:-1]:
        print("<td>")
        ticon = a.get("icon", "default")
        print_icons(resource_folder, ticon, args.embed, args.embedall)
        print("</td><td><img src='" + resource_flecha + "'> </td>")
    print("<td>")
    ticon = diagrama[-1].get("icon", "default")
    print_icons(resource_folder, ticon, args.embed, args.embedall)
    print("</td>")
    print("</tr>")

    # print titles
    print('<tr class="thick">')
    for a in diagrama[:-1]:
        print("<td>")
        print(a.get("text", " "))
        print("</td><td></td>")
    print("<td>")
    print(diagrama[-1].get("text", " "))
    print("</td>")
    print("</tr>")

    # print description
    print("<tr>")
    for a in diagrama[:-1]:
        print("<td>")
        print(a.get("description", " "))
        print("</td><td></td>")
    print("<td>")
    print(diagrama[-1].get("description", " "))
    print("</td>")
    print("</tr>")

    if args.iocs:
        # print iocs
        print('<tr class="iocs">')
        for a in diagrama[:-1]:
            print("<td>")
            tiocs = a.get("iocs", None)
            if not tiocs is None:
                print("<br>".join(tiocs))
            print("</td><td></td>")
        print("<td>")
        tiocs = diagrama[-1].get("iocs", None)
        if not tiocs is None:
            print("<br>".join(tiocs))
        print("</td>")
        print("</tr>")

    if args.ttps:
        # print ttps
        print('<tr class="iocs">')
        for a in diagrama[:-1]:
            tttps = a.get("ttps", None)
            print("<td>")
            if not tttps is None:
                print("<br>".join(tttps))
            print("</td><td></td>")
        print("<td>")
        tttps = diagrama[-1].get("ttps", None)
        if not tttps is None:
            print("<br>".join(tttps))
        print("</td>")
        print("</tr>")

    print("<tr>")
    for a in diagrama[:-1]:
        print("<td></td><td></td>")

    resource_logo = resource_folder + 'logo.png'
    if args.embedall:
        resource_logo = return_image_2_base64(resource_logo)
    print(
        '<td style="text-align:right"><img src="' + resource_logo + '"></td>'
    )
    print("</tr>")
    print("</table>")

    print(
        "<br><br>Generated on "
        + datetime.now().strftime("%Y-%m-%d, %H:%M")
        + " by CTIdiagrams"
    )

    print_resources()
    print(FOOTER)

    if args.output:
        sys.stdout = orig_stdout
        f.close()


if __name__ == "__main__":
    main()
