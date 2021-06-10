from flask import Flask, jsonify,request
from flask_cors import CORS
import pandas as pd 
import numpy as np
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/getNode', methods=['GET'])
def getNode():
    data = pd.read_csv('../../pre_analysis/760_large_v_removed.csv')
    output = data.to_dict('records')
    return jsonify(output)

@app.route('/postEmbedding', methods=['POST'])
def postEmbedding():
    params = request.get_json()
    selected = params['selected']
    selected_index = []
    for ele in selected:
        selected_index.append(ele['Unnamed: 0'])
    ## get embeddings of selected nodes
    selected_embedding = []
    embedding = np.load('../../pre_analysis/760_large_v_removed.npy')
    for ele in selected_index:
        selected_embedding.append(embedding[ele])
    
    
    output = []
    size0 = np.array(selected_embedding).shape[0]
    size1 = np.array(selected_embedding).shape[1]
    for i in range(len(selected_embedding)):
        for dim in range(len(selected_embedding[i])):
            temp = {
                'variable': np.float64(i),
                'group': np.float64(dim),
                'value': np.float64(selected_embedding[i][dim])
            }
            output.append(temp)
    X = [np.float64(ele) for ele in range(0,size1)]
    Y = [np.float64(ele) for ele in range(0,size0)]

    ## get the logs
    data = pd.read_csv('../../pre_analysis/bert_position_withLog.csv')
    text = []
    for ele in selected_index:
        text.append(data.iloc[ele]['log'])

    return jsonify({
        'heatmapdata':output,
        'x_values': X,
        'y_values': Y,
        'text':text
    })
if __name__ == '__main__':
    app.run()