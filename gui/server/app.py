from flask import Flask, jsonify,request
from flask_cors import CORS
import pandas as pd 
import numpy as np
import ast 
import collections
import json
import random 
# configuration
# from scipy.spatial import distance
import umap 
from sklearn.manifold import TSNE
from scipy.spatial import distance
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
def readjson(file_name):
    try:
        with open(file_name, 'r') as f:
            data = [line.rstrip() for line in f.readlines()] # f.readlines().rstrip
    except:  # for some reason if your json data is in single quotes
        data = []
        with open(file_name, 'r') as f:
            for line in f.readlines():
                line = line.rstrip()
                line = re.sub('\"', '\\"', line)
                line = re.sub('\'', '\"', line)
                line = re.sub('^None$', '\"None\"', line)
                data.append(line)
    data = [json.loads(d) for d in data]
    return pd.DataFrame(data)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/postScatter', methods=['POST'])
def postScatter():
    params = request.get_json()
    application = params['application']
    project = params['projection']
    
    # data = pd.read_csv('../../../../Data/XAI/carts/embeddings/combined_windowed_'+ project+'_moreinfo_link2log.csv')
    # data = pd.read_csv('../../../../Data/gui/scatterplot/07_19_normal_refs/computed/'+project+'.csv')
    data = pd.read_csv('../../../../Data/gui/scatterplot/0805_both_refs/'+project+'.csv')
    print(data.columns)
    data['highlight'] = list(np.zeros(len(data)))
    if application =='all':
        # data = data.to_dict(orient="records")
        # print(type(data))
        return jsonify({
            'test': data.to_dict('records')
        })
    else:
        subdata = data[data['app']==application]
        output = subdata.to_dict('records')
        return jsonify({
            'test': output
        })

@app.route('/postLog',methods =['POST'])
def postLog():
    params = request.get_json()
    selected = params['selected']
    # attribute = params['type']
    # event_type = params['event_type']
    
    selected_pd = pd.DataFrame(selected)
    
    # get unique apps
    instance_ids = selected_pd.app.unique()

    # get unique labels, 
    label_error_flag = []
    label_template_ids = []
    label_embedding_ids = []
    for ele in selected:
        label_error_flag+= ast.literal_eval(ele['error_flag'])
        label_template_ids+= ast.literal_eval(ele['template_ids'])
        label_embedding_ids+= ast.literal_eval(ele['embedding_ids'])
        
    unique_error_flag = collections.Counter(label_error_flag).keys()
    unique_template_ids = collections.Counter(label_template_ids).keys()
    unique_embedding_ids = collections.Counter(label_embedding_ids).keys()
    print(unique_error_flag, unique_template_ids, unique_embedding_ids)
    
    ## generate the data for COUNT heatmap 
    # output_error = []
    # output_template = []
    # output_embed = []
    output_heatmap = []
    y_values = []
    
    
    for index, row in selected_pd.iterrows():
        y_values.append(index)
        error_flag = ast.literal_eval(row['error_flag'])
        template_ids = ast.literal_eval(row['template_ids'])
        embed_ids = ast.literal_eval(row['embedding_ids'])
        
        counter_error =collections.Counter(error_flag)
        counter_template = collections.Counter(template_ids)
        counter_embed = collections.Counter(embed_ids)

        for label in unique_error_flag:
            if label in counter_error.keys():
                output_heatmap.append({
                    'group': str(label),
                    'variable': index,
                    'value': counter_error[label]
                })
        for label in unique_template_ids:
            if label in counter_template.keys():
                output_heatmap.append({
                    'group': str(label),
                    'variable': index,
                    'value': counter_template[label]
                })
        for label in unique_embedding_ids:
            if label in counter_embed.keys():
                output_heatmap.append({
                    'group': str(label),
                    'variable': index,
                    'value': counter_embed[label]
                })
    x_total = list(unique_error_flag)+list(unique_template_ids)+ list(unique_embedding_ids)
    return jsonify({
        # 'data_error': output_error,
        # 'data_template':output_template,
        # 'data_embedding': output_embed,
        'data': output_heatmap,
        'y_values':y_values,
        'x_values': x_total,
        'x_error':list(unique_error_flag),
        'x_template': list(unique_template_ids),
        'x_embedding': list(unique_embedding_ids),
    })

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

@app.route('/getTree', methods=['GET'])
def getTree():
    data = []
    with open('../../../../Data/gui/timeline/fault_tree_scatterplot_eventdrops_lime/round1.json') as f:
        for line in f:
            temp = json.loads(line)
            data.append(temp)
    return jsonify(data)

@app.route('/postTree', methods=['POST'])
def postTree():
    data = []
    app = request.get_json()['app']
    if app=='all':
        with open('../../../../Data/gui/timeline/fault_tree_scatterplot_eventdrops_lime/round1.json') as f:
            for line in f:
                temp = json.loads(line)
                data.append(temp)
    else:
        with open('../../../../Data/gui/timeline/fault_tree_scatterplot_eventdrops_lime/round1.json') as f:
            for line in f:
                temp = json.loads(line)
                this_app = temp['alert']['features'][0]['value']['log_anomaly_data']['source_application_id']
                # print(this_app)
                if this_app==app:
                    data.append(temp)
    return jsonify(data)

