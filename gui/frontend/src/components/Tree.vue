<template>
    <div>
         <el-row>
            <el-col :span="5" style="border-right:1px solid grey">
                <div style="overflow:scroll;height:620px">
                    <div>
                        <div id="div_timeline"></div>
                        <el-timeline>
                            <el-timeline-item v-for="(activity, index) in tree_items" :timestamp="activity.utc_timestamp" placement="top" :class="activity.abnormal_flag">
                                <el-card shadow="hover">
                                    <span class="timeline_detail">severity: {{activity.alert.severity}}<br></span>
                                    <span class="timeline_detail">confidence: {{activity.alert.features[0]['value']['log_anomaly_data']['log_anomaly_confidence']}}</span>
                                    <el-button style="float: right; padding: 3px 0" type="text" @click="postLogline(activity)">Select</el-button>
                                    <div :id="activity.div_id"></div>
                                </el-card>
                            </el-timeline-item>
                        </el-timeline>
                    </div>
                </div>
            </el-col>
            <el-col :span="19">
                 
                 <div style="height:220px; width: 1400px;overflow:scroll">
                   <!-- <el-row  class="scatter_row"></el-row> -->
                    <div id="div_event" v-loading="LOAD_D"></div>
                </div>
                <div style="height:220px; width: 1400px;">
                   <!-- <el-row  class="scatter_row"></el-row> -->
                    <div id="div_embed"></div>
                </div>
            </el-col>
        </el-row>

        
    </div>
