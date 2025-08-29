# CTIDiagram #

### New version release 2.1

A minor adjustment to close the modal with the ESCAPE key, very useful when presenting diagrams.

Now is possible to embed all the resources, icons included, only the screenshots or none to create light web pages.

If you want to share the result, like in the conferences, is better to embed all the resources.
To have a website more or less organized, embed only the screenshots and maintain the icons folder.
If you are very tidy, don't embed the resources and just keep them well organized.


### New version release 2.0

``` 
It includes now the option to embed screenshots if you click in the icon.
This is very useful for interactive presentations.
The feature was developed for Pwnterrey 2025 event.
The original format changed a bit, new samples will be coming.
```

This is an intent to produce attack diagrams in a quick and standard way.

Basically it converts yaml file describing the attack flow of some malware to an html with icons, iocs and ttps, then we can share them as html files or make a screenshot and add them to the CTI reports.

The YAML file is basic and descriptive, other details could be added.


### Origins

In a previous work, I needed to produce illustrations on how the attacks were conducted, if you read any CTI report you will find some of this illustrations or diagrams.
We use graphical software to produce this diagrams, aka PowerPoint for example, but I prefer to work in text, so the idea was to have a text file and produce the diagram, you can share the text file, update it, keep it in git or run diff over it.



## Some examples: 

![Casbaneiro](https://github.com/hugo-glez/ctidiagram/blob/main/results/casbaneiro.png)
![Mekotio](https://github.com/hugo-glez/ctidiagram/blob/main/results/mekotio.png)
![Fake CAPTCHA](https://github.com/hugo-glez/ctidiagram/blob/main/results/fc1.html)
