from flask import Flask, jsonify,request
from flask_cors import CORS
import pandas as pd 
import numpy as np
import ast 
import collections
import json
import random 
# configuration
from scipy.spatial import distance
import umap 
from sklearn.manifold import TSNE
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
    data = pd.read_csv('../../../../Data/gui/scatterplot/07_19_normal_refs/computed/'+project+'.csv')
    print(type(data))
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
    output_error = []
    output_template = []
    output_embed = []
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
                output_error.append({
                    'group': str(label),
                    'variable': index,
                    'value': counter_error[label]
                })
        for label in unique_template_ids:
            if label in counter_template.keys():
                output_template.append({
                    'group': str(label),
                    'variable': index,
                    'value': counter_template[label]
                })
        for label in unique_embedding_ids:
            if label in counter_embed.keys():
                output_embed.append({
                    'group': str(label),
                    'variable': index,
                    'value': counter_embed[label]
                })
    
    ## generate data for the sequence event pattern 
    
    sequence_error = []
    x_sequence_error = []
    
    sequence_embedding = []
    sequence_template = []
    for index, row in selected_pd.iterrows():
        flag_list = ast.literal_eval(row['error_flag'])
        
        template_list = ast.literal_eval(row['template_ids'])

        embedding_list = ast.literal_eval(row['embedding_ids'])
        
        for i in range(len(flag_list)):
            if i not in x_sequence_error:
                x_sequence_error.append(i)
            if flag_list[i]==False:
                value = 0
            else:
                value = 1
            sequence_error.append({
                'variable':index,
                'group': i,
                'value': value
            })
            sequence_template.append({
                'variable':index,
                'group':i,
                'value': template_list[i]
            })
            sequence_embedding.append({
                'variable': index,
                'group':i,
                'value': embedding_list[i]
            })
    return jsonify({
        'data_error': output_error,
        'data_template':output_template,
        'data_embedding': output_embed,
        'x_error':list(unique_error_flag),
        'y_values':y_values,
        'x_template': list(unique_template_ids),
        'x_embedding': list(unique_embedding_ids),
        'sequence_error': sequence_error,
        'sequence_embedding': sequence_embedding,
        'sequence_template': sequence_template,
        'sequence_x': x_sequence_error
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
    ## ================================ data for panel D: related log embeddings info ================================
    # one_window = request.get_json()['window_info']
    # output = []

    # start = one_window['alert']['features'][0]['value']['start_timestamp']
    # end = one_window['alert']['features'][0]['value']['end_timestamp']
    # app = one_window['alert']['source']['source_application']['name']
    # reference = readjson('../../../../Data/XAI/carts/embeddings/log_level/cpu_hog.txt')
    # print(reference.columns)
    # print(start, end, app)
    # filtered = reference.loc[(reference['instance_id']==app) & (reference['timestamp']>=start) & (reference['timestamp']<end)]
    # print(len(filtered))
        # print(i)
        # f = reference.loc[reference['embedding_string']==str(i)]
        # if len(f)==0:
        #     print('error')
        # else:
        #     # print(f.index.tolist())
        #     temp = f.drop(['application_id'], axis=1).iloc[0].to_dict()
        #     temp['positive_score'] = random.uniform(0, 1)
        #     temp['positive_uncertainty'] = random.uniform(0, 1)
        #     temp['negative_score'] = random.uniform(0, 1)
        #     output.append(temp)
    ##================================ data for scatterplot ================================
    scatterplot = request.get_json()['scatterplot']
    scatterplot_pd = pd.DataFrame.from_dict(scatterplot)
    

    # embedding_ = np.load('../../../../Data/gui/scatterplot/07_19_normal_refs/computed/allembed.npy')
    new_embedding = request.get_json()['window_embedding']
    embedding_=[]
    for ele in scatterplot_pd['embeddings'].tolist():
        try:
            embedding_.append(ast.literal_eval(ele))
        except:
            embedding_.append(ele)
    list(embedding_).append(new_embedding)

    projection = request.get_json()['projection']
    if projection=='tsne':
        X_embedded = TSNE(n_components=2).fit_transform(embedding_)
    else: 
        X_embedded = umap.UMAP().fit_transform(embedding_)

    temp={
        'anomaly_label': 1,
        'app': request.get_json()['app'],
        'embedding_ids':'',
        'embeddings': new_embedding,
        'error_flag': '',
        'highlight':1,
        'template_ids':'',
        'x': X_embedded[-1,0],
        'y': X_embedded[-1,1]
    }
    scatterplot_pd = scatterplot_pd.append(temp, ignore_index = True)
    # temp1 = list(scatterplot_pd['anomaly_label'].tolist())
    # temp1.append(0)

    # temp2 = list(scatterplot_pd['anomaly_label'].tolist())
    # temp2.append(request.get_json()['app'])

    # temp3 = list(scatterplot_pd['embedding_ids'].tolist())
    # temp3.append('')

    # temp4 = list(scatterplot_pd['error_flag'].tolist())
    # temp4.append('')

    # temp5 = list(scatterplot_pd['highlight'].tolist())
    # temp5.append(1)

    # temp6 = list(scatterplot_pd['template_ids'].tolist())
    # temp6.append('')
    # temp7 = list(scatterplot_pd['embeddings'].tolist())
    # temp7.append(new_embedding)
    # temp8 = list(scatterplot_pd['x'].tolist())
    # temp8.append(X_embedded[-1,0])
    # temp9 = list(scatterplot_pd['y'].tolist())
    # temp9.append(X_embedded[-1,1])

    # # print(X_embedded[-1,0],X_embedded[-1,1])
    # scatterplot_output = pd.DataFrame({
    #     'x': temp8,
    #     'y': temp9,
    #     'anomaly_label': temp1,
    #     'app': temp2,
    #     'embedding_ids':temp3,
    #     'embeddings': temp7,
    #     'error_flag': temp4,
    #     'highlight':temp5,
    #     'template_ids':temp6,
    # })
    return jsonify({
        # 'panel_d':filtered.to_dict('records'),
        'scatterplot': scatterplot_pd.to_dict('records')
        # 'reference': {
        #     'embedding_ids': ref['embedding_ids'],
        #     'error_flag': ref['error_flag'],
        #     'template_ids': ref['template_ids']
        # }
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
        'test':dimensions_sort
    })
if __name__ == '__main__':
    app.run()