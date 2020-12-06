<template>
  <center>
    <v-row align="baseline" justify="space-around">
    <v-col md="2" >
      <v-menu
        ref="menu"
        v-model="menu_a"
        :close-on-content-click="false"
        :return-value.sync="startMonth"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="startMonth"
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
          v-model="startMonth"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu.save(startMonth); pushMonth(startMonth, $route.query.monthList[1]); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    <v-col md="2" >
      <v-menu
        ref="menu"
        v-model="menu_b"
        :close-on-content-click="false"
        :return-value.sync="endMonth"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="endMonth"
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
          v-model="endMonth"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu.save(endMonth); pushMonth($route.query.monthList[0], endMonth); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    </v-row>
    <div id="cmain" :style="{width: '1000px', height: '1000px'}" ></div>
  </center>
</template>

<script>
import echarts from 'echarts'

export default {
  inject: ['reload'],
  data: () => ({
    startMonth: parseInt(new Date().toISOString().substr(0, 4)) - 1 + new Date().toISOString().substr(4, 3),
    endMonth: new Date().toISOString().substr(0, 7),
    menu_a: false,
    menu_b: false,
    modal_a: false,
    modal_b: false,
    isRouterAlive: true,
    itemCostData: {}
  }),
  methods: {
    pushMonth (start, end) {
      if (parseInt(start.replace('-', '')) > parseInt(end.replace('-', ''))) {
        alert('開始月份不能比結束月份晚!')
      } else {
        this.$router.push({
          name: 'ingredientCost',
          query: {
            monthList: [start, end]
          }
        })
      }
    },
    async drawDots () {
      var myChart = echarts.init(document.getElementById('cmain'))
      myChart.showLoading({
        color: '#8BC34A'
      })
      await this.$axios.all([this.$axios.get('/get_item/'), this.$axios.get('/get_misc/'), this.$axios.get('/get_ingredient/'), this.$axios.get('/get_have/')])
        .then(this.$axios.spread((itemResp, miscResp, ingrResp, haveResp) => {
          var itemData = itemResp.data
          var miscData = miscResp.data
          var ingrData = ingrResp.data
          var haveData = haveResp.data
          var monthData = []
          var costData = {}
          var allMonthData = []
          var $this = this
          allMonthData.push(this.startMonth)
          while (allMonthData[allMonthData.length - 1] !== this.endMonth) {
            if (allMonthData[allMonthData.length - 1].substr(-1, 1) === '9') {
              allMonthData.push(allMonthData[allMonthData.length - 1].substr(0, 4) + '-10')
            } else if (allMonthData[allMonthData.length - 1].substr(-2, 2) === '12') {
              allMonthData.push(parseInt(allMonthData[allMonthData.length - 1].substr(0, 4)) + 1 + '-01')
            } else {
              allMonthData.push(allMonthData[allMonthData.length - 1].substr(0, 6) + (parseInt(allMonthData[allMonthData.length - 1].substr(-1, 1)) + 1))
            }
          }
          for (var i = 0; i < itemData.length; i++) {
            if (!monthData.includes(itemData[i].item_time)) {
              monthData.push(itemData[i].item_time)
            }
            if (!(itemData[i].item_name in this.itemCostData)) {
              this.itemCostData[itemData[i].item_name] = []
            }
          }
          for (var j = 0; j < monthData.length; j++) {
            var haveSwitch = true
            for (var k = 0; k < miscData.length; k++) {
              if (monthData[j] === miscData[k].miscellaneous_time) {
                haveSwitch = false
              }
            }
            for (var l = 0; l < miscData.length; l++) {
              if (monthData[j] === miscData[l].miscellaneous_time) {
                haveSwitch = false
              }
            }
            if (haveSwitch) {
              monthData = monthData.slice(0, j).concat(monthData.slice(j + 1, monthData.length))
            }
          }
          for (var m = 0; m < allMonthData.length; m++) {
            if (monthData.includes(allMonthData[m])) {
              var itemNewData = itemData.filter(a => a.item_time === allMonthData[m])
              var miscNewData = miscData.filter(a => a.miscellaneous_time === allMonthData[m])
              var ingrNewData = ingrData.filter(a => a.ingredient_time === allMonthData[m])
              for (var n = 0; n < itemNewData.length; n++) {
                var materialCost = 0
                for (var o = 0; o < ingrNewData.length; o++) {
                  materialCost = materialCost + haveData.filter(a => a.item === itemNewData[n].id).filter(b => b.ingredient === ingrNewData[o].id)[0].proportion * 0.01 * ingrNewData[o].ingredient_price
                }
                var operatingCost = 0
                var timeTotal = 0
                var salesTotal = 0
                var serviceCount = 0
                var cookingCount = 0
                var sortingCount = 0
                for (var p = 0; p < itemNewData.length; p++) {
                  timeTotal = timeTotal + itemNewData[p].time
                  salesTotal = salesTotal + itemNewData[p].sales
                }
                var timePropor = itemNewData[n].time / timeTotal
                var salesPropor = itemNewData[n].sales / salesTotal
                for (var q = 0; q < miscNewData.length; q++) {
                  serviceCount = serviceCount + miscNewData[q].miscellaneous_price * miscNewData[q].service * 0.01
                  serviceCount = serviceCount + miscNewData[q].miscellaneous_price * miscNewData[q].cooking * 0.01
                  serviceCount = serviceCount + miscNewData[q].miscellaneous_price * miscNewData[q].sorting * 0.01
                }
                operatingCost = serviceCount * salesPropor + cookingCount * timePropor + sortingCount * timePropor
                costData[itemNewData[n].item_name] = materialCost + operatingCost
              };
              Object.entries(this.itemCostData).forEach(([k, v]) => {
                if (k in costData) {
                  this.itemCostData[k].push(costData[k])
                } else {
                  this.itemCostData[k].push('')
                }
              })
            } else {
              Object.entries(this.itemCostData).forEach(([k, v]) => {
                this.itemCostData[k].push('')
              })
            }
          }
          var seriesData = []
          var legendData = []
          Object.entries(this.itemCostData).forEach(([k, v]) => {
            seriesData.push({ name: k, type: 'line', data: v })
            legendData.push(k)
          })
          myChart.hideLoading()
          myChart.setOption({
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: legendData
            },
            xAxis: {
              type: 'category',
              data: allMonthData
            },
            yAxis: {
              type: 'value'
            },
            grid: {
              width: '80%',
              height: '80%'
            },
            series: seriesData
          })
        }))
    }
  },
  created () {
    if (this.$route.query.monthList !== undefined) {
      this.startMonth = this.$route.query.monthList[0]
      this.endMonth = this.$route.query.monthList[1]
    } else {
      this.$router.push({name: 'ingredientCost', query: { monthList: [parseInt(new Date().toISOString().substr(0, 4)) - 1 + new Date().toISOString().substr(4, 3), new Date().toISOString().substr(0, 7)] }})
    }
  },
  async mounted () {
    await this.drawDots()
  }
}
</script>