</template>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import cloud from "d3-cloud"
import * as d3Timeline from 'd3-timelines'
import eventDrops from '../src';
// import '../src/style.css';
// import { gravatar, humanizeDate } from './utils';
// import * as eventDrops from 'event-drops';
export default{
    data(){
        return{
           text_detail:'ttt',
           tree_items: null,
           show_tree: false,
           showDetail: true,
           LOAD_D: false,
           eventdrops:[]
        }
    },
    
    created(){
        this.getTreeData()
        
    },
    updated: function(){

    },
    methods: {
       
        drawLogline(data){
            // console.log(data)
            // this.postLogline(data)
            d3.select('#div_detail').html('')
            const rect_width = 90
            const rect_height = 30
            const space = 10

            var margin = {top: 10, right: 30, bottom: 40, left: 50},
                width = d3.max([data.length*(rect_width+space), 1500]),
                height = 600 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#div_detail")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");
            
            const y_position = 100
            // ===================== step1, append line ==================
            svg.append('line')
            .style('stroke', 'grey')
            .style('stroke-width',3)
            .attr('x1',0)
            .attr('x2',1300)
            .attr('y1', y_position)
            .attr('y2', y_position);

            // ===================step2, append rectangle ==================
            var logline = svg.selectAll('.rect')
            .data(data)
            .enter()
            .append('g')
            
           
            var rect = logline.append('rect')
            .attr("rx", 4)
            .attr('width', rect_width)
            .attr('height', rect_height)
            .attr('x',function(d,i){
                return i*rect_width + (i+1)*space
            })
            .attr('y', y_position-rect_height/2)
            .attr('fill',function(d){
                if(d['features'][0]['obj_value']['error_flag']=='false'){
                    return '#91cf60'
                }else{
                    return '#d73027'
                }
            })
            .on('click', function(d){
                console.log(d)
            })
            rect.append('title')
            .text(function(d){
                return d['message']
            })
            // ================== step3: append text ==================
            var text = logline.append('text')
            .text(function(d){
                return d['instance_id']
            })
            .style('text-anchor','middle')
            .attr('x',function(d,i){
                return (i+0.5)*rect_width + (i+1)*space
            })
            .attr('y', y_position+3)
           
            .style('pointer-events', 'none')


            var x_mapping = []
            for(let i=0; i<data.length;i++){
                x_mapping.push(i)
            }
            var x = d3.scaleBand()
                .domain(x_mapping)
                .range([ 0, width ]);

            // ================== step4: append score ==================

            const score_range = 40
            var y1 = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.positive_score; })])
            .range([ score_range, 0 ]);
            
            var y2 = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.negative_score; })])
            .range([ score_range, 0 ]);

            var line_positive_data = []
            var line_negative_data = []
            data.forEach(function(d,i){
                let x = (i+0.5)*rect_width + (i+1)*space
                let y_positive = y_position - y1(d['positive_score'])
                let y_negative = y_position + y2(d['negative_score'])
                line_positive_data.push({
                    'x': x,
                    'y': (y_positive-rect_height/2),
                })
                line_negative_data.push({
                    'x':x,
                    'y':(y_negative+rect_height/2),
                })
            })

            var lineGenerator = d3.line()
            // .curve(d3.curveBasis)
            // .curve(d3.curveLinear)
            .curve(d3.curveCardinal)
            .x(function(d){return d.x})
            // .y0(function(d){return d.y0})
            .y((p)=>p.y);

            var path_positive = svg.append('path')
            .attr('d', lineGenerator(line_positive_data))
            .style('fill','white')
            .style('stroke','black')
            
            var path_positive = svg.append('path')
            .attr('d', lineGenerator(line_negative_data))
            .style('fill','white')
            .style('stroke','black')

            var circles = svg.append('g')
            .selectAll('.line_circle')
            .data(line_positive_data)
            .enter()
            .append('circle')
            .attr('cx', (d)=> d.x)
            .attr('cy', (d)=> d.y)
            .attr('r', 3)

            var circles = svg.append('g')
            .selectAll('.line_circle')
            .data(line_negative_data)
            .enter()
            .append('circle')
            .attr('cx', (d)=> d.x)
            .attr('cy', (d)=> d.y)
            .attr('r', 3)
        },
        drawDetail(div_id, raw){
            d3.select('#'+div_id).html('')
            var ti = raw['template_ids']
            var cv = raw['count_vector']
            var ecv = raw['expected_count_vector']

            var data = []
            ti.forEach(function(d,i){
                data.push({
                    'group': d,
                    'countv': cv[i],
                    'ecountv': ecv[i]
                })
            })

            var margin = {top: 10, right: 30, bottom: 40, left: 50},
                width = 300 - margin.left - margin.right,
                height = 140 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#"+div_id)
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");
            
            // List of subgroups = header of the csv files = soil condition here
            var subgroups = ['group', 'countv','ecountv'].slice(1)

            // List of groups = species here = value of the first column called group -> I show them on the X axis
            var groups = d3.map(data, function(d){return(d.group)}).keys()
            
            // console.log(groups, subgroups)
            // Add X axis
            var x = d3.scaleBand()
                .domain(groups)
                .range([0, width])
                .padding([0.2])
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x).tickSize(0))
                .selectAll("text")  
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-45)");

            var v1 = d3.extent(data, d => d.countv)[1]
            var v2 = d3.extent(data, d=> d.ecountv)[1]
            
            // console.log(v1,)
             // Add Y axis
            var y = d3.scaleLinear()
                .domain([0, d3.max([v1, v2])])
                .range([ height, 0 ]);
            svg.append("g")
                .call(d3.axisLeft(y));

            // Another scale for subgroup position?
            var xSubgroup = d3.scaleBand()
                .domain(subgroups)
                .range([0, x.bandwidth()])
                .padding([0.05])
            // color palette = one color per subgroup
            var color = d3.scaleOrdinal()
                .domain(subgroups)
                .range(['#D49A89','#557571'])
            // Show the bars
            svg.append("g")
                .selectAll("g")
                // Enter in data = loop group per group
                .data(data)
                .enter()
                .append("g")
                .attr("transform", function(d) { return "translate(" + x(d.group) + ",0)"; })
                .selectAll("rect")
                .data(function(d) { 
                    let temp = subgroups.map(function(key) { return {key: key, value: d[key]}; })
                    // console.log(temp)
                    return temp; })
                .enter().append("rect")
                .attr("x", function(d) { return xSubgroup(d.key); })
                .attr("y", function(d) { return y(d.value); })
                .attr("width", xSubgroup.bandwidth())
                .attr("height", function(d) { return height - y(d.value); })
                .attr("fill", function(d) { return color(d.key); });
            //Legend
            
            var legend = svg.selectAll(".legend")
                .data(['real','expected'])
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", function(d,i) { return "translate(0," + i * 20 + ")"; })
                .style("opacity","0");

            legend.append("rect")
                .attr("x", width - 18)
                .attr("width", 10)
                .attr("height", 10)
                .style("fill", function(d) { return color(d); });

            legend.append("text")
                .attr("x", width - 20)
                .attr("y", 7)
                .attr("dy", ".25em")
                .style("text-anchor", "end")
                .style('font-size',12)
                .text(function(d) {return d; });

            legend.transition().duration(500).delay(function(d,i){ return 1300 + 100 * i; }).style("opacity","1");
        },  
        drawTimeline(){
            d3.select('#div_timeline').html('')
            var testData = [
                {label: "person a", times: [
                    {"starting_time": 1355752800000, "ending_time": 1355759900000},
                    {"starting_time": 1355767900000, "ending_time": 1355774400000}]},
                {label: "person b", times: [
                    {"starting_time": 1355759910000, "ending_time": 1355761900000}]},
                {label: "person c", times: [
                    {"starting_time": 1355761910000, "ending_time": 1355763910000}]}
            ];
            var chart = d3Timeline.timelines()
            // .axisZoom()
            .orient('top');

            var svg = d3.select("#div_timeline").append("svg").attr("width", 364)
            .datum(testData).call(chart);

        },
        getTreeData(){
            const path = "http://localhost:5000/getTree"
            
            axios.get(path)
            .then((res)=>{
                // console.log(JSON.parse(res.data))
                console.log(res.data)
                this.drawTimeline()
                this.tree_items = res.data
                this.show_tree = true
                
            })
            .catch((error)=>{
                console.log(error)
            })

        },
        postTreeData(){
            this.show_tree = false
            const path = "http://localhost:5000/postTree"
            const payload = {
                'app': this.SELECTED_APP
            }
            axios.post(path, payload)
            .then((res)=>{
                console.log(res.data)
                
                this.drawTimeline()
                this.tree_items = res.data
                this.show_tree = true
             
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        drawTree(treeData){
            var that = this
        // ************** Generate the tree diagram	 *****************
            var margin = {top: 40, right: 120, bottom: 20, left: 120},
                width = 960 - margin.right - margin.left,
                height = 500 - margin.top - margin.bottom;
            var svg = d3.select("#div_tree").append("svg")
                .attr("width", width + margin.right + margin.left)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate("
                    + margin.left + "," + margin.top + ")");

            var i = 0,
                duration = 750,
                root;

            // declares a tree layout and assigns the size
            var treemap = d3.tree().size([height, width]);
            
            // Assigns parent, children, height, depth
            root = d3.hierarchy(treeData, function(d) { return d.children; });
            root.x0 = height / 2;
            root.y0 = 0;
            // Collapse after the second level
            root.children.forEach(collapse);

            update(root);

            // Collapse the node and all it's children
            function collapse(d) {
                if(d.children) {
                    d._children = d.children
                    d._children.forEach(collapse)
                    d.children = null
                }
            }

            function update(source) {

            // Assigns the x and y position for the nodes
            var treeData = treemap(root);

            // Compute the new tree layout.
            var nodes = treeData.descendants(),
                links = treeData.descendants().slice(1);
            // console.log(links)
            // Normalize for fixed-depth.
            nodes.forEach(function(d){ d.y = d.depth * 180});

            // ****************** Nodes section ***************************
            var num2radius = d3.scaleLinear()
            .domain([1000, 127264]) // unit: km
            .range([6,10]) // unit: pixels

            // Update the nodes...
            var node = svg.selectAll('g.node')
                .data(nodes, function(d) {return d.id || (d.id = ++i); });

            // Enter any new modes at the parent's previous position.
            var nodeEnter = node.enter().append('g')
                .attr('class', 'node')
                .attr("transform", function(d) {
                    // return "translate(" + source.y0 + "," + source.x0 + ")";
                    return "translate(" + source.x0 + "," + source.y0 + ")";
                })
                .on('click', click);

            // Add Circle for the nodes
            nodeEnter.append('circle')
                .attr('class', 'node')
                .attr('r', function(d){
                    // console.log(d)
                    let data = d3.select(this).data()[0]['data']
                    return num2radius(data['num'])
                    // console.log(data)
                    // return 1e-6
                })
                .style("fill", function(d) {
                    return d._children ? "lightsteelblue" : "#fff";
                });

            // Add labels for the nodes
            nodeEnter.append('text')
                .attr("dy", function(d,i){
                    if(i%2==0){
                        return 20
                    }else{
                        return -20
                    }
                })
                .attr("x", function(d) {
                    return 13
                    // return d.children || d._children ? -13 : 13;
                })
                .attr("text-anchor", function(d) {
                    return "middle"
                    // return d.children || d._children ? "end" : "start";
                })
                .style('pointer-events','none')
                .text(function(d) { return d.data.name; });

            // UPDATE
            var nodeUpdate = nodeEnter.merge(node);

            // Transition to the proper position for the node
            nodeUpdate.transition()
                .duration(duration)
                .attr("transform", function(d) { 
                    return "translate(" + d.x + "," + d.y + ")";
                    // return "translate(" + d.y + "," + d.x + ")";
                });

            // Update the node attributes and style
            nodeUpdate.select('circle.node')
                .attr('r', function(d){
                    let data = d3.select(this).data()[0]['data']
                    return num2radius(data['num'])
                })
                .style("fill", function(d) {
                    return d._children ? "lightsteelblue" : "#fff";
                })
                .attr('cursor', 'pointer')
                .on('dblclick',function(d){
                    // console.log(d)
                    let data = d3.select(this).data()[0]['data']
                    that.drawWordCloud(data)
                });


            // Remove any exiting nodes
            var nodeExit = node.exit().transition()
                .duration(duration)
                .attr("transform", function(d) {
                    return "translate(" + source.x + "," + source.y + ")";
                    // return "translate(" + source.y + "," + source.x + ")";
                })
                .remove();

            // On exit reduce the node circles size to 0
            nodeExit.select('circle')
                .attr('r', 1e-6);

            // On exit reduce the opacity of text labels
            nodeExit.select('text')
                .style('fill-opacity', 1e-6);

            // ****************** links section ***************************

            // Update the links...
            var link = svg.selectAll('path.link')
                .data(links, function(d) { return d.id; });
            // console.log(link)
            // Enter any new links at the parent's previous position.
            var linkEnter = link.enter().insert('path', "g")
                .attr("class", "link")
                .attr('d', function(d){
                    // var o = {x: source.x0, y: source.y0}
                    var o = {y: source.y0, x: source.x0}
                    return diagonal(o, o)
                });

            // UPDATE
            var linkUpdate = linkEnter.merge(link);

            // Transition back to the parent element position
            linkUpdate.transition()
                .duration(duration)
                .attr('d', function(d){ return diagonal(d, d.parent) });

            // Remove any exiting links
            var linkExit = link.exit().transition()
                .duration(duration)
                .attr('d', function(d) {
                    var o = {x: source.x, y: source.y}
                    return diagonal(o, o)
                })
                .remove();

            // Store the old positions for transition.
            nodes.forEach(function(d){
                d.x0 = d.x;
                d.y0 = d.y;
            });

            // Creates a curved (diagonal) path from parent to the child nodes
            function diagonal(s, d) {
                //horizontal 
                // var path = `M ${s.y} ${s.x}
                //         C ${(s.y + d.y) / 2} ${s.x},
                //         ${(s.y + d.y) / 2} ${d.x},
                //         ${d.y} ${d.x}`

                //vertical1
                 var path = `M ${s.x} ${s.y}
                        C ${s.x} ${(s.y+d.y)/2},
                        ${d.x} ${(s.y+d.y)/2},
                        ${d.x} ${d.y}`

                // vertical2 

                // var path = `M ${s.x} ${s.y}
                //         C ${(s.x + d.x) / 2} ${s.y},
                //         ${(s.x + d.x) / 2} ${d.y},
                //         ${d.x} ${d.y}`

                return path
            }

            // Toggle children on click.
            function click(d) {
                if (d.children) {
                    d._children = d.children;
                    d.children = null;
                } else {
                    d.children = d._children;
                    d._children = null;
                }
                update(d);
            }
            
            } 
        },
        drawWordCloud(data){
            d3.select('#div_detail').html('')
            var myWords = data['keywords']
            // set the dimensions and margins of the graph
            var margin = {top: 10, right: 10, bottom: 10, left: 10},
                width = 450 - margin.left - margin.right,
                height = 450 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#div_detail").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

            // Constructs a new cloud layout instance. It run an algorithm to find the position of words that suits your requirements
            // Wordcloud features that are different from one word to the other must be here
            var layout = cloud()
            .size([width, height])
            .words(myWords.map(function(d) { return {text: d.word, size:d.size}; }))
            .padding(5)        //space between words
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .fontSize(function(d) { return 20; })      // font size of words
            .on("end", draw);
            layout.start();

            // This function takes the output of 'layout' above and draw the words
            // Wordcloud features that are THE SAME from one word to the other can be here
            var fill = d3.scale.category20();
            function draw(words) {
            svg
                .append("g")
                .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
                .selectAll("text")
                    .data(words)
                .enter().append("text")
                    .style("font-size", '20px')
                    .style("fill", "steerblue")
                    .attr("text-anchor", "middle")
                    .style("font-family", "Impact")
                    .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                    })
                    .text(function(d) { return d.text; });
            }
        },
        postLogline(data){
            // console.log(data)
            this.$store.commit('sliceSCATTERPLOT')
            console.log(this.SCATTERPLOT.length)
            var coordinate_data = []
            var keys = ['dim1', 'dim2', 'dim3','dim4','dim5','dim6','dim7','dim8','dim9','dim10','dim11','dim12','dim13','dim14','dim15','dim16','dim17','dim18','dim19','dim20'];
            var all_number = []

            var result = {};
            keys.forEach((key, i) => result[key] = data['actual_embeddings'][i])
            result['type'] = 'actual'
            all_number = all_number.concat(data['actual_embeddings'])
            coordinate_data.push(result)
            // console.log(data['actual_embeddings'])
            var result = {};
            var values = data['alert']['features'][0]['value']['log_anomaly_data']['embedding_expected']
            keys.forEach((key, i) => result[key] = values[i])
            result['type'] = 'expected'
            all_number = all_number.concat(values)
            coordinate_data.push(result)
            // console.log(values)
            var log_embeddings = data['log_embeddings']
            log_embeddings.forEach(function(d){
                var result = {};
                all_number = all_number.concat(d)
                keys.forEach((key, i) => result[key] = d[i])
                result['type']='logs'
                coordinate_data.push(result)
            })
            // console.log(all_number)
            var min = d3.min(all_number)
            var max = d3.max(all_number)
            // console.log(coordinate_data, min,max);
            //prepare data for coordinates

            this.drawCoordinate(coordinate_data, keys, min, max)
            this.eventdrops = data['eventdrops']
            this.drawEventDrop()
            // console.log(data)
            if(this.SELECTED_PROJECT=='tsne'){
                var temp={
                    'anomaly_label':1,
                    'app': this.SELECTED_APP,
                    'embedding_ids':'',
                    'error_flag':'',
                    'highlight':1,
                    'template_ids':'',
                    'x': data['tsne_x'],
                    'y': data['tsne_y']
                }
                this.$store.commit('pushSCATTERPLOT', temp)
            }else if(this.SELECTED_PROJECT=='umap'){
                var temp={
                    'anomaly_label':1,
                    'app': this.SELECTED_APP,
                    'embedding_ids':'',
                    'error_flag':'',
                    'highlight':1,
                    'template_ids':'',
                    'x': data['umap_x'],
                    'y': data['umap_y']
                }
                this.$store.commit('pushSCATTERPLOT', temp)
            }
        },
        drawEventDrop(){
            const chart = eventDrops({ d3 });
            var repositoriesData = [{
                name: 'Log Lines',
                data: []
            }]
            this.eventdrops.forEach(function(d,i){
                // var time = new Date(d['timestamp']);
                // time.setSeconds(time.getSeconds() + 8*i);
                var time = new Date(d['timestamp']);
                repositoriesData[0].data.push({
                    date: time,
                    embeddings: d['embeddings'],
                    instance_id: d['instance_id'],
                    error_flag: d['features'][0]['obj_value']['error_flag'],
                    template_id: d['features'][0]['obj_value']['template_id'],
                    positive_score: d['positive_score'],
                    message: d['message']
                })
            })
            
            console.log(repositoriesData)
            d3.select('#div_event')
                .data([repositoriesData])
                .call(chart);
        },
        drawCoordinate(data,dimensions,min,max){
            d3.select('#div_embed').html('')
            // set the dimensions and margins of the graph
            var margin = {top: 30, right: 50, bottom: 10, left: 50},
            width = 1400 - margin.left - margin.right,
            height = 220 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#div_embed")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

            // Color scale: give me a specie name, I return a color
            var color = d3.scaleOrdinal()
                .domain(["actual", "expected", "logs" ])
                .range([ "red", "blue", "yellow"])

            // Here I set the list of dimension manually to control the order of axis:
            // dimensions = ["Petal_Length", "Petal_Width", "Sepal_Length", "Sepal_Width"]

            // For each dimension, I build a linear scale. I store all in a y object
            
            var y = {}
            for (let i in dimensions) {
                name = dimensions[i]
                y[name] = d3.scaleLinear()
                .domain( [min,max] ) // --> Same axis range for each group
                // --> different axis range for each group --> .domain( [d3.extent(data, function(d) { return +d[name]; })] )
                .range([height, 0])
            }

            // Build the X scale -> it find the best position for each Y axis
            var x = d3.scalePoint()
                .range([0, width])
                .domain(dimensions);
            // Highlight the specie that is hovered
            var highlight = function(d){
                var selected_specie = d.type
                // first every group turns grey
                d3.selectAll(".line")
                // .transition().duration(200)
                .style("stroke", "lightgrey")
                .style("opacity", "0.2")
                // Second the hovered specie takes its color
                d3.selectAll("." + selected_specie)
                // .transition().duration(200)
                .style("stroke", color(selected_specie))
                .style("opacity", "1")
            }
                        // Unhighlight
            var doNotHighlight = function(d){
                d3.selectAll(".line")
                // .transition().duration(200).delay(1000)
                .style("stroke", function(d){ return( color(d.type))} )
                .style("opacity", "1")
            }

            // The path function take a row of the csv as input, and return x and y coordinates of the line to draw for this raw.
            function path(d) {
                return d3.line()(dimensions.map(function(p) { return [x(p), y[p](d[p])]; }));
            }

            // Draw the lines
            svg.selectAll("myPath")
                .data(data)
                .enter()
                .append("path")
                .attr("class", function (d) { return "line " + d.type } ) // 2 class for each line: 'line' and the group name
                .attr("d",  path)
                .style("fill", "none" )
                .style("stroke", function(d){ return( color(d.type))})
                .style('stroke-width',function(d){
                    if(d.type == 'actual' || d.type=='expected'){
                        return 4
                    } else{
                        return 2
                    }
                })
                .style("opacity", 0.5)
                .on("mouseover", highlight)
                .on("mouseleave", doNotHighlight )

            // Draw the axis:
            svg.selectAll("myAxis")
                // For each dimension of the dataset I add a 'g' element:
                .data(dimensions).enter()
                .append("g")
                .attr("class", "axis")
                // I translate this element to its right position on the x axis
                .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
                // And I build the axis with the call function
                .each(function(d) { d3.select(this).call(d3.axisLeft().ticks(5).scale(y[d])); })
                // Add axis title
                .append("text")
                .style("text-anchor", "middle")
                .attr("y", -9)
                .text(function(d) { return d; })
                .style("fill", "black")

        }

    },
    watch:{
        show_tree(){
            var that = this
            setTimeout(function () {
                // console.log('test')
                // console.log(d3.select('#div0'))
                that.tree_items.forEach(function(d){
                    that.drawDetail(d['div_id'], d['alert']['features'][0]['value']['log_anomaly_data']['text_dict'])
                })
            }, 10);    
        },
        SELECTED_APP(){
            this.postTreeData()
        },
        SCATTERPLOT(){
            console.log(this.SCATTERPLOT)
        }

    },
    mounted(){
         let recaptchaScript = document.createElement('script')
        recaptchaScript.setAttribute('src', 'https://unpkg.com/d3')
        let js2 = document.createElement('script')
        js2.setAttribute('src','https://unpkg.com/event-drops')

       

        document.head.appendChild(recaptchaScript)
        document.head.appendChild(js2)
    },
    computed:{
        SELECTED_APP(){
            return this.$store.getters.SELECTED_APP
        },
        SCATTERPLOT(){
            return this.$store.getters.SCATTERPLOT
        },
        SELECTED_PROJECT(){
            return this.$store.getters.SELECTED_PROJECT
        }
    }
}
</script>

<style>
@import 'https://unpkg.com/event-drops/dist/style.css';

.node circle {
  fill: #fff;
  stroke: steelblue;
  stroke-width: 3px;
}

.node text {
  font: 12px sans-serif;
}

.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 2px;
}

.el-timeline-item__tail{
    border-left: 2px solid #D6D2C4
}
.normal .el-timeline-item__node{
    background-color: #9DAB86
}
.abnormal .el-timeline-item__node{
    background-color: #CC7351
}
.normal .el-timeline-item__node{
    background-color: #9DAB86
}
.both .el-timeline-item__node{
    background-color: #CC7351
}
.unknown .el-timeline-item__node{
    background-color: #CC7351
}
.el-timeline-item__wrapper{
    width:290px;
}
.el-timeline-item__content{
    width:290px;
}
.el-card__body{
    height:200px;
    padding:0px;
    text-align: start;
    
}
.timeline_detail{
    margin-left: 20px;
    padding-top:10px;
    /* border-left: steelblue 3px solid; */
}
ul{
    padding-inline-start: 20px;
}
</style>