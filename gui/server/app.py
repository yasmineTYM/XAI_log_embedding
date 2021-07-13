from flask import Flask, jsonify,request
from flask_cors import CORS
import pandas as pd 
import numpy as np
import ast 
import collections
import json
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


@app.route('/postScatter', methods=['POST'])
def postScatter():
    params = request.get_json()
    application = params['application']
    project = params['projection']
    
    # data = pd.read_csv('../../../../Data/XAI/carts/embeddings/combined_windowed_'+ project+'_moreinfo_link2log.csv')
    data = pd.read_csv('../../../../Data/gui/scatterplot/'+project+'.csv')
    print(type(data))
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
    # if event_type == 'count':
    #     output = []
    #     y_values = []
    #     x_values = []
    #     for i in instance_ids:
    #         for j in unique_label_list:
    #             x_values.append(str(i)+'_'+str(j))
    #     for index, row in selected_pd.iterrows():
    #         y_values.append(index)
    #         log_count = ast.literal_eval(row[attribute])
    #         counter=collections.Counter(log_count)
    #         for label in unique_label_list:
    #             if label in counter.keys():
    #                 output.append({
    #                     'group': row['app']+'_'+str(label),
    #                     'variable': index,
    #                     'value': counter[label]
    #                 })
    # else:
    #     output = []
        # x_values = []
        # y_values = []
        # for index, row in selected_pd.iterrows():
        #     y_values.append(index)
        #     log_list = ast.literal_eval(row[attribute])
        #     for i in range(len(log_list)):
        #         if i not in x_values:
        #             x_values.append(i)
        #         output.append({
        #             'variable':index,
        #             'group': i,
        #             'value': log_list[i]
        #         })
            

    return jsonify({
        'data_error': output_error,
        'data_template':output_template,
        'data_embedding': output_embed,
        'x_error':list(unique_error_flag),
        'y_values':y_values,
        'x_template': list(unique_template_ids),
        'x_embedding': list(unique_embedding_ids)
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

    # treeData = {
    #     "name": "Top Level",
    #     "children": [
    #     { 
    #         "name": "Level 2: A",
    #         "children": [
    #         { "name": "Son of A" },
    #         { "name": "Daughter of A" }
    #         ]
    #     },
    #     { "name": "Level 2: B" }
    #     ]
    # }
    with open('../../../../Data/XAI/carts/embeddings/log_level/log_by_app/with_label/keywords/tree_data.txt') as json_file:
        treeData = json.load(json_file)
    # treeData = [
    #     {
    #     "name": "Top Level",
    #     "parent": "null",
    #     "children": [
    #         {
    #         "name": "Level 2: A",
    #         "parent": "Top Level",
    #         "children": [
    #         {
    #             "name": "Son of A",
    #             "parent": "Level 2: A"
    #         },
    #         {
    #             "name": "Daughter of A",
    #             "parent": "Level 2: A"
    #         }
    #         ]
    #         },
    #         {
    #             "name": "Level 2: B",
    #             "parent": "Top Level"
    #         }
    #         ]  
    return jsonify(treeData)
if __name__ == '__main__':
    app.run()