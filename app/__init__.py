import pyndri
from flask import Flask, request, g, render_template
import logging
import os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(__name__)


def get_index():
    index = getattr(g, 'index', None)

    if index is None:
        logging.info('Loading index.')

        index_path = os.environ.get('INDEX_PATH', None)
        assert index_path is not None and os.path.isdir(index_path)

        index = pyndri.Index(index_path)
        g.index = index

        logging.info('Opened index %s.', index)

    dictionary = getattr(g, 'dictionary', None)

    if dictionary is None:
        logging.info('Extracting dictionary.')

        dictionary = pyndri.extract_dictionary(index)
        g.dictionary = dictionary

    return index, dictionary


@app.teardown_appcontext
def teardown_index(exception):
    index = getattr(g, 'index', None)

    if index is not None:
        logging.info('Closing index.')

        index.close()


def build_smoothing_rule(smoothing_method, smoothing_param):
    if smoothing_method == 'jm':
        assert smoothing_param > 0.0 and smoothing_param <= 1.0

        return (
            'method:linear,collectionLambda:{:.2f},'
            'documentLambda:{:.2f}'.format(
                smoothing_param, 1.0 - smoothing_param))
    elif smoothing_method == 'dirichlet':
        assert smoothing_param >= 0

        return 'method:dirichlet,mu:{}'.format(int(smoothing_param))
    else:
        return None


@app.route("/")
def search():
    index, dictionary = get_index()

    query_string = request.args.get('q', None)

    smoothing_method = request.args.get('smoothing_method', 'dirichlet')
    smoothing_param = float(request.args.get('smoothing_param', 1000))
    results_requested = int(request.args.get('results_requested', 10))

    documents = []

    if query_string is not None:
        logging.info('Query string: %s', query_string)

        highlighted_token_ids = set()

        if not query_string.startswith('docid:'):
            for token in index.tokenize(pyndri.escape(query_string)):
                if dictionary.has_token(token):
                    highlighted_token_ids.add(
                        dictionary.translate_token(token))

        def _include_document(int_doc_id):
            ext_doc_id, doc_token_ids = index.document(int_doc_id)

            def _format_token(token_id):
                term = dictionary[token_id]

                if token_id in highlighted_token_ids:
                    term = '<strong>{}</strong>'.format(term)

                return term

            doc_tokens = [_format_token(token_id)
                          if token_id > 0 else '&lt;unk&gt;'
                          for token_id in doc_token_ids]

            documents.append((ext_doc_id, ' '.join(doc_tokens)))

        if query_string.startswith('docid:'):
            ext_document_id = query_string[6:]
            lookup = dict(index.document_ids([ext_document_id]))

            if lookup:
                _include_document(lookup[ext_document_id])
        else:
            query_env = pyndri.QueryEnvironment(
                index, rules=(
                    build_smoothing_rule(smoothing_method, smoothing_param),))

            results = query_env.query(query_string,
                                      results_requested=results_requested)

            for int_doc_id, _ in results:
                _include_document(int_doc_id)

    return render_template('index.html',
                           query=query_string,
                           results=documents,
                           smoothing_method=smoothing_method,
                           smoothing_param=smoothing_param)
