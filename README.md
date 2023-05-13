
# ID3 Algorithm Implementation

Generating a binary decision tree based on a dataset.



## Data Preparation
The data should be prepared in a .csv file format. The dataset should be in a long format with two levels of headers. The first level should consist of condition names, and the next level should contain values for each condition. Conclusions should be placed in the last columns of the table.

### Example Data Structure

![structure](examples/lecture/data_structure.png)
    
## Required Libraries

```
numpy
pandas
anytree
tkinter
```


## Execution

After running the `ID3.py` script, you need to select the location of the data file. The script will generate a `tree.dot` file that represents the connections between elements of the binary decision tree, and an `ID3.png` file if GraphViz software is detected. The contents of the `.dot` file for the example data will look like this:
```
digraph tree {
    "0. mieszka: wieś";
    "1a. wiek: <20";
    "2a. płeć: K";
    "3a. konkluzja: Prasa";
    "3b. wiek: 20-30";
    "4a. konkluzja: Telewizja";
    "4b. konkluzja: Prasa";
    "2b. konkluzja: Internet";
    "1b. konkluzja: Telewizja";
    "0. mieszka: wieś" -> "1a. wiek: <20";
    "0. mieszka: wieś" -> "1b. konkluzja: Telewizja";
    "1a. wiek: <20" -> "2a. płeć: K";
    "1a. wiek: <20" -> "2b. konkluzja: Internet";
    "2a. płeć: K" -> "3a. konkluzja: Prasa";
    "2a. płeć: K" -> "3b. wiek: 20-30";
    "3b. wiek: 20-30" -> "4a. konkluzja: Telewizja";
    "3b. wiek: 20-30" -> "4b. konkluzja: Prasa";
}
```


## Visualization

The binary decision tree will be exported to `ID3.png` if [GraphViz](https://graphviz.org/) is installed. All graph element attributes, such as color, shape, and arrow descriptions, will be preserved.

![GraphViz](examples/lecture/ID3.png)

The tree generated in `.dot` format can also be visualized without installing any additional software using the online version: [GraphVizOnline](https://dreampuf.github.io/GraphvizOnline/)

![GraphViz](examples/lecture/graphviz.png)
