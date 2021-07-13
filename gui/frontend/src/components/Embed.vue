<template>
    <div>
        <el-row>
            <el-col :span="5">
                <div style="height:340px; border: 1px solid black; margin-right:3px">
                    <el-row style="background-color:#002d9c; height:34px" class="scatter_row">
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
                        <!-- <el-col :span="6">
                            <el-select v-model="selected_attribute" placeholder="log Info">
                                <el-option
                                v-for="item in attributes"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="6">
                            <el-select v-model="selected_event" placeholder="event/not">
                                <el-option
                                v-for="item in events"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col> -->
                    </el-row>
                    <el-row>
                        <div id="div_scatter"></div>
                    </el-row>
                </div>
            </el-col>
            <el-col :span="19">
                <div style="height:340px; border: 1px solid black;">
                    <el-row style="background-color:#002d9c; height:34px" class="scatter_row">
                        
                    </el-row>
                    <el-row>
                        <div id="div_heatmap"></div>
                    </el-row>
                </div>
            </el-col>
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
                value:'shipping',
                label:'shipping'
            },{
                value:'queue-master',
                label:'queue-master'
            },{
                value:'user-db',
                label:'user-db'
            }],
            projections:[{
                'value': 'tsne',
                'label': 't-SNE'
            },{
                'value':'umap',
                'label':'UMAP'
            }],
            attributes:[{
                'value': 'error_flag',
                'label': 'error/not'
            },{
                'value':'linkage',
                'label':'log pattern'
            }],
            events: [{
                'value': 'count',
                'label': 'count'
            },{
                'value': 'sequence',
                'label': 'sequence'
            }],
            selected_event: 'count',
            selected_app: 'all',
            selected_project:'umap',
            selected_attribute: 'error_flag'
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
                console.log(res.data['test'])
                // console.log(res.data)
                this.draw(res.data['test'])
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        draw(data){
            console.log(data)
            d3.select('#div_scatter').html('')
            // var data = new Array(100).fill(null).map(m=>[Math.random(),Math.random()]);
            var w = 380, margin=5;
            var h = 280;
            var r = 3.5;
            var that = this;

            var svg = d3.select("#div_scatter").append("svg")
                .attr("width",w+margin)
                .attr("height",h+margin);
            
            var scale_x = d3.scaleLinear()
                .domain(d3.extent(data, d => d.x))
                .range([ r, w ]);
            var scale_y = d3.scaleLinear()
                .domain(d3.extent(data, d => d.y))
                .range([ r, h ]);
            var circles = svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr('class',function(d){
                    if(d['anomaly_label']==0){
                        return 'normal';
                    }else{
                        return 'abnormal'
                    }
                })
                .attr("cx",d=>scale_x(d['x']))
                .attr("cy",d=>scale_y(d['y']))
                .attr("r",r)
                
            // Lasso functions
            var lasso_start = function() {
                that.lasso_selected = []
                lasso.items()
                    .attr("r",3.5) // reset size
                    .classed("not_possible",true)
                    .classed("selected",false);
            };

            var lasso_draw = function() {
            
                // Style the possible dots
                lasso.possibleItems()
                    .classed("not_possible",false)
                    .classed("possible",true);

                // Style the not possible dot
                lasso.notPossibleItems()
                    .classed("not_possible",true)
                    .classed("possible",false);
            };

            var lasso_end = function() {
                // Reset the color of all dots
                lasso.items()
                    .classed("not_possible",false)
                    .classed("possible",false);

                // Style the selected dots
                var selected_nodes = lasso.selectedItems()
                    .classed("selected",true)
                    .attr("r",7)
                    .attr('test', function(d){
                        that.lasso_selected.push(d)
                    });

                // Reset the style of the not selected dots
                lasso.notSelectedItems()
                    .attr("r",3.5);
                that.request_postLog()
            };
            //  var lasso = .lasso();
            var lasso = d3Lasso.lasso()
                .closePathSelect(true)
                .closePathDistance(100)
                .items(circles)
                .targetArea(svg)
                .on("start",lasso_start)
                .on("draw",lasso_draw)
                .on("end",lasso_end);
            
            svg.call(lasso);
        },
        // draw_hexbin(data){
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
        //      // Reformat the data: d3.hexbin() needs a specific format
        //     var inputForHexbinFun = []
        //     data.forEach(function(d) {
        //         inputForHexbinFun.push( [scale_x(d.x), scale_y(d.y), d['anomaly_label']] )  // Note that we had the transform value of X and Y !
        //     })
        //      // Prepare a color palette
        //     var color = d3.scaleLinear()
        //         .domain([0, 289]) // Number of points in the bin?
        //         .range(["transparent",  "#69b3a2"])

        //     // Compute the hexbin data
        //     var hexbin = d3Hexbin.hexbin()
        //         .radius(9) // size of the bin in px
        //         .extent([ [0, 0], [w, h] ])
        //     var colors = d3.scaleOrdinal(d3.schemeCategory10).range().slice(0, 4);
        //     var attenuation = d3.scaleLog().range([0,1]);

        //     // Plot the hexbins
        //     svg.append("clipPath")
        //         .attr("id", "clip")
        //         .append("rect")
        //         .attr("width", w)
        //         .attr("height", h)
        //      svg.append("g")
        //         .attr("clip-path", "url(#clip)")
        //         .selectAll("path")
        //         .data( hexbin(inputForHexbinFun) )
        //         .enter().append("path")
        //         .attr("d", hexbin.hexagon())
        //         .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        //         .attr("fill", function(d, i) { 
        //             var counts = [0,0];
        //             d.forEach(function(p) {
        //                 let index = parseInt(p[2])
        //                 counts[index]++;
        //             });
        //             // // console.log(counts)
        //             let output = counts.reduce(function(p, c, i) { 
        //                 let temp = d3.interpolateLab(p, colors[i])(c / d.length);
        //                 // console.log(temp)
        //                 return temp
        //             }, "white")
        //             // // console.log(output)
        //             return output;
        //             // console.log(d.length)
        //             // return color(d.length);
        //          })
        //         .style('fill-opacity', function(d) { return attenuation(d.length); })
        //         .attr("stroke", "black")
        //         .attr("stroke-width", "0.1")

            

                
        // },
        request_postLog(){
         
            const path = 'http://localhost:5000/postLog'
            var payload={
                'selected': this.lasso_selected,
                'type':this.selected_attribute,
                'event_type':this.selected_event
            }
            axios.post(path, payload)
            .then((res)=>{
                console.log(res.data)
                this.draw_heatmap(res.data)
            })
        },
        draw_heatmap(RAW){
            var DATA = RAW['heatmapdata']
            d3.select('#div_heatmap').html('')
            // set the dimensions and margins of the graph
            var margin = {top: 30, right: 30, bottom: 30, left: 30},
            width = 450 - margin.left - margin.right,
            height = 450 - margin.top - margin.bottom;
            // append the svg object to the body of the page
            var svg = d3.select("#div_heatmap")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform","translate(" + margin.left + "," + margin.top + ")");

            // Labels of row and columns
            var myGroups = RAW['x_values']
            var myVars = RAW['y_values']

            // Build X scales and axis:
            var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(myGroups)
            .padding(0.01);
            svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))

            // Build X scales and axis:
            var y = d3.scaleBand()
            .range([ height, 0 ])
            .domain(myVars)
            .padding(0.01);
            svg.append("g")
            .call(d3.axisLeft(y));

            // Build color scale
            var myColor = d3.scaleLinear()
            .range(["white", "#69b3a2"])
            .domain([-5,5])

                        //Read the data
            // d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv", function(data) {
            // console.log('ddd',DATA)
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

        }
    },
    watch:{
        selected_project(){
            this.request_postScatter()
        },
        selected_app(){
            this.request_postScatter()
        }
    },
    mounted(){

    },
    computed:{

    }
}
</script>

<style>
circle {
    fill-opacity: 0.5;
}
.normal {
    fill: #346751;
    /* stroke:hsl(0, 3%, 73%);
    stroke-width:1; */
    fill-opacity: 0.5;
}
.abnormal {
    fill: #c84b31;
    stroke:hsl(0, 3%, 73%);
    stroke-width:1;
    fill-opacity: 0.5;
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
    fill:#3399FF;
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
    padding-right: 20px;
    height: 28px;
    width:120px;
    background-color:#002d9c;
    color: white;
}
</style>