<template> 
  <div id="cmain" :style="{width: '1000px', height: '1000px'}" ></div>
</template>

<script>
  import echarts from 'echarts'
  import axios from 'axios'
  export default {
    data: () => ({
      
    }),
    methods:{
      drawDots(){
        var myChart = echarts.init(document.getElementById('cmain'));
        myChart.showLoading({
          color: '#8BC34A'
        });
        axios.all([axios.get('http://127.0.0.1:8000/api/accounting/item/'), 
                   axios.get('http://127.0.0.1:8000/api/accounting/misc/'),
                   axios.get('http://127.0.0.1:8000/api/accounting/have/'),
                   axios.get('http://127.0.0.1:8000/api/accounting/ingredient/')
                   ]).then(axios.spread((itemResp, miscResp, haveResp, ingrResp) => {   
          var itemData = itemResp.data;
          var miscData = miscResp.data;
          var haveData = haveResp.data;
          var ingrData = ingrResp.data;
          var container = [];
          var costData = [];
          var turnoverCount = 0;
          var costCount = 0;
          var turnoverMax = -Infinity;
          var abcMax = -Infinity;
          var turnoverMin = Infinity;
          var abcMin = Infinity;
          for (var i = 0; i < itemData.length; i++) {
            var sales = itemData[i].item_price * itemData[i].sales
            turnoverCount = turnoverCount + sales;
            if (sales > turnoverMax){
              turnoverMax = sales
            };
            if (sales < turnoverMin){
              turnoverMin = sales
            }
            var materialCost = 0;
            for (var j = 0; j < ingrData.length; j++){
              var propor = haveData.filter(a => a.item == itemData[i].id).filter(b => b.ingredient == ingrData[j].id)[0].proportion
              materialCost = materialCost + propor * 0.01 * ingrData[j].ingredient_price
            }
            var operatingCost = 0;
            var timePropor = 0;
            var serviceCount = 0;
            var cookingCount = 0;
            var sortingCount = 0;
            for (var j = 0; j < itemData.length; j++){
              timePropor = timePropor + itemData[j].time
            }
            timePropor = itemData[i].sales / timePropor
            for (var j = 0; j < miscData.length; j++){
              serviceCount = serviceCount + miscData[j].miscellaneous_price * miscData[j].service * 0.01
            }
            for (var j = 0; j < miscData.length; j++){
              serviceCount = serviceCount + miscData[j].miscellaneous_price * miscData[j].cooking * 0.01
            }
            for (var j = 0; j < miscData.length; j++){
              serviceCount = serviceCount + miscData[j].miscellaneous_price * miscData[j].sorting * 0.01
            }
            operatingCost = (serviceCount + sortingCount) * timePropor + cookingCount * timePropor
            costData.push(materialCost + operatingCost)
            costCount = costCount + materialCost + operatingCost
            if ((sales - materialCost - operatingCost) > abcMax){
              abcMax = sales - materialCost - operatingCost
            };
            if ((sales - materialCost - operatingCost) < abcMin){
              abcMin = sales - materialCost - operatingCost
            }
          };
          for (var i = 0; i < itemData.length; i++) {
            container.push([(itemData[i].item_price * itemData[i].sales - turnoverCount / itemData.length)/(turnoverMax - turnoverMin),
                            ((itemData[i].item_price * itemData[i].sales - costData[i]) - (turnoverCount - costCount) / itemData.length)/(abcMax - abcMin),
                            itemData[i].item_name]);
          };
          myChart.hideLoading();
          myChart.setOption({
          xAxis: {
            name: ' ↑\n毛\n利\n額\n愈\n大',
            nameTextStyle: {
              fontSize: 30,
              verticalAlign: 'bottom'
            },
            axisLabel:{
              show: false,
            }
          },
          yAxis: {
            name: '營業額愈大 →',
            nameTextStyle: {
              fontSize: 30,
              align: 'left'
            },
            axisLabel:{
              show: false,
            }
          },
          grid: {
            width: '80%',
            height: '80%'
          },
          series: [{
            type: 'scatter',
            data: container,
            symbolSize: 10,
            itemStyle: {
                color: '#8BC34A',
            },
            label: {
              normal: {
                show: true,
                position: "bottom",
                formatter: function(params) {
                  return params.data[2];
                }
              }
            },
            emphasis: {
              label: {
                show: true,
                formatter: function (param) {
                    return '(' + Math.round(param.data[0]*10000)/10000 + ', ' + Math.round(param.data[1]*10000)/10000 + ')';
                },
                position: 'top'
            }
        },
          }]
        });
        }));
         
        
         
      }
    },
    mounted(){
      this.drawDots();
    }
    
      
}
</script>