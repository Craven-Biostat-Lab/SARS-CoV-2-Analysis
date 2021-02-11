# Protein Analysis Tool 

## Easily generate graphs of interactions stemming from a protein of your choice.

## Prerequisites and setup

* [Python 3+](https://www.python.org/)
* [Tkinter](https://docs.python.org/3/library/tkinter.html)

This tool only requires Tkinter as an outside prerequisite. To install, run `sudo apt-get install python-tk` from your Linux terminal, or follow [these instructions](https://tkdocs.com/tutorial/install.html) on a different operating system.


## Using the tool

To start, run `python main.pyw` from this directory, or simply double click the program in your file explorer. After a bit of preparation, this will summon the graphical analysis tool:

![base](img/base.png)

### Step one: selecting a protein

First, we must specify a protein to originate as our "home node" within the generated graph. All connections will stem from this original protein, be it proteins with direct connections, or proteins connecting to those connections (a layer 2).

![step1](img/step1.png)

We first enter the symbol of the protein at hand, which is not case-sensitive. Then, we specify max distance away from this protein; as of now, we can only look at 1 or 2 edges away, since anything more than that would take immense computational power to display in Tkinter (greater distances will be possible with a purely terminal-based version of this program for HPC systems). Note that, even with beefier consumer computers, a max distance of 2 will take a few minutes to compute, and will seemingly freeze the window. Do not close the program during this time.

We can specify if we'd like the results sorted alphabetically, before finally asking the program to generate results with the `"Generate graph!"` button.

In the example above, we're searching for proteins interacting directly with the `mov10` protein. We check that we want these results sorted alphabetically. This brings us to step two:

### Step two: viewing results

Results are displayed in the text box to the right. Interactions between two proteins are displayed as `proteinA >> proteinB`, as explained below the header. 

![step2](img/step2.png)

Interactions are clustered by layer. First shown are any proteins interacting directly with our targeted protein. If max distance is set to 2, it will then list all interactions branching out from this first layer of connections as a second layer.

Regardless of max distance specified, the program will then search for all viral interactions with each protein involved in the graph. This is displayed as the final cluster, under the header `## VIRAL INTERACTIONS:`, as below.

![step2b](img/step2b.png)

"But hey! This is a really long list! What if I want to jump directly to a specific protein in one of the layers?" Well, I'm glad you asked. That brings us to step three:

### Step three: jumping to a specific protein

We can use this last feature to jump to a protein of our choosing. The text box will automatically scroll to wherever the protein is located in the layer specified, and if it can't find the protein at hand, it will say so in a small error message.

![step3](img/step3.png)