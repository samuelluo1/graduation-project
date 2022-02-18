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
    isRouterAlive: true
  }),
  methods: {
    pushMonth (start, end) {
      if (parseInt(start.replace('-', '')) > parseInt(end.replace('-', ''))) {
        alert('開始月份不能比結束月份晚!')
      } else {
        this.$router.push({
          name: 'turnover',
          query: {
            monthList: [start, end]
          }
        })
      }
    },
    drawDots () {
      var myChart = echarts.init(document.getElementById('cmain'))
      myChart.showLoading({
        color: '#8BC34A'
      })
      this.$axios.all([this.$axios.get('/get_item/'), this.$axios.get('/get_misc/'), this.$axios.get('/get_ingredient/')])
        .then(this.$axios.spread((itemResp, miscResp, ingrResp) => {
          var itemData = itemResp.data
          var miscData = miscResp.data
          var ingrData = ingrResp.data
          var container = []
          var monthData = []
          var allMonthData = []
          var $this = this
          function getMaterialCost (i, j) {
            $this.$axios.get('/get_have/?ingredient=' + ingrData[j].id + '&item=' + itemData[i].id)
              .then(res => {
                materialCost = materialCost + res.data[0].proportion * 0.01 * ingrData[j].ingredient_price
              })
          }
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
              var turnoverCount = 0
              var ingrCostCount = 0
              var miscCostCount = 0
              for (var n = 0; n < itemNewData.length; n++) {
                var sales = itemNewData[n].item_price * itemNewData[n].sales
                turnoverCount = turnoverCount + sales
              }
              for (var o = 0; o < ingrNewData.length; o++) {
                ingrCostCount = ingrCostCount + ingrNewData[o].ingredient_price
              }
              for (var p = 0; p < miscNewData.length; p++) {
                miscCostCount = miscCostCount + miscNewData[p].miscellaneous_price
              }
              container.push(turnoverCount - ingrCostCount - miscCostCount)
            } else {
              container.push('')
            }
          }
          myChart.hideLoading()
          myChart.setOption({
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
            series: [{
              type: 'line',
              data: container,
              symbolSize: 10,
              itemStyle: {
                color: '#8BC34A'
              },
              label: {
              },
              emphasis: {
                label: {
                  show: true,
                  position: 'top'
                }
              }
            }]
          })
        }))
    }
  },
  created () {
    if (this.$route.query.monthList !== undefined) {
      this.startMonth = this.$route.query.monthList[0]
      this.endMonth = this.$route.query.monthList[1]
    } else {
      this.$router.push({name: 'turnover', query: { monthList: [parseInt(new Date().toISOString().substr(0, 4)) - 1 + new Date().toISOString().substr(4, 3), new Date().toISOString().substr(0, 7)] }})
    }
  },
  mounted () {
    this.drawDots()
  }
}
</script>
