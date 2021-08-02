<template>
    <div>
        <el-row class="scatter_row">
            <el-col :span="12">
                <el-select v-model="selected_app" placeholder="application">
                    <el-option
                    v-for="item in applications"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span="12">
                <el-select v-model="selected_project" placeholder="projections">
                    <el-option
                    v-for="item in projections"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
        </el-row>
        <el-row>
            <div style="height:320px; border-bottom:1px solid grey;border-right:1px solid grey">
                <div id="div_scatter" v-loading="LOAD_B">
                    <el-slider v-model="hexbin_radius_ratio" style="width:70px; margin-left:5px" @change="draw"></el-slider>
                </div>
            </div>
        </el-row>
        <el-row>
            <div style="height:620px;border-right:1px solid grey; overflow:scroll" class="heatmap_div">
                <el-row>
                     <div id="div_heatmap_count_error"></div>
                </el-row>
                <el-row>
                    <div id="div_heatmap_count_template"></div>
                </el-row>
                <el-row>
                    <div id="div_heatmap_count_embedding"></div>
                </el-row>
                <!-- <el-row>
                    <el-col :span="3">
                       
                    </el-col>
                    <el-col :span="3">
                        
                    </el-col>
                    <el-col :span="3">
                        
                    </el-col>
                    <el-col :span="10">
                        <div id="div_heatmap_sequence_error"></div>
                    </el-col>
                </el-row> -->
            </div>
        </el-row>
        
        
        
    </div>
</template>


