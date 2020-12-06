<template>
  <v-row>
  <v-col md="6">
    <v-row align="baseline" justify="center">
    <v-col md="6">
      <v-menu
        ref="menu1"
        v-model="menu1"
        :close-on-content-click="false"
        :return-value.sync="monthOne"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="monthOne"
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
          v-model="monthOne"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu1 = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu1.save(monthOne); pushMonth(monthOne, $route.query.monthList[1], $route.query.monthList[2], $route.query.monthList[3]); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    </v-row>
    <div id="cmain1" :style="{width: '450px', height: '450px'}" >
    </div>
    <v-row align="baseline" justify="center">
    <v-col md="6">
      <v-menu
        ref="menu2"
        v-model="menu2"
        :close-on-content-click="false"
        :return-value.sync="monthTwo"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="monthTwo"
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
          v-model="monthTwo"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu2 = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu2.save(monthTwo); pushMonth($route.query.monthList[0], monthTwo, $route.query.monthList[2], $route.query.monthList[3]); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    </v-row>
    <div id="cmain2" :style="{width: '450px', height: '450px'}" >
    </div>
  </v-col>
  <v-col md="6">
    <v-row align="baseline" justify="center">
    <v-col md="6">
      <v-menu
        ref="menu3"
        v-model="menu3"
        :close-on-content-click="false"
        :return-value.sync="monthThree"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="monthThree"
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
          v-model="monthThree"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu3 = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu3.save(monthThree); pushMonth($route.query.monthList[0], $route.query.monthList[1], monthThree, $route.query.monthList[3]); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    </v-row>
    <div id="cmain3" :style="{width: '450px', height: '450px'}" >
    </div>
    <v-row align="baseline" justify="center">
    <v-col md="6">
      <v-menu
        ref="menu4"
        v-model="menu4"
        :close-on-content-click="false"
        :return-value.sync="monthFour"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="monthFour"
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
          v-model="monthFour"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu4 = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu4.save(monthFour); pushMonth($route.query.monthList[0], $route.query.monthList[1], $route.query.monthList[2], monthFour); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    </v-row>
    <div id="cmain4" :style="{width: '450px', height: '450px'}" >
    </div>
  </v-col>
  </v-row>
</template>

<script>
import echarts from 'echarts'

export default {
  inject: ['reload'],
  data: () => ({
    monthOne: new Date().toISOString().substr(0, 7),
    monthTwo: new Date().toISOString().substr(0, 7),
    monthThree: new Date().toISOString().substr(0, 7),
    monthFour: new Date().toISOString().substr(0, 7),
    menu1: false,
    menu2: false,
    menu3: false,
    menu4: false
  }),
  methods: {
    pushMonth (one, two, three, four) {
      this.$router.push({
        name: 'coordinate',
        query: {
          monthList: [one, two, three, four]
        }
      })
    },
    drawDots (month, id) {
      var myChart = echarts.init(document.getElementById(id))
      myChart.showLoading({
        color: '#8BC34A'
      })
      this.$axios.all([this.$axios.get('/get_item/'), this.$axios.get('/get_misc/'), this.$axios.get('/get_ingredient/'), this.$axios.get('/get_have/')])
        .then(this.$axios.spread((itemResp, miscResp, ingrResp, haveResp) => {
          var itemData = itemResp.data.filter(a => a.item_time === month)
          var miscData = miscResp.data.filter(a => a.miscellaneous_time === month)
          var ingrData = ingrResp.data.filter(a => a.ingredient_time === month)
          var haveData = haveResp.data
          var container = []
          var costData = []
          var turnoverCount = 0
          var abcCount = 0
          var turnoverMax = -Infinity
          var abcMax = -Infinity
          var turnoverMin = Infinity
          var abcMin = Infinity
          var $this = this
          for (var i = 0; i < itemData.length; i++) {
            var sales = itemData[i].sales
            turnoverCount = turnoverCount + sales
            if (sales > turnoverMax) {
              turnoverMax = sales
            };
            if (sales < turnoverMin) {
              turnoverMin = sales
            }
            var materialCost = 0
            for (var j = 0; j < ingrData.length; j++) {
              materialCost = materialCost + haveData.filter(a => a.item === itemData[i].id).filter(b => b.ingredient === ingrData[j].id)[0].proportion * 0.01 * ingrData[j].ingredient_price
              console.log(materialCost)
            }
            var operatingCost = 0
            var timeTotal = 0
            var salesTotal = 0
            var serviceCount = 0
            var cookingCount = 0
            var sortingCount = 0
            for (var k = 0; k < itemData.length; k++) {
              timeTotal = timeTotal + itemData[k].time
              salesTotal = salesTotal + itemData[k].sales
            }
            var timePropor = itemData[i].time / timeTotal
            var salesPropor = itemData[i].sales / salesTotal
            for (var l = 0; l < miscData.length; l++) {
              serviceCount = serviceCount + miscData[l].miscellaneous_price * miscData[l].service * 0.01
              serviceCount = serviceCount + miscData[l].miscellaneous_price * miscData[l].cooking * 0.01
              serviceCount = serviceCount + miscData[l].miscellaneous_price * miscData[l].sorting * 0.01
            }
            operatingCost = serviceCount * salesPropor + cookingCount * timePropor + sortingCount * timePropor
            costData.push((materialCost + operatingCost) / itemData[i].sales)
            var tempAbc = itemData[i].item_price - materialCost / itemData[i].sales - operatingCost / itemData[i].sales
            abcCount = abcCount + tempAbc
            if (tempAbc > abcMax) {
              abcMax = tempAbc
            };
            if (tempAbc < abcMin) {
              abcMin = tempAbc
            }
            console.log(materialCost, operatingCost)
            console.log(abcMax, abcMin)
          };
          for (var m = 0; m < itemData.length; m++) {
            container.push([(itemData[m].sales - turnoverCount / itemData.length) / (turnoverMax - turnoverMin),
              ((itemData[m].item_price - costData[m]) - abcCount / itemData.length) / (abcMax - abcMin),
              itemData[m].item_name,
              '單位成本 : ' + Math.round(costData[m] * 100) / 100 + ' 毛利率 : ' + Math.round((itemData[m].item_price - costData[m]) / abcCount * 100 * 100) / 100  + '%'
              ])
            console.log(container)
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
                  formatter: function (params) {
                    return params.data[3]
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
    if (this.$route.query.monthList !== undefined) {
      this.monthOne = this.$route.query.monthList[0]
      this.monthTwo = this.$route.query.monthList[1]
      this.monthThree = this.$route.query.monthList[2]
      this.monthFour = this.$route.query.monthList[3]
    } else {
      var thisMonth = new Date().toISOString().substr(0, 7)
      this.$router.push({name: 'coordinate', query: { monthList: [thisMonth, thisMonth, thisMonth, thisMonth] }})
    }
  },
  async mounted () {
    await this.drawDots(this.monthOne, 'cmain1')
    await this.drawDots(this.monthTwo, 'cmain2')
    await this.drawDots(this.monthThree, 'cmain3')
    await this.drawDots(this.monthFour, 'cmain4')
  }
}
</script>