@app.route('/postLogline', methods =['POST'])
def postLogline(): 
    ##================================ data for scatterplot ================================
    scatterplot = request.get_json()['scatterplot']
    scatterplot_pd = pd.DataFrame.from_dict(scatterplot)
    
    
    selected = request.get_json()['window_info']['actual_embeddings']
    highlight_ = []
    # print(selected)
    for index, row in scatterplot_pd.iterrows():
        
        embed = ast.literal_eval(row['embeddings'])
        embed_round = [round(b,10) for b in embed]
        # print(embed_round)
        if str(embed_round)==str(selected):
            highlight_.append(1)
            print('yes')
        else:
            highlight_.append(0)
    temp = pd.DataFrame({
        'highlight': highlight_
    })
    scatterplot_pd.update(temp)
    return jsonify({
        'scatterplot': scatterplot_pd.to_dict('records')
    })

@app.route('/findRef', methods=['POST'])
def findRef():
    scatterplot = request.get_json()['scatterplot']
    scatterplot_pd = pd.DataFrame.from_dict(scatterplot)
    # print(scatterplot_pd.columns)
    # print(len(scatterplot_pd))
    scatterplot_pd = scatterplot_pd.loc[scatterplot_pd['anomaly_label']==0]
    # print(len(scatterplot_pd))

    ## get windowed embeddings, find the closet window embedding from the reference windows     
    new_embedding = request.get_json()['window_embedding'] ## selected one 
    log_embeddings_selected = request.get_json()['log_embeddings'] ## selected one 
    distance_list=[]
    
    for ele in scatterplot_pd['embeddings'].tolist():
        try:
            temp = ast.literal_eval(ele)
            d = distance.euclidean(temp, new_embedding)
            distance_list.append(d)
        except:
            print('error')
    min_index = distance_list.index(min(distance_list))
    
    ## get the log embeddings of the min_index
    log_embeddings_ref = ast.literal_eval(scatterplot_pd.iloc[min_index]['log_embeddings'])
    print(log_embeddings_ref)
    print(log_embeddings_selected)
    log_errors = ast.literal_eval(scatterplot_pd.iloc[min_index]['log_original'])
    
    distance_matrix = distance.cdist( log_embeddings_ref, log_embeddings_selected,'euclidean')
    print(distance_matrix.shape)
    distance_matrix_normed = distance_matrix / distance_matrix.max(axis=0)
    x2 = np.ones((distance_matrix.shape))
    x3 = np.subtract(x2, distance_matrix_normed)
    # print(np.array(log_embeddings_selected).shape, np.array(log_embeddings_ref).shape)
    print(distance_matrix.shape)
    
    return jsonify({
        # 'log_embeddings': log_embeddings_ref,
        'ref_errors': log_errors,
        'matrix_distance': x3.tolist()
    })
@app.route('/getTemplate', methods=['GET'])
def getTemplate():
    data = pd.read_json('../../../../Data/XAI/baseline/log_embedding_template.json', lines=True)

    return jsonify(data.to_dict('records'))

@app.route('/baseLine', methods = ['POST'])
def baseLine():
    input_embedding = request.get_json()['actual']
    expected_embedding = request.get_json()['expected']
    log_embeddings = np.array(request.get_json()['logs'])

    ## input - expected 
    substraction_embdding = np.subtract(input_embedding,expected_embedding)
    ## get the largest k dimensions 
    abs_embedding = np.absolute(substraction_embdding)
    # print(abs_embedding)
    k_dimensions = abs_embedding.argsort()[-3:][::-1]
    dimensions_sort = abs_embedding.argsort()[-20:][::-1].tolist()
    dimensions_sort_list = []
    for i in range(len(dimensions_sort)):
        dimensions_sort_list.append({
            'dim':dimensions_sort[i],
            'value': len(dimensions_sort)-i
        })
    log_indicator = []
    for dim in k_dimensions:
        # iv > ev 
        if input_embedding[dim]-expected_embedding[dim]>0:
            output = log_embeddings[log_embeddings[:, dim]>=input_embedding[dim]]
        else:
            output = log_embeddings[log_embeddings[:, dim]<=input_embedding[dim]]
        # print(type(output)) 
    # print(output)
    output = np.unique(output, axis=0).tolist()
    # print(output)
    for i in log_embeddings.tolist():
        if i in output:
            log_indicator.append(1)
        else:
            log_indicator.append(0)       
    return jsonify({
        'dimension_sort': sorted(dimensions_sort_list, key = lambda i: i['dim']),
        'output': log_indicator,
        'test':dimensions_sort,
        'test_linechart': np.random.random_sample(log_embeddings.shape).tolist()
    })
if __name__ == '__main__':
    app.run()