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
    console.log(tym)
    var temp = []
    tym[0][0]['fullData'].forEach(function(d){
        temp.push(d)
    })
    // console.log(tym[0][0])
    // console.log(tym[0][0]['data'])
    

    const drops = selection
        // .data(temp)
        .selectAll('.drop')
        .data(temp)
        // .data(filterOverlappingDrop(xScale, dropDate));

   
   
    drops.enter()
        .append('circle')
        .classed('drop', true)
        .on('click', onClick)
        .on('mouseover', onMouseOver)
        .on('mouseout', onMouseOut)
        .merge(drops)
        .attr('r', dropRadius)
        .attr('fill', dropColor)
        .attr('cx',function(d){
            console.log(d);
            // let cx = xScale(dropDate(d.fullData[0].date))
            let cx = xScale(dropDate(d.date))
            
            let cxx = xScale(d.date)
            console.log(cx, cxx)
            return cx
        })
        // .attr('cx', d => xScale(dropDate(d)));

    drops
        .exit()
        .on('click', null)
        .on('mouseover', null)
        .on('mouseout', null)
        .remove();
};
