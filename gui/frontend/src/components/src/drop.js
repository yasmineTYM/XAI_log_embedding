import { BIconDice3 } from 'bootstrap-vue';
import uniqBy from 'lodash.uniqby';

const filterOverlappingDrop = (xScale, dropDate) => d =>
    uniqBy(d.data, data => Math.round(xScale(dropDate(data))));
// const filterOverlappingDrop = (xScale, dropDate) => d =>
// uniqBy(d.data, function(data){
//     return Math.round(xScale(dropDate(data)))
// });


export default (config, xScale,tym,d) => selection => {
    // console.log(d)
    const {
        drop: {
            color: dropColor,
            radius: dropRadius,
            hover_radius:dropHoverR,
            date: dropDate,
            onClick,
            onMouseOver,
            onMouseOut,
        },
    } = config;

    // tym.forEach(function(d){
    //     // uniqBy(d, function(d){
    //         return Math.round(xScale(dropDate(d)))
    //     // })
    // })
    // console.log(tym)
    var temp = []
    tym[0][0]['fullData'].forEach(function(d){
        temp.push(d)
    })
    // console.log(tym[0][0])
    // console.log(tym[0][0]['data'])
    // console.log(tym)
    var id = tym[0][0]['id']
    const drops = selection
        // .data(temp)
        .selectAll('.drop')
        .data(temp)
        // .data(filterOverlappingDrop(xScale, dropDate));

   
   
    var circles = drops.enter()
        .append('circle')
        .classed('drop', true)
        .on('click', function(d,i){
            // console.log(d,i)
            // console.log(d)
            this.$store.commit('updateLOG_ID', i)
        })
        .on('mouseover', function(d){
            d3.select(this).attr('r',dropHoverR)
        })
        .on('mouseout', function(d){
            circles.attr('r', dropRadius)
        })
        .merge(drops)
        .attr('r', function(d,i){
            // console.log(id)
            if(i==id && id!=null){
                console.log('yes')
                return 8
            }else{
                
                return 5
            }
        })
        .attr('fill', function(d){
            if(d['error_flag']=='true'){
                return '#C05555'
            }else{
                return '#59886B'
            }
        })
        .attr('cx',function(d){
            let cx = xScale(dropDate(d.date))
            return cx
        })
      // .attr('cx', d => xScale(dropDate(d)));
    circles.append('title')
    .text(function(d){return d.message})
    drops
        .exit()
        .on('click', null)
        .on('mouseover', null)
        .on('mouseout', null)
        .remove();
};
