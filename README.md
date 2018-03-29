# Documents matching API based on word2vec VSM

This project is an example API for getting the n closest match from the FDA GUDID database, based on a word2vec averaging documents model. 

## Getting Started

Clone the repo to your machine with conda installed with Python 3.6. 

### Prerequisites

Create an environment from the spec file. This will install flask, gensim, numpy and pandas with their dependencies. 

```
conda create --name myenv --file spec-file.txt
```

Activate this environment. 
Get the GUDID full delimited realease, extract it to `data/AccessGUDID_Delimited_Full_Release_yyyymmdd/` or any other location to specify in `params.json`.

```
{
	"gudidfile": "data/AccessGUDID_Delimited_Full_Release_20180102/device.txt",
	"modelfile": "w2v_model.pickle",
	"docmatrixfile": "doc_matrix.npy",
	"textfile": "GUDID_device.txt"
}
```

Note that there is only one input file (`gudidfile`), the others being output temporary files generated after model training. 

### Installing

First run model training on the data. 

```
python w2v_modelbuild.py
```

which will create the following files (file names and locations can be reset in `params.json`: 

```
GUDID_device.txt
doc_matrix.npy
w2v_model.pickle
```

Then run the flask API: 
```
python wv_flask_app_run.py
```

That's it! 

## Running the tests

Running tests on the data can be done with a jupyter notebook. 
An example can be found [here](w2v_flask_api_test.ipynb).
It includes a `%timeit` execution for benchmarking response time. 


## Deployment

Make sure the ports on which you are serving the API are open (default is `5000`). 

## Built With

* [Anaconda](https://www.anaconda.com/) - Python distribution
* [flask](http://flask.pocoo.org/) - Python web framework
* [gensim](https://radimrehurek.com/gensim/) - Unsupervised semantic modelling


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Further reading

* [From Word Embeddings To Document Distances](http://proceedings.mlr.press/v37/kusnerb15.pdf)
