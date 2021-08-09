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
            <el-slider v-model="hexbin_radius_ratio" style="width:70px; margin-left:5px" @change="draw()"></el-slider>
             <div id="overview" v-loading="load_overview"></div>
        </el-row>
       
    </div>
</template>


<script>
import * as d3 from 'd3'
import axios from 'axios'
import * as d3Hexbin from 'd3-hexbin'
import * as d3Contour from 'd3-contour'
export default{
    data(){
        return{
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
            selected_app: 'carts',
            selected_project:'tsne',
            hexbin_radius_ratio:50,
            load_overview: false,
            scatterplot_data:null
        }
    },
    created(){
        this.request_postScatter()
    },
    methods: {
        request_postScatter(){
            this.load_overview = true
            const path = 'http://localhost:5000/postScatter'
            const payload = {
                'application': this.selected_app,
                'projection': this.selected_project
            }
            axios.post(path, payload)
            .then((res)=>{
                this.scatterplot_data = res.data['test']
                this.draw()
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        draw(data){
            this.load_overview = false
            data = this.scatterplot_data
            d3.selectAll('#overview svg').remove()
            // var data = new Array(100).fill(null).map(m=>[Math.random(),Math.random()]);
            var w = 1902, margin=5;
            var h = 970;
            var r = 350;
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
            var svg = d3.select("#overview").append("svg")
                .attr("width",w+margin)
                .attr("height",h+margin)
                .call(zoom);

            var scale_x = d3.scaleLinear()
                .domain(d3.extent(data, d => d.x))
                .range([ r, w-r ]);
            var scale_y = d3.scaleLinear()
                .domain(d3.extent(data, d => d.y))
                .range([ r, h-r ]);
            // draw contour line 
            
             // Reformat the data: d3.hexbin() needs a specific format
            var inputForHexbinFun = []
                data.forEach(function(d) {
                    inputForHexbinFun.push( [scale_x(d.x), scale_y(d.y), d['anomaly_label'], d,d['highlight']] )  // Note that we had the transform value of X and Y !
            })
            console.log(inputForHexbinFun)
             // Prepare a color palette
            var color = d3.scaleLinear()
                .domain([0, 289]) // Number of points in the bin?
                .range(["transparent",  "#69b3a2"])

            // Compute the hexbin data
            var hexbin = d3Hexbin.hexbin()
                .radius(15*(50/that.hexbin_radius_ratio))// size of the bin in px
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

            
           // ================================= compute the hexigon data =================================  
                g.attr("clip-path", "url(#clip)")
                .selectAll("path")
                .data( hexbin(inputForHexbinFun) )
                .enter().append("path")
                .attr("d", hexbin.hexagon())
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
                    that.$alert('Do you want to start analysis now?', 'Confirm', {
                        confirmButtonText: 'Yes',
                        callback: action => {
                            that.$store.commit('updateSHOW_DETAIL', true)
                            that.$store.commit('updateSHOW_OVERVIEW',false)
                            }
                        });

                })
                .attr("fill", function(d, i) { 
                    // console.log(d)
                    var counts = [0,0];
                    d.forEach(function(p) {
                        let index = parseInt(p[2])
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

             // ================================= compute the density data =================================
            var densityData = d3Contour.contourDensity()
                .x(function(d) { return scale_x(d.x); })   // x and y = column name in .csv input data
                .y(function(d) { return scale_y(d.y); })
                .size([w+margin, h+margin])
                .bandwidth(50)    // smaller = more precision in lines = more lines
                (data)
            g.selectAll(".contour_path")
                .data(densityData)
                .enter()
                .append("path")
                .attr('class','contour_path')
                .attr("d", d3.geoPath())
                .attr("fill", "none")
                .attr("stroke", "#999999")
                .attr("stroke-linejoin", "round")   
             
        },
    },
    watch:{
        selected_app(){
            this.request_postScatter()
        },
    },
    mounted(){

    },
    computed:{

    }
}
</script>

<style>

</style>