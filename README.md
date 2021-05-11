# Propositional-Calculus-Application
___
This is a Python application regarding Propositional Calculus. 
Firstly `pcabuilder` defines the propositions, then `pcabuilder` which extends the application with law applications, truth table creation for all possible interpretations and other functionalities. The `pcabuilder` is initialized with a string, which is parsed and transformed into proposition with the `pcaparser` file. Finally, the `pcacontroller` is used to create an API which is used with the [Front-End](https://github.com/p2424630/PCA-Front).

<hr style="border:2px solid gray"> </hr>

### Setup

___

1. Have python installed (recommended miniconda)
2. Run `pip install -e PCA_DIRECTORY`
3. Navigate to folder and run `uvicorn pcacontroller:app` to start the API server. Use `--port PORT` to specify the port
   and `--reload` to have automatic reload of server on file change.

<hr style="border:2px solid gray"> </hr>

### Usage

___

![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "pcabuilder image"
   
<hr style="border:2px solid gray"> </hr>

### License

___

The project is MIT licenced.
>More info can be found [here](https://github.com/p2424630/PCA/blob/test/LICENSE)
