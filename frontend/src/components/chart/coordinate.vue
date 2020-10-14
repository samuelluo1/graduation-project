<template>
  <center>
    <v-row align="baseline" justify="center">
    <v-col md="2">
      <v-menu
        ref="menu"
        v-model="menu"
        :close-on-content-click="false"
        :return-value.sync="date"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="date"
            placeholder=" 請選擇年月份"
            readonly
            prepend-icon="event"
            v-bind="attrs"
            v-on="on"
            hide-details
            class="ma-0 pa-0"
          ></v-text-field>
        </template>
        <v-date-picker
          color='light-green'
          v-model="date"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu.save(date); $router.push({name: 'coordinate', query:{date: date}}); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    </v-row>
    <div id="cmain" :style="{width: '1000px', height: '1000px'}" >
    </div>
  </center>
</template>

<script>
import echarts from 'echarts'

export default {
  data: () => ({
    date: new Date().toISOString().substr(0, 7),
    menu: false
  }),
  methods: {
    drawDots () {
      var myChart = echarts.init(document.getElementById('cmain'))
      myChart.showLoading({
        color: '#8BC34A'
      })
      this.$axios.all([this.$axios.get('/get_item/'), this.$axios.get('/get_misc/'), this.$axios.get('/get_ingredient/')])
        .then(this.$axios.spread((itemResp, miscResp, ingrResp) => {
          var itemData = itemResp.data.filter(a => a.item_time === this.date)
          var miscData = miscResp.data.filter(a => a.miscellaneous_time === this.date)
          var ingrData = ingrResp.data.filter(a => a.ingredient_time === this.date)
          var container = []
          var costData = []
          var turnoverCount = 0
          var costCount = 0
          var turnoverMax = -Infinity
          var abcMax = -Infinity
          var turnoverMin = Infinity
          var abcMin = Infinity
          var $this = this
          function getMaterialCost (i, j) {
            $this.$axios.get('/get_have/?ingredient=' + ingrData[j].id + '&item=' + itemData[i].id)
              .then(res => {
                materialCost = materialCost + res.data[0].proportion * 0.01 * ingrData[j].ingredient_price
              })
          }
          for (var i = 0; i < itemData.length; i++) {
            var sales = itemData[i].item_price * itemData[i].sales
            turnoverCount = turnoverCount + sales
            if (sales > turnoverMax) {
              turnoverMax = sales
            };
            if (sales < turnoverMin) {
              turnoverMin = sales
            }
            var materialCost = 0
            for (var j = 0; j < ingrData.length; j++) {
              getMaterialCost(i, j)
            }
            var operatingCost = 0
            var timePropor = 0
            var serviceCount = 0
            var cookingCount = 0
            var sortingCount = 0
            for (var k = 0; k < itemData.length; k++) {
              timePropor = timePropor + itemData[k].time
            }
            timePropor = itemData[i].sales / timePropor
            for (var l = 0; l < miscData.length; l++) {
              serviceCount = serviceCount + miscData[l].miscellaneous_price * miscData[l].service * 0.01
              serviceCount = serviceCount + miscData[l].miscellaneous_price * miscData[l].cooking * 0.01
              serviceCount = serviceCount + miscData[l].miscellaneous_price * miscData[l].sorting * 0.01
            }
            operatingCost = (serviceCount + sortingCount) * timePropor + cookingCount * timePropor
            costData.push(materialCost + operatingCost)
            costCount = costCount + materialCost + operatingCost
            if ((sales - materialCost - operatingCost) > abcMax) {
              abcMax = sales - materialCost - operatingCost
            };
            if ((sales - materialCost - operatingCost) < abcMin) {
              abcMin = sales - materialCost - operatingCost
            }
          };
          for (var m = 0; m < itemData.length; m++) {
            container.push([(itemData[m].item_price * itemData[m].sales - turnoverCount / itemData.length) / (turnoverMax - turnoverMin),
              ((itemData[m].item_price * itemData[m].sales - costData[m]) - (turnoverCount - costCount) / itemData.length) / (abcMax - abcMin),
              itemData[m].item_name])
          };
          myChart.hideLoading()
          myChart.setOption({
            xAxis: {
              name: ' ↑\n毛\n利\n額\n愈\n大',
              nameTextStyle: {
                fontSize: 30,
                verticalAlign: 'bottom'
              },
              axisLabel: {
                show: false
              }
            },
            yAxis: {
              name: '營業額愈大 →',
              nameTextStyle: {
                fontSize: 30,
                align: 'left'
              },
              axisLabel: {
                show: false
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
                color: '#8BC34A'
              },
              label: {
                normal: {
                  show: true,
                  position: 'bottom',
                  formatter: function (params) {
                    return params.data[2]
                  }
                }
              },
              emphasis: {
                label: {
                  show: true,
                  formatter: function (param) {
                    return '(' + Math.round(param.data[0] * 10000) / 10000 + ', ' + Math.round(param.data[1] * 10000) / 10000 + ')'
                  },
                  position: 'top'
                }
              }
            }]
          })
        }))
    }
  },
  created () {
    if (this.$route.query.date !== undefined) {
      this.date = this.$route.query.date
    }
  },
  mounted () {
    this.drawDots()
  }
}
</script>
