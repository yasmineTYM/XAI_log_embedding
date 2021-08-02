<template>
    <div>
        <el-row class="scatter_row"></el-row>
        <el-row style="overflow-x:scroll;height:321px;border-bottom:1px solid grey" class="timeLine">
            <div id="div_timeline"></div>
            <div class="app-container" v-if="show_tree">
                <div class="timeLine" style="overflow: scroll;">
                    <div class="ul_box" :style="{ width: ulWidth + 'px' }">
                        <ul class="my_timeline" ref="mytimeline" style="margin-left: 10px;">
                            <li class="my_timeline_item" v-for="(activity,index) in tree_items" :key="index">
                                <!--圈圈节点-->
                                <span>{{activity.utc_timestamp}}</span>
                                <div class="my_timeline_node" :class="activity.abnormal_flag" :style="{'position':index===tree_items.length-1?'relative':'', 'top':index===tree_items.length-1?'-4px':''}"></div>
                                <!--线-->
                                <div class="my_timeline_item_line" v-if="index !== tree_items.length-1"></div>
                                <!--标注-->
                                <div class="my_timeline_item_content">
                                    <el-card shadow="hover">
                                        <span class="timeline_detail">severity: {{activity.alert.severity}}<br></span>
                                        <span class="timeline_detail">confidence: {{activity.alert.features[0]['value']['log_anomaly_data']['log_anomaly_confidence']}}</span>
                                        <el-button style="float: right; padding: 3px 0" type="text" @click="postLogline(activity)">Select</el-button>
                                        <div :id="activity.div_id"></div>
                                    </el-card>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- <el-timeline>
                <el-timeline-item v-for="(activity, index) in tree_items" :timestamp="activity.utc_timestamp" placement="top" :class="activity.abnormal_flag">
                    <el-card shadow="hover">
                        <span class="timeline_detail">severity: {{activity.alert.severity}}<br></span>
                        <span class="timeline_detail">confidence: {{activity.alert.features[0]['value']['log_anomaly_data']['log_anomaly_confidence']}}</span>
                        <el-button style="float: right; padding: 3px 0" type="text" @click="postLogline(activity)">Select</el-button>
                        <div :id="activity.div_id"></div>
                    </el-card>
                </el-timeline-item>
            </el-timeline> --> 
        </el-row>
        <el-row style="height:620px;"> 
            <el-col :span="19" style="height:620px;border-right:1px solid grey">
                <div style="height:120px; width: 1053px;">
                    <div id="div_event" v-loading="LOAD_D"></div>
                </div>
                <div style="height:220px; width: 1053px;">
                    <div id="div_embed"></div>
                </div>
                <div style="height:320px; width: 1053px;">
                    <div id="div_lime"></div>
                </div>
            </el-col>
            <el-col :span="5">
                <div style="height:620px; width:290px">
                    <div id="div_log_detail">
                        <!-- <VueTabulator v-model="brushed_items" :options="options" /> -->
                    </div>
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
import eventDrops from './src';
// import  "vue-tabulator/dist/scss/bootstrap/tabulator_bootstrap4";
import "tabulator-tables/dist/css/tabulator_simple.min.css"
import Tabulator from 'tabulator-tables';
// import EMBED_TEMPLATE from '../../static/log_embedding_template.json'
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
           eventdrops:[],
           embed_template:[],
           timeline:[],
           ulWidth: null,
           div_width:1110,
           brushed_items: [],
           baseline:[],
           dim_s:[]
        }
    },
    
    created(){
        this.getTreeData()
        
    },
    updated: function(){

    },
    methods: {
        // drawLogline(data){
        //     // console.log(data)
        //     // this.postLogline(data)
        //     d3.select('#div_detail').html('')
        //     const rect_width = 90
        //     const rect_height = 30
        //     const space = 10

        //     var margin = {top: 10, right: 30, bottom: 40, left: 50},
        //         width = d3.max([data.length*(rect_width+space), 1500]),
        //         height = 600 - margin.top - margin.bottom;

        //     // append the svg object to the body of the page
        //     var svg = d3.select("#div_detail")
        //         .append("svg")
        //         .attr("width", width + margin.left + margin.right)
        //         .attr("height", height + margin.top + margin.bottom)
        //         .append("g")
        //         .attr("transform",
        //             "translate(" + margin.left + "," + margin.top + ")");
            
        //     const y_position = 100
        //     // ===================== step1, append line ==================
        //     svg.append('line')
        //     .style('stroke', 'grey')
        //     .style('stroke-width',3)
        //     .attr('x1',0)
        //     .attr('x2',1300)
        //     .attr('y1', y_position)
        //     .attr('y2', y_position);

        //     // ===================step2, append rectangle ==================
        //     var logline = svg.selectAll('.rect')
        //     .data(data)
        //     .enter()
        //     .append('g')
            
           
        //     var rect = logline.append('rect')
        //     .attr("rx", 4)
        //     .attr('width', rect_width)
        //     .attr('height', rect_height)
        //     .attr('x',function(d,i){
        //         return i*rect_width + (i+1)*space
        //     })
        //     .attr('y', y_position-rect_height/2)
        //     .attr('fill',function(d){
        //         if(d['features'][0]['obj_value']['error_flag']=='false'){
        //             return '#91cf60'
        //         }else{
        //             return '#d73027'
        //         }
        //     })
        //     .on('click', function(d){
        //         console.log(d)
        //     })
        //     rect.append('title')
        //     .text(function(d){
        //         return d['message']
        //     })
        //     // ================== step3: append text ==================
        //     var text = logline.append('text')
        //     .text(function(d){
        //         return d['instance_id']
        //     })
        //     .style('text-anchor','middle')
        //     .attr('x',function(d,i){
        //         return (i+0.5)*rect_width + (i+1)*space
        //     })
        //     .attr('y', y_position+3)
           
        //     .style('pointer-events', 'none')


        //     var x_mapping = []
        //     for(let i=0; i<data.length;i++){
        //         x_mapping.push(i)
        //     }
        //     var x = d3.scaleBand()
        //         .domain(x_mapping)
        //         .range([ 0, width ]);

        //     // ================== step4: append score ==================

        //     const score_range = 40
        //     var y1 = d3.scaleLinear()
        //     .domain([0, d3.max(data, function(d) { return +d.positive_score; })])
        //     .range([ score_range, 0 ]);
            
        //     var y2 = d3.scaleLinear()
        //     .domain([0, d3.max(data, function(d) { return +d.negative_score; })])
        //     .range([ score_range, 0 ]);

        //     var line_positive_data = []
        //     var line_negative_data = []
        //     data.forEach(function(d,i){
        //         let x = (i+0.5)*rect_width + (i+1)*space
        //         let y_positive = y_position - y1(d['positive_score'])
        //         let y_negative = y_position + y2(d['negative_score'])
        //         line_positive_data.push({
        //             'x': x,
        //             'y': (y_positive-rect_height/2),
        //         })
        //         line_negative_data.push({
        //             'x':x,
        //             'y':(y_negative+rect_height/2),
        //         })
        //     })

        //     var lineGenerator = d3.line()
        //     // .curve(d3.curveBasis)
        //     // .curve(d3.curveLinear)
        //     .curve(d3.curveCardinal)
        //     .x(function(d){return d.x})
        //     // .y0(function(d){return d.y0})
        //     .y((p)=>p.y);

        //     var path_positive = svg.append('path')
        //     .attr('d', lineGenerator(line_positive_data))
        //     .style('fill','white')
        //     .style('stroke','black')
            
        //     var path_positive = svg.append('path')
        //     .attr('d', lineGenerator(line_negative_data))
        //     .style('fill','white')
        //     .style('stroke','black')

        //     var circles = svg.append('g')
        //     .selectAll('.line_circle')
        //     .data(line_positive_data)
        //     .enter()
        //     .append('circle')
        //     .attr('cx', (d)=> d.x)
        //     .attr('cy', (d)=> d.y)
        //     .attr('r', 3)

        //     var circles = svg.append('g')
        //     .selectAll('.line_circle')
        //     .data(line_negative_data)
        //     .enter()
        //     .append('circle')
        //     .attr('cx', (d)=> d.x)
        //     .attr('cy', (d)=> d.y)
        //     .attr('r', 3)
        // },
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
            var data = this.timeline
            // set the dimensions and margins of the graph
            var margin = {top: 0, right: 30, bottom: 20, left: 60},
                width = 1200 - margin.left - margin.right,
                height = 40 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#div_timeline")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");
            
            
            // Add X axis --> it is a date format
            var x = d3.scaleTime()
            .domain(d3.extent(data, function(d) { return d.date; }))
            .range([ 5, width-5 ]);
            var xAxis = svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

            // Add Y axis
            var y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.value; })])
            .range([ height, 0 ]);
            // var yAxis = svg.append("g")
            // .call(d3.axisLeft(y));

            // Add a clipPath: everything out of this area won't be drawn.
            var clip = svg.append("defs").append("svg:clipPath")
                .attr("id", "clip")
                .append("svg:rect")
                .attr("width", width )
                .attr("height", height )
                .attr("x", 0)
                .attr("y", 0);
                    // Add brushing
            var brush = d3.brushX()                   // Add the brush feature using the d3.brush function
                .extent( [ [0,0], [width,height] ] )  // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
                .on("end", updateChart)               // Each time the brush selection changes, trigger the 'updateChart' function

            // Create the line variable: where both the line and the brush take place
            var line = svg.append('g')
            .attr("clip-path", "url(#clip)")

            // Add the line
            // line.append("path")
            // .datum(data)
            // .attr("class", "line")  // I add the class line to be able to modify this line later on.
            // .attr("fill", "none")
            // .attr("stroke", "steelblue")
            // .attr("stroke-width", 1.5)
            // .attr("d", d3.line()
            //     .x(function(d) { return x(d.date) })
            //     .y(function(d) { return y(d.value) })
            //     )
            var nodes = line.append('g')
            .selectAll('.rr')
            .data(data)
            .enter()
            .append('g')
            .append('circle')
            .attr('class','rr')
            .attr('cx', d=>x(d.date))
            .attr('cy', d=>y(0))
            .attr('r',3)
    // Add the brushing
            line
            .append("g")
                .attr("class", "brush")
                .call(brush);

            // A function that set idleTimeOut to null
            var idleTimeout
            function idled() { idleTimeout = null; }
            var that = this
            // A function that update the chart for given boundaries
            function updateChart() {
                
                // What are the selected boundaries?
                var extent = d3.event.selection
                
                // that.fiterTree(x.invert(extent[0]), x.invert(extent[1]), that)
                // If no selection, back to initial coordinate. Otherwise, update X axis domain
                if(!extent){
                    console.log('yes')
                    if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
                    x.domain([ 4,8])
                }else{
                    let a = x.invert(extent[0])
                    let b = x.invert(extent[1])
                    that.fiterTree(a,b,that)
                    x.domain([ a,b ])
                    line.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
                }

                // Update axis and line position
                xAxis.transition().duration(1000).call(d3.axisBottom(x))
                // line
                //     .select('.line')
                //     .transition()
                //     .duration(1000)
                //     .attr("d", d3.line()
                //         .x(function(d) { return x(d.date) })
                //         .y(function(d) { return y(d.value) })
                //     )
                line.selectAll('.rr').remove()
                line.append('g')
                .selectAll('.rr')
                .data(data)
                .enter()
                .append('g')
                .append('circle')
                .attr('class','rr')
                .attr('cx', d=>x(d.date))
                .attr('cy', d=>y(0))
                .attr('r',3)
            }

             // If user double click, reinitialize the chart
            svg.on("dblclick",function(){
                x.domain(d3.extent(data, function(d) { return d.date; }))
                xAxis.transition().call(d3.axisBottom(x))
                // line
                //     .select('.line')
                //     .transition()
                //     .attr("d", d3.line()
                //     .x(function(d) { return x(d.date) })
                //     .y(function(d) { return y(d.value) })
                // )
                that.postTreeData()
            });


        },
        getTreeData(){
            const path = "http://localhost:5000/getTree"
            
            axios.get(path)
            .then((res)=>{
                // console.log(JSON.parse(res.data))
                // console.log(res.data)
                var that = this
                that.timeline=[]
                var parse = d3.timeParse("%s");

                res.data.forEach(function(d){
                    that.timeline.push({
                        'date': parse(d['timestamp']),
                        'value':1
                    })
                })
                this.drawTimeline()

                this.tree_items = res.data
                this.ulWidth = res.data.length * 300 +200
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
                // console.log(res.data)
                var that = this
                that.timeline=[]
                var parse = d3.timeParse("%s");

                res.data.forEach(function(d){
                    that.timeline.push({
                        'date': parse(d['timestamp']),
                        'value':1
                    })
                })
                this.drawTimeline()
                this.tree_items = res.data
                this.ulWidth = res.data.length * 300 +200
                this.show_tree = true
             
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        fiterTree(start, end, that){
            // console.log(start,end)
            // console.log(that.tree_items)
            that.show_tree = false
            var new_item = []
            var parse = d3.timeParse("%s");
            that.tree_items.forEach(function(d){
                if(parse(d['timestamp'])<end && parse(d['timestamp'])>=start){
                    new_item.push(d)
                    //  console.log('yes')
                }{
                   
                }
            })
            that.tree_items= new_item
            that.ulWidth = new_item.length * 300 +200
            that.show_tree = true
        },
        postLogline(data){
            // console.log(data)
            var that = this
            var coordinate_data = []
            var keys = ['dim1', 'dim2', 'dim3','dim4','dim5','dim6','dim7','dim8','dim9','dim10','dim11','dim12','dim13','dim14','dim15','dim16','dim17','dim18','dim19','dim20'];
            // ================================= 
            var test = "http://localhost:5000/baseLine"
            var payload1 = {
                'actual': data['actual_embeddings'],
                'expected': data.alert.features[0].value.log_anomaly_data.embedding_expected,
                'logs': data['log_embeddings']
            }
            axios.post(test, payload1)
            .then((res)=>{
                console.log(res.data.dimension_sort)
                // console.log(res.data.output)
                that.baseline = res.data.output
                that.dim_s = res.data.dimension_sort
                // ===========================1. append log embeddings ===========================
                var log_embeddings = data['log_embeddings']
                var id = 0
                log_embeddings.forEach(function(d, index){
                    // console.log(that.baseline)
                    var result = {};
                    keys.forEach((key, i) => result[key] = d[i])
                    result['type']='logs'
                    result['player'] = id
                    result['baseline'] = that.baseline[index]
                    // result['dimension'] = that.dim_s[index-1]
                    coordinate_data.push(result)
                    id = id+1
                })
                // ===========================. append actual embeddings  ===========================
                var result = {};
                keys.forEach((key, i) => result[key] = data['actual_embeddings'][i])
                result['type'] = 'actual'
                result['player'] = id
                result['baseline'] = -1
                // result['dimension'] = 0
                id+=1
                coordinate_data.push(result)
                // ===========================. append expected embeddings  ===========================
                var result = {};
                var values = data['alert']['features'][0]['value']['log_anomaly_data']['embedding_expected']
                keys.forEach((key, i) => result[key] = values[i])
                result['player'] = id
                result['type'] = 'expected'
                result['baseline'] = -1
                // result['dimension'] = 0
                coordinate_data.push(result)
                
                // var min = d3.min(all_number)
                // var max = d3.max(all_number)
                var features = []
                keys.forEach(function(d){
                    let e = d3.extent(coordinate_data, p=>p[d])
                    features.push({
                        'name': d,
                        'range': e
                    })
                })
                data['eventdrops'].sort(function(a,b) {return (a.date > b.date) ? 1 : ((b.date > a.date) ? -1 : 0);} );

                this.eventdrops = data['eventdrops']

                let copy_eventdrops = []
                data['eventdrops'].forEach(function(d){
                    copy_eventdrops.push(d)
                })

                this.drawCoordinate(copy_eventdrops,coordinate_data, features,that.dim_s)
                
                this.drawEventDrop(null)
            })
            .catch((error)=>{
                console.log(error)
            })
            // console.log(that.baseline)
            // ================================== update scatterplot 
            
            this.$store.commit('updateLOAD_B', true)
            this.$store.commit('sliceSCATTERPLOT')
            this.LOAD_D = true
            const path = "http://localhost:5000/postLogline"
            const payload = {
                'window_info': data,
                'scatterplot': this.SCATTERPLOT,
                'window_embedding': data['actual_embeddings'],
                'projection': this.SELECTED_PROJECT,
                'app': this.SELECTED_APP
            }
            axios.post(path, payload)
            .then((res)=>{
                // console.log(res.data)
                this.$store.commit('updateLOAD_B', false)
                this.LOAD_D = false
                this.$store.commit('updateSCATTERPLOT', res.data['scatterplot'])
            })
            .catch((error)=>{
                console.log(error)
            })
            this.drawLIME(data['lime'])
        },
        drawEventDrop(id){
            // console.log('func')
            d3.select('#div_event').html('')
            const chart = eventDrops({ d3 });
            var repositoriesData = [{
                name: 'Log Lines',
                id: id,
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
            // console.log(repositoriesData)
            d3.select('#div_event')
                .data([repositoriesData])
                .call(chart);
        },
        drawCoordinate(raw,data, features, dimension){
            /*
            * Parameters
            *****************************/
        //    console.log(data)
            const  padding = 38, brush_width = 20;
            const filters = {};
            var margin = {top: 30, right: 5, bottom: 10, left: 30},
            width = this.div_width - margin.left - margin.right,
            height = 220 - margin.top - margin.bottom;

            /*
            * Helper functions
            *****************************/
            // Horizontal scale
            const xScale = d3.scalePoint()
            .domain(features.map(x=>x.name))
            .range([padding, width-padding]);

            // Each vertical scale
            const yScales = {};
            features.map(x=>{
                // console.log(x.name)
            yScales[x.name] = d3.scaleLinear()
                .domain(x.range)
                .range([height-padding, padding]);
            });
            // Each axis generator
            const yAxis = {};
            d3.entries(yScales).map(x=>{
                yAxis[x.key] = d3.axisLeft(x.value);
            });

            // Each brush generator
            const brushEventHandler = function(feature){
                if (d3.event.sourceEvent && d3.event.sourceEvent.type === "zoom") 
                    return; // ignore brush-by-zoom
                if(d3.event.selection != null){
                    filters[feature] = d3.event.selection.map(d=>yScales[feature].invert(d));
                }else{
                    if(feature in filters)
                    delete(filters[feature]);
                }
                applyFilters();
            }
            var that = this
            const applyFilters = function(){
                // that.brushed_items = []
                d3.select('g.active').selectAll('path')
                .style('display', function(d,i){
                    
                    if(selected(d)){
                        // console.log('yes')
                        if(i<raw.length){
                            that.brushed_items.push(raw[i])
                        }
                        return null
                    }else{
                        // console.log('no')
                        return 'none'
                    }
                })
                    // .style('display', d=>(selected(d)?null:'none'));
            }
                    
            const selected = function(d){
                const _filters = d3.entries(filters);
                return _filters.every(f=>{
                    return f.value[1] <= d[f.key] && d[f.key] <= f.value[0];
                });
            }

            const yBrushes = {};
            d3.entries(yScales).map(x=>{
                let extent = [
                    [-(brush_width/2), padding],
                    [brush_width/2, height-padding]
            ];
            function test(){
                that.brushed_items = []
            }
            yBrushes[x.key]= d3.brushY()
                .extent(extent)
                .on('start',()=>test(x.key))
                // .on('brush', ()=>brushEventHandler(x.key))
                .on('end', ()=>brushEventHandler(x.key));
            });

            // Paths for data
            const lineGenerator = d3.line();

            const linePath = function(d){
                const _data = d3.entries(d).filter(x=>(x.key!='player' & x.key!='type' & x.key!='baseline' ));
                let points = _data.map(x=>([xScale(x.key),yScales[x.key](x.value)]));
                    return(lineGenerator(points));
            }

            /*
            * Parallel Coordinates
            *****************************/
            d3.select('#div_embed').html('')
            // Main svg container
            const pcSvg = d3.select('#div_embed')
            .append('svg')
            .attr('width', width)
            .attr('height', height);

            // Inactive data
            pcSvg.append('g').attr('class','inactive').selectAll('path')
                .data(data)
                .enter()
                .append('path')
                .attr('class', function(d){return d['type']})
                .attr('d', d=>linePath(d));

            // active data
            pcSvg.append('g').attr('class','active').selectAll('path')
                .data(data)
                .enter()
                .append('path')
                .attr('class', function(d){return d['type']+'_'+d['baseline'].toString()})
                .attr('d', d=>linePath(d))
                .style('stroke-width','2px');

            // Vertical axis for the features
            const featureAxisG = pcSvg.selectAll('g.feature')
                .data(features)
                .enter()
                .append('g')
                .attr('class','feature')
                .attr('transform',d=>('translate('+xScale(d.name)+',0)'))
                
            featureAxisG
                .append('g')
                .each(function(d){
                    d3.select(this).call(yAxis[d.name]);
                });

            featureAxisG
            .each(function(d){
                d3.select(this)
                .append('g')
                .attr('class','brush')
                .call(yBrushes[d.name]);
            });

            // featureAxisG
            // .append("text")
            // .attr("text-anchor", "middle")
            // .attr('y', padding/2)
            // .text(d=>d.name);


            var dim_x = d3.scalePoint()
            .domain(Object.keys(dimension))
            .range([padding, width-padding])

            
            var dim_y = d3.scaleLinear()
            .domain([0, dimension.length])
            .range([30,0])

            var line_data = []
            dimension.forEach(function(d){
                line_data.push({
                    'x': dim_x(d['dim']),
                    'y': dim_y(d['value'])
                })
            })
            // console.log(line_data)
            var lineGenerator_dim = d3.line()
            .curve(d3.curveStepAfter)
            .x(d=>d.x)
            .y(d=>d.y)

            var path = pcSvg.append('path')
            .attr('d', lineGenerator_dim(line_data))
            .style('fill', 'white')
            .style('stroke-width','3px')
            .style('stroke','#D79771')

             // Add the scatterplot
            var dots = pcSvg.selectAll("dot")
            .data(line_data)
            .enter().append("circle")
            .style('opacity',1)
            .style('fill','#B05B3B')
            .attr("r", 4)
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

        },
     
        drawLIME(data){
            d3.select('#div_lime').html('')
            var data = data.replace('[(','').replace(')]','').split('), (')
            

            var draw_data =[]
            data.forEach(function(d){
                let value = parseFloat(d.split(',')[1])
                let key = d.split(',')[0].replace("'",'')
                let id = key.split(' ')[0]
                draw_data.push({
                    'key': key,
                    'value': value,
                    'id': parseInt(id)
                })

            })
            // console.log(draw_data)
            draw_data = draw_data.slice(0, 40)
            // console.log(data)
            // set the dimensions and margins of the graph
            var margin = {top: 30, right: 5, bottom: 70, left: 30},
                width = this.div_width - margin.left - margin.right,
                height = 320 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#div_lime")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");
                        // X axis
            var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(draw_data.map(function(d) { return d.key; }))
            .padding(0.4);
            

            // Add Y axis
            var yp = d3.scaleLinear()
            .domain([0,0.5])
            .range([ height/2,0]);

            var yn = d3.scaleLinear()
            .domain([-0.5,0])
            .range([height/2, 0]);

            svg.append("g")
            .call(d3.axisLeft(d3.scaleLinear()
            .domain([-0.5,0.5])
            .range([height,0])));

            //  svg.append("g")
            // .call(d3.axisLeft(yn));

            // Bars
            var bars = svg.selectAll("mybar")
            .data(draw_data)
            .enter()
            .append("rect")
            .attr("x", function(d) { return x(d.key); })
            .attr("y", function(d) { 
                if(d.value>0){
                    return yp(d.value)
                }else{
                    return height/2
                }
                return 0; })
            .attr("width", x.bandwidth())
            .attr("height", function(d) { 
                if(d.value>0){
                    return height/2-yp(d.value)
                }else{
                    return yn(d.value)
                }
             })
            .attr("fill", function(d){
                if(d.value>0){
                    return '#ED6663'
                }else{
                    return '#4E89AE'
                }
            })
        
            var that = this
            bars.append('title')
            .text(function(d){
                return that.embed_template[d.id]['message']
            })

            svg.append("g")
            .attr("transform", "translate(0," + height/2 + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-45)")
            .style("text-anchor", "end");

            // console.log(this.embed_template)
        },
        getTemplate(){
            const path = "http://localhost:5000/getTemplate"
            
            axios.get(path)
            .then((res)=>{
                // console.log(JSON.parse(res.data))
                // console.log(res.data)
                this.embed_template = res.data
                // this.drawTimeline()
                // this.tree_items = res.data
                // this.show_tree = true
                
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        drawTable(){
            var that = this
            console.log(that.brushed_items)
            var tableData = []
            that.brushed_items.forEach(function(d){
                tableData.push({
                    'message': d['message'],
                    'instance_id': d['instance_id'],
                    'timestamp': d['timestamp'],
                    'error_flag': d['features'][0]['obj_value']['error_flag']
                })
            })
            var table = new Tabulator("#div_log_detail", {
                data: tableData,
                height:'620px',
                // width: '270px',
                layout: "fitColumns",
                pagination:"local",
                paginationSize:6,
                paginationSizeSelector:[3, 6, 8, 10],
                movableColumns:true,
                columns:[
                    {title: 'message', field:'message', tooltip:true},
                    {title: 'app', field: 'instance_id'},
                    {title: 'timestamp', field: 'timestamp'},
                    {title: 'flag', field:'error_flag'}
                ]
            })
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
            // console.log(this.SCATTERPLOT)
        },
        LOG_ID(){
            console.log(this.LOG_ID)
        },
        brushed_items(){
            console.log(this.brushed_items)
            this.drawTable()
        }

    },
    mounted(){
        this.getTemplate();
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
        },
        LOG_ID(){
            return this.$store.getters.LOG_ID
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
.el-card__body{
    height:200px;
    padding:0px;
    text-align: start;
    
}
.el-card{
    width:280px;
}

ul{
    padding-inline-start: 20px;
}

/* timeline */
.ul_box {
  /* width: 2800px; */
  height: 270px;
  /* width:100%; */
  display: inline-block;
  float: left;
  overflow:auto;
  overflow-y:hidden
}
.my_timeline{
    display: inline-block;
    overflow: auto;
    overflow-y: hidden;
    max-width: 100%;
}
.my_timeline_item {
  display: inline-block;
  width: 300px;
  vertical-align: top;
}
.abnormal{
  width:10px;
  height: 10px;
  color: red;
  font-size: 18;
  background: red;
  box-sizing: border-box;
  border-radius: 50%;
}
.unknown{
  width:10px;
  height: 10px;
  color: red;
  font-size: 18;
  background: red;
  box-sizing: border-box;
  border-radius: 50%;
}
.uncertain{
  width:10px;
  height: 10px;
  color: orange;
  font-size: 18;
  background: orange;
  box-sizing: border-box;
  border-radius: 50%;
}
.normal{
  width:10px;
  height: 10px;
  color: green;
  font-size: 18;
  background: green;
  box-sizing: border-box;
  border-radius: 50%;
}
.my_timeline_item_line {
  width: 300px;
  height: 10px;
  margin: -6px 0 0 10px;
  border-top: 2px solid #E4E7ED;
  border-left: none;
}
.my_timeline_item_content {
  margin: 10px 0 0 -10px;
  display: flex;
  flex-flow: column;
  cursor: pointer;
}

/* scroll bar  */
.timeLine::-webkit-scrollbar-track {
  /* -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  background-color: #F5F5F5; */
}

.timeLine::-webkit-scrollbar {
  width: 4px;
  background-color: white;
}

.timeLine::-webkit-scrollbar-thumb {
  /* border-radius: 6px;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
  background-color: rgb(197, 194, 194); */
}
g.inactive path, g.active path{
  fill: none;
  stroke: lightgrey;
  stroke-linecap:"round"
}

g.active .expected_-1{ 
    stroke: #66bd63;
}
g.active .actual_-1{
    stroke: #d73027;
}
/* normal log embeddings not in the baseline result */
g.active .logs_0{
    stroke:#92c5de;
}
/* result generated by baseline model  */
g.active .logs_1{
    stroke: #2166ac;
}
.feature .domain{
    stroke: #BBBBBB;
}
.feature .tick line{
    stroke: #BBBBBB;
}
.feature .tick text{
    fill: #BBBBBB;
}
</style>