<script>
import * as d3 from 'd3'
import axios from 'axios'
import * as d3Lasso from "d3-lasso"
import * as d3Hexbin from 'd3-hexbin'
export default{
    data(){
        return{
            lasso_selected: [],
            applications: [            
            {
                value:'all',
                label:'all'
            },
            {
                value: "front-end",
                label: "front-end"
            },
            {
                value: 'carts',
                label: 'carts'
            }, {
                value: 'carts-db',
                label: 'carts-db'
            }, {
                value: 'catalogue',
                label: 'catalogue'
            }, {
                value: 'orders',
                label: 'orders'
            },{
                value: 'orders-db',
                label: 'orders-db'
            },{
                value: "payment",
                label: "payment"
            },
            {
                value:'shipping',
                label:'shipping'
            },{
                value:'queue-master',
                label:'queue-master'
            },{
                value:'user-db',
                label:'user-db'
            },{
                value:'user',
                label:'user'
            }],
            projections:[{
                'value': 'tsne',
                'label': 't-SNE'
            },{
                'value':'umap',
                'label':'UMAP'
            }], 
            // selected_event: 'count',
            selected_app: 'carts',
            selected_project:'tsne',
            hexbin_radius_ratio:20,
            scatterplotData: null 
        }
    },
    
    created(){
        this.request_postScatter()
    },
    methods: {
        request_postScatter(){
            const path = 'http://localhost:5000/postScatter'
            const payload = {
                'application': this.selected_app,
                'projection': this.selected_project
            }
            axios.post(path, payload)
            .then((res)=>{
                // console.log(res.data['test'])
                // console.log(res.data)
                this.scatterplotData = res.data['test']
                this.$store.commit('updateSCATTERPLOT', res.data['test'])
                this.draw()
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        request_postLog(){
         
            const path = 'http://localhost:5000/postLog'
            var payload={
                'selected': this.lasso_selected
            }
            axios.post(path, payload)
            .then((res)=>{
                console.log(res.data)
                this.draw_heatmap(180,'Count of Error Flag','#div_heatmap_count_error',res.data['data_error'], res.data['x_error'], res.data['y_values'])
                this.draw_heatmap(180,'Count of Template', '#div_heatmap_count_template', res.data['data_template'], res.data['x_template'], res.data['y_values'])
                this.draw_heatmap(180,'Count of Embedding','#div_heatmap_count_embedding', res.data['data_embedding'], res.data['x_embedding'], res.data['y_values'])
                // this.draw_heatmap(500,'Sequence of Error Flag','#div_heatmap_sequence_error', res.data['sequence_error'], res.data['sequence_x'], res.data['y_values'])
            })
        },
        draw_heatmap(size,Title,div_id,DATA,myGroups,myVars){
            // var DATA = RAW['heatmapdata']
            d3.select(div_id).html('')
            // set the dimensions and margins of the graph
            var margin = {top: 30, right: 10, bottom: 50, left: 50},
            width = d3.max([400,myGroups.length*20]) - margin.left - margin.right,
            height = 210 - margin.top - margin.bottom;
            // append the svg object to the body of the page
            var svg = d3.select(div_id)
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("id", div_id)
            .attr("transform","translate(" + margin.left + "," + margin.top + ")");
            
            svg.append('g')
            .append('text')
            .attr('font-size','12px')
            .attr('y',-8)
            .attr('x',width/2)
            .attr('text-anchor','middle')
            .text(Title)
            // Labels of row and columns
            // var myGroups = RAW['x_values']
            // var myVars = RAW['y_values']

            // Build X scales and axis:
            var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(myGroups)
            .padding(0.01);
            svg.append("g")
            .attr("class",'x_axis')
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-25)");
            // Build X scales and axis:
            var y = d3.scaleBand()
            .range([ height, 0 ])
            .domain(myVars)
            .padding(0.01);
            svg.append("g")
            .attr('class','y_axis')
            .call(d3.axisLeft(y));

            // Build color scale
            var myColor = d3.scaleLinear()
            .range(["#bdc9e1", "#045a8d"])
            .domain(d3.extent(DATA, d => d.value))

            var rects = svg.selectAll()
                .data(DATA, function(d) {return d.group+':'+d.variable;})
                .enter()
                .append("rect")
                .attr("x", function(d) { return x(d.group) })
                .attr("y", function(d) { return y(d.variable) })
                .attr("width", x.bandwidth() )
                .attr("height", y.bandwidth() )
                .style("fill", function(d) { return myColor(d.value)} )
            rects.append('title').text(function(d){return d.value})
            // })

            var ticks = d3.selectAll(div_id+" .y_axis .tick text");
            var space = parseInt(DATA.length/10)
            ticks.each(function(_,i){
                if(i%space !== 0) d3.select(this).remove();
            });

            // var lines = d3.selectAll(div_id+" .y_axis .tick line");
            // var space = parseInt(DATA.length/10)
            // lines.each(function(_,i){
            //     if(i%space !== 0) d3.select(this).remove();
            // });


            // var ticks = d3.selectAll('#div_heatmap_count_embedding'+" .y_axis .tick text");
            // var space = parseInt(DATA.length/5)
            // ticks.each(function(_,i){
            //     if(i%space !== 0) d3.select(this).remove();
            // });

        },
        
        draw(){
            // console.log('ttttt')
            var data = this.SCATTERPLOT
            d3.selectAll('#div_scatter svg').remove()
            // var data = new Array(100).fill(null).map(m=>[Math.random(),Math.random()]);
            var w = 350, margin=5;
            var h = 260;
            var r = 3.5;
            var that = this;

            // console.log(data)
            function zoomed() {
                // console.log(d3.event.transform)
                // this.hexbin_radius_ratio = parseInt(d3.event.transform.k)
                g.style("stroke-width", 1.5 / d3.event.transform.k + "px");
                // g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")"); // not in d3 v4
                g.attr("transform", d3.event.transform); // updated for d3 v4
            }
            var zoom = d3.zoom() 
            .scaleExtent([1, 8])
            .on("zoom", zoomed);
            var svg = d3.select("#div_scatter").append("svg")
                .attr("width",w+margin)
                .attr("height",h+margin)
                .call(zoom);

            var scale_x = d3.scaleLinear()
                .domain(d3.extent(data, d => d.x))
                .range([ r, w ]);
            var scale_y = d3.scaleLinear()
                .domain(d3.extent(data, d => d.y))
                .range([ r, h ]);
             // Reformat the data: d3.hexbin() needs a specific format
            var inputForHexbinFun = []
            data.forEach(function(d) {
                inputForHexbinFun.push( [scale_x(d.x), scale_y(d.y), d['anomaly_label'], d,d['highlight']] )  // Note that we had the transform value of X and Y !
            })
             // Prepare a color palette
            var color = d3.scaleLinear()
                .domain([0, 289]) // Number of points in the bin?
                .range(["transparent",  "#69b3a2"])

            // Compute the hexbin data
            var hexbin = d3Hexbin.hexbin()
                .radius(4*(20/that.hexbin_radius_ratio))// size of the bin in px
                .extent([ [0, 0], [w+margin, h+margin] ])
            var colors = d3.scaleOrdinal(d3.schemeCategory10).range().slice(0, 4);
            
            var attenuation = d3.scaleLog().range([0,1]);
            attenuation.domain([.1, d3.max(hexbin(inputForHexbinFun).map(function(d) { return d.length; }))]);
            // Plot the hexbins
            svg.append("clipPath")
                .attr("id", "clip")
                .append("rect")
                .attr("width", w+margin)
                .attr("height", h+margin)
            var g = svg.append("g")
                g.attr("clip-path", "url(#clip)")
                .selectAll("path")
                .data( hexbin(inputForHexbinFun) )
                .enter().append("path")
                .attr("d", hexbin.hexagon())
                .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
                .on('mouseover', function (d, i) {
                    console.log(d)
                    d3.select(this).style('stroke-width','1')
                })
                .on('mouseout', function(d,i){
                    // console.log(d)
                    d3.select(this).style('stroke-width','0.1')
                })
                .on('click', function(d,i){
                    that.lasso_selected = []
                    d.forEach(function(p){
                        that.lasso_selected.push(p[3])
                    })
                    that.request_postLog()
                })
                .attr("fill", function(d, i) { 
                    var counts = [0,0];
                    d.forEach(function(p) {
                        let index = parseInt(p[4])
                        counts[index]++;
                    });
                    // // console.log(counts)
                    let output = counts.reduce(function(p, c, i) { 
                        let temp = d3.interpolateLab(p, colors[i])(c / d.length);
                        // console.log(temp)
                        return temp
                    }, "white")
                    // // console.log(output)
                    return output;
                    // console.log(d.length)
                    // return color(d.length);
                 })
                .style('opacity', function(d) { 
                    let temp = attenuation(d.length)
                    // console.log(temp)
                    return temp; })
                .attr("stroke", "black")
                .attr("stroke-width", "0.1")        
        },
        // draw(data){
        //     console.log(data)
        //     d3.select('#div_scatter').html('')
        //     // var data = new Array(100).fill(null).map(m=>[Math.random(),Math.random()]);
        //     var w = 380, margin=5;
        //     var h = 280;
        //     var r = 3.5;
        //     var that = this;

        //     var svg = d3.select("#div_scatter").append("svg")
        //         .attr("width",w+margin)
        //         .attr("height",h+margin);
           
        //     var scale_x = d3.scaleLinear()
        //         .domain(d3.extent(data, d => d.x))
        //         .range([ r, w ]);
        //     var scale_y = d3.scaleLinear()
        //         .domain(d3.extent(data, d => d.y))
        //         .range([ r, h ]);
        //     var circles = svg.selectAll("circle")
        //         .data(data)
        //         .enter()
        //         .append("circle")
        //         .attr('class',function(d){
        //             if(d['anomaly_label']==0){
        //                 return 'normal';
        //             }else{
        //                 return 'abnormal'
        //             }
        //         })
        //         .attr("cx",d=>scale_x(d['x']))
        //         .attr("cy",d=>scale_y(d['y']))
        //         .attr("r",r)
                
        //     // Lasso functions
        //     var lasso_start = function() {
        //         that.lasso_selected = []
        //         lasso.items()
        //             .attr("r",3.5) // reset size
        //             .classed("not_possible",true)
        //             .classed("selected",false);
        //     };

        //     var lasso_draw = function() {
            
        //         // Style the possible dots
        //         lasso.possibleItems()
        //             .classed("not_possible",false)
        //             .classed("possible",true);

        //         // Style the not possible dot
        //         lasso.notPossibleItems()
        //             .classed("not_possible",true)
        //             .classed("possible",false);
        //     };

        //     var lasso_end = function() {
        //         // Reset the color of all dots
        //         lasso.items()
        //             .classed("not_possible",false)
        //             .classed("possible",false);

        //         // Style the selected dots
        //         var selected_nodes = lasso.selectedItems()
        //             .classed("selected",true)
        //             .attr("r",7)
        //             .attr('test', function(d){
        //                 that.lasso_selected.push(d)
        //             });

        //         // Reset the style of the not selected dots
        //         lasso.notSelectedItems()
        //             .attr("r",3.5);
        //         that.request_postLog()
        //     };
        //     //  var lasso = .lasso();
        //     var lasso = d3Lasso.lasso()
        //         .closePathSelect(true)
        //         .closePathDistance(100)
        //         .items(circles)
        //         .targetArea(svg)
        //         .on("start",lasso_start)
        //         .on("draw",lasso_draw)
        //         .on("end",lasso_end);
            
        //     svg.call(lasso);
        // }
    
    
    
    },
    watch:{
        selected_project(){
            this.request_postScatter()
        },
        selected_app(){
            this.$store.commit('updateSELECTED_APP', this.selected_app)
            this.request_postScatter()
        },
        selected_project(){
            this.$store.commit('updateSELECTED_PROJECT', this.selected_project)
        },
        SCATTERPLOT(){
            this.draw()
        }
        
    },
    mounted(){

    },
    computed:{
        LOAD_B(){
            return this.$store.getters.LOAD_B
        },
        SCATTERPLOT(){
            return this.$store.getters.SCATTERPLOT
        }
    }
}
</script>

<style>
circle {
    fill-opacity: 0.5;
}
.scatter_row{
    background-color:#515E63; 
    height:34px;
    border-radius: 5px;
    
}
.normal {
    fill: #346751;
    /* stroke:hsl(0, 3%, 73%);
    stroke-width:1; */
    /* fill-opacity: 0.5; */
}
.abnormal {
    fill: #c84b31;
    stroke:hsl(0, 3%, 73%);
    stroke-width:1;
    /* fill-opacity: 0.5; */
}
.lasso path {
    stroke: rgb(80,80,80);
    stroke-width:2px;
}

.lasso .drawn {
    fill-opacity:.05 ;
}

.lasso .loop_close {
    fill:none;
    stroke-dasharray: 4,4;
}

.lasso .origin {
    fill:#515E63;
    fill-opacity:.5;
}

.not_possible {
    fill: rgb(200,200,200);
}

.possible {
    fill: #EC888C;
}

.selected {
    fill: steelblue;
}

.scatter_row .el-input__inner {
    border-radius: 8px;
    padding-right: 20px;
    height: 28px;
    width:120px;
    background-color:#515E63;
    color: white;
}
.el-row {
    margin-bottom:5px
}
.el-slider__button {
    width: 6px;
    height: 6px;
    /* margin-top: 10px; */
}

/* scroll bar  */
.heatmap_div::-webkit-scrollbar-track {
  /* -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  background-color: #F5F5F5; */
}
.heatmap_div::-webkit-scrollbar {
  width: 4px;
  background-color: white;
}
.heatmap_div::-webkit-scrollbar-thumb {
  /* border-radius: 6px;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
  background-color: rgb(197, 194, 194); */
}
</style>