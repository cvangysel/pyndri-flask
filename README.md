pyndri-flask
============

pyndri-flask is an example application that demonstrates how [pyndri](http://github.com/cvangysel/pyndri) can be used to serve an Indri index using [Flask](http://github.com/cvangysel/pyndri).

<img src="screenshot.png?raw=true" width="500px" alt="Screenshot of pyndri-flask showing the search box and retrieval model configuration." />

It can be used as the basis for a search engine or as a convenient way to navigate an index for Information Retrieval research.

Requirements
------------

pyndri-flask has the same requirements as [pyndri](http://github.com/cvangysel/pyndri) and it is advised to first follow the instructions to install pyndri before attempting to install pyndri-flask.

You will also need to install Flask:

	pip install Flask==0.12.2
	
Getting started
---------------

After installing Flask, pyndri-flask can be started as follows. First, change your current working directory to the repository root and then execute:

	INDEX_PATH=<PATH TO INDRI INDEX> \
	FLASK_APP=app flask run -h 0.0.0.0 -p 8888

This will start an instance of pyndri-flask that listens to port 8888 on all network interfaces configured on your machine. It will return results of the index referenced by `INDEX_PATH`.

Citation
--------

If you use pyndri to produce results for your scientific publication, please refer to our [ECIR 2017](https://arxiv.org/abs/1701.00749) paper.

	@inproceedings{VanGysel2017pyndri,
	  title={Pyndri: a Python Interface to the Indri Search Engine},
	  author={Van Gysel, Christophe and Kanoulas, Evangelos and de Rijke, Maarten},
	  booktitle={ECIR},
	  volume={2017},
	  year={2017},
	  organization={Springer}
	}

License
-------

pyndri-flask and pyndri are licensed under the [MIT license](LICENSE). Please note that [Indri](http://www.lemurproject.org/indri.php) is licensed separately. If you modify pyndri-flask in any way, please link back to this repository.
