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
                    <div id="div_heatmap" style="height:620px"></div>
                </el-row>
                <!-- <el-row>
                    <div id="div_heatmap_count_error"></div>
                </el-row>
                <el-row>
                    <div id="div_heatmap_count_two"></div>
                </el-row> -->
                <!-- <el-row>
                    <div id="div_heatmap_count_embedding"></div>
                </el-row> -->
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
import MAP from '../../../../../../Data/gui/heatmap/mapping.json'
import * as d3Contour from 'd3-contour'
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
            this.$store.commit('updateLOAD_B', true)
            const path = 'http://localhost:5000/postScatter'
            const payload = {
                'application': this.selected_app,
                'projection': this.selected_project
            }
            axios.post(path, payload)
            .then((res)=>{
                // console.log(res.data['test'])
                // console.log(res.data)
                this.$store.commit('updateLOAD_B', false)
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
                // console.log(res.data)
                this.draw_heatmap('Count of Cluster Info', '#div_heatmap', res.data)
                // this.draw_heatmap(180,210,'Count of Error Flag','#div_heatmap_count_error',res.data['data_error'], res.data['x_error'], res.data['y_values'])
                // this.draw_two(res.data)
                
            })
        },
        draw_two(data){

            d3.select('#div_heatmap_count_two').html('')
            // ======================================== draw the second heatmap ========================================
            var margin = {top: 30, right: 10, bottom: 20, left: 50},
            width = d3.max([400,data['x_embedding'].length*20]) - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;
            

            var svg = d3.select('#div_heatmap_count_two')
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height*2 + margin.top + margin.bottom)
            .append("g")
            // .attr("id", div_id)
            .attr("transform","translate(" + margin.left + "," + margin.top + ")");

            svg.append('g')
            .append('text')
            .attr('font-size','12px')
            .attr('y',-8)
            .attr('x',width/2)
            .attr('text-anchor','middle')
            .text('test')


            // Build X scales and axis:
            var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(data['x_template'])
            .padding(0.01);

            svg.append("g")
            .attr("class",'x_axis')
            .attr("transform", "translate(0," + height/2 + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-25)");
            // Build X scales and axis:
            var y = d3.scaleBand()
            .range([ height/2, 0 ])
            .domain(data['y_values'])
            .padding(0.01);
            svg.append("g")
            .attr('class','y_axis')
            .call(d3.axisLeft(y));

            // Build color scale
            var myColor = d3.scaleLinear()
            .range(["#bdc9e1", "#045a8d"])
            .domain(d3.extent(data['data_template'], d => d.value))

            var rects = svg.selectAll()
                .data(data['data_template'], function(d) {return d.group+':'+d.variable;})
                .enter()
                .append("rect")
                .attr("x", function(d) { return x(d.group) })
                .attr("y", function(d) { return y(d.variable) })
                .attr("width", x.bandwidth() )
                .attr("height", y.bandwidth() )
                .style("fill", function(d) { return myColor(d.value)} )
            rects.append('title').text(function(d){return d.value})
            // })

            var ticks = d3.selectAll("#div_heatmap_count_two .y_axis .tick text");
            var space = parseInt(data['data_template'].length/10)
            ticks.each(function(_,i){
                if(i%space !== 0) d3.select(this).remove();
            });

            // this.draw_heatmap(180,300,'Count of Template', '#div_heatmap_count_template', data['data_template'], data['x_template'], data['y_values'])
            // ======================================== draw the links ========================================

            var sorted_x = this.draw_Link(data['x_template'], data['x_embedding'], height)
            // this.draw_heatmap(180,210,'Count of Embedding','#div_heatmap_count_embedding', data['data_embedding'], sorted_x, data['y_values'])

                    // Build X scales and axis:
            var x_embed = d3.scaleBand()
            .range([ 0, width ])
            .domain(sorted_x)
            .padding(0.01);

             svg.append("g")
            .attr("class",'x_axis_embed')
            .attr("transform", "translate(0," + height*1.25 + ")")
            .call(d3.axisBottom(x_embed))
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-25)");
            
            var y_embed = d3.scaleBand()
            .range([ height*1.25, 3*height/4])
            .domain(data['y_values'])
            .padding(0.01);
            
            svg.append("g")
            .attr('class','y_axis_embed')
            .call(d3.axisLeft(y_embed));

            // Build color scale
            var myColor_embed = d3.scaleLinear()
            .range(["#bdc9e1", "#045a8d"])
            .domain(d3.extent(data['data_embedding'], d => d.value))

            var rects_embed = svg.selectAll('.rects_embed')
                .data(data['data_embedding'], function(d) {return d.group+':'+d.variable;})
                .enter()
                .append("rect")
                .attr('class', 'rects_embed')
                .attr("x", function(d) { return x_embed(d.group) })
                .attr("y", function(d) { return y_embed(d.variable) })
                .attr("width", x_embed.bandwidth() )
                .attr("height", y_embed.bandwidth() )
                .style("fill", function(d) { return myColor_embed(d.value)} )
            rects_embed.append('title').text(function(d){return d.value})
            // })

            var ticks = d3.selectAll("#div_heatmap_count_two .y_axis_embed .tick text");
            var space = parseInt(data['data_embedding'].length/10)
            ticks.each(function(_,i){
                if(i%space !== 0) d3.select(this).remove();
            });

        },
        draw_Link(tem_data, embed_data, height){
            var computed_mapping = []
            tem_data.forEach(function(tem){
                var candidates = MAP[tem]
                candidates.forEach(function(ele){
                    if(embed_data.includes(ele)){
                        computed_mapping.push({
                            'source': tem,
                            'target': ele
                        })
                    }
                })
            })
            var sorted_embed_data = computed_mapping.map(function(A) {return A['target'];})
             

            var margin = {top: 30, right: 10, bottom: 20, left: 50},
            width_tem = d3.max([400,embed_data.length*20]) - margin.left - margin.right,
            width_embed = width_tem
            
            var x_tem = d3.scaleBand()
            .range([ 0, width_tem ])
            .domain(tem_data)
            .padding(0.01);

            var x_embed = d3.scaleBand()
            .range([0, width_embed])
            .domain(sorted_embed_data)
            .padding(0.01);

            var paths= []
            computed_mapping.forEach(function(d){
                var temp = {}
                temp['source'] = [x_tem(d['source'])+margin.left+x_tem.bandwidth()/2,height/2+margin.top]
                temp['target'] = [x_embed(d['target'])+margin.left+x_embed.bandwidth()/2,3*height/4+margin.top]
                paths.push(temp)
            })

            // console.log(paths)
            // var line = d3.line()
            // .curve(d3.curveBasis)
            // .x(d=>d.x)
            // .y(d=>d.y)

           
            d3.select('#div_heatmap_count_two svg')
            .selectAll('.line_mapping')
            .data(paths)
            .enter()
            .append('path')
            .attr("d", d3.linkHorizontal())
            .style('stroke', '#999999')
            .style('stroke-width','1px')
            .style('fill','white')
            .style('fill-opacity',0)

            return sorted_embed_data
        },
        draw_heatmap(Title,div_id,raw){
            var DATA = raw['data'],
            myGroups = raw['x_values'],
            myVars = raw['y_values'],
            x_error_flag =raw['x_error'],
            x_template = raw['x_template'],
            x_embedding = raw['x_embedding']
            // var DATA = RAW['heatmapdata']
            d3.select(div_id).html('')
            // set the dimensions and margins of the graph
            var margin = {top: 50, right: 10, bottom: 40, left: 50},
            width = d3.max([400,myGroups.length*10])- margin.left - margin.right,
            height = d3.max([620,myVars.length*10]) - margin.top - margin.bottom;
            // append the svg object to the body of the page
            var svg = d3.select(div_id)
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            // .attr("id", div_id)
            .attr("transform","translate(" + margin.left + "," + margin.top + ")");
          
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
            
            
            var tooltip = d3.select("#div_heatmap")
                .append("div")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "2px")
                .style("border-radius", "5px")
                .style("padding", "5px")
                .style('pointer-events','none')
            var mouseover = function(d) {
                tooltip
                .style("opacity", 1)
                d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1)
            }
            var mousemove = function(d) {
                // console.log(d)
                var text = ''
                if(x_error_flag.includes(d['group'])){
                    text = 'In the window:' + d.variable.toString() + ', there are '+ d.value.toString() +' logs with error flag of '+ d.group.toString()
                }else if(x_template.includes(d['group'])){
                    text = 'In the window:' + d.variable.toString() + ', there are '+ d.value.toString() +' logs with log template id of '+ d.group.toString()
                }else{
                    text = 'In the window:' + d.variable.toString() + ', there are '+ d.value.toString() +' logs with embedding id of '+ d.group.toString()
                }
                tooltip
                .html(text)
                .style("left", (d3.mouse(this)[0]) + "px")
                .style("top", (d3.mouse(this)[1]) + "px")
            }
            var mouseleave = function(d) {
                tooltip
                .style("opacity", 0)
                d3.select(this)
                .style("stroke", "none")
                .style("opacity", 0.8)
            }
            var rects = svg.selectAll()
                .data(DATA, function(d) {return d.group+':'+d.variable;})
                .enter()
                .append("rect")
                .attr("rx", 4)
                .attr("ry", 4)
                .attr("x", function(d) { return x(d.group) })
                .attr("y", function(d) { return y(d.variable) })
                .attr("width", x.bandwidth() )
                .attr("height", y.bandwidth() )
                .style("fill", function(d) { return myColor(d.value)})
                .style("opacity", 0.8)
                .on("mouseover", mouseover)
                .on("mousemove", mousemove)
                .on("mouseleave", mouseleave)
            
            // rects.append('title').text(function(d){return d.value})
            // })

            var ticks = d3.selectAll(div_id+" .y_axis .tick text");
            var space = parseInt(DATA.length/10)
            ticks.each(function(_,i){
                if(DATA.length>60){
                    if(i%space !== 0) d3.select(this).remove();
                }
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
            var w = 380, margin=5;
            var h = 270;
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
                .range([ r*10, w-r*10 ]);
            var scale_y = d3.scaleLinear()
                .domain(d3.extent(data, d => d.y))
                .range([ r*12, h-r*10 ]);
            // draw contour line 
            
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
            var g = svg.append("g").attr("clip-path", "url(#clip)")

              // ================================= compute the density data =================================
        //     var densityData = d3Contour.contourDensity()
        //         .x(function(d) { return scale_x(d.x); })   // x and y = column name in .csv input data
        //         .y(function(d) { return scale_y(d.y); })
        //         .size([w+margin, h+margin])
        //         .bandwidth(20)    // smaller = more precision in lines = more lines
        //         (data)
        //     g.selectAll(".contour_path")
        //         .data(densityData)
        //         .enter()
        //         .append("path")
        //         .attr('class','contour_path')
        //         .attr("d", d3.geoPath())
        //         .attr("fill", "none")
        //         .attr("stroke", "#a6bddb")
        //         .attr("stroke-linejoin", "round")  
             
        //    // ================================= compute the hexigon data =================================  
                g.selectAll(".hexigon_path")
                .data( hexbin(inputForHexbinFun) )
                .enter().append("path")
                .attr('class','hexigon_path')
                .attr("d", function(d){
                    // console.log(d)
                    if(d[0][3]['highlight']==0){
                        return hexbin.hexagon()
                    }
                    // else{
                    //     var symbolGenerator = d3.symbol()
	                //     .size(100)
                    //     .type(d3['symbolCross']);
                    //     return symbolGenerator()
                    // }
                    
                })
                .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
                .on('mouseover', function (d, i) {
                    // console.log(d)
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
                        let index = parseInt(p[2])
                        counts[index]++;
                    });
                    let output = counts.reduce(function(p, c, i) { 
                        let temp = d3.interpolateLab(p, colors[i])(c / d.length);
                        return temp
                    }, "white")
                    return output;
                  
                 })
                .style('opacity', function(d) { 
                    let temp = attenuation(d.length)
                    // console.log(temp)
                    return temp; })
                .attr("stroke", "black")
                .attr("stroke-width", "0.1")   

            
        },
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
.tooltip{
    position: absolute;
    z-index: 1070;
    display: block;
    margin: 0;
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
    font-style: normal;
    font-weight: 400;
    line-height: 1.5;
    text-align: left;
    text-align: start;
    text-decoration: none;
    text-shadow: none;
    text-transform: none;
    letter-spacing: normal;
    word-break: normal;
    word-spacing: normal;
    white-space: normal;
    line-break: auto;
    font-size: .875rem;
    word-wrap: break-word;
}
</style>